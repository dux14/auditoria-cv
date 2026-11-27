"""Bateria E2E de insumos y casos limite. Todas las fixtures se generan en tmp_path (sin binarios en el repo)."""
import base64, json, pathlib, random, subprocess, sys

import pytest
from docx import Document
from docx.oxml import parse_xml
from docx.shared import RGBColor

SCRIPTS = pathlib.Path(__file__).parent.parent / "skills/auditoria-cv/scripts"
PC, BUILD = SCRIPTS / "parse_check.py", SCRIPTS / "build_cv.py"
WNS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

CUERPO = """<h1>{nombre}</h1><p>Madrid | ana@example.com | +34 600 000 000</p>
<h2>Experiencia</h2><h3>Analista de datos | Acme | Mar 2022 - Presente</h3>
<ul><li>Construi 12 dashboards en Power BI usados por 80 personas.</li>
<li>Reduje el tiempo de refresco de 6 a 1 hora en el modelo semantico.</li></ul>
<h3>Auxiliar | Beta | 2019 - 2022</h3><ul><li>Automatice reportes semanales con Python y SQL.</li></ul>
<h2>Educacion</h2><p>Licenciatura en Estadistica | UCM | 2018</p>
<h2>Habilidades</h2><p>SQL, Python, Power BI, Excel avanzado</p>"""


def doc_html(cuerpo, extra_css=""):
    return (f'<!doctype html><meta charset="utf-8"><style>body{{font-family:Arial;font-size:11pt}}'
            f"{extra_css}</style>{cuerpo}")


def cv_html(nombre="Ana Perez"):
    return doc_html(CUERPO.format(nombre=nombre))


@pytest.fixture
def pdf_de(chromium, tmp_path):
    def hacer(html, nombre="cv.pdf"):
        pg = chromium.new_page()
        pg.set_content(html)
        ruta = tmp_path / nombre
        pg.pdf(path=str(ruta), format="A4", print_background=True)  # sin esto Chromium aclara el texto blanco a gris
        pg.close()
        return ruta
    return hacer


@pytest.fixture
def png_de(chromium, tmp_path):
    def hacer(html, nombre="cv.png", **kw):
        pg = chromium.new_page(viewport={"width": 800, "height": 1000})
        pg.set_content(html)
        ruta = tmp_path / nombre
        pg.screenshot(path=str(ruta), **kw)
        pg.close()
        return ruta
    return hacer


def correr(script, *args, ok=True):
    r = subprocess.run([sys.executable, str(script), *map(str, args)], capture_output=True, text=True)
    assert "Traceback" not in r.stderr + r.stdout, r.stderr
    if ok:
        assert r.returncode == 0, r.stderr
    return r


def pc(path, *extra):
    """parse_check con --json: devuelve (json, stdout)."""
    out = pathlib.Path(str(path) + ".json")
    r = correr(PC, path, "--json", out, *extra)
    return json.loads(out.read_text()), r.stdout


def sin_bloqueos(r, out):
    assert not r["es_pdf_imagen"] and "BLOQUEANTE" not in out
    assert not r["columnas"]["multicolumna"] and not r["oculto"]["texto_oculto"]


# ---------- PDF ----------

def test_01_pdf_bueno(pdf_de):
    r, out = pc(pdf_de(cv_html()))
    sin_bloqueos(r, out)
    c = r["campos"]
    assert c["email"] == ["ana@example.com"] and c["telefono"]
    assert c["rangos_de_fecha"] >= 2
    assert all(c["secciones"][k] for k in ("experiencia", "educacion", "habilidades"))


def test_02_barra_lateral(pdf_de):
    lado = " ".join(["Python SQL Docker Kubernetes Terraform Airflow Spark"] * 8)
    lat = " ".join(["Liderazgo comunicacion negociacion mentoria estrategia"] * 8)
    html = doc_html(f'<div style="display:grid;grid-template-columns:30% 60%;gap:10%">'
                    f"<div>{lat}</div><div>{lado}</div></div>")
    r, _ = pc(pdf_de(html))
    assert r["columnas"]["multicolumna"] is True


def test_03_texto_blanco(pdf_de):
    r, out = pc(pdf_de(cv_html() + '<p style="color:#fff">kubernetes snowflake</p>'))
    assert r["oculto"]["texto_oculto"] > 0 and "CRITICO" in out


