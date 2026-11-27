#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["pdfplumber==0.11.11", "python-docx==1.2.0", "pillow==13.0.0"]
# ///
"""
parse_check.py — Diagnostico de parseabilidad de un CV en PDF, DOCX, imagen (PNG/JPG/WEBP/GIF) o texto (TXT/MD).

Simula lo que un ATS extrae realmente del documento y detecta las fallas
que hacen que un CV quede invisible: PDF-imagen, doble columna, tablas,
texto oculto, contacto no detectable, bullets sin metricas.

Uso (uv instala las dependencias solo; sin uv: pip install pdfplumber==0.11.11 python-docx==1.2.0 pillow==13.0.0):
    uv run parse_check.py CV.pdf|CV.docx [--vacante vacante.txt] [--json salida.json] [--png]

Salida: informe legible en stdout (+ JSON opcional).
El texto crudo extraido se guarda junto al PDF como <nombre>.ats.txt
"""

import argparse, json, logging, os, re, sys

logging.getLogger("pdfminer").setLevel(logging.ERROR)  # avisos de fuentes que no afectan la extraccion
from collections import Counter

# ---------- utilidades ----------

def norm(s):
    s = s.lower()
    repl = {'á':'a','é':'e','í':'i','ó':'o','ú':'u','ü':'u','ñ':'n'}
    for k, v in repl.items():
        s = s.replace(k, v)
    return s

# ---------- capa 0: el documento ----------

def abrir_pdf(path):
    import pdfplumber
    try:
        pdf = pdfplumber.open(path)
        pdf.pages  # fuerza la lectura: un PDF roto o cifrado falla aqui
        return pdf
    except Exception as e:
        sys.exit(f"PDF ilegible o protegido ({type(e).__name__}). Pide al usuario otra exportacion "
                 "sin contrasena, o el DOCX.")

def inventario(path):
    with abrir_pdf(path) as pdf:
        return {"paginas": len(pdf.pages),
                "fuentes": len({c.get("fontname") for p in pdf.pages for c in p.chars}),
                "imagenes": sum(len(p.images) for p in pdf.pages),
                "kb": round(os.path.getsize(path) / 1024, 1),
                "encabezado_pie": ""}

def texto_ats(path):
    """Lo que el parser lee: orden de flujo (raw) vs. orden visual (layout). Paginas separadas por \f."""
    with abrir_pdf(path) as pdf:
        raw = "\f".join(p.extract_text(use_text_flow=True) or "" for p in pdf.pages)
        layout = "\f".join(p.extract_text(layout=True) or "" for p in pdf.pages)
    return raw, layout

def png_paginas(path, base, n):
    """Guarda las primeras n paginas como <base>.pN.png y devuelve las rutas."""
    rutas = []
    with abrir_pdf(path) as pdf:
        for i, page in enumerate(pdf.pages[:n], 1):
            ruta = f"{base}.p{i}.png"
            page.to_image(resolution=110 if n == 1 else 150).save(ruta)
            rutas.append(ruta)
    return rutas

def imagenes_docx(path, base):
    """Extrae las imagenes incrustadas de un DOCX (CV pegado como imagen) para transcribirlas."""
    import zipfile
    rutas = []
    def orden(n):  # image2 antes que image10
        return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", n)]
    with zipfile.ZipFile(path) as z:
        medios = [n for n in z.namelist() if n.startswith("word/media/") and not n.endswith("/")
                  and os.path.splitext(n)[1].lower() in IMAGENES]  # .emf/.wmf: el modelo no los lee
        for i, nombre in enumerate(sorted(medios, key=orden), 1):
            ruta = f"{base}.img{i}{os.path.splitext(nombre)[1]}"
            with open(ruta, "wb") as f:
                f.write(z.read(nombre))
            rutas.append(ruta)
    return rutas

IMAGENES = {".png", ".jpg", ".jpeg", ".webp", ".gif"}  # las que un modelo con vision puede leer
CONVERTIR = {".heic", ".heif", ".tif", ".tiff", ".bmp"}
TEXTO = {".txt", ".md"}
EXPORTAR = {".doc", ".odt", ".pages", ".rtf"}

# ---------- DOCX: los ATS lo leen directo, sin pasar por PDF ----------

