# Agent.md

Perfil operativo para un agente de ChatGPT Codex en este repositorio.

## Mission
- Entregar cambios pequeños, verificables y alineados a `rules/`.
- Reutilizar `skills/` y `agents/` existentes como sistema modular.

## Startup checklist
1. Leer `AGENTS.md` más cercano al archivo objetivo.
2. Identificar reglas aplicables en `rules/common/*.md`.
3. Seleccionar skills de `skills/*/SKILL.md` según tarea.
4. Planear validaciones antes de modificar código.

## Working mode
- Plan corto -> cambio pequeño -> verificación -> siguiente cambio.
- Si hay ambigüedad, preferir la opción más conservadora y documentar trade-offs.
- No incluir secretos ni datos sensibles en salidas o commits.

## Done criteria
- Cambios consistentes con reglas y estilo del repo.
- Checks relevantes ejecutados y reportados.
- Commit claro y enfocado.