def test_04_pdf_escaneado(pdf_de, png_de):
    png = png_de(cv_html(), "captura.png")
    b64 = base64.b64encode(png.read_bytes()).decode()
    pdf = pdf_de(f'<!doctype html><body style="margin:0"><img src="data:image/png;base64,{b64}" '
                 f'style="width:100%"></body>', "escaneado.pdf")
    r, out = pc(pdf)
    assert r["es_pdf_imagen"] is True and "BLOQUEANTE" in out
    assert r["transcribir"] and all(pathlib.Path(p).is_file() and p.endswith(".png") for p in r["transcribir"])


def test_05_dos_paginas_con_tabla(pdf_de, tmp_path):
    relleno = "".join(f"<p>Responsabilidad {i}: coordine entregas, revise codigo y documente procesos.</p>"
                      for i in range(15))
    tabla = ('<table style="border-collapse:collapse"><tr><th style="border:1px solid #000">Area</th>'
             '<th style="border:1px solid #000">Nivel</th></tr><tr><td style="border:1px solid #000">SQL</td>'
             '<td style="border:1px solid #000">Alto</td></tr></table>')
    pdf = pdf_de(cv_html() + relleno + '<div style="page-break-before:always"></div>' + tabla)
    r, _ = pc(pdf)
    assert r["inventario"]["paginas"] == 2 and r["tablas"]["tablas"] >= 1
    assert "--- salto de pagina ---" in pathlib.Path(str(pdf) + ".ats.txt").read_text()


@pytest.mark.parametrize("caso", ["vacio", "basura", "cifrado"])
def test_06_pdf_ilegible(caso, pdf_de, tmp_path):
    p = tmp_path / f"{caso}.pdf"
    if caso == "vacio":
        p.write_bytes(b"")
    elif caso == "basura":
        p.write_bytes(random.Random(1).randbytes(2048))
    else:
        from pypdf import PdfReader, PdfWriter
        w = PdfWriter(clone_from=PdfReader(str(pdf_de(cv_html(), "orig.pdf"))))
        w.encrypt("secreto")
        with open(p, "wb") as f:
            w.write(f)
    r = correr(PC, p, ok=False)
    assert r.returncode != 0 and "ilegible" in r.stderr


def test_07_no_latinos_y_emoji(pdf_de):
    html = cv_html("Zoë Ñúñez 李雷").replace("<ul>", "<ul><li>🚀 Lanzamiento de producto con 30% mas ventas.</li>", 1)
    r, out = pc(pdf_de(html))
    assert "Zo" in r["campos"]["posible_nombre"] and not r["es_pdf_imagen"]


def test_08_ruta_con_espacios_y_mayusculas(pdf_de, tmp_path):
    carpeta = tmp_path / "mi carpeta"; carpeta.mkdir()
    p = pdf_de(cv_html(), "Mi CV Final.PDF")
    dest = carpeta / p.name; p.rename(dest)
    r, _ = pc(dest)
    assert r["formato"] == "pdf" and r["campos"]["email"]


# ---------- DOCX ----------

def docx_base(contacto=True):
    doc = Document()
    doc.add_paragraph("Ana Perez", style="Title")
    if contacto:
        doc.add_paragraph("Madrid | ana@example.com | +34 600 000 000")
    doc.add_heading("Experience", 1)
    doc.add_paragraph("Data Analyst | Acme | Mar 2022 - Present")
    doc.add_paragraph("Built 12 Power BI dashboards used by 80 people.", style="List Bullet")
    doc.add_paragraph("Data Engineer | Beta | 2019 - 2022")
    doc.add_heading("Education", 1)
    doc.add_paragraph("BSc Statistics | UCM | 2018")
    doc.add_heading("Skills", 1)
    doc.add_paragraph("SQL, Python, Power BI")
    return doc


def test_09_docx_limpio(tmp_path):
    p = tmp_path / "a.docx"; docx_base().save(p)
    r, out = pc(p)
    assert not r["es_pdf_imagen"] and r["campos"]["email"] == ["ana@example.com"]
    assert r["campos"]["rangos_de_fecha"] >= 2 and not r["columnas"]["multicolumna"]


def test_10_contacto_solo_en_encabezado(tmp_path):
    doc = docx_base(contacto=False)
    doc.sections[0].header.paragraphs[0].text = "ana@example.com | +34 600 000 000"
    p = tmp_path / "enc.docx"; doc.save(p)
    r, out = pc(p)
    assert "ana@example.com" in r["inventario"]["encabezado_pie"] and "encabezado" in out.lower()


