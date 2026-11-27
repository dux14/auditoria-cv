---
name: auditoria-cv
description: "Entrevista al usuario y reescribe su CV / hoja de vida / currículum / resume en dos modos: (1) un CV genérico fuerte para un tipo de rol, o (2) un CV a medida de una oferta concreta. Pregunta el enfoque, pide el CV actual (PDF, DOCX, foto o texto), diagnostica qué extrae un ATS (PDF-imagen, columnas, tablas, texto oculto), investiga en la web la oferta, la empresa y el rol, cruza requisitos contra el perfil, pregunta métricas, periodos y alcance reales, y entrega el CV nuevo en DOCX y PDF con un informe QUITAR / CAMBIAR / MEJORAR / AÑADIR y un perfil maestro reutilizable; opcional: carta de presentación y preparación de entrevista. Alineado a cómo se filtra hoy: preguntas eliminatorias, parseo, búsqueda y ranking con IA (p. ej. Workday HiredScore) y triaje humano. Úsala SIEMPRE que el usuario mencione CV, hoja de vida, currículum, resume, ATS, filtros automáticos, postular a una oferta, adaptar el CV a una vacante, LinkedIn o 'por qué no me llaman', aunque no pida una 'auditoría'."
license: MIT
---

# Auditoría y reescritura de CV (edición 2026-12)

## Qué hace

Lleva al usuario de su CV actual a uno nuevo, listo para enviar, mediante una
entrevista corta en fases. No devuelve un "puntaje ATS": esos números los inventan las
herramientas que los venden. Devuelve qué ve la máquina, qué ve el humano en la primera
pasada, qué pide el rol o la oferta, qué del perfil lo prueba, y la versión reescrita.

Dos modos, elegidos en la Fase 0:

- **Genérico**: CV fuerte para un tipo de rol y mercado. Se compara contra ofertas
  reales y recientes de ese rol.
- **Oferta**: CV a medida de una vacante. Se compara contra esa oferta, su empresa y su
  proceso.

Idioma: habla con el usuario en su idioma. El CV se entrega en el idioma acordado en la
Fase 0 (por defecto, el de la oferta o el mercado).

## Cómo se filtra hoy (léelo antes de afirmar nada)

Detalle y fuentes en `references/ats-realidad.md`. Resumen, en el orden en que eliminan:

1. **Preguntas eliminatorias** del formulario (autorización de trabajo, ubicación,
   años, salario). Es el rechazo automático real más común.
2. **Parseo**: si el ATS no extrae bien el texto (PDF-imagen, columnas mal hechas,
   contacto en el encabezado), el perfil queda vacío o desordenado.
3. **Búsqueda y ranking**: el reclutador busca por título, herramientas y términos;
   capas con LLM (p. ej. Workday HiredScore, calificación A-D por requisitos) leen
   contexto y priorizan, casi nunca rechazan solas. El relleno de palabras no sirve; el
   requisito real escrito con el término exacto, sí.
4. **Triaje humano** de pocos segundos con cientos de postulaciones. Penaliza el texto
   genérico que suena a IA.
5. Antes de todo eso: **referidos y sourcing** convierten varias veces más que postular
   en frío. Dilo cuando ayude.

Si el usuario pide trucos (texto blanco, keyword stuffing, instrucciones ocultas a un
LLM), explica que se detectan (≈1 % de CVs reales ya lo intentan y los sistemas y
reclutadores lo buscan) y que dañan la candidatura. No lo hagas.

## Herramientas: instálalas, no dependas de lo que haya

Los scripts declaran sus dependencias (PEP 723) y solo necesitan Python 3.9+. Las rutas
de `scripts/` son relativas a la carpeta de esta skill.

1. Si existe `uv`, úsalo: `uv run scripts/<script>.py ...` instala todo en un entorno
   aislado la primera vez.
2. Si no existe, instálalo sin permisos de administrador: `python3 -m pip install --user uv`
   y ejecuta con `python3 -m uv run scripts/<script>.py ...`.
