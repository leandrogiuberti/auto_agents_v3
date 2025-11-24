# agente_auto_evolutivo

Projeto simples em Python que demonstra um agente de linha de comando capaz de:

- listar e executar ferramentas dinâmicas;
- gerar novas ferramentas a partir de um texto ou de um processo de busca/"aprendizado";
- registrar ações em `memory.log` para consulta futura.

Tudo roda localmente, sem dependências externas além da biblioteca padrão do Python.

## Estrutura

- `agent.py`: chatbot CLI principal.
- `agente_auto_evolutivo/tool_manager.py`: carregamento dinâmico e execução de ferramentas.
- `agente_auto_evolutivo/auto_evo.py`: geração e persistência de novas ferramentas.
- `agente_auto_evolutivo/tools/`: ferramentas prontas (cmd, DuckDuckGo, Wikipedia) e as geradas pelo agente.

## Como usar

1. Certifique-se de ter Python 3 instalado.
2. No diretório do projeto, execute:

```bash
python agent.py
```

3. Exemplos de comandos dentro do prompt:

- Listar ferramentas disponíveis:

  ```
  list
  ```

- Executar um comando de shell via ferramenta `cmd`:

  ```
  run cmd "echo ola"
  ```

- Criar uma nova ferramenta baseada em texto livre:

  ```
  new_tool anotacoes "anota e repete" --prompt "Lembre-se de beber agua"
  ```

- Roteamento automático baseado em palavras-chave (busca ou resumo):

  ```
  auto resuma energia solar
  auto wikipedia Ada Lovelace
  auto buscar carros elétricos 2024
  ```

- Aprender sobre um assunto (busca online + resumo + ferramenta dedicada):

  ```
  learn Python programming language
  ```

4. Para sair, digite `exit` ou `quit`.

Os resultados e ações são registrados em `memory.log`. Novas ferramentas são salvas em `agente_auto_evolutivo/tools/` e podem ser reutilizadas em sessões futuras.