def test_11_docx_dos_columnas(tmp_path):
    doc = docx_base()
    doc.sections[0]._sectPr.append(parse_xml(f'<w:cols xmlns:w="{WNS}" w:num="2" w:space="720"/>'))
    p = tmp_path / "cols.docx"; doc.save(p)
    r, _ = pc(p)
    assert r["columnas"]["multicolumna"] is True


def test_12_docx_solo_imagen(png_de, tmp_path):
    doc = Document(); doc.add_picture(str(png_de(cv_html())))
    p = tmp_path / "img.docx"; doc.save(p)
    r, out = pc(p)
    assert r["es_pdf_imagen"] is True and r["transcribir"]
    assert all(pathlib.Path(x).is_file() for x in r["transcribir"])


def test_13_docx_blanco_y_vanish(tmp_path):
    doc = docx_base()
    doc.add_paragraph().add_run("kubernetes snowflake").font.color.rgb = RGBColor(255, 255, 255)
    doc.add_paragraph()._p.append(parse_xml(
        f'<w:r xmlns:w="{WNS}"><w:rPr><w:vanish/></w:rPr><w:t>terraform airflow</w:t></w:r>'))
    p = tmp_path / "oc.docx"; doc.save(p)
    r, _ = pc(p)
    assert r["oculto"]["texto_oculto"] >= len("kubernetes snowflake") + len("terraform airflow")


# ---------- imagenes y texto ----------

@pytest.mark.parametrize("ext,kw", [(".png", {}), (".jpg", {"type": "jpeg"})])
def test_14_imagenes(ext, kw, png_de):
    p = png_de(cv_html(), "cv" + ext, **kw)
    r, out = pc(p)
    assert r["es_pdf_imagen"] is True and r["formato"] == "imagen" and r["transcribir"] == [str(p)]


MD_CV = ("Ana Perez\n\nMadrid | ana@example.com | +34 600 000 000\n\n## Experiencia\n\n"
         "Analista | Acme | 2020 - 2022\n\n- Construi 12 dashboards usados por 80 personas.\n\n"
         "## Educacion\n\nEstadistica | UCM | 2018\n\n## Habilidades\n\nSQL, Python\n")


@pytest.mark.parametrize("ext", [".txt", ".md"])
def test_15_texto_plano(ext, tmp_path):
    p = tmp_path / ("cv" + ext); p.write_text(MD_CV, encoding="utf-8")
    r, _ = pc(p)
    assert r["campos"]["email"] == ["ana@example.com"] and r["campos"]["secciones"]["experiencia"]
    assert r["campos"]["rangos_de_fecha"] >= 1 and not r["es_pdf_imagen"]


def test_15b_txt_vacio(tmp_path):
    p = tmp_path / "vacio.txt"; p.write_text("")
    r, out = pc(p)
    assert r["es_pdf_imagen"] is True and "BLOQUEANTE" in out


@pytest.mark.parametrize("nombre", ["a.doc", "a.odt", "a.pages", "a.xyz", "sin_ext"])
def test_16_formatos_no_soportados(nombre, tmp_path):
    p = tmp_path / nombre; p.write_bytes(b"x")
    r = correr(PC, p, ok=False)
    assert r.returncode != 0 and r.stderr.strip()


def test_16b_inexistente(tmp_path):
    r = correr(PC, tmp_path / "nada.pdf", ok=False)
    assert r.returncode != 0 and "No existe" in r.stderr


# ---------- vacante ----------

def test_17_vacantes(pdf_de, tmp_path):
    cv = pdf_de(cv_html())
    lat = tmp_path / "lat1.txt"
    lat.write_bytes("Buscamos analista con Kubernetes, Snowflake y Power BI. Kubernetes Snowflake "
                    "Terraform; formación en ingeniería.".encode("latin-1"))
    vacia = tmp_path / "vacia.txt"; vacia.write_text("")
    normal = tmp_path / "normal.txt"
    normal.write_text("Power BI y Python. Power BI, Kubernetes, Kubernetes, Snowflake, Snowflake.")
    assert "match" in pc(cv, "--vacante", lat)[0]
    assert pc(cv, "--vacante", vacia)[0]["match"]["cobertura_pct"] == 0
    m = pc(cv, "--vacante", normal)[0]["match"]
    assert 0 <= m["cobertura_pct"] <= 100 and {"kubernetes", "snowflake"} <= set(m["ausentes"])


