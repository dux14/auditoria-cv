#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["python-docx==1.2.0", "playwright==1.65.2"]
# ///
"""
build_cv.py - Convierte un CV en Markdown simple a DOCX, HTML y PDF de una columna (ATS-seguro).

Uso (uv instala las dependencias solo; sin uv: pip install python-docx==1.2.0 playwright==1.65.2):
    uv run scripts/build_cv.py cv.md [--letter] [--sin-pdf] [--force]   # --letter: EE.UU./Canadá; por defecto A4
Genera cv.docx, cv.html y cv.pdf junto al .md. El PDF se imprime con Chromium vía
Playwright; si Chromium no está, se descarga una vez (~150 MB, sin permisos de admin).

Markdown aceptado (lo que produce assets/cv-ats-base.md):
    primera línea = nombre; líneas antes del primer "## " = contacto;
    "## Sección" = encabezado; "### X" o línea entera en **negrita** = cargo; "- " = bullet;
    el resto, párrafo. Se quitan negrita/cursiva y "---"; [texto](url) queda "texto (url)".
    No sobrescribe .docx/.html/.pdf existentes salvo con --force.
    shortcut: cada línea es un párrafo (no une líneas partidas); escribe cada párrafo en una línea.
"""
import html, pathlib, re, subprocess, sys

from docx import Document
from docx.shared import Pt


def bloques(md):
    """Devuelve [(tipo, texto)] con tipo en name|contact|h|job|li|p."""
    out, vistos_h = [], False
    md = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", " ", md.lstrip("\ufeff"))
    for linea in md.splitlines():
        t = linea.strip()
        if not t or re.fullmatch(r"[-*_]{3,}", t):
            continue
        if t.startswith("### "):
            out.append(("job", t[4:].strip())); vistos_h = True
        elif t.startswith("## "):
            out.append(("h", t[3:].strip())); vistos_h = True
        elif not out:
            out.append(("name", t.lstrip("# ").strip()))
        elif not vistos_h:
            out.append(("contact", t))
        elif re.fullmatch(r"\*\*(.+)\*\*", t):
            out.append(("job", t[2:-2]))
        elif t[:2] in ("- ", "* ", "+ "):
            out.append(("li", t[2:]))
        else:
            out.append(("p", t))
    def limpio(v):
        v = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", v)
        v = re.sub(r"(\*\*|__)(.+?)\1", r"\2", v)
        v = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"\1", v)
        return re.sub(r"\s{2,}", " ", v).strip()
    return [(k, limpio(v)) for k, v in out]


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


def a_pdf(html_path, pdf_path, formato="A4"):
    from playwright.sync_api import sync_playwright, Error
    def imprimir():
        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page()
            pg.goto(html_path.resolve().as_uri())
            pg.pdf(path=str(pdf_path), format=formato, print_background=False)
            b.close()
    try:
        try:
            imprimir()
        except Error as e:
            if "Executable doesn't exist" not in str(e):
                raise
            print("Instalando Chromium para generar el PDF (una sola vez)...", file=sys.stderr)
            subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
            imprimir()
    except (Error, subprocess.CalledProcessError, OSError) as e:
        sys.exit(f"No se pudo generar el PDF con Chromium ({str(e).splitlines()[0][:200]}).\n"
                 "El DOCX y el HTML ya estan listos. Alternativas: `soffice --headless --convert-to pdf "
                 "<archivo>.docx`, o en Linux `python -m playwright install --with-deps chromium`.")


def main():
    banderas = ("--sin-pdf", "--letter", "--force")
    args = [x for x in sys.argv[1:] if x not in banderas]
    if len(args) != 1:
        sys.exit("Uso: build_cv.py cv.md [--letter] [--sin-pdf] [--force]")
    src = pathlib.Path(args[0])
    if not src.is_file():
        sys.exit(f"No existe el archivo: {src}")
    exts = [".docx", ".html"] + ([] if "--sin-pdf" in sys.argv else [".pdf"])
    existentes = [str(src.with_suffix(e)) for e in exts if src.with_suffix(e).exists()]
    if existentes and "--force" not in sys.argv:
        # el CV original del usuario suele llamarse igual: no lo pisamos sin permiso
        sys.exit("Ya existen: " + ", ".join(existentes) + ". Usa otro nombre para el .md o --force.")
    bs = bloques(src.read_text(encoding="utf-8-sig"))
    if not bs:
        sys.exit("El Markdown está vacío.")
    a_docx(bs, src.with_suffix(".docx"))
    a_html(bs, src.with_suffix(".html"))
    hechos = [src.with_suffix(".docx"), src.with_suffix(".html")]
    if "--sin-pdf" not in sys.argv:
        a_pdf(src.with_suffix(".html"), src.with_suffix(".pdf"), "Letter" if "--letter" in sys.argv else "A4")
        hechos.append(src.with_suffix(".pdf"))
    print("OK: " + ", ".join(map(str, hechos)))


if __name__ == "__main__":
    main()
