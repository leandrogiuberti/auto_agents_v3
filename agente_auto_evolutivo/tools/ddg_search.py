"""Busca simples usando a API pública do DuckDuckGo."""

from __future__ import annotations

import json
import urllib.parse
import urllib.request

TOOL_META = {
    "name": "ddg_search",
    "description": "Busca resumida na web usando DuckDuckGo (API pública).",
}


API_URL = "https://api.duckduckgo.com/"


def _fetch(query: str) -> dict:
    params = urllib.parse.urlencode({"q": query, "format": "json", "no_html": 1, "no_redirect": 1})
    url = f"{API_URL}?{params}"
    with urllib.request.urlopen(url, timeout=10) as response:
        data = response.read().decode("utf-8")
    return json.loads(data)


def run(query: str = "") -> str:
    if not query:
        return "Informe um termo para buscar."

    try:
        payload = _fetch(query)
    except Exception as exc:  # pragma: no cover - acesso externo
        return f"Erro ao buscar: {exc}"

    abstract = payload.get("AbstractText") or payload.get("Abstract") or ""
    if abstract:
        return abstract.strip()

    related = payload.get("RelatedTopics") or []
    for item in related:
        if isinstance(item, dict) and item.get("Text"):
            return item["Text"]
        if isinstance(item, dict) and item.get("Topics"):
            for topic in item["Topics"]:
                if topic.get("Text"):
                    return topic["Text"]

    return "Nenhum resultado encontrado."
