# AI Operations Copilot — MVP Scope

## 1. Objetivo

O AI Operations Copilot tem como objetivo auxiliar analistas de suporte e infraestrutura na investigação inicial de incidentes técnicos, centralizando análise, consulta de documentação e execução de diagnósticos básicos.

A solução utiliza IA para interpretar o contexto do incidente, sugerir possíveis causas, recomendar próximos passos e apoiar a tomada de decisão, reduzindo tempo de troubleshooting e padronizando o processo de atendimento.

## 2. Persona principal

A persona principal é o analista de suporte ou infraestrutura, atuando em níveis N1, N2 ou N3, responsável por diagnosticar incidentes relacionados a rede, sistemas, aplicações e serviços.

O usuário possui conhecimento técnico suficiente para validar as recomendações geradas pela IA e continua responsável pela decisão final sobre qualquer ação no ambiente.

## 3. Casos de uso

### UC-01 — Análise de incidente

O analista informa o título, a descrição e, quando disponível, contexto adicional sobre um incidente.

O sistema interpreta as informações e retorna uma análise estruturada contendo possíveis causas, criticidade, evidências identificadas, ações recomendadas e indicação de necessidade de escalonamento.

### UC-02 — Consulta de documentação técnica

O analista realiza uma pergunta técnica ou envia o contexto de um incidente.

O sistema consulta a base de conhecimento interna, composta por runbooks, procedimentos e documentação técnica, utilizando busca semântica para recuperar os conteúdos mais relevantes antes de gerar a resposta.

A resposta deve indicar as fontes utilizadas sempre que houver conteúdo recuperado da base.

### UC-03 — Diagnóstico de infraestrutura

O analista solicita validações técnicas básicas relacionadas a um incidente, como resolução DNS ou conectividade TCP.

O sistema executa apenas ferramentas previamente autorizadas e não destrutivas, coleta os resultados e utiliza essas informações como contexto adicional para melhorar a análise do incidente.

Nesta fase, a execução das ferramentas permanece controlada pela aplicação e não é decidida autonomamente pelo modelo.

## 4. Entradas

O sistema deverá aceitar, inicialmente:

título do incidente;
descrição detalhada;
contexto adicional opcional informado pelo analista;
pergunta técnica para consulta da base de conhecimento;
hostname ou FQDN para diagnóstico de DNS;
host e porta para teste de conectividade TCP.

Os dados enviados devem passar por validação antes do processamento.

## 5. Saídas

O sistema deverá retornar respostas estruturadas contendo, quando aplicável:

categoria do incidente;
nível de severidade;
possíveis causas;
evidências identificadas;
ações recomendadas;
indicação de escalonamento;
nível de confiança da análise;
fontes utilizadas no RAG;
resultados das ferramentas de diagnóstico executadas.

As respostas devem deixar claro quando não houver informação suficiente para uma conclusão confiável.

## 6. Limites do modelo

O modelo atua como mecanismo de apoio à análise técnica e não possui autoridade para executar alterações administrativas no ambiente.

A IA pode:

interpretar descrições de incidentes;
classificar e priorizar possíveis causas;
sugerir procedimentos de troubleshooting;
consultar contexto recuperado da base de conhecimento;
interpretar resultados retornados pelas ferramentas de diagnóstico;
indicar quando as informações disponíveis são insuficientes;
recomendar escalonamento quando necessário.

A IA não deve:

executar comandos arbitrários no sistema operacional;
alterar configurações de rede, servidores ou aplicações;
reiniciar serviços ou equipamentos;
criar, excluir ou alterar usuários;
modificar registros DNS;
acessar credenciais ou segredos;
executar operações destrutivas;
apresentar hipóteses como fatos quando não houver evidência suficiente.

As decisões e ações finais continuam sob responsabilidade do analista.

## 7. Ações permitidas

No MVP, o sistema poderá executar somente ferramentas previamente implementadas, validadas e classificadas como não destrutivas.

Inicialmente serão permitidas:

consulta de resolução DNS;
teste de conectividade TCP para host e porta;
consulta à base de conhecimento;
recuperação de informações previamente armazenadas sobre incidentes e documentação.

Toda ferramenta deverá possuir:

entrada validada;
timeout definido;
retorno estruturado;
tratamento de erros;
registro da execução;
escopo de atuação explícito.

O modelo não poderá criar ou executar comandos livremente. A camada de aplicação será responsável por decidir quais ferramentas podem ser utilizadas e validar seus parâmetros antes da execução.

## 8. Fora do escopo

## 8. Fora do escopo

Não fazem parte do MVP inicial:

* execução autônoma de ações administrativas;
* reinício automático de serviços, servidores ou containers;
* alteração de configurações de rede;
* criação, alteração ou exclusão de usuários;
* integração com Active Directory, Microsoft 365, Azure ou outros ambientes corporativos reais;
* execução remota via SSH, WinRM ou PowerShell Remoting;
* abertura automática de chamados em ferramentas ITSM;
* integração com sistemas de monitoramento externos;
* agente autônomo com múltiplas etapas de decisão;
* memória de longo prazo do usuário ou do ambiente;
* suporte a múltiplos tenants;
* controle avançado de RBAC;
* interface web completa;
* processamento de grandes volumes de documentos;
* alta disponibilidade e escalabilidade horizontal;
* execução distribuída de workers;
* deploy em ambiente cloud;
* uso de modelos externos pagos como dependência obrigatória.

Esses itens poderão ser adicionados em fases posteriores conforme a evolução do projeto e a necessidade de validar cenários mais próximos de produção.
