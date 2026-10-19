# CV para roles de IA (AI engineer) - edición 2026-10-19

Fuente: research-1, 53 ofertas públicas de las API de Greenhouse y Ashby, leídas el
**2026-10-19** (muestra de conveniencia, sesgada hacia empresas de IA de EE.UU. y
big tech, y hacia roles senior; no incluye LinkedIn ni Wellfound). Los conteos incluyen
texto boilerplate: son cotas superiores. La división "obligatorio / deseable" es
heurística. Al citar esto al usuario, escribe "según 53 ofertas revisadas el
2026-10-19" y recuerda que el mercado cambia en semanas.

## Frecuencia de vocabulario (de 53 ofertas)

| Término | Ofertas | Estado típico |
|---|---|---|
| Construir/desplegar agentes (agentic) | 40 | Obligatorio |
| Python | 34 | Obligatorio (TypeScript: 21) |
| Observabilidad / tracing / trayectorias | 28 | Obligatorio en evals/plataforma |
| Evals / harness / benchmarks / detección de regresiones | 25 | Obligatorio en Applied AI, Agent Quality |
| Guardrails / seguridad | 22 | Mixto |
| Fluidez con herramientas de código con IA | 19 | Obligatorio en varias (Anthropic AgentOps, Stripe, Ramp) |
| Fiabilidad / modos de fallo / no determinismo / flake | 19 | Obligatorio en roles de eval |
| Latencia / costo / eficiencia de tokens | 19 | Obligatorio en Perplexity, Reddit, OpenAI |
| Seguridad: prompt injection, mínimo privilegio, permisos | 15 | Obligatorio en Databricks, Anthropic AgentOps |
| CI/CD | 15 | Obligatorio en DevProd/SDET |
| Test automation (pytest, Playwright, e2e) | 13 | Obligatorio en QA/DevProd |
| Tool/function calling | 11 | Obligatorio en Databricks, Perplexity |
| RAG / retrieval | 11 | Deseable salvo contexto/retrieval |
| MCP | 8 | Obligatorio en 3 ofertas; deseable en otras |
| Frameworks de agentes nombrados | 8 | Deseable |
| Context engineering | 7 | Obligatorio en Anthropic GTM, Databricks, Perplexity |
| LLM-as-judge / graders automáticos | 5 | Obligatorio en Perplexity, Scale |
| Fine-tuning / RL | 3 | Deseable |
| Comunicación con clientes/stakeholders | 39 | Obligatorio en Applied AI/FDE |

Solo 15/53 nombran Claude y 17/53 OpenAI/Codex: mantén las habilidades neutrales de
proveedor y nombra herramientas solo si las dominas. Ninguna de las 53 pide una
certificación (hallazgo de un escaneo propio: "no encontrado", no prueba de ausencia).

## Obligatorio frente a deseable (síntesis)

**Obligatorio**: Python/TypeScript con ingeniería de producción; Git, pruebas
automatizadas, CI/CD; trabajo práctico con LLM/agentes (tool calling, flujos de varios
pasos, salidas estructuradas, contexto); evals (conjuntos de tareas, golden datasets,
graders de código, modelo y humano, compuertas de regresión, lectura de
transcripciones); criterio de producción (fiabilidad, latencia, costo por tarea,
observabilidad, mínimo privilegio); uso activo y con criterio de herramientas de código
con IA; comunicación escrita clara.

**Deseable**: desarrollo de servidores MCP, SDK de agentes (Claude Agent SDK, OpenAI
Agents SDK, LangGraph), RAG, herramientas de observabilidad LLM, Docker/Kubernetes,
nube, fine-tuning, SQL.

## Ajuste de título objetivo

Titula el CV por el rol al que apuntas, no por "QA en transición". Cero de 10.261
títulos revisados contienen "Prompt Engineer": no uses esa etiqueta como título.

| Título | Qué enfatizar |
|---|---|
| Applied AI Engineer / AI Engineer | LLM apps desplegadas, evals, tool use, costo, MCP, comunicación con clientes |
| Agent Evaluation / AI Quality Engineer | Harness, graders, compuertas de regresión, trayectorias, estadística, calibración de jueces |
| Developer Productivity (AI) | Compuertas de CI, presupuesto de flake, pipelines de PR de agentes, métricas de adopción, herramientas internas |
| SDET with AI | Playwright + pytest + CI con generación/triage de pruebas asistido por LLM medido; pruebas de productos no deterministas |
| AI Automation Engineer | Servidores MCP, integraciones de API/OAuth, aprobaciones humanas, trazas de auditoría |

