# Changelog

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
