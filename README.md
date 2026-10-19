# auditoria-cv

Skill de Claude que audita una hoja de vida (PDF o DOCX) y entrega un informe accionable por secciones, con la versión reescrita lista para enviar.

## Qué hace

1. **Diagnóstico ATS.** Antes de opinar sobre el contenido, extrae el texto como lo haría un ATS y detecta PDF-imagen, doble columna, tablas, texto oculto y campos no mapeables.
2. **Informe por secciones** con acciones QUITAR / CAMBIAR / MEJORAR / AÑADIR.
3. **Versión reescrita** del CV, lista para enviar.
4. **Registro de evidencia:** cada cifra y herramienta del CV queda enlazada con su fuente, y lo que no se puede respaldar se retira.

Modos adicionales:

- **CV de IA / AI engineer:** agentes, MCP, evals y bloque de habilidades defendible.
- **Perfil de LinkedIn:** texto listo para pegar, optimizado para búsqueda de reclutadores.
- **Mercados:** España/UE, Colombia/LATAM y EE.UU./remoto.

Funciona con o sin una vacante específica. Si hay oferta, calcula la brecha de términos clave contra ella.

## Instalación

### Claude Code (recomendado: se actualiza con `git pull`)

```bash
git clone https://github.com/dux14/auditoria-cv ~/.claude/skills/auditoria-cv
```

Actualizar:

```bash
git -C ~/.claude/skills/auditoria-cv pull
```

Reinicia la sesión de Claude Code para que cargue la versión nueva.

### Claude (app o web)

1. Descarga el archivo `auditoria-cv-<versión>.skill` desde [Releases](https://github.com/dux14/auditoria-cv/releases/latest).
2. Ve a Settings → Capabilities → Skills y sube el archivo.
3. Para actualizar, elimina la versión anterior y sube la nueva. Si no la eliminas, pueden quedar archivos viejos mezclados.

## Uso

Pídele a Claude, por ejemplo:

- «Audita mi hoja de vida» (adjunta el PDF o DOCX).
- «Adapta mi CV a esta oferta» (pega la vacante).
- «Reescribe mi perfil de LinkedIn para roles de AI engineer».

La skill se activa sola cuando mencionas CV, hoja de vida, resume, ATS, LinkedIn o reclutadores.

## Contenido

| Ruta | Para qué sirve |
|---|---|
| `SKILL.md` | Flujo principal y reglas de la skill |
| `references/` | ATS, redacción, LinkedIn, roles de IA, mercado de España y plantilla del informe |
| `assets/` | CVs base (ATS general y AI engineer) |
| `scripts/parse_check.py` | Diagnóstico de qué texto extrae un ATS |

## Límites

- Las cifras de mercado y de LinkedIn de `references/` están fechadas en octubre de 2026. Reverifícalas antes de usarlas como base de decisiones.
- La skill no inventa logros: lo que no tenga evidencia se marca o se retira.

## Contribuir

Los issues y pull requests son bienvenidos, sobre todo para actualizar datos de mercado o añadir mercados nuevos. Registra los cambios en `CHANGELOG.md`.

## Publicar una versión

```bash
git tag v2026.10 && git push origin v2026.10
```

El workflow de `.github/workflows/release.yml` empaqueta el `.skill` y lo adjunta al release.

## Licencia

[MIT](LICENSE)
