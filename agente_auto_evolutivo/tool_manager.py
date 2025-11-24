"""Gerenciador de ferramentas dinâmicas."""

from __future__ import annotations

import importlib.util
import inspect
from pathlib import Path
from types import ModuleType
from typing import Any


class ToolManager:
    """Carrega e executa ferramentas a partir de um diretório."""

    def __init__(self, tools_dir: Path) -> None:
        self.tools_dir = Path(tools_dir)
        self.tools_dir.mkdir(parents=True, exist_ok=True)
        self.loaded_tools: dict[str, ModuleType] = {}

    def _iter_tool_files(self) -> list[Path]:
        return sorted([p for p in self.tools_dir.glob("*.py") if p.name != "__init__.py"])

    def load_tool(self, name: str) -> ModuleType:
        if name in self.loaded_tools:
            return self.loaded_tools[name]

        tool_path = self.tools_dir / f"{name}.py"
        if not tool_path.exists():
            raise FileNotFoundError(f"Ferramenta '{name}' não encontrada em {self.tools_dir}.")

        spec = importlib.util.spec_from_file_location(f"tools.{name}", tool_path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Não foi possível carregar a ferramenta '{name}'.")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.loaded_tools[name] = module
        return module

    def load_all(self) -> None:
        for path in self._iter_tool_files():
            self.load_tool(path.stem)

    def list_tools(self) -> list[dict[str, Any]]:
        tools: list[dict[str, Any]] = []
        for path in self._iter_tool_files():
            module = self.load_tool(path.stem)
            meta = getattr(module, "TOOL_META", {})
            tools.append({
                "name": meta.get("name", path.stem),
                "description": meta.get("description", ""),
                "path": str(path),
            })
        return tools

    def run_tool(self, name: str, argument: str = "") -> Any:
        module = self.load_tool(name)
        if not hasattr(module, "run") or not inspect.isfunction(module.run):
            raise AttributeError(f"Ferramenta '{name}' não possui função run().")
        return module.run(argument)
