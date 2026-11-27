# Qué filtra de verdad un ATS (y qué no)

**Verificado el 2026-10-19.** Fuente: investigación de esa fecha. La
evidencia sobre formato es débil: casi todo son pruebas de proveedores sobre uno o pocos
documentos. Las fechas y fuentes van junto a cada dato; vuelve a verificar lo perecedero.

## Qué se retira como mito

- "El 75 % de los CV los rechaza el ATS": origen en una afirmación comercial de 2012
  (Preptel), sin método publicado. Retirada.
- "Puntaje ATS de 0 a 100": los ATS casi no lo exponen; el número de las herramientas
  verificadoras es solapamiento de palabras inventado por el proveedor. Sin estudio
  independiente de precisión. No lo uses como métrica.
- "El ATS solo cuenta palabras clave": desactualizado (ver LLM más abajo).
- "6 segundos": cifra de Ladders 2012; 7,4 s en 2018 (eye-tracking, muestra pequeña);
  sin réplica creíble reciente. Di "unos pocos segundos, menos de ~10".
- "Nunca columnas ni tablas": exagerado. Lo mal construido falla; lo bien construido puede
  parsear. Una columna sigue siendo el valor por defecto seguro.

## Lo que muestran los datos (con fecha y sesgo)

**Enhancv, 25 reclutadores de EE.UU.** (publicado 2025-11-03; trabajo de campo
sep-oct 2025; la página muestra "actualizado" en 2026). No es un estudio de 2026.
Lo hace un vendedor de herramientas de CV (conflicto de interés); muestra pequeña, no
representativa.
- 23/25 (92 %) dicen que su sistema no rechaza automáticamente por formato, contenido o
  diseño; 2/25 (8 %) usan rechazo por contenido (Bullhorn, BambooHR).
- 44 % tiene puntaje de ajuste con IA; 36 % lo usa solo como guía, 8 % de forma
  definitiva, 56 % lo ignora o no lo tiene.
- Las preguntas eliminatorias son el filtro automático real.
- 52 % dice que postular temprano ayuda; 36 % ve poca diferencia. Magnitudes (2-8x) son
  de blogs. Consejo moderado.
- 20 % (5/25) desaprueba gráficos pesados tipo Canva; 8 % marca CV de 7-8 páginas.
- Volumen estimado por reclutadores: 400-600 postulantes en puestos de entrada; más de
  2.000 en tech/ingeniería; menos de 200 en senior/especializado.
- Corroboración independiente: escasa (una encuesta de ~100 reclutadores, sin verificar).

**Gem, Recruiting Benchmarks 2026** (publicado 2025-12-01; datos jun 2021-may 2025;
datos del proveedor): reclutadores manejan 93 % más postulaciones que en 2021; 8 %
pasa el primer filtro; ~1 contratación por 200 postulaciones; los referidos convierten
11x que las postulaciones directas; el sourcing directo, ~8x; 46 % de las contrataciones
sourced son candidatos "redescubiertos" en el ATS/CRM.

**Greenhouse, AI in Hiring Report** (2025-11-19; encuesta del proveedor, n=4.136,
EE.UU./Reino Unido/Irlanda/Alemania): 91 % de reclutadores detectó engaño de candidatos;
22 % de los gerentes halló inyección oculta de prompts; 39 % añade entrevistas
presenciales para verificar.

## LLM en la selección (cambio de fondo)

- Workday HiredScore (notas de versión 2026-08-05): la asignación de calificación pasó a
  un enfoque con LLM. Evalúa cada requisito; quien cumple todos los básicos recibe A/B,
  los demás C/D; los preferidos separan A de B y C de D. Nueva vista opcional "Fit &
  Gap" enlazada a secciones del CV. Una doc anterior (solo vía búsqueda) indica que
  A-D priorizan y no son cortes duros, y que sin CV legible o sin descripción no hay nota.
- Implicación: lee contexto, así que espejar los términos de la oferta (solo los ciertos)
  ayuda, y el relleno de palabras no. Los requisitos deben aparecer literalmente en las
  secciones del CV, también en la experiencia.
- Workday afirma que su IA no decide ni está diseñada para rechazar automáticamente, pero
  el cliente puede configurar preguntas eliminatorias (vía fuente secundaria).
- Greenhouse: el rechazo automático actúa sobre respuestas a preguntas (autorización,
  ubicación), no sobre la prosa del CV (vía blogs; no verificado en documentación).
- LinkedIn Hiring Assistant: criterios de evaluación NO encontrados en documentación.
- Autopreferencia de LLM (arXiv 2509.00462, borrador de trabajo): los evaluadores LLM
  prefieren CV escritos por un LLM. Pero los humanos penalizan el texto genérico (77 % de
  gerentes dice que muchos CV parecen de IA; Resume Genius, metodología no hallada).
  Resolución: IA para editar; detalles verificables del humano.

## Qué te elimina, en orden de letalidad

1. **Fallo de parsing**: PDF-imagen (Canva), orden de lectura roto, contacto solo en
   encabezado o pie (algunos motores lo omiten o lo triplican), encabezados creativos.
2. **No salir en la búsqueda**: el reclutador usa búsqueda booleana o semántica. Mirror
   de términos reales sigue ganando; el relleno no.
