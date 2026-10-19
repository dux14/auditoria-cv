# Reescritura: de funciones a logros verificables

Los ejemplos de bullets están en inglés porque el CV que entrega la skill es en inglés.
Los marcadores `<...>` se completan con datos reales del usuario; no se rellenan con
cifras inventadas.

## La regla

La mayoría de los CV describen **funciones** (lo que te asignaron). Los que funcionan
describen **logros** (lo que cambió porque estabas ahí) y se pueden defender en voz alta.

**Prefiere alcance verificable a porcentajes inventados.** La antigua meta de "70 % de
bullets con métrica" se retira: empuja a inventar. Una cifra solo entra si tiene fuente
(ver Registro de evidencia en SKILL.md) o está marcada USER-ATTESTED. Un bullet con
alcance concreto y sin porcentaje es mejor que uno con un porcentaje que el usuario no
puede explicar.

## La fórmula base

    [Verbo de acción] + [qué hiciste, con el término técnico exacto] + [alcance o resultado verificable] + [con qué]

**Before:** Responsible for monthly reports.
**After:** Built `<N>` Power BI dashboards used by `<N>` people across `<N>` teams, replacing a manual monthly spreadsheet process.

**Before:** Supported process improvements.
**After:** Redesigned the month-end close with `<N>` departments, cutting it from `<A>` to `<B>` days.

## Fórmulas de la era de IA (con marcadores)

Fórmula: `Verb + artifact you owned + how it was measured (dataset / grader / gate) +
before -> after + constraint (cost, latency, safety) + stack`. Fuente: síntesis de
ofertas y guías de contratación (research-1, sección 3.1); las guías son blogs.

- **Eval harness:** Built a `<N>`-task eval harness for `<agent / skill / MCP server>` (Python, pytest, `<Inspect / promptfoo / custom>`) with code-based and LLM-judge graders calibrated against `<M>` human-labelled traces; wired into CI as a merge gate that caught `<K>` regressions before release.
- **MCP:** Shipped a `<N>`-tool MCP server (`<TypeScript / Python>`) exposing `<system>` to agents with least-privilege scopes and `<approval / rate-limit>` controls; tool-call accuracy `<x>` on `<N>` eval tasks.
- **Agent workflow / skills:** Designed Claude Code skills and hooks for `<workflow>`; agent-authored PRs must pass `<lint / tests / eval gate>` before human review; `<review time / defect escape / cycle time>` moved `<a>` -> `<b>` over `<period>`.
- **Quality gates:** Replaced `<manual process>` with CI quality gates (GitHub Actions) combining deterministic checks and agent-trajectory evals; flake rate `<a>` -> `<b>`.
- **Failure analysis:** Built a failure taxonomy from `<N>` traces (wrong tool, wrong arguments, loop, premature stop); fixed the largest bucket, raising task success `<a>` -> `<b>`.
- **Cost / latency:** Added model routing and prompt caching, cutting cost per successful task `<a>` -> `<b>` with no drop on the regression suite.

Usa el vocabulario con precisión (task, trial, grader, transcript, pass@k) solo si lo
usaste de verdad. Si no puedes nombrar el dataset, el grader y la compuerta, el bullet
no está listo.

## Desarrollo asistido por IA, redactado con honestidad

Describe un flujo que gobiernas, no un atajo: qué hace el agente, qué revisa un humano,
qué compuertas existen. Nunca "vibe coding". El agente no es el autor de lo que tú no
puedes explicar.

- **Good:** Delivered `<system>` with Claude Code under a spec-first, test-first workflow: the agent drafts changes, I review every diff for `<correctness / security / scope>`, and `<tests / lint / eval gate>` block merges that fail.
- **Good:** Defined the human-agent boundary for `<team / repo>`: agents open PRs for `<task class>`; humans own `<design / security-sensitive changes>`; `<gate>` enforces it.
- **Bad:** Used AI to code faster. / Built the app with vibe coding. / AI-driven engineer.

Nombra la herramienta como contexto, no como titular. Ofrece evidencia revisable (repo
con la configuración del agente, CI). No hay fuente autoritativa sobre cómo divulgar
esto (research-4); es práctica defendible, no norma.

## Traducción QA / SDET a IA

Traduce cada logro de QA al concepto de evaluación que demuestra, solo si el trabajo
realmente equivale. No inflar a "ML engineer".

| Trabajo de QA/SDET | Concepto en IA | Ejemplo de bullet |
|---|---|---|
| Suite de regresión | Regression evals | Maintained a `<N>`-case regression suite; extended it into regression evals for `<agent>`. |
| Pruebas inestables (flaky) | Manejo de no determinismo | Reduced flake rate `<a>` -> `<b>` via retries, seeds and multi-run scoring. |
| Datos de prueba | Golden datasets | Curated `<N>` golden cases from real failures. |
| Triage de defectos | Taxonomía de fallos | Classified `<N>` failures into `<K>` categories to prioritise fixes. |
| Compuertas de release | Merge gates | Gated merges on `<checks>`; `<K>` regressions blocked. |

Cuidado: la evaluación "no es QA pegado al final"; el valor está en diseñar mediciones,
no solo ejecutar pruebas (guía de Hero Hunt, blog). Titula por el rol objetivo, no por
"QA en transición". Detalle de títulos en `roles-ia-2026.md`.

## Verbos

Abre con: built, designed, automated, migrated, reduced, shipped, implemented,
consolidated, redesigned, scaled, standardised, integrated, trained, owned.
Evita: "responsible for", "in charge of", "helped with", "participated in",
"collaborated with", "various duties", y los "spearheaded / leveraged" repetidos (lectura
de texto generado; evidencia débil, de blogs).

## Cuando no hay números: alcance

- Equipo: "coordinated 6 engineers in 2 time zones"
- Volumen: "over 5 million records", "40-client portfolio"
- Frecuencia: "weekly release", "40 daily tickets"
- Antes/después reales: "from 8 to 5 days"
- Adopción: "adopted by 4 teams"

Pregunta bien al usuario ("¿cuánta gente usaba eso que construiste?"). Si no recuerda,
usa `<N>` y márcalo como pendiente; no estimes.

## El resumen

Dos a cuatro líneas factuales: nivel, stack central, dominio, prueba. Sin adjetivos
genéricos. No existe comparación publicada entre CV con y sin resumen (research-4);
el consejo es convergencia de blogs.

**Weak:** Proactive, results-driven professional seeking to grow with a dynamic team.
**Good:** AI Quality Engineer (SDET background) with `<X>` years building test automation and, most recently, eval harnesses and CI gates for LLM agents. Python, TypeScript, pytest, Playwright. Shipped `<artifact>` (repo linked below).

## Qué se elimina casi siempre

"References available upon request"; objetivo genérico; barras de nivel; habilidades
blandas sueltas (salvo si la oferta las nombra); software obvio; experiencia de hace más
de 15 años en detalle; dirección exacta, documento, estado civil, edad; foto en procesos
corporativos o internacionales.

## Coherencia

Un solo formato de fecha ("Mar 2023 - Present"); un solo formato de cargo ("Title |
Company | City | Dates"); sigla y forma completa la primera vez; encabezados estándar
(Summary, Skills, Experience, Education, Projects). Fechas o títulos contradictorios
dañan más ahora que los parsers leen contexto.
