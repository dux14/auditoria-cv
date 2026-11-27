# Plantilla del informe de auditoría

Usa esta estructura. La tabla de hallazgos por sección es el corazón: el usuario debe
poder aplicar los cambios sin volver a preguntar nada. Prosa del informe en el idioma
del usuario; el texto propuesto para el CV o LinkedIn, en el idioma acordado en la Fase 0.

---

# Auditoría de CV - [Nombre] -> [Rol / vacante, o "CV genérico para <rol>"]
Fecha: [AAAA-MM-DD] | Modo: [genérico / oferta] | Mercado: [país o remoto] | Idioma: [..]

## Veredicto en una línea
[¿Qué es lo único que hay que arreglar si solo se arregla una cosa?]

## 1. Lo que ve la máquina

| Chequeo | Resultado |
|---|---|
| Capa de texto | OK / **PDF-imagen (bloqueante)** |
| Columnas | Una / **Multicolumna** |
| Tablas | 0 / N (advertencia: revisar el .ats.txt) |
| Texto oculto | Ninguno / **N caracteres** |
| Contacto en el cuerpo | email, teléfono, LinkedIn |
| Fechas parseables | N rangos |
| Secciones estándar | cuáles faltan |

**Extracto real de lo que lee el parser:**
> [pegar el fragmento roto del .ats.txt]

## 2. Triaje humano rápido
[Qué se entiende en el tercio superior de la página 1, y qué no.]

## 3. Brecha contra la vacante
Cobertura de términos: **N%** (indicador de brecha, no puntaje de ATS)

| Término de la oferta | ¿En el CV? | Acción |
|---|---|---|
| Power BI | No | Añadir a Skills y al bullet donde lo usaste |
| SAP S/4HANA | No | **Brecha real**: no lo has usado. No inventar. |

## 4. Hallazgos por sección

### Encabezado
| Acción | Actual | Propuesto | Por qué |
|---|---|---|---|
| QUITAR | Foto, cédula, dirección | - | Ruido y riesgo de sesgo |

### Resumen / Experiencia / Habilidades / Proyectos / Educación
(Misma tabla en cada una. QUITAR / CAMBIAR / MEJORAR / AÑADIR. Siempre el texto original
y el reemplazo literal, listo para copiar.)

## 5. Registro de evidencia
Cada cifra y herramienta del CV reescrito. Sin fuente ni atestación, no entra.

| Afirmación en el CV | Fuente verificable | Estado | Riesgo en entrevista |
|---|---|---|---|
| Built `<N>` Power BI dashboards | enlace a portafolio | VERIFICADO | ¿Qué decisiones cambiaron? |
| Cut month-end close `<a>` -> `<b>` days | - | USER-ATTESTED | Piden método de medición |
| Led migration to `<tool>` | - | PENDIENTE (falta fuente) | ¿Tu rol exacto? ¿Equipo? |

Estados: VERIFICADO (enlace, PR, documento), USER-ATTESTED (el usuario lo afirma y puede
defenderlo), ESTIMADO (el usuario lo estima con método; va como aproximado, "~N" o rango,
y se marca para confirmar), PENDIENTE (se retira del CV). Marca aparte lo que
el entrevistador va a sondear (lo técnico y lo cuantitativo).

## 6. Alcance y lenguaje de impacto
Bullets con alcance verificable: **N de M**. [Sin porcentajes inventados.] Los bullets que
necesitan un dato que solo tiene el usuario, con la pregunta exacta que hay que hacerle.

## 7. Brecha de pruebas públicas
| Prueba que piden las ofertas objetivo | ¿Existe? | Qué crear (mínimo) |
|---|---|---|
| Portafolio / repo / caso de estudio del tipo de trabajo que pide la oferta | No | Una muestra mínima y honesta |
| Certificación exigida como requisito duro | No | Ruta y fecha realista; no listarla hasta tenerla |

## 8. Kit de LinkedIn (opcional, solo si se pidió)
Salida de `references/linkedin-2026.md`, texto listo para pegar. Aplicación
manual por el usuario; nada se automatiza.

| Acción | Campo | Actual | Propuesto |
|---|---|---|---|
| CAMBIAR | Headline | ... | ... |
| MEJORAR | About (primeros ~370 caracteres) | ... | ... |
| AÑADIR | Skills / Featured / Open to Work / idioma secundario | - | ... |

## 9. Mercado y autorización (si aplica)
[Notas de `references/mercados.md` y de la investigación de la Fase 3; marca como "verificar" lo legal.]

## 10. Plan
1. [Lo bloqueante]
2. [La brecha de términos y de pruebas públicas]
3. [La redacción y el registro de evidencia]

## 11. Lo que NO hay que hacer
[Si el usuario venía pidiendo trucos: texto oculto, relleno, inyección de prompts,
automatizar LinkedIn, inflar títulos, métricas inventadas.]
