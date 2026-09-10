# AI Operations Copilot — Architecture

## 1. Visão geral

O AI Operations Copilot será uma aplicação backend desenvolvida em FastAPI para auxiliar analistas de suporte e infraestrutura na análise de incidentes técnicos.

A primeira versão utilizará o Qwen2.5 14B executado localmente via Ollama, com evolução posterior para RAG, ferramentas de diagnóstico, observabilidade e suporte a múltiplos providers de LLM.

A arquitetura será desenvolvida de forma incremental, evitando abstrações e frameworks de agentes antes que exista uma necessidade real.

## 2. Fluxo inicial

```text
Client
  |
  v
FastAPI
  |
  v
Application Service
  |
  v
AI Layer
  |
  v
Ollama
  |
  v
Qwen2.5 14B
```

Com a evolução do projeto:

```text
Client
  |
  v
FastAPI
  |
  v
Application Service
  |
  +----> RAG
  |       |
  |       +----> Embeddings
  |       +----> PostgreSQL + pgvector
  |
  +----> Diagnostic Tools
  |       |
  |       +----> DNS Lookup
  |       +----> TCP Check
  |
  +----> LLM Provider
          |
          +----> Ollama / Qwen2.5 14B
          +----> OpenAI
          +----> Azure OpenAI
```

## 3. Responsabilidades dos módulos

### `api`

Responsável pela interface HTTP da aplicação.

Contém rotas, schemas de entrada e saída e integração entre requisições HTTP e os serviços da aplicação.

Não deve conter regras de negócio ou lógica específica do LLM.

### `core`

Contém componentes compartilhados pela aplicação, como configurações, exceptions e definições globais.

### `ai`

Responsável pela integração com modelos de linguagem.

Inicialmente conterá a comunicação com Ollama, construção de prompts e serviços relacionados à análise de incidentes.

Posteriormente poderá conter abstrações para múltiplos providers.

### `rag`

Responsável pelo pipeline de Retrieval-Augmented Generation.

Inclui ingestão de documentos, chunking, geração de embeddings, recuperação semântica e montagem de contexto para o LLM.

### `tools`

Contém ferramentas controladas utilizadas durante o diagnóstico técnico.

As ferramentas devem possuir entradas validadas, timeout, retorno estruturado e não permitir execução arbitrária de comandos.

### `db`

Responsável pela persistência.

Contém configuração do SQLAlchemy, models, migrations e acesso ao PostgreSQL/pgvector.

### `observability`

Responsável por logs, métricas e traces.

Posteriormente será integrado ao OpenTelemetry e às ferramentas utilizadas para monitoramento do projeto.

## 4. Princípios arquiteturais

* O LLM não deve executar comandos diretamente.
* A API não deve conter lógica de negócio.
* Integrações externas devem permanecer isoladas.
* RAG e tools devem funcionar independentemente do modelo de linguagem sempre que possível.
* Componentes devem ser testáveis sem depender de serviços externos reais.
* Segredos e configurações específicas de ambiente não devem ser incluídos no código.
* Novas abstrações devem ser adicionadas apenas quando houver necessidade concreta.

## 5. Evolução prevista

A arquitetura será evoluída progressivamente para incluir:

1. integração local com Ollama;
2. análise estruturada de incidentes;
3. PostgreSQL e pgvector;
4. pipeline RAG;
5. ferramentas de diagnóstico;
6. observabilidade;
7. múltiplos providers de LLM;
8. comportamento agêntico controlado, caso necessário.