3. Si `pip` está bloqueado: `python3 -m pip install pdfplumber python-docx playwright`
   y `python3 scripts/<script>.py ...`.
4. Para el PDF, `build_cv.py` descarga Chromium (Playwright) la primera vez si no está.
   Si la red lo impide y existe LibreOffice, `soffice --headless --convert-to pdf CV.docx`.

No pidas al usuario que instale nada a mano salvo que todo lo anterior falle; en ese
caso dile el comando exacto. Si no puedes ejecutar comandos (chat sin herramientas),
haz el análisis leyendo el texto del archivo y dilo en el informe.

## Flujo

Sigue las fases en orden. No saltes la entrevista: sin contexto, la reescritura es
cosmética. Banco de preguntas en `references/entrevista.md`.

### Fase 0 - Enfoque

Pregunta (como mucho 5 cosas, numeradas): modo genérico u oferta, rol y nivel objetivo,
mercado, idioma del CV y situación (empleado, cambio de carrera, pausa...). Si el
usuario ya respondió algo en su mensaje, no lo repitas.

### Fase 1 - Insumos

Pregunta primero si tiene un **perfil maestro** (`perfil-<nombre>.md`) de una sesión
anterior. Si lo tiene, léelo: es la fuente de verdad, y en la Fase 5 solo preguntas lo
que falte para este rol u oferta.

Pide el CV actual, el que realmente envía. Acepta PDF, DOCX, imagen (foto o captura:
PNG, JPG, WEBP), TXT o Markdown. Si es .doc, .odt o .pages, pide que lo exporte a PDF o
DOCX. En modo oferta, la oferta completa (enlace o texto); guarda el texto como
`vacante.txt`. Opcional: LinkedIn como texto, portafolio, repos. No audites de memoria ni
a partir de una descripción verbal; si el usuario no tiene CV, la entrevista de la Fase 5
construye el perfil maestro desde cero y la Fase 2 se salta.

### Fase 2 - Diagnóstico mecánico

```bash
uv run scripts/parse_check.py CV.pdf [--vacante vacante.txt] --json diag.json --png
```

Acepta PDF, DOCX, imagen (PNG, JPG, WEBP, GIF) o texto (TXT, MD). El DOCX se analiza
directo, como lo lee un ATS: tablas, columnas, cuadros de texto, texto oculto, contacto
en encabezado o pie e imágenes pegadas. Cubre además
PDF-imagen, contacto, fechas, secciones estándar, bullets con alcance y cobertura de
términos.

- **`[BLOQUEANTE]` imagen o PDF escaneado**: el ATS extrae cero palabras. Díselo y
  sigue, porque igual vas a reconstruir el documento. El script deja cada página como
  PNG (`<archivo>.pN.png`; en un DOCX, `<archivo>.imgN.*`; con una imagen, el propio archivo): **léelas tú y transcribe
  el contenido** a `cv-transcrito.md` antes de seguir. Marca lo ilegible como `<?>` y
  pregúntalo en la Fase 5; no adivines cifras ni fechas borrosas.
- Lee el `.ats.txt` completo: ¿nombre y cargo pegados?, ¿barra lateral intercalada?,
  ¿fechas huérfanas? Cita los fragmentos rotos textualmente.
- Triaje visual: mira `CV.pdf.p1.png` (lo genera `--png` con un PDF con texto; en uno
  escaneado las páginas salen siempre, hasta 10). En el tercio
  superior, ¿queda claro quién es, qué hace y para qué rol sirve?

### Fase 3 - Investigación externa

Usa la búsqueda web si la tienes. Cita cada dato con enlace y fecha. Si no hay
búsqueda, dilo y trabaja con la oferta y el estándar del rol.

**Modo oferta:**
- La oferta completa: requisitos duros frente a deseables, título exacto, años,
  ubicación o modalidad, idioma. Greenhouse y Lever tienen API pública de solo lectura
  que da el texto íntegro y la fecha (`boards-api.greenhouse.io/v1/boards/<empresa>/jobs/<id>`,
  `api.lever.co/v0/postings/<empresa>?mode=json`). Los agregadores (Jobgether, Remotive,
  etc.) suelen tener ofertas vencidas.
