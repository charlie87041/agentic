#!/usr/bin/env python3
"""
Generador de configuración para ChatGPT Codex.
Crea estructura base de .codex/ y archivos de instrucciones para reutilizar
skills/rules/agents/commands existentes del repositorio.
"""

import argparse
import json
import shutil
from datetime import UTC, datetime
from pathlib import Path


class CodexConfigGenerator:
    def __init__(self, output_dir: str = ".codex", agents_location: str = "both"):
        self.output_dir = Path(output_dir)
        self.agents_location = agents_location
        self.templates_dir = Path(__file__).resolve().parent.parent / "stubs"
        self.repo_root = Path(__file__).resolve().parents[3]

    def generate(self, project_name: str, language: str, framework: str | None = None, build_tool: str | None = None):
        print(f"🚀 Generando configuración de ChatGPT Codex para '{project_name}'...\n")

        build_tool_resolved = build_tool or self._infer_build_tool(language)

        self._create_directory_structure()
        self._write_instruction_files()
        self._write_codex_config(project_name, language, framework, build_tool_resolved)
        self._write_package_manager(build_tool_resolved)

        print("\n✅ Configuración generada exitosamente")
        print(f"📁 Archivos creados en: {self.output_dir}/")
        self._print_next_steps()

    def _create_directory_structure(self):
        self.output_dir.mkdir(parents=True, exist_ok=True)
        dirs_to_copy = [
            "agents",
            "commands",
            "contexts",
            "skills",
            "rules",
            "hooks",
            "schemas",
            "scripts",
            "plugins",
            "mcp-configs",
        ]

        for dir_name in dirs_to_copy:
            source_dir = self.repo_root / dir_name
            destination_dir = self.output_dir / dir_name
            if source_dir.is_dir():
                shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
                print(f"  ✅ {destination_dir}")
            else:
                destination_dir.mkdir(parents=True, exist_ok=True)
                print(f"  📁 {destination_dir}")

    def _write_instruction_files(self):
        memory = "user-CODEX.md"
        ag_source = self.templates_dir / "AGENTS.md"
        agent_source = self.templates_dir / "Agent.md"

        memory_source = self.templates_dir / memory
        memory_target = self.output_dir / memory

        if self.agents_location in {"codex", "both"}:
            ag_target = self.output_dir / "AGENTS.md"
            agent_target = self.output_dir / "Agent.md"
            ag_target.write_text(ag_source.read_text())
            agent_target.write_text(agent_source.read_text())
            memory_target.write_text(memory_source.read_text())
            print(f"  ✅ {ag_target}")
            print(f"  ✅ {agent_target}")

        if self.agents_location in {"root", "both"}:
            root_ag_target = self.repo_root / "AGENTS.md"
            root_agent_target = self.repo_root / "Agent.md"
            if not root_ag_target.exists():
                root_ag_target.write_text(ag_source.read_text())
                print(f"  ✅ {root_ag_target}")
            else:
                print(f"  ℹ️  Se conserva existente: {root_ag_target}")
            if not root_agent_target.exists():
                root_agent_target.write_text(agent_source.read_text())
                print(f"  ✅ {root_agent_target}")
            else:
                print(f"  ℹ️  Se conserva existente: {root_agent_target}")

    def _write_codex_config(self, project_name: str, language: str, framework: str | None, build_tool: str):
        source = self.templates_dir / "codex_config.json"
        config = json.loads(source.read_text())

        config["generatedAt"] = self._utc_now()
        config["project"]["name"] = project_name
        config["project"]["language"] = language
        config["project"]["framework"] = framework
        config["project"]["buildTool"] = build_tool
        config["skills"]["recommended"] = self._get_recommended_skills(language, framework)
        config["agents"]["recommended"] = self._get_recommended_agents(language)

        target = self.output_dir / "codex_config.json"
        target.write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n")
        print(f"  ✅ {target}")

    def _write_package_manager(self, build_tool: str):
        payload = {
            "packageManager": build_tool,
            "setAt": self._utc_now(),
        }
        target = self.output_dir / "package-manager.json"
        target.write_text(json.dumps(payload, indent=2) + "\n")
        print(f"  ✅ {target}")

    def _utc_now(self):
        return datetime.now(UTC).isoformat().replace("+00:00", "Z")

    def _get_recommended_skills(self, language: str, framework: str | None = None):
        by_language = {
            "java": ["java-coding-standards", "backend-patterns", "jpa-patterns"],
            "python": ["backend-patterns", "coding-standards"],
            "javascript": ["frontend-patterns", "coding-standards"],
            "typescript": ["frontend-patterns", "coding-standards"],
            "go": ["backend-patterns", "coding-standards"],
            "rust": ["coding-standards"],
        }
        by_framework = {
            "spring-boot": ["springboot-patterns", "springboot-security", "springboot-tdd"],
            "django": ["backend-patterns", "security-review"],
            "react": ["frontend-patterns"],
            "vue": ["frontend-patterns"],
        }
        result = by_language.get(language, ["coding-standards"]).copy()
        if framework:
            result.extend(by_framework.get(framework, []))
        result.extend(["tdd-workflow", "verification-loop", "security-review"])
        return sorted(set(result))

    def _get_recommended_agents(self, language: str):
        result = ["planner", "code-reviewer", "tdd-guide", "security-reviewer", "refactor-cleaner", "doc-updater"]
        by_language = {
            "python": ["python-reviewer"],
            "go": ["go-reviewer", "go-build-resolver"],
            "java": ["database-reviewer", "build-error-resolver"],
        }
        result.extend(by_language.get(language, []))
        return sorted(set(result))

    def _infer_build_tool(self, language: str):
        tools = {
            "javascript": "npm",
            "typescript": "npm",
            "python": "pip",
            "java": "gradle",
            "go": "go",
            "rust": "cargo",
        }
        return tools.get(language, "npm")

    def _print_next_steps(self):
        print("\n" + "=" * 60)
        print("🎯 PRÓXIMOS PASOS")
        print("=" * 60)
        print("1. Revisa y personaliza .codex/AGENTS.md y .codex/Agent.md")
        print("2. Ajusta .codex/codex_config.json según tu stack")
        print("3. Si elegiste --agents-location root|both, valida AGENTS.md en la raíz")
        print("4. Ejecuta el agente desde la raíz del proyecto para que cargue instrucciones")
        print("5. Versiona la carpeta .codex/ y los archivos raíz si deseas compartir configuración")


def main():
    parser = argparse.ArgumentParser(description="Genera configuración de ChatGPT Codex")
    parser.add_argument("--project-name", default="MyProject", help="Nombre del proyecto")
    parser.add_argument(
        "--language",
        default="java",
        choices=["java", "javascript", "typescript", "python", "go", "rust"],
        help="Lenguaje principal",
    )
    parser.add_argument("--framework", default=None, help="Framework principal")
    parser.add_argument("--build-tool", choices=["npm", "yarn", "pnpm", "gradle", "maven", "pip", "go", "cargo"])
    parser.add_argument("--output-dir", default=".codex", help="Directorio de salida")
    parser.add_argument(
        "--agents-location",
        default="both",
        choices=["codex", "root", "both"],
        help="Dónde generar AGENTS.md/Agent.md: solo en .codex, solo en raíz o en ambos",
    )

    args = parser.parse_args()
    generator = CodexConfigGenerator(args.output_dir, args.agents_location)
    generator.generate(args.project_name, args.language, args.framework, args.build_tool)


if __name__ == "__main__":
    main()