MC_FALLBACK = "{http://schemas.openxmlformats.org/markup-compatibility/2006}Fallback"

def leer_docx(path):
    """Devuelve (inv, raw, col, tab, oculto) con la misma forma que el camino PDF."""
    from docx import Document
    from docx.oxml.ns import qn
    doc = Document(path)
    body = doc.element.body
    W = lambda tag: qn("w:" + tag)
    T, TAB, BR, CR, R, TXBX = W("t"), W("tab"), W("br"), W("cr"), W("r"), W("txbxContent")

    def en_fallback(el):  # Word guarda cada cuadro dos veces (Choice + Fallback VML)
        return any(a.tag == MC_FALLBACK for a in el.iterancestors())

    def propio(el):
        """Texto y runs del parrafo, sin entrar en cuadros de texto anidados ni Fallback."""
        texto, runs = [], []
        for h in el:
            if h.tag in (TXBX, MC_FALLBACK):
                continue
            if h.tag == T:
                texto.append(h.text or "")
            elif h.tag == TAB:
                texto.append(" ")
            elif h.tag in (BR, CR):
                texto.append("\n")
            else:
                if h.tag == R:
                    runs.append(h)
                t, r = propio(h); texto.append(t); runs += r
        return "".join(texto), runs

    def oculto(rpr):
        if rpr is None:
            return False
        v = rpr.find(W("vanish"))
        if v is not None and (v.get(W("val")) or "true").lower() not in ("0", "false"):
            return True
        c = rpr.find(W("color"))
        return c is not None and ((c.get(W("val")) or "").upper() in ("FFFFFF", "FEFEFE", "FDFDFD")
                                  or c.get(W("themeColor")) in ("background1", "light1"))

    lineas, ocultos = [], 0
    for p in body.iter(W("p")):  # orden del documento, incluye tablas y cuadros de texto
        if en_fallback(p):
            continue
        texto, runs = propio(p)
        if not texto.strip():
            continue
        ppr = p.find(W("pPr"))
        estilo = ppr.find(W("pStyle")) if ppr is not None else None
        es_lista = ppr is not None and (ppr.find(W("numPr")) is not None or
                   (estilo is not None and "List" in (estilo.get(W("val")) or "")))
        lineas.append(("- " if es_lista else "") + texto)
        ocultos += sum(len(propio(r)[0]) for r in runs if oculto(r.find(W("rPr"))))
    cajas = sum(1 for c in body.iter(TXBX) if not en_fallback(c))
    multicol = any(int(c.get(W("num")) or 1) > 1 for c in body.iter(W("cols")))
    enc_pie = " | ".join(p.text for s in doc.sections for hf in (s.header, s.footer)
                         for p in hf.paragraphs if p.text.strip())
    detalle = []
    if multicol:
        detalle.append("La seccion del documento tiene varias columnas (Formato > Columnas).")
    if cajas:
        detalle.append(f"{cajas} cuadro(s) de texto: muchos ATS los omiten o los leen fuera de orden.")
    inv = {"paginas": None, "fuentes": 1, "imagenes": len(doc.inline_shapes),
           "kb": round(os.path.getsize(path) / 1024, 1), "encabezado_pie": enc_pie}
    col = {"multicolumna": bool(multicol or cajas), "paginas_afectadas": ["docx"],
           "detalle": " ".join(detalle)}
    return inv, "\n".join(lineas), col, {"tablas": len(doc.tables)}, {"texto_oculto": ocultos}

# ---------- capa 1: layout que rompe el parsing ----------

