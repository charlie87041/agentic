# AGENTS.md

Estas son instrucciones base para usar ChatGPT Codex en este proyecto.

## Objetivo
- Usar los artefactos de este repo como sistema modular para Codex: `skills/`, `rules/`, `agents/`, `commands/`.
- Mantener trazabilidad de cambios, foco en seguridad y validación antes de cerrar una tarea.

## Flujo recomendado
1. Leer contexto del feature y restricciones.
2. Revisar reglas aplicables en `rules/common/*.md`.
3. Elegir uno o más agentes en `agents/*.md` para guiar implementación/review.
4. Cargar skills relevantes desde `skills/*/SKILL.md`.
5. Ejecutar cambios pequeños con tests/verificaciones incrementales.

## Archivos de orquestación
- `AGENTS.md`: reglas e instrucciones de ejecución.
- `Agent.md`: perfil operativo resumido del agente para sesiones rápidas.
- `codex_config.json`: índice documental (skills/agentes/rules/commands recomendados).

## Mapeo rápido (orientativo)
- Planificación: `agents/planner.md`, `agents/planner-tdd.md`
- Implementación backend: `skills/backend-patterns`, `skills/springboot-patterns`
- Testing/TDD: `skills/tdd-workflow`, `agents/tdd-guide.md`
- Seguridad: `skills/security-review`, `agents/security-reviewer.md`
- Refactor/documentación: `agents/refactor-cleaner.md`, `agents/doc-updater.md`

## Reglas mínimas
- No exponer secretos o credenciales en commits/salidas.
- Ejecutar validaciones locales antes de finalizar.
- Mantener commits pequeños y descriptivos.
- Priorizar legibilidad y consistencia con reglas del proyecto.

## Nota
Codex no soporta exactamente todas las capacidades de Claude Code (por ejemplo algunos hooks/autoload internos),
pero esta estructura mantiene la misma organización para maximizar reutilización.
