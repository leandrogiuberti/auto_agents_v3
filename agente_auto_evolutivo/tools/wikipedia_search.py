"""Consulta rápida ao resumo de um verbete na Wikipedia."""

from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request

TOOL_META = {
    "name": "wikipedia_search",
    "description": "Obtém um resumo curto da Wikipedia (en).",
}

API_URL = "https://en.wikipedia.org/api/rest_v1/page/summary/"


def _fetch_summary(query: str) -> dict:
    encoded = urllib.parse.quote(query.strip())
    url = f"{API_URL}{encoded}"
    with urllib.request.urlopen(url, timeout=10) as response:
        data = response.read().decode("utf-8")
    return json.loads(data)


def run(query: str = "") -> str:
    if not query:
        return "Informe um verbete para pesquisar."

    try:
        payload = _fetch_summary(query)
    except urllib.error.HTTPError as exc:  # pragma: no cover - acesso externo
        return f"Erro HTTP: {exc.code}"
    except Exception as exc:  # pragma: no cover - acesso externo
        return f"Erro ao buscar: {exc}"

    extract = payload.get("extract") or payload.get("description")
    if extract:
        return extract.strip()
    return "Nenhum resumo disponível."
