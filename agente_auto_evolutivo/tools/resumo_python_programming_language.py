"""Ferramenta de resumo criada automaticamente pelo agente."""

import textwrap

TOOL_META = {
    "name": "resumo_python_programming_language",
    "description": "Resumo automatizado sobre Python programming language.",
}


def run(_: str = "") -> str:
    """Retorna um resumo gerado previamente pelo agente."""
    return textwrap.dedent("""Resumo DuckDuckGo:
Python is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability with the use of significant indentation. Python is dynamically type-checked and garbage-collected. It supports multiple programming paradigms, including structured, object-oriented and functional programming. Guido van Rossum began working on Python in the late 1980s as a successor to the ABC programming language. Python 3.0, released in 2008, was a major revision and not completely backward-compatible with earlier versions. Beginning with Python 3.5, capabilities and keywords for typing were added to the language, allowing optional static typing. Currently only versions in the 3.x series are supported. Python has gained widespread use in the machine learning community. It is widely taught as an introductory programming language.

Resumo Wikipedia:
Erro HTTP: 403""")