- **¿Sigue abierta?** Si la página da 404/410 o la oferta no aparece en el portal de la
  empresa, díselo antes de invertir la entrevista: puede adaptar el CV igual (sirve para
  ofertas parecidas) o elegir otra. Si el usuario pegó el texto, úsalo aunque haya cerrado.
- El ATS, por la URL del portal: `myworkdayjobs.com` → Workday; `greenhouse.io` →
  Greenhouse; `lever.co` → Lever; `ashbyhq.com` → Ashby; `smartrecruiters.com`,
  `icims.com`, `successfactors` → los suyos. Ajusta: en Workday, requisitos escritos con
  el término exacto, porque la calificación por requisitos los busca.
- La empresa: qué hace, producto, stack o herramientas, noticias recientes, valores y
  vocabulario propio. Sirve para el resumen y para elegir qué logros poner arriba.
- Preguntas eliminatorias probables del formulario.

**Modo genérico:**
- 5-10 ofertas reales de los últimos 60 días del rol, nivel y mercado elegidos.
  Extrae títulos usados, requisitos que se repiten (con cuántas ofertas lo piden),
  herramientas y certificaciones. Escribe "según N ofertas revisadas el <fecha>".
- Usa `references/mercados.md` para las convenciones del país.

### Fase 4 - Mapa de brechas

Cruza requisitos contra el CV en una tabla: requisito, peso (duro / deseable), evidencia
en el CV (dónde), estado (cubierto / parcial / ausente). Cura los términos en cuatro
cubetas: herramientas, título del cargo, metodologías o dominio, certificaciones e
idiomas. Lo ausente que el usuario no tiene es **brecha real**: se dice, no se tapa.
Muestra el mapa al usuario de forma breve antes de la Fase 5.

### Fase 5 - Entrevista de evidencia

Pregunta lo que solo el usuario sabe, priorizado por impacto (ver
`references/entrevista.md`): periodos (mes/año), títulos oficiales, métricas y alcance
por bullet, experiencia real con cada requisito ausente o parcial, certificaciones,
pausas. Como mucho 5 preguntas por turno; repite hasta cubrir lo importante o hasta que
el usuario diga que no tiene más datos. Cada respuesta entra al registro de evidencia
con su estado. **No pases a la Fase 6 mientras quede un requisito duro del mapa de
brechas sin preguntar**: cada uno termina como evidencia o como brecha real confirmada.

Al terminar, escribe o actualiza el **perfil maestro** con la forma de
`assets/perfil-maestro.md` en la carpeta de trabajo del usuario: todo lo que contó,
también lo que no entra en este CV, con su estado y fuente. Díselo en una línea: la
próxima vez lo adjunta y te ahorras preguntas.

### Fase 6 - Reescritura

Parte de `assets/cv-ats-base.md`. Reglas de redacción en `references/redaccion.md`.

- Una columna, encabezados estándar, contacto en el cuerpo, fechas en un solo formato.
- Arriba, en dos a cuatro líneas: título objetivo (el de la oferta si es cierto), años,
  dominio, herramientas clave y una prueba.
- Bullets de logro: verbo + qué, con el término exacto + alcance o resultado + con qué.
- Términos de la oferta escritos igual que en la oferta, en Skills **y** en la
  experiencia donde se usaron. Sigla y forma completa la primera vez.
- Orden por relevancia para el rol; lo antiguo o irrelevante se resume.
- Modo genérico: sin nombres de empresa objetivo; título y resumen del rol, no de una
  oferta.

### Fase 7 - Entrega y verificación

1. **CV en DOCX** (el formato más seguro para portales) y **PDF**. Escribe el CV en
   Markdown con la forma de `assets/cv-ats-base.md` como `Nombre-Apellido-Rol.md` y:
   ```bash
   uv run scripts/build_cv.py Nombre-Apellido-Rol.md            # A4
   uv run scripts/build_cv.py Nombre-Apellido-Rol.md --letter   # EE.UU./Canadá
   ```
   Genera `.docx`, `.html` y `.pdf`. Nunca sobrescribe archivos existentes: si el nombre
   choca con el CV original, usa otro (p. ej. `-v2`); no uses `--force` sobre el original. Si no puedes generar archivos, entrega el texto
   completo listo para pegar en una plantilla de una columna y explica cómo exportar a
   PDF desde Word o Google Docs.
