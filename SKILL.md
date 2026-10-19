---
name: auditoria-cv
description: "Audita una hoja de vida / CV / resume (PDF o DOCX) y produce un informe accionable por secciones con QUITAR / CAMBIAR / MEJORAR / AÑADIR, más la versión reescrita lista para enviar. Diagnostica primero qué texto extrae realmente un ATS (PDF-imagen, doble columna, tablas, texto oculto, campos no mapeables) y luego el contenido. Incluye registro de evidencia (cada cifra y herramienta del CV con su fuente), modo CV de IA / AI engineer (agentes, MCP, evals), modo perfil de LinkedIn (texto listo para pegar, optimizado para búsqueda de reclutadores) y adaptación al mercado de España/UE, Colombia/LATAM y EE.UU./remoto. Funciona con o sin una vacante específica. Usa esta skill SIEMPRE que el usuario mencione hoja de vida, CV, currículum, resume, ATS, filtros automáticos, postulación, LinkedIn, perfil de LinkedIn, reclutadores, headline, 'por qué no me llaman', CV de IA, AI engineer, mercado de España, o pida revisar/mejorar/adaptar su CV o su perfil, incluso si no pide explícitamente una 'auditoría'."
---

# Auditoría de CV (edición 2026-10)

## Qué hace esta skill

Convierte un CV (y, si se pide, un perfil de LinkedIn) en cambios concretos. No
devuelve un "puntaje ATS": esos números los inventan las herramientas que los venden.
Devuelve qué ve la máquina, qué ve el humano en la primera pasada, qué afirmaciones
del CV no tienen respaldo, y qué línea exacta cambiar por cuál.

Idioma: la prosa de la skill y del informe va en español neutro. Todo texto que el
usuario vaya a enviar o publicar (CV, bullets, headline, About) se produce en
**inglés**, salvo que pida expresamente otro idioma.

## Premisa correcta (verificada el 2026-10-19)

Lee `references/ats-realidad.md` antes de afirmar algo sobre filtros. Resumen:

- El estudio de Enhancv (2 de 25 reclutadores con rechazo automático por contenido)
  es de **nov. 2025**, no de 2026. Lo hizo un proveedor de herramientas de CV, con
  muestra pequeña y no representativa. Úsalo como indicio, no como prueba.
- El rechazo automático real son las **preguntas eliminatorias** del formulario.
- Existe ranking con LLM (p. ej. calificaciones A-D de Workday HiredScore, ago.
  2026): prioriza, no suele rechazar. Lee contexto, así que el relleno de palabras
  clave no sirve y el texto oculto es un riesgo (inyección de prompts, detectada y
  mal vista).
- Pesan más los **referidos y el sourcing** que el CV en frío (Gem: referidos 11x
  frente a postulación directa). El CV se lee tras una recomendación o una búsqueda.
- "6 segundos" es una cifra antigua (2012; 7,4 s en 2018) y no se ha replicado.
  Di "unos pocos segundos, menos de ~10".
- Ningún "puntaje ATS" de herramienta es predictivo. Confía en: extracción
  determinista (`pdftotext`), autorrelleno del portal real, revisión humana.

Si el usuario pide trucos para engañar al filtro (texto blanco, stuffing, inyección de
prompts), explica que no funciona de forma demostrada, que un humano o un LLM lo ve, y
redirige. No lo hagas.

## Insumos

- **Obligatorio**: el CV, PDF preferido. Si es DOCX, conviértelo
  (`soffice --headless --convert-to pdf`) o léelo con la skill `docx`, y audita también
  el PDF que el usuario realmente envía.
- **Decisivo**: la vacante (`vacante.txt`). Sin ella, el cruce de términos se hace contra
  el estándar del rol.
- **Para el registro de evidencia**: repos, enlaces, notas del usuario. Pídelos.
- No auditar de memoria ni a partir de una descripción verbal.

## Modos

Elige según el pedido; pueden combinarse. El flujo de CV (abajo) es la base.

- **CV general o para una vacante**: Pasos 1-7.
- **CV para roles de IA / AI engineer**: Pasos 1-7 más `references/roles-ia-2026.md`
  (vocabulario de ofertas, título objetivo, headline, bloque de habilidades, qué
  preguntará la entrevista) y `assets/cv-ai-engineer-base.md`.