def detectar_columnas(path):
    """Busca un gutter: banda vertical sin NINGUNA palabra, con texto sustancial a ambos lados.
    Es la firma inequivoca de un sidebar. Un CV de una columna tiene parrafos que cruzan
    el centro, asi que no puede tener banda vacia."""
    try:
        import pdfplumber
    except ImportError:
        return {"multicolumna": None, "detalle": "pdfplumber no disponible"}

    v = {"multicolumna": False, "paginas_afectadas": [], "detalle": ""}
    NB = 60
    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages, 1):
            words = page.extract_words() or []
            if len(words) < 40:
                continue
            w = page.width
            cov = [0] * NB
            for wd in words:
                b0 = max(0, min(NB - 1, int(wd["x0"] / w * NB)))
                b1 = max(0, min(NB - 1, int(wd["x1"] / w * NB)))
                for b in range(b0, b1 + 1):
                    cov[b] += 1
            mx = max(cov) or 1
            umbral = max(1, 0.10 * mx)  # casi-vacio, no exactamente vacio:
            # texto oculto o lineas sueltas pueden cruzar el gutter sin ser cuerpo real
            b = int(0.18 * NB)
            lim = int(0.78 * NB)
            while b < lim:
                if cov[b] <= umbral:
                    ini = b
                    while b < NB and cov[b] <= umbral:
                        b += 1
                    if b - ini >= 3:  # banda de >=5% del ancho casi sin texto
                        izq, der = sum(cov[:ini]), sum(cov[b:])
                        if izq and der and min(izq, der) / (izq + der) > 0.12:
                            v["multicolumna"] = True
                            v["paginas_afectadas"].append(i)
                            v["detalle"] = (f"Gutter vacio entre el {round(100*ini/NB)}% y el "
                                            f"{round(100*b/NB)}% del ancho: hay columna lateral.")
                            break
                else:
                    b += 1
    if v["multicolumna"] and not v["detalle"]:
        v["detalle"] = "Columna lateral detectada."
    return v


def detectar_tablas(path):
    try:
        import pdfplumber
    except ImportError:
        return {"tablas": None}
    total = 0
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            try:
                total += len(page.find_tables())
            except Exception:
                pass
    return {"tablas": total}

def detectar_texto_oculto(path):
    """Texto que no se ve: se renderiza la pagina y se mide el contraste dentro del recuadro de
    cada caracter. Sin contraste = invisible (blanco sobre blanco, sobre una imagen o un degradado
    del mismo color, o tamano diminuto), sea cual sea el espacio de color. Blanco sobre una barra
    oscura tiene contraste: es diseño, no trampa."""
    from PIL import ImageStat
    RES = 150
    k = RES / 72
    sospechosos = 0
    with abrir_pdf(path) as pdf:
        for page in pdf.pages:
            chars = [c for c in (page.chars or []) if c["text"].strip()]
            if not chars:
                continue
            img = page.to_image(resolution=RES).original.convert("L")
            W, H = img.size
            for ch in chars:
                caja = (max(0, int(ch["x0"] * k)), max(0, int(ch["top"] * k)),
                        min(W, int(ch["x1"] * k) + 1), min(H, int(ch["bottom"] * k) + 1))
                if caja[2] - caja[0] < 2 or caja[3] - caja[1] < 2:
                    sospechosos += 1  # menos de ~1 pt: ilegible para una persona
                    continue
                if ImageStat.Stat(img.crop(caja)).stddev[0] < 6:  # caja uniforme: no hay trazo visible
                    sospechosos += 1
    return {"texto_oculto": sospechosos}

# ---------- capa 2: campos que el ATS debe mapear ----------

RE_EMAIL = re.compile(r"[\w\.\-\+]+@[\w\-]+\.[\w\.\-]+")
RE_TEL = re.compile(r"(?:\+?\d[\d\s\-\(\)\.]{7,}\d)")
RE_SOLO_ANIOS = re.compile(r"^(19|20)\d{2}\s*[-–—/]\s*((19|20)\d{2})?$")
RE_URL = re.compile(r"(?:linkedin\.com/\S+|github\.com/\S+|https?://\S+)", re.I)
RE_ANIO = re.compile(r"\b(19|20)\d{2}\b")
RE_RANGO = re.compile(
    r"((19|20)\d{2}|ene|feb|mar|abr|may|jun|jul|ago|sep|oct|nov|dic|jan|apr|aug|dec)"
    r"[^\n]{0,20}?[-–—/aA]{1,3}\s?(?:[a-z]{3,9}\.?\s+)?((19|20)\d{2}|presente|actual|present|current|hoy)", re.I)