2. **Verificación**: corre `parse_check.py` sobre el PDF nuevo y muestra el antes y el
   después (contacto, fechas, secciones, cobertura de términos, bullets con alcance).
3. **Informe** breve con la estructura de `references/plantilla-informe.md`: cambios
   QUITAR / CAMBIAR / MEJORAR / AÑADIR con original y reemplazo, registro de evidencia,
   brechas reales y respuestas sugeridas para las preguntas del formulario.
4. **Perfil maestro** actualizado (`perfil-<nombre>.md`).
5. Ofrece en una línea los extras de `references/extras.md`: **carta de presentación**
   y **preparación de entrevista** (preguntas probables desde el registro de evidencia y
   las brechas, con puntos STAR). Solo si los pide.
6. Si pide otro formato (Google Docs, LaTeX, versión con diseño, LinkedIn con
   `references/linkedin-2026.md`), hazlo aparte. La versión con diseño sirve para
   referidos o entrega en mano, nunca para el portal.

## Reglas de honestidad

- **Sin métricas inventadas.** Si no hay cifra, usa alcance verificable o deja `<N>`
  para que el usuario lo complete. Nada de números redondos estimados por ti.
- **Registro de evidencia**: cada cifra y herramienta del CV nuevo tiene un estado:
  - VERIFICADO: enlace, documento o carta.
  - USER-ATTESTED: el usuario la afirma con certeza y puede defenderla en voz alta.
  - ESTIMADO: el usuario la estima con un método que sabe explicar ("unos 40 tickets
    al día según el tablero"). Entra solo como aproximado ("~40", "30-40") y la anotas
    para confirmar. La estimación es del usuario, nunca tuya.
  - PENDIENTE: falta el dato. No entra; usa alcance o `<N>`.
- **No inflar** títulos, fechas ni niveles. Se describe el alcance real con el título
  oficial. No se esconden fechas para tapar huecos.
- **Nada oculto**: ni texto blanco, ni palabras en márgenes, ni instrucciones a un LLM.
- **No inventar certificaciones** ni insinuarlas.
- **Sin prosa genérica de IA** ("results-driven", "spearheaded", "leveraged"): los
  detalles concretos son del usuario.
- Si el CV es débil para la oferta, dilo y explica la brecha. Vale más que una
  reescritura cosmética.
- Los datos del usuario (CV, contacto, empleadores) se usan solo para esta tarea. No
  los pongas en búsquedas web: busca la oferta, la empresa y el rol, no a la persona.
- **Archivos personales en local**: el perfil maestro, `cv-transcrito.md`, los `.ats.txt`
  y los PNG de páginas contienen datos personales (y el perfil, salario y visa). Se
  guardan en la carpeta de trabajo del usuario; dile que no los suba a repos ni a sitios
  públicos. Si la carpeta es un repo git, sugiere ignorarlos.

## Archivos

- `scripts/parse_check.py`: diagnóstico de PDF, DOCX, imagen o texto (Fases 2 y 7)
- `scripts/build_cv.py`: Markdown a DOCX, HTML y PDF de una columna (Fase 7)
- `references/ats-realidad.md`: qué filtra de verdad, con fechas y fuentes
- `references/entrevista.md`: banco de preguntas por fase
- `references/mercados.md`: convenciones por país o región
- `references/redaccion.md`: bullets, verbos, alcance, resumen
- `references/plantilla-informe.md`: estructura del informe
- `references/linkedin-2026.md`: perfil de LinkedIn (opcional)
- `references/extras.md`: carta de presentación y preparación de entrevista (opcional)
- `assets/cv-ats-base.md`: esqueleto de CV a prueba de parser
- `assets/perfil-maestro.md`: inventario reutilizable de la entrevista
