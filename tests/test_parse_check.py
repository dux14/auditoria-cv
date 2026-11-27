"""Prueba de parse_check.py sin herramientas del sistema. Correr: uv run --with pdfplumber --with python-docx --with pytest pytest tests/"""
import json, pathlib, subprocess, sys

from docx import Document
from docx.shared import RGBColor

SCRIPT = pathlib.Path(__file__).parent.parent / "skills/auditoria-cv/scripts/parse_check.py"


def correr(path, *extra):
    out = path.with_suffix(".json")
    r = subprocess.run([sys.executable, str(SCRIPT), str(path), "--json", str(out), *extra],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    return json.loads(out.read_text()), r.stdout


def cv_docx(tmp_path, trampas=False):
    doc = Document()
    if trampas:
        doc.sections[0].header.paragraphs[0].text = "ana@example.com | +34 600 000 000"
    doc.add_paragraph("Ana Pérez", style="Title")
    if not trampas:
        doc.add_paragraph("Madrid | ana@example.com | +34 600 000 000")
    doc.add_heading("Experience", 1)
    doc.add_paragraph("Data Analyst | Acme | Mar 2022 - Present")
    doc.add_paragraph("Built 12 Power BI dashboards used by 80 people.", style="List Bullet")
    doc.add_heading("Education", 1)
    doc.add_paragraph("BSc Statistics | UCM | 2020")
    doc.add_heading("Skills", 1)
    doc.add_paragraph("SQL, Python, Power BI")
    if trampas:
        doc.add_table(rows=1, cols=2)
        r = doc.add_paragraph().add_run("snowflake kubernetes")
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    p = tmp_path / ("trampas.docx" if trampas else "limpio.docx")
    doc.save(p)
    return p


def test_docx_limpio(tmp_path):
    r, _ = correr(cv_docx(tmp_path))
    assert r["campos"]["email"] == ["ana@example.com"]
    assert r["campos"]["secciones"]["experiencia"] and r["campos"]["secciones"]["educacion"]
    assert r["tablas"]["tablas"] == 0 and not r["oculto"]["texto_oculto"]
    assert r["impacto"]["bullets"] >= 1
    assert not r["es_pdf_imagen"]


def test_docx_con_trampas(tmp_path):
    r, out = correr(cv_docx(tmp_path, trampas=True))
    assert r["tablas"]["tablas"] == 1
    assert r["oculto"]["texto_oculto"] >= len("snowflake kubernetes")
    assert "ana@example.com" in r["inventario"]["encabezado_pie"]
    assert "encabezado" in out.lower()


def test_pdf_y_png(tmp_path):
    # PDF real generado por build_cv (Chromium vía Playwright)
    md = tmp_path / "cv.md"
    md.write_text("Ana Pérez\n\nMadrid | ana@example.com | +34 600 000 000\n\n## Experience\n\n"
                  "**Data Analyst | Acme | Mar 2022 - Present**\n\n- Built 12 dashboards used by 80 people.\n\n"
                  "## Education\n\nBSc Statistics | UCM | 2020\n", encoding="utf-8")
    build = SCRIPT.parent / "build_cv.py"
    subprocess.run([sys.executable, str(build), str(md)], check=True)
    r, _ = correr(tmp_path / "cv.pdf", "--png")
    assert r["inventario"]["paginas"] == 1 and r["inventario"]["fuentes"] >= 1
    assert not r["es_pdf_imagen"] and not r["columnas"]["multicolumna"]
    assert r["campos"]["email"] == ["ana@example.com"]
    assert (tmp_path / "cv.p1.png").stat().st_size > 1000
