# Quick Start - ChatGPT Codex Configuration

## Generador automático

```bash
python3 build/codex/scripts/generate_codex.py \
  --project-name "my-project" \
  --language java \
  --framework spring-boot \
  --build-tool gradle \
  --agents-location both
```

Esto genera `.codex/` con:
- `AGENTS.md`
- `Agent.md`
- `codex_config.json`
- `package-manager.json`
- Copias de `agents/`, `skills/`, `rules/`, `commands/`, etc.

Además, con `--agents-location root|both`, también genera `AGENTS.md` y `Agent.md`
en la raíz (si no existen), para que Codex los detecte directamente.

## Parámetros clave
- `--output-dir`: carpeta destino (default `.codex`).
- `--agents-location`: `codex`, `root` o `both` (default `both`).
- `--language`/`--framework`: ajustan recomendaciones de skills y agentes.

## Personalización recomendada
1. Editar `.codex/AGENTS.md` y `.codex/Agent.md` con reglas de tu equipo.
2. Ajustar `.codex/codex_config.json` (skills/agentes/rules).
3. Si no necesitas todas las carpetas copiadas, elimina las que no apliquen.

## Alcance y limitaciones
Esta configuración replica la organización modular de `.claude` para usarla con Codex.
No todas las integraciones de Claude Code tienen equivalente directo en Codex, pero sí:
- Skills como instrucciones reutilizables.
- Rules como políticas del proyecto.
- Agents como guías de rol especializadas.
- `AGENTS.md`/`Agent.md` como entrypoint operativo en runtime.
