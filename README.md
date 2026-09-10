## Desenvolvimento local

### Instalar dependências

```bash
uv sync
```

### Executar testes

```bash
uv run pytest
```

### Executar lint

```bash
uv run ruff check .
```

### Validar formatação

```bash
uv run ruff format --check .
```

### Aplicar formatação

```bash
uv run ruff format .
```

### Validar configurações da aplicação

```bash
uv run python -c "from app.core.config import settings; print(settings)"
```

### Validar comunicação com o Ollama

```bash
curl http://localhost:11434/api/tags
```

O projeto utiliza atualmente o modelo local:

```text
qwen2.5-coder:14b
```

executado através do Ollama.