- **LinkedIn**: `references/linkedin-2026.md`. Auditoría por campos, salida
  QUITAR/CAMBIAR/MEJORAR/AÑADIR y texto listo para pegar.
  **Regla fija: nunca automatices LinkedIn** (Acuerdo de Usuario, sección 8.2, vigente
  desde nov. 2025: prohíbe bots, scraping y automatización; riesgo de restricción de
  la cuenta). La skill produce texto; el usuario lo aplica a mano. No uses ni
  recomiendes MCP ni extensiones de LinkedIn sobre una cuenta principal (además, el
  MCP no-oficial evaluado no puede editar perfiles; detalle en la referencia).
- **Mercado**: confirma el destino antes de recomendar foto, documento o extensión.
  - Colombia / LATAM ("hoja de vida"): foto y cédula siguen apareciendo en ofertas
    locales, pero son ruido en procesos corporativos o multinacionales. Portales:
    Computrabajo, elempleo, Magneto, LinkedIn.
  - EE.UU. / Reino Unido / remoto internacional: sin foto, edad, estado civil ni
    documento (riesgo de sesgo).
  - España / UE: `references/espana.md` (CV en inglés válido en tech, autorización de
    trabajo para candidatos no UE, mercado, zona horaria).
  - Extensión: 1 página con 0-5 años; 2 páginas aceptables si la segunda está al
    menos medio llena y es relevante. No hay regla estricta con evidencia. Evita
    "una página y tres líneas".

## Flujo de CV

### Paso 1 - Diagnóstico mecánico (siempre primero)

```bash
python3 scripts/parse_check.py CV.pdf --vacante vacante.txt --json diag.json
```

Cubre PDF-imagen, columnas, tablas, texto oculto, contacto, fechas, secciones estándar
(incluye Summary, Skills, Experience, Education, Certifications, Projects, Languages),
referencia de bullets con alcance y cobertura de términos.

**Si reporta `[BLOQUEANTE] PDF-imagen`, detente.** El ATS extrae cero palabras.
Ofrece reconstruir el documento (típico en exportaciones de Canva).

Las tablas son advertencia, no bloqueo: una cuadrícula simple de habilidades puede
parsear bien (una sola prueba, de un proveedor). Verifica en el `.ats.txt`. Además
comprueba que el contacto esté en el cuerpo y no solo en encabezado o pie.

### Paso 2 - Leer lo que lee la máquina

Abre el `.ats.txt` completo. Ninguna herramienta reemplaza esto: ¿nombre y cargo
pegados?, ¿la barra lateral intercalada?, ¿fechas huérfanas?, ¿se entiende la
trayectoria? Cita los fragmentos rotos textualmente en el informe. Si el portal real
autorrellena campos al subir el CV, revisa nombre, correo, fechas y cargos: es la
señal más cercana a un ATS real.

### Paso 3 - Triaje humano rápido

```bash
pdftoppm -jpeg -r 150 -f 1 -l 1 CV.pdf /tmp/pag && ls /tmp/pag*
```

En el tercio superior de la página 1: ¿queda claro **quién es**, **qué hace** y **para
qué rol sirve**? Si hay que bajar para entenderlo, es un hallazgo grave.

### Paso 4 - Curar los términos de la vacante

El script propone candidatos ruidosos; cúralos en cuatro cubetas:

| Cubeta | Ejemplos | Peso |
|---|---|---|
| Herramientas / tecnologías | Playwright, MCP, Kubernetes | Alto |
| Título del cargo | "Applied AI Engineer" | Alto |
| Metodologías / dominios | evals, CI quality gates | Medio |
| Certificaciones / idiomas | requisito duro | Alto solo si es duro |

Reglas:

- Espeja el lenguaje exacto de la oferta, solo donde sea cierto. Sigla y forma completa
  la primera vez.
- Un término ausente que el usuario no domina es una brecha real, no un hallazgo de
  redacción: díselo.
- Las habilidades van como líneas simples separadas por comas bajo un encabezado
  estándar. Los parsers las leen peor que otros campos (46-65 % en una prueba de
  proveedor), así que además deben aparecer en bullets de experiencia con contexto.
- No hay evidencia de que la sección de Habilidades pese más que el resto. No lo
  afirmes.

### Paso 5 - Registro de evidencia (obligatorio antes de reescribir)