SECCIONES = {
    "experiencia": ["experiencia", "experiencia laboral", "experiencia profesional",
                    "work experience", "experience", "trayectoria"],
    "educacion": ["educacion", "formacion", "formacion academica", "education", "estudios"],
    "habilidades": ["habilidades", "competencias", "skills", "conocimientos",
                    "habilidades tecnicas", "technical skills", "aptitudes"],
    "resumen": ["perfil", "perfil profesional", "resumen", "summary", "acerca de",
                "objetivo", "about"],
    "certificaciones": ["certificaciones", "certificados", "certifications", "cursos", "licencias"],
    "proyectos": ["proyectos", "proyectos destacados", "projects", "selected projects"],
    "idiomas": ["idiomas", "languages"],
}
# Secciones que no todo CV necesita: se informan sin marcarlas como falta.
OPCIONALES = {"certificaciones", "proyectos", "idiomas"}

def campos(texto):
    t = texto
    n = norm(t)
    encontrados = {}
    for clave, variantes in SECCIONES.items():
        encontrados[clave] = any(re.search(r"^[\s#]*" + re.escape(v) + r"\b", n, re.M) for v in variantes)
    primeras = [l.strip() for l in t.splitlines() if l.strip()][:4]
    return {
        "email": RE_EMAIL.findall(t)[:2],
        "telefono": [x for x in (y.strip() for y in RE_TEL.findall(t))
                     if not RE_SOLO_ANIOS.match(x) and len(re.sub(r"\D", "", x)) >= 7][:2],
        "enlaces": RE_URL.findall(t)[:3],
        "posible_nombre": primeras[0] if primeras else None,
        "secciones": encontrados,
        "rangos_de_fecha": len(RE_RANGO.findall(t)),
        "anios_mencionados": len(set(RE_ANIO.findall(t))),
    }

# ---------- capa 3: impacto ----------

RE_BULLET = re.compile(r"^\s*[•▪◦\-\*\u2022\u25cf\u00b7]\s*(.+)$", re.M)
RE_METRICA = re.compile(r"(\d+\s?%|\$\s?\d|\bCOP\b|\bUSD\b|\d+\s?(x|veces|millones|mil|k\b)|\b\d{2,}\b)", re.I)

def impacto(texto):
    bullets = [b.strip() for b in RE_BULLET.findall(texto) if len(b.strip()) > 12]
    if not bullets:
        # fallback: lineas cortas dentro de experiencia sin vinieta
        bullets = [l.strip() for l in texto.splitlines()
                   if 25 < len(l.strip()) < 200 and not l.strip().endswith(":")]
        bullets = bullets[:40]
    con_metrica = [b for b in bullets if RE_METRICA.search(b)]
    pct = round(100 * len(con_metrica) / len(bullets)) if bullets else 0
    return {
        "bullets": len(bullets),
        "bullets_con_metrica": len(con_metrica),
        "pct_con_metrica": pct,
        "sin_metrica_ejemplos": [b for b in bullets if not RE_METRICA.search(b)][:6],
    }

# ---------- capa 4: match con la vacante ----------

STOP = set("""
de la el los las un una unos unas y o u en con para por del al que se su sus es son ser si no
the a an of and or to for in on with as at by is are be will your you we our from that this it
experiencia trabajo empleo puesto rol cargo candidato candidata empresa equipo anos ano nivel
job role work team company candidate years year experience must have should required requirements
responsabilidades responsibilities about position sobre buscamos ofrecemos requisitos requisito
deseable deseables indispensable conocimiento conocimientos dominio manejo capacidad habilidad
habilidades competencias funciones funcion perfil descripcion vacante oferta area sector
excelente excelentes solida solidas fuerte buena buenas alto alta nuestro nuestra tus sus
minimo minima mas menos etc entre cada todo toda todos todas donde como cuando muy tambien
ademas asi mismo tanto parte lugar forma manera tipo caso vez veces dia dias mes meses
senior junior semi ssr sr jr pleno trainee practicante estudiante profesional titulado
what who why how when where which while within without into onto over under across along
one two three our ours their them they these those there here also just only very more most
can could would should may might shall must need needs needed want wants looking look seek
strong deep solid great good excellent proven demonstrated ability able skills skill knowledge
working work works worked help helps helping make makes making build builds building
opportunity opportunities ideal passion passionate drive driven self sufficient confident
including include includes such etc like well other others new key core based
part full time day days week weeks month months company's we're you're you'll we'll it's
across apply applying application benefits salary compensation competitive hourly rate
team's teams business businesses partner partners partnering closely ensure ensuring
""".split())

