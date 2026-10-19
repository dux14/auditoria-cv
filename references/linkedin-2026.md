# Perfil de LinkedIn para búsqueda de reclutadores - edición 2026-10-19

Fuente: research-3 y research-5, verificadas el **2026-10-19**. Etiquetas: [OFICIAL] =
página de LinkedIn leída; [TERCEROS] = blogs/proveedores; [REC] = recomendación de la
skill; [FOLKLORE] = repetido sin fuente primaria. LinkedIn **no publica pesos de
ranking**: cualquier "el headline pesa más" es folklore.

## Regla fija: no automatizar LinkedIn

El Acuerdo de Usuario (vigente 2025-11-03), sección 8.2, prohíbe software, scripts,
bots, extensiones o cualquier medio automatizado para raspar o acceder, incluidas
conexiones, mensajes y comentarios automáticos [OFICIAL]. El Centro de Ayuda advierte de
restricción o cierre de cuentas. LinkedIn demanda activamente (LinkedIn v. ProAPIs, 2025;
desenlace de 2026 con una sola fuente, verificar). **La skill redacta texto listo para
pegar; el usuario lo aplica a mano.** Seguro: programador nativo de publicaciones,
funciones de Premium, uso manual, exportación oficial de datos ("Get a copy of your
data").

### Conclusión sobre el MCP no oficial

`stickerdaniel/linkedin-mcp-server` (v4.27.0, 2026-10-10) es sobre todo de lectura y
mensajería: lee perfiles, empresas, empleos, bandeja; sus únicas herramientas de
escritura envían mensajes y solicitudes de conexión. **No puede editar un perfil**; la
edición existe solo en un PR de terceros sin fusionar (#1209, 2026-10-02, sin auditar).
Riesgos: viola la sección 8.2 (su README lo admite y usa un navegador parcheado para
evadir detección); guarda cookies de sesión; `@latest` con `uvx` ejecuta cada versión
nueva sin fijar; superficie alta de inyección de prompts (devuelve texto raspado de
terceros al LLM, junto a herramientas que envían mensajes). **No lo uses en una cuenta
principal.** Leer tu propio perfil una vez no lo justifica: copia el texto a mano o usa
la exportación de datos. La API oficial de perfil es de solo lectura y requiere
aprobación de LinkedIn; no hay API pública de edición.

## Cómo busca hoy el reclutador

- Recruiter: filtros de título, ubicación, habilidades, industria (40+); sigue aceptando
  booleanos [OFICIAL].
- Búsqueda asistida por IA: el reclutador pega la descripción en lenguaje natural y
  Recruiter la interpreta más allá de filtros y palabras clave [OFICIAL].
- Hiring Assistant (complemento de Recruiter): un LLM convierte la solicitud en título,
  seniority, ubicación y calificaciones; recuperación semántica sobre embeddings de
  perfiles (>1.000 millones) y un ranker con 100+ señales. Los embeddings dan más peso a
  señales gruesas (título, seniority, ubicación); habilidades duras se puntúan aparte;
  la trayectoria y el estado Open to Work son señales del lado del perfil (blog de
  ingeniería, 2026-06-11) [OFICIAL]. Criterios de evaluación y pesos: no publicados.
- Búsqueda de personas reconstruida con LLM (2026-01-21): coincidencia semántica, no solo
  de palabras exactas [OFICIAL].
- Verified Skills y fuentes profesionales (mayo 2026): datos de confianza de GitHub y
  patentes entran al Hiring Assistant [OFICIAL]. Inferencia [REC]: un GitHub público y
  mantenido, enlazado a tu identidad, puede ser evidencia de sourcing.
- Colombia: 19 % de las búsquedas de reclutadores filtran solo por habilidades (Skills
  Signal 2025) [OFICIAL]: la lista de habilidades pesa para quien está ubicado allí.
- Cobertura en español del Hiring Assistant: probable, no confirmada oficialmente.
- Consecuencia [REC]: título, seniority y ubicación claros y verdaderos; texto concreto
  de experiencia (coincidencia por significado); trayectoria y Open to Work al día.
- Obsoleto: las Skill Assessments y sus insignias ya no existen [OFICIAL]. Estado de
  All-Star y SSI: sin confirmación oficial; ignóralos.

## Campos, límites y estado de la fuente

| Campo | Límite | Fuente |
|---|---|---|
| Headline | 220 caracteres (el viejo 120 está obsoleto) | TERCEROS |
| About | 2.600; ~370 visibles antes de "ver más" | TERCEROS |
| Descripción de experiencia | 2.000 | TERCEROS débil (una fuente) |
| Habilidades | 100 máx.; las asociadas a un cargo no cuentan en el tope (muchos blogs aún dicen 50) | OFICIAL (ayuda 31888) |
| URL personalizada | 3-100 caracteres; 5 cambios por 6 meses | OFICIAL |
| Perfil en otro idioma | solo escritorio; la traducción no es automática | OFICIAL |

Verifica los límites de TERCEROS en la interfaz de edición antes de decir que son firmes.

## Guía por sección [REC]

1. **Headline**: título que el reclutador escribe + 2-4 sustantivos de stack + diferenciador
   + ubicación/disponibilidad verdadera. Ej.: `AI Quality / Agent Evaluation Engineer |
   Evals, CI gates, MCP | Python, TypeScript | Remote (UTC-5)`. Sin títulos creativos ni
   "Open to work" (no aporta si es modo solo reclutadores).
2. **About**: en los ~370 caracteres visibles: título, años, stack, ubicación,
   disponibilidad (remoto, zona horaria, autorización de trabajo, nivel de inglés). Luego
   3-5 líneas de prueba con alcance verificable y una línea de términos. Escribe oraciones
   completas, no relleno.
3. **Experiencia**: cargos de mercado estándar (sin inflar), fechas exactas, 3-5 bullets de
   resultado + stack (ver `redaccion.md`), habilidades asociadas a cada cargo.
4. **Habilidades**: llena muchas (LinkedIn asocia 10+ con menor tiempo sin empleo); las 3
   fijadas = habilidades del título objetivo (la fijación se describe por terceros;
   verifícala en la interfaz). Solo las defendibles.
5. **Featured / Proyectos**: 1-3 artefactos públicos (repo de agente, texto de eval).
   Sin evidencia de que puntúen en el ranking; sirven como prueba. GitHub: repos fijados
   con README.
6. **Recomendaciones, foto, banner**: sin evidencia primaria de efecto en ranking. Las
   cifras "21x vistas" son folklore. Foto profesional sencilla por confianza.
7. **Verificación**: hazla (documento, correo laboral o académico). Es señal de confianza;
   la afirmación de "60 % más vistas" no tiene fuente. El Verified Applicant Spotlight
   aplica a postulantes, no a búsqueda entrante.
8. Servicios y Creator mode (retirado en 2024): ignóralos para buscar empleo.

## Open to Work

Tres modos [OFICIAL]: todos los miembros (marco #OpenToWork), solo reclutadores, o solo
tú/recomendaciones. Solo reclutadores se oculta a usuarios de Recruiter de la empresa
marcada como actual, sin garantía completa de privacidad. Solo ubicación y tipo de
ubicación (remoto/híbrido/presencial) son visibles; cargos y tipos de empleo quedan
privados. Ignorar InMails puede quitar la función. El Hiring Assistant usa el estado
como señal: no lo dejes apagado si buscas. [REC] Empleado: solo reclutadores. Sin
empleo: el marco público es defendible. Rellena cargos y tipo remoto siempre.

## Perfil bilingüe y ubicación

- Principal en inglés (remoto global, la mayoría de roles de IA). Secundario en español
  [REC], traducido a mano con términos locales ("Ingeniero/a de IA"), mismos cargos y
  fechas. LinkedIn indica que ayuda a ser hallado, pero no dice que la búsqueda de
  reclutadores indexe perfiles secundarios, ni hay coincidencia entre idiomas
  documentada. No dependas de ello.
- **Ubicación verdadera.** País/región es obligatorio y es una señal gruesa. No pongas un
  país donde no resides: engaña sobre autorización de trabajo y daña la confianza. Mantén
  la real y en headline/About di "Open to relocate to Spain / EU" (ver `espana.md`);
  añade los países objetivo en Open to Work.

## Actividad (secundaria, de bajo volumen)

El feed se reconstruyó (2026-03-12): recomendación semántica por intereses
[OFICIAL]. Ninguna fuente primaria dice que publicar suba el ranking en Recruiter; el
contenido genera vistas y confianza. [REC] 1 publicación por semana o 2 al mes sobre
artefactos concretos (resultados de evals, lecciones de QA para LLM) con enlace al repo
en el primer comentario; comentarios con sustancia a ingenieros de empresas objetivo. No
hay cadencia óptima demostrada. Evita pods, comentarios automáticos, texto genérico de IA.
Las afirmaciones sobre enlaces externos penalizados o carruseles son folklore.

## Premium

Premium Career (desde ~US$39,99/mes en EE.UU.): 5 InMails, quién vio tu perfil 365 días.
**Sin evidencia de que suba tu rango en Recruiter.** Opcional, para medir vistas.

## Checklist de auditoría de perfil (salida QUITAR/CAMBIAR/MEJORAR/AÑADIR)

Pide el texto del perfil pegado por el usuario (no lo raspes). Por campo, entrega
actual -> propuesto, en inglés:

- Headline: ¿título estándar + stack + ubicación verdadera? (CAMBIAR/MEJORAR)
- About: ¿primeros ~370 caracteres con lo esencial? (CAMBIAR)
- Experiencia: ¿cargos y fechas coinciden con el CV? Incoherencias entre CV y perfil
  restan confianza. ¿Bullets de resultado? (MEJORAR)
- Habilidades: ¿faltan términos ciertos de las ofertas objetivo? ¿sobran no defendibles?
  (AÑADIR/QUITAR)
- Featured/GitHub: ¿hay prueba pública enlazada? (AÑADIR)
- Open to Work: modo, cargos, ubicaciones, remoto. (CAMBIAR)
- Idioma secundario y URL personalizada. (AÑADIR)
- Verificación hecha. (AÑADIR)
- QUITAR: titulares creativos, promesas sin prueba, habilidades de relleno, datos
  personales innecesarios.

## NO se encontró

Texto oficial de ayuda para los límites de headline, About y experiencia; anuncio de que
publicar suba el ranking en Recruiter; filtro de "activo recientemente"; documentación de
las 3 habilidades fijadas; máximo de cargos en Open to Work; datos primarios de que foto o
verificación suban las vistas; estado oficial de All-Star.