Cada cifra y cada herramienta del CV reescrito debe mapearse a una fuente verificable
(repo, PR, documento, ticket, perfil público, carta laboral) o quedar marcada
**USER-ATTESTED** (el usuario la afirma y puede defenderla en voz alta). Sin una de las
dos, no entra al CV; se reemplaza por alcance o se pregunta al usuario.

Advierte de lo que el entrevistador va a sondear: MCP (¿cuántas herramientas, qué
permisos, cómo lo probaste?), RAG (¿qué métrica de recuperación?), evals (¿qué dataset,
qué grader, qué compuerta?), agentes (¿por qué un agente y no un script?). Regla
práctica: toda cifra y herramienta debe poder explicarse en dos minutos y sin el IDE.
Es una regla de criterio, no un dato medido. Formato en `references/plantilla-informe.md`.

### Paso 6 - El informe

Estructura exacta en `references/plantilla-informe.md`. Cada hallazgo es una acción con
el texto original y el reemplazo lado a lado:

- **QUITAR**: foto, documento, dirección exacta, "referencias disponibles", objetivos
  genéricos, barras de nivel.
- **CAMBIAR**: función a logro; título no estándar a estándar.
- **MEJORAR**: bullet sin alcance, verbo débil.
- **AÑADIR**: habilidades reales ausentes, prueba pública que falta.

Prioridad: parsing, luego brecha de términos y de pruebas públicas, luego redacción.
Redacción y fórmulas de bullets en `references/redaccion.md`.

### Paso 7 - Entregables y verificación

1. **Informe** (chat o `.md`), con registro de evidencia y, si hay brecha, la sección
   "Brecha de pruebas públicas".
2. **CV reescrito en `.docx` real** (skill `docx`; una columna, sin cuadros de texto)
   y **PDF** exportado de ese DOCX. Parte de `assets/cv-ats-base.md`, o de
   `assets/cv-ai-engineer-base.md` para roles de IA.
3. **`.ats.txt`** de la versión nueva, generado por `parse_check.py`.
4. **Kit de LinkedIn** (headline, About, experiencia, habilidades, Featured) solo si lo
   pidió, en inglés y listo para pegar.
5. Versión con diseño solo si la pide, para referidos o entrega en mano; nunca para el
   portal.

Corre `parse_check.py` sobre el PDF nuevo y muestra el antes/después.

## Reglas de honestidad

- **Sin métricas inventadas.** Si no hay cifra, usa alcance verificable (tamaño del
  equipo, volumen, frecuencia, antes/después reales) o deja un marcador `<N>` para que
  el usuario lo complete con su dato real. Evita números redondos sospechosos.
- **No inflar títulos** ni fechas. Prohibido "Lead" o "Senior" que el empleador no haya
  otorgado, aunque el rol lo exigiera de facto. Se describe el alcance real
  ("coordiné a N personas") y el título oficial.
- **Desarrollo asistido por IA**: divúlgalo como flujo gobernado (el agente hace X, un
  humano revisa Y, las compuertas Z), con evidencia revisable. Nunca "vibe coding", y
  nunca atribuyas al usuario autoría de lo que no puede explicar.
- **Nunca ocultar texto**, ni palabras clave en blanco ni instrucciones a un LLM
  ("ignora lo anterior"). Es inyección de prompts: medida en ~1 % de CVs, vista por 22 %
  de los gerentes de contratación encuestados por Greenhouse, y de efecto no demostrado.
- Las certificaciones no se inventan ni se insinúan. Las de Claude no están abiertas a
  individuos.
- Si el CV es débil para la vacante, dilo. Vale más que una reescritura cosmética.
- Los reclutadores penalizan el texto genérico escrito con IA. Usa IA para editar y
  deja que los detalles verificables sean del usuario.

## Archivos de esta skill

- `scripts/parse_check.py`: diagnóstico mecánico (Paso 1)
- `references/ats-realidad.md`: qué filtra de verdad, con fechas y fuentes
- `references/redaccion.md`: bullets, verbos, alcance, fórmulas para IA, QA a IA
- `references/roles-ia-2026.md`: vocabulario de ofertas de IA, títulos, headline, entrevista
- `references/linkedin-2026.md`: perfil de LinkedIn, límites, límites de ToS, checklist
- `references/espana.md`: CV en España, autorización de trabajo, mercado
- `references/plantilla-informe.md`: estructura exacta del informe
- `assets/cv-ats-base.md`: esqueleto general a prueba de parser
- `assets/cv-ai-engineer-base.md`: esqueleto en inglés para roles de IA
