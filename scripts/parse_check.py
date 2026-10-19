#!/usr/bin/env python3
"""
parse_check.py — Diagnostico de parseabilidad de un CV en PDF.

Simula lo que un ATS extrae realmente del documento y detecta las fallas
que hacen que un CV quede invisible: PDF-imagen, doble columna, tablas,
texto oculto, contacto no detectable, bullets sin metricas.

Uso:
    python3 parse_check.py CV.pdf [--vacante vacante.txt] [--json salida.json]

Salida: informe legible en stdout (+ JSON opcional).
El texto crudo extraido se guarda junto al PDF como <nombre>.ats.txt
"""

import argparse, json, os, re, subprocess, sys
from collections import Counter

# ---------- utilidades ----------

def sh(cmd):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return r.stdout
    except Exception:
        return ""

def norm(s):
    s = s.lower()
    repl = {'á':'a','é':'e','í':'i','ó':'o','ú':'u','ü':'u','ñ':'n'}
    for k, v in repl.items():
        s = s.replace(k, v)
    return s

# ---------- capa 0: el documento ----------

def inventario(path):
    out = {}
    info = sh(["pdfinfo", path])
    m = re.search(r"Pages:\s+(\d+)", info)
    out["paginas"] = int(m.group(1)) if m else None
    fonts = sh(["pdffonts", path])
    lineas_fuente = [l for l in fonts.splitlines()[2:] if l.strip()]
    out["fuentes"] = len(lineas_fuente)
    imgs = sh(["pdfimages", "-list", path])
    out["imagenes"] = max(0, len([l for l in imgs.splitlines()[2:] if l.strip()]))
    out["kb"] = round(os.path.getsize(path) / 1024, 1)
    return out

def texto_ats(path):
    """Lo que el parser lee: orden de flujo (raw) vs. orden visual (layout)."""
    raw = sh(["pdftotext", "-raw", path, "-"])
    layout = sh(["pdftotext", "-layout", path, "-"])
    return raw, layout

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
    """Texto blanco o casi blanco sobre fondo blanco = bandera de fraude en Workday/Greenhouse/Lever."""
    try:
        import pdfplumber
    except ImportError:
        return {"texto_oculto": None}
    sospechosos = 0
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            for ch in (page.chars or []):
                col = ch.get("non_stroking_color")
                if col is None:
                    continue
                if isinstance(col, (int, float)):
                    col = [col]
                try:
                    vals = [float(c) for c in col]
                except Exception:
                    continue
                if vals and all(v > 0.94 for v in vals):
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
        encontrados[clave] = any(re.search(r"^\s*" + re.escape(v) + r"\b", n, re.M) for v in variantes)
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
    ap.add_argument("pdf")
    ap.add_argument("--vacante", help="archivo .txt con la descripcion de la vacante")
    ap.add_argument("--json", help="ruta para volcar el resultado en JSON")
    a = ap.parse_args()

    inv = inventario(a.pdf)
    raw, layout = texto_ats(a.pdf)
    escaneado = inv["fuentes"] == 0 or len(raw.strip()) < 100

    r = {"archivo": os.path.basename(a.pdf), "inventario": inv, "es_pdf_imagen": escaneado}

    print("=" * 62)
    print(f"DIAGNOSTICO DE PARSEABILIDAD — {os.path.basename(a.pdf)}")
    print("=" * 62)
    print(f"Paginas: {inv['paginas']} | Fuentes: {inv['fuentes']} | "
          f"Imagenes: {inv['imagenes']} | Peso: {inv['kb']} KB")

    if escaneado:
        print("\n[BLOQUEANTE] El PDF no tiene capa de texto util (PDF-imagen).")
        print("  El ATS extrae CERO palabras. Equivale a enviar una hoja en blanco.")
        print("  Causa tipica: exportado desde Canva/Figma como imagen, o escaneado.")
        print("  Accion: rehacer el documento con texto real seleccionable.")
        if a.json:
            json.dump(r, open(a.json, "w"), ensure_ascii=False, indent=2)
        return

    col = detectar_columnas(a.pdf)
    tab = detectar_tablas(a.pdf)
    oculto = detectar_texto_oculto(a.pdf)
    cmp_ = campos(raw)
    imp = impacto(layout)
    r.update({"columnas": col, "tablas": tab, "oculto": oculto,
              "campos": cmp_, "impacto": imp})

    print("\n--- CAPA 1: LAYOUT ---")
    if col.get("multicolumna"):
        print(f"[GRAVE] Multicolumna en pagina(s) {col['paginas_afectadas']}.")
        print(f"  {col['detalle']}")
    else:
        print("[OK] Una sola columna.")
    if tab["tablas"]:
        print(f"[RIESGO] {tab['tablas']} tabla(s) detectada(s). Verifica en el .ats.txt si el orden se conserva (una cuadricula simple suele parsear bien; un layout con tablas no).")
    else:
        print("[OK] Sin tablas.")
    if oculto["texto_oculto"]:
        print(f"[CRITICO] {oculto['texto_oculto']} caracteres casi blancos (posible keyword stuffing oculto).")
        print("  Los filtros con LLM y los reclutadores lo ven; es riesgo reputacional. Eliminar.")
    else:
        print("[OK] Sin texto oculto.")
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

    txt_out = os.path.splitext(a.pdf)[0] + ".ats.txt"
    with open(txt_out, "w", encoding="utf-8") as f:
        # pdftotext separa paginas con un salto de formulario invisible; se hace visible
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
