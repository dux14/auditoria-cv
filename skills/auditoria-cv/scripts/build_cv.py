#!/usr/bin/env python3
"""
build_cv.py - Convierte un CV en Markdown simple a DOCX y HTML de una columna (ATS-seguro).

Uso:
    uv run --with python-docx scripts/build_cv.py cv.md      # o: pip install python-docx
Genera cv.docx y cv.html junto al .md. Para el PDF:
    soffice --headless --convert-to pdf cv.docx              # si hay LibreOffice
    "<chrome>" --headless --no-pdf-header-footer --print-to-pdf=cv.pdf cv.html   # si no

Markdown aceptado (lo que produce assets/cv-ats-base.md):
    primera línea = nombre; líneas antes del primer "## " = contacto;
    "## Sección" = encabezado; línea entera en **negrita** = cargo; "- " = bullet;
    el resto, párrafo. Negrita en línea se quita.
    shortcut: cada línea es un párrafo (no une líneas partidas); escribe cada párrafo en una línea.
"""
import html, pathlib, re, sys

from docx import Document
from docx.shared import Pt


def bloques(md):
    """Devuelve [(tipo, texto)] con tipo en name|contact|h|job|li|p."""
    out, vistos_h = [], False
    for linea in md.splitlines():
        t = linea.strip()
        if not t:
            continue
        if t.startswith("## "):
            out.append(("h", t[3:].strip())); vistos_h = True
        elif not out:
            out.append(("name", t.lstrip("# ").strip()))
        elif not vistos_h:
            out.append(("contact", t))
        elif re.fullmatch(r"\*\*(.+)\*\*", t):
            out.append(("job", t[2:-2]))
        elif t[:2] in ("- ", "* "):
            out.append(("li", t[2:]))
        else:
            out.append(("p", t))
    return [(k, re.sub(r"\*\*(.+?)\*\*", r"\1", v)) for k, v in out]


def a_docx(bs, ruta):
    doc = Document()
    st = doc.styles["Normal"]; st.font.name = "Arial"; st.font.size = Pt(10.5)
    estilo = {"name": "Title", "h": "Heading 1", "li": "List Bullet"}
    for k, v in bs:
        p = doc.add_paragraph(style=estilo.get(k, "Normal"))
        p.add_run(v).bold = k == "job"
    doc.save(ruta)


def a_html(bs, ruta):
    tag = {"name": "h1", "contact": "p", "h": "h2", "job": "h3", "p": "p"}
    partes, en_lista = [], False
    for k, v in bs:
        if k == "li" and not en_lista:
            partes.append("<ul>"); en_lista = True
        if k != "li" and en_lista:
            partes.append("</ul>"); en_lista = False
        t = "li" if k == "li" else tag[k]
        partes.append(f"<{t}>{html.escape(v, quote=False)}</{t}>")
    if en_lista:
        partes.append("</ul>")
    css = ("body{font-family:Arial,Helvetica,sans-serif;font-size:10.5pt;max-width:7.5in;margin:auto}"
           "h1{font-size:18pt;margin:0}h2{font-size:12pt;border-bottom:1px solid #999;margin-top:14pt}"
           "h3{font-size:10.5pt;margin:8pt 0 2pt}ul{margin:2pt 0;padding-left:16pt}"
           "@page{margin:0.6in}")
    ruta.write_text(f'<!doctype html><html><head><meta charset="utf-8"><title>CV</title>'
                    f"<style>{css}</style></head><body>\n" + "\n".join(partes) + "\n</body></html>\n",
                    encoding="utf-8")


def main():
    if len(sys.argv) != 2:
        sys.exit("Uso: build_cv.py cv.md")
    src = pathlib.Path(sys.argv[1])
    if not src.is_file():
        sys.exit(f"No existe el archivo: {src}")
    bs = bloques(src.read_text(encoding="utf-8"))
    if not bs:
        sys.exit("El Markdown está vacío.")
    a_docx(bs, src.with_suffix(".docx"))
    a_html(bs, src.with_suffix(".html"))
    print(f"OK: {src.with_suffix('.docx')} y {src.with_suffix('.html')}")


if __name__ == "__main__":
    main()
