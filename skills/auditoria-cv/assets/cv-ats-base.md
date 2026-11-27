# Esqueleto de CV a prueba de parser

Una columna. Sin tablas, sin cuadros de texto, sin iconos, sin barras, sin foto.
Nada en encabezado ni pie de página. Fuente estándar 10–12 pt. Márgenes 1" (mínimo 0.5").
Formato Markdown que entiende `scripts/build_cv.py`: `## ` = sección, línea en
**negrita** = cargo, `- ` = bullet. Encabezados en el idioma del CV (aquí en inglés).
Orden de secciones (el que mejor parsea): contacto → resumen → habilidades →
experiencia → educación → certificaciones.

---

NOMBRE APELLIDO
Ciudad, País | correo@dominio.com | +<código país> <teléfono> | linkedin.com/in/usuario

## Summary
[Título del rol al que aplicas] con [X años] en [dominio]. [2-3 herramientas duras que
pide la oferta, con el nombre exacto]. [Un logro con cifra].

## Skills
[Lista simple separada por comas, agrupada por tipo si ayuda. Los términos clave también
deben aparecer en la experiencia, con contexto. Sigla y forma completa la primera vez.]

## Experience

**Cargo | Empresa | Ciudad | MM/AAAA – MM/AAAA**
- [Verbo] + [qué, con el término técnico] + [resultado cuantificado]
- ...

**Cargo | Empresa | Ciudad | MM/AAAA – MM/AAAA**
- ...

## Education
Título | Institución | AAAA

## Certifications
Nombre exacto de la certificación | Emisor | AAAA

## Languages
<Idioma> (nativo), <Idioma> (<nivel MCER o certificado>)

---

Notas de exportación:
- DOCX es el formato más seguro salvo que el portal pida PDF explícitamente.
- Si exportas a PDF: abre el PDF, selecciona todo y copia. Si no puedes copiar el
  texto, el ATS tampoco. Nunca exportes desde Canva/Figma como imagen.
- Guarda el archivo como Nombre_Apellido_Cargo.pdf, no como "CV final v3 (2).pdf".
