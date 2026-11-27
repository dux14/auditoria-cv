# Changelog

## 2026.12 - 2026-11-27

- Perfil maestro (`assets/perfil-maestro.md`): la entrevista queda guardada y el siguiente CV solo pregunta lo que falte.
- Extras opcionales (`references/extras.md`): carta de presentación y preparación de entrevista desde el registro de evidencia.
- Estado ESTIMADO en el registro de evidencia: cifras que el usuario estima con método, solo como aproximadas.
- Insumos: imágenes (foto o captura), TXT/MD, PDF escaneado y DOCX con el CV pegado como imagen; se exportan las páginas para transcribirlas.
- La entrevista no avanza a la reescritura con requisitos duros sin preguntar; se avisa si la oferta ya cerró.
- `parse_check.py`: el texto blanco sobre un fondo oscuro ya no se marca como oculto; sin ruido de pdfminer; menos relleno en inglés al comparar con la vacante.
- Batería E2E de 44 pruebas con PDF, DOCX, imágenes, texto y casos límite (cifrados, corruptos, no latinos, rutas con espacios, Letter).

## 2026.11 - 2026-11-27

- Flujo de entrevista en fases: enfoque, insumos, diagnóstico, investigación web de la oferta o el rol, mapa de brechas, preguntas de evidencia (métricas, periodos, alcance) y entrega.
- Dos modos: CV genérico para un rol y CV a medida de una oferta, con detección del ATS por la URL del portal.
- Nuevo `scripts/build_cv.py`: Markdown a DOCX, HTML y PDF de una columna (A4 o Letter).
- Sin herramientas del sistema: los scripts declaran sus dependencias (PEP 723) y se instalan solas con `uv`; Chromium se descarga la primera vez para el PDF.
- `parse_check.py`: sin poppler (pdfplumber); analiza DOCX directo (tablas, columnas, cuadros de texto, texto oculto, encabezado/pie) y genera el PNG de la página 1 con `--png`. Corrige el falso «PDF-imagen» cuando faltaba poppler.
- Skill genérica: se retiran el modo AI engineer y la guía de España (siguen en el tag `v2026.10`); se añaden `references/entrevista.md` y `references/mercados.md`.
- El repo es un marketplace de Claude Code: instalación con `/plugin marketplace add dux14/auditoria-cv` y actualización automática.

## 2026.10 — 2026-10-19

- Modo CV de IA / AI engineer: agentes, MCP, evals y bloque de habilidades defendible.
- Modo perfil de LinkedIn: kit de texto listo para pegar, optimizado para búsqueda de reclutadores.
- Adaptación al mercado de España/UE, además de Colombia/LATAM y EE.UU./remoto.
- Registro de evidencia: cada cifra y herramienta del CV se enlaza con su fuente.

## 2026.07

- Primera versión: auditoría de CV con diagnóstico ATS e informe QUITAR / CAMBIAR / MEJORAR / AÑADIR.
