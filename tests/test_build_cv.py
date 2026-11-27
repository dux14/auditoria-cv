"""Prueba de build_cv.py. Correr: uv run --with python-docx --with pytest pytest tests/"""
import pathlib, subprocess, sys

from docx import Document

SCRIPT = pathlib.Path(__file__).parent.parent / "skills/auditoria-cv/scripts/build_cv.py"
MD = """Ana Pérez

Madrid, España | ana@example.com | +34 600 000 000

## Summary

Data Analyst with **4 years** in retail.

## Experience

**Data Analyst | Acme | Madrid | Mar 2022 - Present**

- Built 12 Power BI dashboards used by 80 people.
- Cut refresh time from 6 to 1 hours.
"""


def test_md_a_docx_y_html(tmp_path):
    src = tmp_path / "cv.md"
    src.write_text(MD, encoding="utf-8")
    subprocess.run([sys.executable, str(SCRIPT), str(src)], check=True)

    doc = Document(tmp_path / "cv.docx")
    paras = [(p.style.name, p.text) for p in doc.paragraphs if p.text]
    assert paras[0] == ("Title", "Ana Pérez")
    assert paras[1][1].startswith("Madrid, España | ana@example.com")
    assert ("Heading 1", "Summary") in paras
    assert ("Normal", "Data Analyst with 4 years in retail.") in paras  # sin asteriscos
    assert ("List Bullet", "Cut refresh time from 6 to 1 hours.") in paras
    job = next(p for p in doc.paragraphs if p.text.startswith("Data Analyst | Acme"))
    assert all(r.bold for r in job.runs)
    # ATS-seguro: sin tablas ni encabezado/pie con texto
    assert not doc.tables
    assert not any(p.text for p in doc.sections[0].header.paragraphs)

    html = (tmp_path / "cv.html").read_text(encoding="utf-8")
    assert "<h1>Ana Pérez</h1>" in html and "<li>Built 12 Power BI" in html
    assert "**" not in html