SUF_VERBO = ("ar", "er", "ir", "ando", "iendo", "amos", "emos", "imos", "aran", "eran")

def _util(p):
    if p in STOP or p.isdigit() or len(p) < 3:
        return False
    # descarta infinitivos/gerundios sueltos (construir, escribir, automatizando)
    if len(p) > 4 and p.endswith(SUF_VERBO) and p not in ("power", "docker", "scrum"):
        return False
    return True

def terminos(texto, minlen=3):
    palabras = re.findall(r"[a-zA-Záéíóúñü0-9\+\#\.]{%d,}" % minlen, texto.lower())
    palabras = [norm(p).strip(".") for p in palabras]
    return [p for p in palabras if _util(p)]

def bigramas(toks):
    return [f"{a} {b}" for a, b in zip(toks, toks[1:])]

def match_vacante(cv_texto, vacante_texto, top=30):
    cv_toks = set(terminos(cv_texto)) | set(bigramas(terminos(cv_texto)))
    v_toks = terminos(vacante_texto)
    v_bi = bigramas(v_toks)
    freq = Counter(v_toks) + Counter(v_bi)
    candidatos = [(t, c) for t, c in freq.most_common(200) if c >= 1]
    # priorizamos terminos que se repiten o que parecen tecnicos
    clave = [t for t, c in candidatos if c >= 2][:top]
    if len(clave) < top:
        clave += [t for t, c in candidatos if c == 1 and len(t) > 4][: top - len(clave)]
    presentes = [t for t in clave if t in cv_toks]
    ausentes = [t for t in clave if t not in cv_toks]
    cobertura = round(100 * len(presentes) / len(clave)) if clave else 0
    return {"cobertura_pct": cobertura, "presentes": presentes, "ausentes": ausentes}

