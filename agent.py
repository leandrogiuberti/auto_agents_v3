"""CLI principal para o projeto agente_auto_evolutivo.

O agente interpreta comandos em linha de comando e escolhe ferramentas
existentes ou cria novas ferramentas automaticamente quando necessário.
"""

from __future__ import annotations

import json
import shlex
from datetime import datetime
from pathlib import Path
from typing import Any

from agente_auto_evolutivo.auto_evo import AutoEvo
from agente_auto_evolutivo.tool_manager import ToolManager


class AgentCLI:
    """Agente conversacional em linha de comando.

    Comandos disponíveis:
    - list: lista ferramentas conhecidas
    - run <tool> [argumentos]: executa a ferramenta
    - new_tool <nome> <descricao> --prompt "texto": cria ferramenta baseada em texto
    - learn <assunto>: busca online, resume e gera ferramenta para esse assunto
    - exit/quit: encerra a sessão
    """

    def __init__(self, base_path: Path | None = None) -> None:
        repo_path = base_path or Path(__file__).resolve().parent
        tools_dir = repo_path / "agente_auto_evolutivo" / "tools"
        self.tool_manager = ToolManager(tools_dir)
        self.auto_evo = AutoEvo(tools_dir)
        self.memory_path = repo_path / "memory.log"
        self.tool_manager.load_all()

    # region memória
    def _log_event(self, action: str, payload: dict[str, Any]) -> None:
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "action": action,
            "payload": payload,
        }
        with self.memory_path.open("a", encoding="utf-8") as mem_file:
            mem_file.write(json.dumps(entry, ensure_ascii=False) + "\n")

    # endregion

    # region comandos básicos
    def list_tools(self) -> None:
        tools = self.tool_manager.list_tools()
        if not tools:
            print("Nenhuma ferramenta encontrada.")
            return
        print("Ferramentas disponíveis:")
        for meta in tools:
            print(f"- {meta['name']}: {meta['description']}")

    def run_tool(self, name: str, argument: str) -> None:
        result = self.tool_manager.run_tool(name, argument)
        print(result)
        self._log_event("run_tool", {"name": name, "argument": argument, "result": result})

    def auto_decide_and_run(self, message: str) -> None:
        """Escolhe uma ferramenta com base em palavras-chave simples e executa."""

        lowered = message.lower()

        if lowered.startswith("cmd "):
            command = message[len("cmd ") :].strip()
            self.run_tool("cmd", command)
            return

        if lowered.startswith("resuma "):
            topic = message[len("resuma ") :].strip() or message
            self.learn_and_create(topic)
            return

        if any(keyword in lowered for keyword in ("wikipedia", "wiki")):
            query = message.replace("wikipedia", "", 1).replace("wiki", "", 1).strip() or message
            self.run_tool("wikipedia_search", query)
            return

        if any(keyword in lowered for keyword in ("buscar", "search", "pesquise")):
            query = message
        else:
            # fallback para busca curta na web
            query = message

        self.run_tool("ddg_search", query)

    def create_tool_from_prompt(self, name: str, description: str, prompt: str) -> None:
        path = self.auto_evo.create_tool_from_text(name=name, description=description, prompt=prompt)
        self.tool_manager.load_tool(path.stem)
        print(f"Ferramenta '{name}' criada em {path}.")
        self._log_event("new_tool", {"name": name, "description": description, "prompt": prompt})

    def learn_and_create(self, topic: str) -> None:
        """Busca online, resume e cria uma ferramenta que retorna o resumo."""
        ddg_summary = self.tool_manager.run_tool("ddg_search", topic)
        wiki_summary = self.tool_manager.run_tool("wikipedia_search", topic)
        combined = f"Resumo DuckDuckGo:\n{ddg_summary}\n\nResumo Wikipedia:\n{wiki_summary}"
        path = self.auto_evo.create_summary_tool(topic, combined)
        self.tool_manager.load_tool(path.stem)
        print(f"Ferramenta de resumo criada: {path.stem}\n{combined}")
        self._log_event("learn", {"topic": topic, "summary": combined})

    # endregion

    def handle_command(self, raw: str) -> bool:
        """Processa uma linha de comando. Retorna False para encerrar."""
        cleaned = raw.strip()
        if not cleaned:
            return True

        if cleaned.lower() in {"exit", "quit"}:
            return False

        if cleaned == "list":
            self.list_tools()
            return True

        if cleaned.startswith("run "):
            try:
                _, name, *arg_parts = shlex.split(cleaned)
            except ValueError:
                print("Falha ao interpretar argumentos.")
                return True
            argument = " ".join(arg_parts)
            self.run_tool(name, argument)
            return True

        if cleaned.startswith("new_tool"):
            try:
                tokens = shlex.split(cleaned)
                name = tokens[1]
                description = tokens[2]
                if "--prompt" in tokens:
                    prompt_index = tokens.index("--prompt")
                    prompt = " ".join(tokens[prompt_index + 1 :])
                else:
                    prompt = " ".join(tokens[3:])
            except (IndexError, ValueError):
                print("Uso: new_tool <nome> <descricao> --prompt \"texto\"")
                return True
            self.create_tool_from_prompt(name, description, prompt)
            return True

        if cleaned.startswith("learn "):
            topic = cleaned[len("learn ") :].strip()
            if not topic:
                print("Informe um assunto: learn <assunto>")
                return True
            self.learn_and_create(topic)
            return True

        if cleaned.startswith("auto "):
            self.auto_decide_and_run(cleaned[len("auto ") :].strip())
            return True

        print("Comando desconhecido. Use list, run, new_tool, learn ou auto.")
        return True

    def run(self) -> None:
        print("Agente auto-evolutivo iniciado. Digite 'exit' para sair.")
        while True:
            try:
                line = input("> ")
            except EOFError:
                break
            if not self.handle_command(line):
                break


def main() -> None:
    AgentCLI().run()


if __name__ == "__main__":
    main()
