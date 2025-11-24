"""Ferramenta para executar comandos locais de shell."""

from __future__ import annotations

import shlex
import subprocess
from typing import List

TOOL_META = {
    "name": "cmd",
    "description": "Executa comandos de shell locais de forma simples.",
}


def run(command: str = "") -> str:
    if not command:
        return "Nenhum comando informado."

    tokens: List[str] = shlex.split(command)
    try:
        completed = subprocess.run(tokens, check=True, capture_output=True, text=True)
        output = completed.stdout.strip()
        return output or completed.stderr.strip() or "Comando executado sem saída."
    except subprocess.CalledProcessError as exc:
        return f"Falha ao executar: {exc}"