# ---------- informe ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf", help="CV en .pdf, .docx, imagen (.png/.jpg/...) o texto (.txt/.md)")
    ap.add_argument("--vacante", help="archivo .txt con la descripcion de la vacante")
    ap.add_argument("--json", help="ruta para volcar el resultado en JSON")
    ap.add_argument("--png", action="store_true", help="guarda la pagina 1 como <archivo>.p1.png (triaje visual, solo PDF)")
    a = ap.parse_args()

    if not os.path.isfile(a.pdf):
        sys.exit(f"No existe el archivo: {a.pdf}")
    ext = os.path.splitext(a.pdf)[1].lower()
    es_docx, base = ext == ".docx", a.pdf  # base: los archivos derivados cuelgan del nombre completo
    if ext in EXPORTAR:
        sys.exit(f"Formato {ext}: pide al usuario que lo exporte a PDF o DOCX desde su editor.")
    if ext in CONVERTIR:
        sys.exit(f"Imagen {ext}: pide al usuario que la exporte como PNG o JPG (captura o 'Guardar como').")
    if ext in IMAGENES:
        r = {"archivo": os.path.basename(a.pdf), "es_pdf_imagen": True, "formato": "imagen",
             "transcribir": [a.pdf]}
        print("=" * 62 + f"\nDIAGNOSTICO DE PARSEABILIDAD — {os.path.basename(a.pdf)}\n" + "=" * 62)
        print("\n[BLOQUEANTE] El CV es una imagen. Un ATS no extrae ninguna palabra de una imagen.")
        print("  Accion: transcribe la imagen (leela tu) a cv-transcrito.md y reconstruye el CV.")
        print(f"  Transcribir: {a.pdf}")
        if a.json:
            json.dump(r, open(a.json, "w"), ensure_ascii=False, indent=2)
        return
    if ext not in TEXTO and ext not in (".pdf", ".docx"):
        sys.exit(f"Formato no soportado ({ext or 'sin extension'}): usa PDF, DOCX, imagen, TXT o MD.")
    try:
        import pdfplumber, docx  # noqa: F401
    except ImportError:
        sys.exit("Faltan dependencias. Corre con `uv run parse_check.py ...` o instala: "
                 "pip install pdfplumber==0.11.11 python-docx==1.2.0 pillow==13.0.0")

    transcribir = []
    if ext in TEXTO:
        raw = open(a.pdf, encoding="utf-8-sig", errors="replace").read()
        if ext == ".md":  # quita marcas de Markdown que no son contenido
            raw = "\n".join(re.sub(r"\*\*|__", "", l.lstrip("#").strip()) if not l.lstrip().startswith(("- ", "* "))
                            else l for l in raw.splitlines())
        layout = raw
        inv = {"paginas": None, "fuentes": 1, "imagenes": 0,
               "kb": round(os.path.getsize(a.pdf) / 1024, 1), "encabezado_pie": ""}
        col = {"multicolumna": False, "paginas_afectadas": [], "detalle": ""}
        tab, oculto = {"tablas": 0}, {"texto_oculto": 0}
        escaneado = len(raw.strip()) < 100
        print("(Texto plano: se revisa contenido y campos; el formato se revisa al generar el CV.)")
    elif es_docx:
        inv, raw, col, tab, oculto = leer_docx(a.pdf)
        layout = raw
        escaneado = len(raw.strip()) < 100
        if escaneado or (inv["imagenes"] and len(raw.strip()) < 400):
            transcribir = imagenes_docx(a.pdf, base)
    else:
        inv = inventario(a.pdf)
        raw, layout = texto_ats(a.pdf)
        escaneado = inv["fuentes"] == 0 or len(raw.strip()) < 100
        if escaneado:
            transcribir = png_paginas(a.pdf, base, 10)  # shortcut: max 10 paginas; un CV no deberia tener mas
            if inv["paginas"] > 10:
                print(f"Aviso: el PDF tiene {inv['paginas']} paginas; solo se exportan las 10 primeras.")
        elif a.png:
            png = png_paginas(a.pdf, base, 1)[0]
            print(f"Pagina 1 guardada en: {png}")

    r = {"archivo": os.path.basename(a.pdf), "inventario": inv, "es_pdf_imagen": escaneado,
         "formato": ext.lstrip("."), "transcribir": transcribir}

    print("=" * 62)
    print(f"DIAGNOSTICO DE PARSEABILIDAD — {os.path.basename(a.pdf)}")
    print("=" * 62)
    print(f"Paginas: {inv['paginas'] or 'n/d'} | Fuentes: {inv['fuentes']} | "
          f"Imagenes: {inv['imagenes']} | Peso: {inv['kb']} KB")

    if escaneado:
        if ext in TEXTO:
            print("\n[BLOQUEANTE] El archivo de texto casi no tiene contenido (<100 caracteres).")
            print("  No hay CV que analizar: pide el CV completo o construye el perfil en la Fase 5.")
        elif es_docx:
            print("\n[BLOQUEANTE] El DOCX casi no tiene texto (<100 caracteres).")
            print("  Suele ser un CV pegado como imagen dentro de Word. El ATS no lee imagenes.")
        else:
            print("\n[BLOQUEANTE] El PDF no tiene capa de texto util (PDF-imagen).")
            print("  El ATS extrae CERO palabras. Equivale a enviar una hoja en blanco.")
            print("  Causa tipica: exportado desde Canva/Figma como imagen, o escaneado.")
        print("  Accion: rehacer el documento con texto real seleccionable.")
        if transcribir:
            print("  Transcribe estas imagenes (leelas tu) a cv-transcrito.md antes de seguir:")
            for t in transcribir:
                print(f"    {t}")
        if a.json:
            json.dump(r, open(a.json, "w"), ensure_ascii=False, indent=2)
        return

    if ext == ".pdf":
        col = detectar_columnas(a.pdf)
        tab = detectar_tablas(a.pdf)
        oculto = detectar_texto_oculto(a.pdf)
    cmp_ = campos(raw)
    imp = impacto(layout)
    r.update({"columnas": col, "tablas": tab, "oculto": oculto,
              "campos": cmp_, "impacto": imp})

    print("\n--- CAPA 1: LAYOUT ---")
    if ext in TEXTO:
        print("n/d: texto plano, sin layout que revisar.")
    if transcribir:
        print(f"[RIESGO] El DOCX tiene poco texto y {len(transcribir)} imagen(es): parte del CV puede estar")
        print("  pegado como imagen, que el ATS no lee. Transcribe y revisa:")
        for t in transcribir:
            print(f"    {t}")
    if ext in TEXTO:
        pass
    elif col.get("multicolumna"):
        print(f"[GRAVE] Multicolumna en pagina(s) {col['paginas_afectadas']}.")
        print(f"  {col['detalle']}")
    else:
        print("[OK] Una sola columna.")
    if tab["tablas"]:
        print(f"[RIESGO] {tab['tablas']} tabla(s) detectada(s). Verifica en el .ats.txt si el orden se conserva (una cuadricula simple suele parsear bien; un layout con tablas no).")
    elif ext not in TEXTO:
        print("[OK] Sin tablas.")
    if oculto["texto_oculto"]:
        print(f"[CRITICO] {oculto['texto_oculto']} caracteres invisibles (sin contraste, ocultos o diminutos): posible keyword stuffing.")
        print("  Los filtros con LLM y los reclutadores lo ven; es riesgo reputacional. Eliminar.")
    elif ext not in TEXTO:
        print("[OK] Sin texto oculto.")
    if inv["encabezado_pie"]:
        print(f"[RIESGO] Texto en encabezado/pie: '{inv['encabezado_pie'][:80]}'. Algunos ATS lo omiten:")
        print("  el contacto debe estar tambien en el cuerpo del documento.")
    if inv["imagenes"] > 2:
        print(f"[RIESGO] {inv['imagenes']} imagenes. Iconos/barras de nivel no aportan texto al parser.")

    print("\n--- CAPA 2: CAMPOS QUE EL ATS DEBE MAPEAR ---")
    print(f"Nombre (1a linea): {cmp_['posible_nombre']}")
    print(f"Email:    {cmp_['email'] or '[FALTA]'}")
    print(f"Telefono: {cmp_['telefono'] or '[FALTA]'}")
    print(f"Enlaces:  {cmp_['enlaces'] or '[ninguno]'}")
    print(f"Rangos de fecha detectados: {cmp_['rangos_de_fecha']}"
          + ("  [FALTA: sin fechas parseables el ATS no calcula tu experiencia]"
             if cmp_["rangos_de_fecha"] == 0 else ""))
    for k, v in cmp_["secciones"].items():
        falta = "(opcional, no detectada)" if k in OPCIONALES else "[FALTA o con titulo no estandar]"
        print(f"  seccion '{k}': {'OK' if v else falta}")

    print("\n--- CAPA 3: IMPACTO ---")
    print(f"Bullets analizados: {imp['bullets']} | con metrica: {imp['bullets_con_metrica']} "
          f"({imp['pct_con_metrica']}%)  [referencia: prefiere alcance verificable a porcentajes inventados]")
    for b in imp["sin_metrica_ejemplos"]:
        print(f"  sin metrica -> {b[:90]}")

    if a.vacante:
        vac = open(a.vacante, encoding="utf-8", errors="ignore").read()
        m = match_vacante(raw, vac)
        r["match"] = m
        print("\n--- CAPA 4: MATCH CON LA VACANTE ---")
        print(f"Cobertura de terminos clave: {m['cobertura_pct']}%")
        print(f"Presentes: {', '.join(m['presentes'][:20]) or '-'}")
        print(f"AUSENTES:  {', '.join(m['ausentes'][:20]) or '-'}")
        print("  (Incluir solo los ausentes que sean CIERTOS para ti. Nada de inventar.)")

    txt_out = a.pdf + ".ats.txt"  # CV.pdf y CV.docx en la misma carpeta no se pisan
    with open(txt_out, "w", encoding="utf-8") as f:
        # las paginas van separadas con un salto de formulario invisible; se hace visible
        # para que una linea no parezca pegada a la siguiente al cruzar de pagina.
        pagina = "\n--- salto de pagina ---\n"
        f.write("=== ORDEN DE FLUJO (lo que lee el parser) ===\n" + raw.replace("\f", pagina) +
                "\n\n=== ORDEN VISUAL ===\n" + layout.replace("\f", pagina))
    print(f"\nTexto extraido guardado en: {txt_out}")
    print("Leelo: si no se entiende ahi, tampoco lo entiende el ATS.")

    if a.json:
        json.dump(r, open(a.json, "w"), ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
