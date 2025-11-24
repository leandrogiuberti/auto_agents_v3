"""Módulo responsável por gerar e salvar novas ferramentas."""

from __future__ import annotations

import ast
import textwrap
from pathlib import Path
from typing import Any


class AutoEvo:
    """Gera código de ferramentas simples e salva no diretório de ferramentas."""

    def __init__(self, tools_dir: Path) -> None:
        self.tools_dir = Path(tools_dir)
        self.tools_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _sanitize_name(name: str) -> str:
        allowed = [c for c in name.lower().replace(" ", "_") if c.isalnum() or c == "_"]
        cleaned = "".join(allowed).strip("_") or "tool"
        return cleaned

    def _validate_code(self, code: str) -> None:
        ast.parse(code)

    def _write_tool(self, filename: str, code: str) -> Path:
        path = self.tools_dir / filename
        with path.open("w", encoding="utf-8") as file:
            file.write(code)
        return path

    def create_tool_from_text(self, name: str, description: str, prompt: str) -> Path:
        """Cria uma ferramenta que retorna o prompt como resposta principal."""
        safe_name = self._sanitize_name(name)
        code = textwrap.dedent(
            f'''"""Ferramenta gerada automaticamente a partir de entrada de texto."""

import textwrap

TOOL_META = {{
    "name": "{safe_name}",
    "description": "{description}",
}}


def run(text: str = "") -> str:
    """Retorna o prompt original e o texto recebido."""
    detalhes = textwrap.dedent("""{prompt}""")
    complemento = textwrap.dedent(text or "")
    if complemento:
        return detalhes + "\n\nEntrada complementar:\n" + complemento
    return detalhes
'''
        )
        self._validate_code(code)
        return self._write_tool(f"{safe_name}.py", code)

    def create_summary_tool(self, topic: str, summary: str) -> Path:
        safe_name = self._sanitize_name(f"resumo_{topic}")
        condensed = textwrap.dedent(summary).strip()
        code = textwrap.dedent(
            f'''"""Ferramenta de resumo criada automaticamente pelo agente."""

import textwrap

TOOL_META = {{
    "name": "{safe_name}",
    "description": "Resumo automatizado sobre {topic}.",
}}


def run(_: str = "") -> str:
    """Retorna um resumo gerado previamente pelo agente."""
    return textwrap.dedent("""{condensed}""")
'''
        )
        self._validate_code(code)
        return self._write_tool(f"{safe_name}.py", code)


__all__ = ["AutoEvo"]