3. **Preguntas eliminatorias** del formulario (autorización, años, ubicación).
4. **Triaje humano de segundos**, con cientos de postulaciones.
5. **Referidos y sourcing**: lo que ocurre antes de que tu CV compita en frío.
6. **Tiempo**: postular pronto ayuda según algunos; magnitud no verificada.

## Formato: qué aguanta y qué no (todo evidencia de proveedores)

- Una columna: promedio 93 % frente a 86 % de dos columnas (Enhancv/Indeed, 2023, un ATS);
  plantillas bien construidas de dos columnas igualaron o superaron. Habilidades: 65 % vs
  46 %. Peor campo: ubicación en el encabezado (50-75 %).
- PDF vs DOCX: prácticamente igual en esa prueba. Verifica que el texto sea extraíble.
- atsverification.com (2026-06-30, un CV, un parser propio, vende escáner): doble columna
  desordena la lectura; una cuadrícula de habilidades parseó bien; comillas curvas y
  guiones largos sin problema; encabezados creativos penalizan. No probó Workday ni
  Greenhouse. Aun así, prefiere "-" y viñetas estándar (convención, sin evidencia).
- Tablas: ablanda la regla a "evítalas para el layout; una cuadrícula simple de
  habilidades puede ir si el `.ats.txt` queda en orden".
- Fuentes, nombre de archivo, accesibilidad: sin datos creíbles. Convención: fuente de
  sistema 10-12 pt, `Nombre-Apellido-Rol.pdf`.
- Enlaces: usa URL visibles en texto plano; los hipervínculos solo como anotación pueden
  no sobrevivir a la extracción (verifica con `pdftotext`).
- Longitud: ver SKILL.md. ResumeGo (2018, simulación) y Jobscan (datos propios) son de
  proveedores.

## Texto oculto e inyección de prompts

- Medido: ~1 % de ~200.000 CV reales (2019-2025) tenía inyección oculta, en aumento; más
  del 90 % sin instrucción explícita (palabras clave extra). No se midió si cambió
  decisiones (arXiv 2605.28999, USENIX Security 2026).
- Greenhouse: 22 % de los gerentes la encontró; reacción sobre todo reputacional. Cifra
  de descalificación automática: no encontrada. Regla: nunca. Un LLM o un humano lo ve.

## Regulación (verificar vigencia antes de citar)

- **Ley de IA de la UE**: IA de reclutamiento/selección de CV es de alto riesgo
  (Anexo III). El "Digital AI Omnibus" retrasa la aplicación del 2026-08-02 al
  2027-12-02 (productos integrados: 2028-08-02); la Comisión indica entrada en vigor
  2026-07-27. La fecha del artículo 50 (transparencia) tiene fuentes en conflicto.
  **Verificar vigencia.** Hoy: las obligaciones de alto riesgo no aplican aún; el RGPD y
  la normativa antidiscriminación sí.
- **España, Real Decreto 723/2026** (2026-09-09, vigor 2026-10-05): desarrolla el art. 8.5
  del Estatuto de los Trabajadores (informar por escrito sobre sistemas algorítmicos).
  Cubre trabajadores, no postulantes directamente. Nota AEPD 2026-10-07 y aviso
  AI-00009-2026 (evaluación de riesgo, intervención humana). **Verificar vigencia.**
- **RGPD art. 22**: derecho a intervención humana e impugnación en decisiones
  únicamente automatizadas.
- NYC Local Law 144 (auditorías de sesgo): solo roles en Nueva York; aplicación ineficaz (2025-12-02).
- Mobley v. Workday (N.D. Cal.): colectivo ADEA certificado en 2025; sin fallo final
  hallado.

## Herramientas de validación (qué confiar)

1. `pdftotext -layout cv.pdf -` y también sin `-layout` (los parsers suelen leer por
   filas). `pdffonts` para fuentes y páginas sin texto.
2. Autorrelleno del portal real: revisa nombre, correo, fechas, cargos.
3. Demo de un parser comercial (Affinda, Textkernel): mejor proxy disponible de un ATS.
4. Revisión humana de un reclutador o par.
Desconfía de cualquier "puntaje ATS". OpenResume y pyresparser están poco mantenidos.

## NO se encontró (no lo afirmes)

Datos primarios de iCIMS, Lever, SmartRecruiters y Ashby (referidos/IA); criterios de
puntuación del Hiring Assistant de LinkedIn; estudio independiente de precisión de
verificadores ATS; encuesta sobre resumen vs. sin resumen; efecto de enlaces a GitHub;
datos de fuentes, nombre de archivo, Unicode y accesibilidad; regla sobre cómo divulgar
desarrollo asistido por IA; datos de Sterling/Checkr; informes originales de Resume
Genius, Resume.io y Resume Now (solo resúmenes secundarios). Las páginas de ayuda de
Greenhouse y Workday dieron 404; sus afirmaciones vienen de fuentes secundarias.

## Cómo hablarle al usuario

Sin condescendencia: "el cuello de botella suele ser el volumen y la atención humana,
no un robot que te vete. Lo que sí controlas: que el documento se lea bien, que contenga
los términos ciertos con los que te buscan, que las afirmaciones se sostengan en
entrevista, y que llegues por referido o búsqueda cuando se pueda."