# ---------- build_cv ----------

MD_BUENO = ("Ana Perez\n\nMadrid | ana@example.com | +34 600 000 000\n\n## Experiencia\n\n"
            "**Analista | Acme | Mar 2022 - Presente**\n\n- Construi 12 dashboards usados por 80 personas.\n\n"
            "**Auxiliar | Beta | 2019 - 2022**\n\n- Automatice reportes con Python.\n\n"
            "## Educacion\n\nEstadistica | UCM | 2018\n\n## Habilidades\n\nSQL, Python, Power BI\n")


def build(tmp_path, md, *extra):
    src = tmp_path / "cv.md"; src.write_text(md, encoding="utf-8")
    return correr(BUILD, src, *extra), tmp_path / "cv.pdf"


def test_18_md_largo(tmp_path):
    jobs = "".join(f"**Cargo {i} | Empresa {i} | 20{10 + i % 10} - 20{11 + i % 10}**\n\n" +
                   "".join(f"- Logro numero {j} con impacto de {j * 10}% en el area {i}.\n" for j in range(1, 5)) + "\n"
                   for i in range(12))
    _, pdf = build(tmp_path, MD_BUENO.split("## Educacion")[0] + jobs + "## Educacion\n\nEstadistica | UCM | 2018\n")
    r, out = pc(pdf)
    assert r["inventario"]["paginas"] >= 2 and not r["columnas"]["multicolumna"] and not r["es_pdf_imagen"]


def test_19_letter(tmp_path):
    import pdfplumber
    _, pdf = build(tmp_path, MD_BUENO, "--letter")
    with pdfplumber.open(pdf) as p:
        assert abs(p.pages[0].width - 612) <= 2 and abs(p.pages[0].height - 792) <= 2


@pytest.mark.parametrize("md", ["", "   \n\n  \n"])
def test_20_md_vacio(md, tmp_path):
    src = tmp_path / "cv.md"; src.write_text(md)
    r = correr(BUILD, src, "--sin-pdf", ok=False)
    assert r.returncode != 0 and r.stderr.strip()


def test_21_ciclo_completo(tmp_path):
    _, pdf = build(tmp_path, MD_BUENO)
    for f in (pdf, tmp_path / "cv.docx"):
        r, out = pc(f)
        sin_bloqueos(r, out)
        assert r["tablas"]["tablas"] == 0 and r["campos"]["email"] == ["ana@example.com"], f


# ---------- regresiones de la corrida completa (2026-11-27) ----------

def test_22_blanco_sobre_barra_oscura_no_es_oculto(pdf_de):
    """Diseño legítimo: texto blanco sobre una barra lateral oscura NO es keyword stuffing."""
    html = doc_html('<div style="background:#1f3a5f;color:#fff;padding:12px">'
                    'Bogota | ana@example.com | SQL Python Power BI</div>' + CUERPO.format(nombre="Ana Perez"))
    r, out = pc(pdf_de(html))
    assert r["oculto"]["texto_oculto"] == 0 and "CRITICO" not in out


def test_23_sin_ruido_de_pdfminer(pdf_de):
    html = doc_html('<p style="font-family:Georgia,serif">' + CUERPO.format(nombre="Ana Perez") + "</p>")
    r = correr(PC, pdf_de(html))
    assert "FontBBox" not in r.stderr and "Could not" not in r.stderr


def test_24_vacante_en_ingles_sin_relleno(pdf_de, tmp_path):
    vac = tmp_path / "v.txt"
    vac.write_text("What you'll do: build dbt models across teams. One team, one dream. "
                   "We are looking for an opportunity to work with real estate data. "
                   "Strong experience with dbt and Airflow. Experience with dbt and SQL.")
    r, _ = pc(pdf_de(cv_html()), "--vacante", vac)
    todos = r["match"]["presentes"] + r["match"]["ausentes"]
    assert "dbt" in todos
    assert not {"what", "one", "across", "opportunity", "looking", "strong"} & set(todos)


def test_25_txt_vacio_no_habla_de_pdf(tmp_path):
    p = tmp_path / "vacio.txt"; p.write_text("hola")
    _, out = pc(p)
    assert "BLOQUEANTE" in out and "PDF" not in out.split("BLOQUEANTE", 1)[1].splitlines()[0]