Banda de seniority realista con ~3,5 años: ofertas con mínimo de 2-4 años (Stripe Dev
Productivity AI 2-5; LangChain Developer Productivity 3+; Databricks AI Automation 3 de
Python/Go; Cognition Applied AI 3). Las de eval de plataforma suelen pedir 5+ o Staff:
son estiramiento. Los roles son de capa de aplicación; no inflar a "ML engineer".

## Fórmulas de headline (en inglés; completar con datos reales)

- `AI Quality / Agent Evaluation Engineer | Evals, CI quality gates, MCP | Python, TypeScript`
- `Applied AI Engineer | LLM agents, tool use, evals | <N> years in test automation (SDET)`
- `Developer Productivity (AI) Engineer | Agent-authored PR pipelines, merge gates | Python, GitHub Actions`

## Bloque de habilidades agrupado por función (solo lo defendible)

- Agents & tool use: MCP, tool schemas, `<Claude Agent SDK / OpenAI Agents SDK / LangGraph>`
- Evals & quality: pytest, Playwright, `<promptfoo / Inspect / Braintrust>`, LLM-as-judge, golden datasets
- Languages: Python, TypeScript
- CI / Infra / Observability: GitHub Actions, `<tracing tool>`, Docker

Palabras que las ofertas repiten y encajan si son ciertas: agents, evals, tool calling,
MCP, observability/tracing, guardrails, prompt injection, CI/CD.

## Señales de alerta (los guías de contratación las nombran; fuentes en blog)

- Lista larga de frameworks sin profundidad ("sopa de frameworks"); "LangChain +
  Pinecone" a secas.
- "Implemented RAG" sin métrica de recuperación; "100 % accuracy" sin conjunto de prueba.
- Adjetivos sin cifras ("cutting-edge agentic solutions").
- Describir el proceso como "escribir prompts hasta que funcione".
- Portafolios solo en notebooks, un envoltorio de API.
- Sin historia de medición; no poder nombrar un enfoque de observabilidad o de eval.
- Pegar salida de IA sin entenderla ("vibe coding"): preguntan por un error hallado en
  código generado.
- Métricas redondas o imposibles.

## Temas de entrevista que el CV debe anticipar

| Tema | Qué debe mostrar el CV |
|---|---|
| Evals | Tamaño y origen del conjunto (fallos reales), tipos de grader, calibración humana, compuerta de CI |
| Diseño de agentes | Una decisión con contención y un límite de seguridad (aprobación, sandbox, mínimo privilegio) |
| Tool calling / MCP | Servidor nombrado con número de herramientas, alcance, pruebas, precisión medida |
| Costo / latencia | Costo por tarea y latencia antes/después; caché o enrutamiento |
| Modos de fallo | Una taxonomía de fallos y su corrección |
| Seguridad | Inyección de prompts, exceso de agencia (OWASP LLM06), allowlists |
| Código asistido por IA | Flujo de revisión y compuertas que protegen la salida del agente |
| Observabilidad | Enfoque de tracing/registro (LangSmith, Langfuse, Phoenix, OpenTelemetry...) |
| Comunicación | Un enlace a un documento de diseño o un texto técnico |

No reclames una "parte difícil" que no puedas defender: se profundiza en ella.

## Certificaciones

Ninguna es requisito en las ofertas revisadas. Las certificaciones de Claude (familia de
cuatro, jul. 2026) **no están abiertas a individuos**: solo a personal de organizaciones
de la Claude Partner Network. No las insinúes. ISTQB CT-AI/CT-GenAI existen, sin efecto
de contratación hallado. No gastes espacio salvo que ya existan y sean relevantes
(una línea al pie). Reemplázalas por evidencia pública.

## Evidencia pública que más pesa (blogs, no datos duros)

Repo con harness de eval y README con resultados y fallos; servidor MCP publicado; PR
fusionados a repos de agentes/evals; un texto que explique un sistema de eval. "Un
proyecto profundo vale más que cinco superficiales." Si falta, regístralo en la sección
"Brecha de pruebas públicas" del informe. Referencias técnicas útiles para el
vocabulario: Anthropic, "Demystifying evals for AI agents" (2026-01-09); Anthropic,
"Writing effective tools for agents" (2025-09-11); Hamel Husain, "Evals FAQ"
(2026-09-18); OWASP LLM06:2025.

## No verificado (no lo cites como dato)

Cifras de "49 % descarta CV con IA", "2,6x con palabras clave de eval", tablas
salariales de blogs, "80 % más interacción con repos ejecutables", y la caída de ~30 %
de "prompt engineer". No se hallaron CV públicos nombrados y verificables de ingenieros
de agentes/evals.
