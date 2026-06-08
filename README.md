# Pull, Otimização e Avaliação de Prompts com LangChain e LangSmith

Entregável do desafio de Prompt Engineering do MBA IA. O objetivo era otimizar um prompt de baixa qualidade (`bug_to_user_story_v1`) para transformar bug reports em User Stories, avaliado automaticamente pelo LangSmith em cinco métricas.

---

## Resultados Finais

### Evolução por experimento

O trabalho envolveu **5 experimentos** com múltiplas rodadas de execução, aplicação de **4 técnicas de Prompt Engineering** (Role Prompting, Few-Shot Learning, Chain of Thought e Skeleton of Thought) e análise caso a caso do reasoning do avaliador LLM-as-Judge para identificar onde o prompt precisava evoluir. As métricas Clarity, Precision e Helpfulness foram aprovadas com ≥ 0.9. F1-Score e Correctness atingiram um teto inerente ao ground truth do dataset — detalhado na seção [Decisões Técnicas](#decisões-técnicas) — que não é superável via prompt sem comprometer a validade da avaliação.


| Experimento | F1-Score | Clarity | Precision | Helpfulness | Correctness | Média | O que mudou |
|-------------|----------|---------|-----------|-------------|-------------|-------|-------------|
| Exp 1 — melhor rodada (v3) | 0.797 | 0.910 | **0.904 ✓** | **0.907 ✓** | 0.851 | 0.874 | Role Prompting + CoT 5 passos + Few-shot 3 exemplos — 10 versões testadas (v2–v11) |
| Exp 2 — melhor rodada | 0.549 | 0.593 | 0.585 | 0.589 | 0.567 | 0.577 | Reestruturação completa do prompt partindo do zero — primeiro run do experimento com novo formato ainda sem ajuste |
| Exp 3 — melhor rodada | 0.723 | 0.860 | 0.799 | 0.829 | 0.761 | 0.794 | Refinamentos de recall e persona — prompt retomou evolução após reestruturação |
| Exp 4 — melhor rodada | 0.815 | **0.923 ✓** | **0.927 ✓** | **0.925 ✓** | 0.871 | 0.892 | Análise caso a caso via reasoning do avaliador + intervenções cirúrgicas no F1 |
| **Exp 5 — melhor rodada (final)** | **0.831** | **0.927 ✓** | **0.913 ✓** | **0.920 ✓** | **0.872** | **0.893** | Ajustes pontuais por caso + aceitação do teto do ground truth |

### Resultado do `evaluate.py`

Execução do script de avaliação principal contra o prompt publicado no LangSmith Hub:

![Resultado evaluate.py](docs/images/evaluate-result.png)

Helpfulness, Clarity e Precision aprovados. F1-Score (0.82) e Correctness (0.87) ficaram abaixo de 0.9 pelos motivos documentados na seção de Decisões Técnicas abaixo.

---

### Evidências visuais (Experimento 5)

**Visão geral das rodadas — gráfico de métricas e tabela comparativa:**

![Dashboard Exp 5](docs/images/exp5-dashboard-overview.png)

**Detalhe dos 15 exemplos na melhor rodada (`bug_to_user_story_v2-befdec82`):**

![Detalhe por exemplo](docs/images/exp5-best-run-detail.png)

**Trace do avaliador LLM-as-Judge (`all_metrics_evaluator`) com reasoning completo:**

![Trace do avaliador](docs/images/exp5-trace-evaluator.png)

---

### Experimentos no LangSmith

Cada experimento está disponível publicamente para consulta, com tracing completo de todas as execuções e o reasoning do avaliador por exemplo:

| Experimento | Foco | Link |
|-------------|------|------|
| Experimento 1 | Baseline mensurável + estrutura base (Role Prompting, CoT, Few-shot) | [Abrir no LangSmith](https://smith.langchain.com/public/a5cacf1e-4a15-416d-a601-38747333fbdb/d) |
| Experimento 2 | Aumento critério por critério — foco em Clarity e extração de persona | [Abrir no LangSmith](https://smith.langchain.com/public/52fdc1c8-327d-404b-8ffe-81526d163e12/d) |
| Experimento 3 | Geração de novo prompt com todos os aprendizados + refinamento de recall | [Abrir no LangSmith](https://smith.langchain.com/public/2d98ae6d-d6af-49fe-84f5-e13d00a2dbef/d) |
| Experimento 4 | Análise caso a caso via Excel + intervenções cirúrgicas no F1 | [Abrir no LangSmith](https://smith.langchain.com/public/963c33b5-0050-47d7-9973-a3e4aeb59c6b/d) |
| Experimento 5 (final) | Ajustes pontuais por caso + aceitação do teto do ground truth | [Abrir no LangSmith](https://smith.langchain.com/public/8dca1a00-73e2-4a74-81f9-5befd46b562d/d) |

- **Prompt Hub:** https://smith.langchain.com/hub/andrematecki/bug_to_user_story_v2
- **Dashboard de avaliações:** https://smith.langchain.com/projects/prompt-optimization-challenge-resolved

---

## Técnicas Aplicadas

Foram aplicadas quatro técnicas de Prompt Engineering, escolhidas e refinadas ao longo de 5 experimentos com múltiplas rodadas de execução e análise individual de cada um dos 15 casos do dataset.

### 1. Role Prompting

**O que é:** Atribuição de uma persona específica ao modelo antes de qualquer instrução.

**Por que foi escolhida:** Sem persona definida, o modelo tendia a descrever o bug do ponto de vista técnico (o que está quebrado) em vez do ponto de vista do usuário (o que ele precisa). A persona de PM Sênior calibra o tom, o vocabulário e o foco em valor de negócio — exatamente o que o avaliador media em Helpfulness e Precision.

**Como foi aplicada:**
```
Você é um Product Manager Sênior especializado em metodologias ágeis,
com mais de 10 anos de experiência transformando bugs e problemas técnicos
em User Stories claras e acionáveis para times de desenvolvimento.
```

**Impacto:** Principal responsável pelo salto de 0.80 → 0.87 na média geral na primeira iteração significativa.

---

### 2. Few-Shot Learning (obrigatório)

**O que é:** Inclusão de exemplos concretos de entrada/saída no prompt para calibrar o comportamento do modelo por imitação.

**Por que foi escolhida:** O modelo aprende o nível de detalhe esperado nos critérios de aceitação diretamente pela estrutura dos exemplos — não pelo texto das regras. Foi identificado nos experimentos que a quantidade de condições `E` geradas pelo modelo era proporcional à quantidade presente nos exemplos. Um exemplo raso ensinava critérios rasos.

**Como foi aplicada:** Três exemplos por nível de complexidade (simples, médio, complexo), cada um demonstrando o formato completo esperado para aquele nível — incluindo número de critérios `E`, presença ou ausência de Contexto Técnico e estrutura dos critérios Given-When-Then.

**Impacto:** Clarity e Precision aprovadas (≥ 0.9) após a inclusão dos exemplos calibrados. O exemplo 3 (complexo) foi o maior driver de F1, pois ensina ao modelo quantas sub-condições são esperadas em bugs com múltiplos componentes.

---

### 3. Chain of Thought (CoT)

**O que é:** Instrução explícita para o modelo raciocinar passo a passo antes de produzir a resposta final.

**Por que foi escolhida:** Identificado nos experimentos que F1 baixo = recall baixo = o modelo descartava detalhes técnicos presentes no bug report (algoritmos, protocolos, race conditions, etc.). Sem CoT, o modelo pulava direto para o formato e gerava personas genéricas e critérios incompletos. O CoT força a análise explícita de persona, necessidade real, valor de negócio e completude antes de escrever.

**Como foi aplicada:** Seção `RACIOCÍNIO PASSO A PASSO` com 7 perguntas obrigatórias a serem respondidas mentalmente antes da geração, incluindo um checklist de completude no passo 6 com gatilhos específicos para padrões recorrentes de omissão (notificação de múltiplos atores, processamento assíncrono, operações atômicas, etc.).

**Impacto:** Intervenção que mais moveu o F1 ao longo dos experimentos. Sem o checklist explícito, detalhes técnicos presentes no bug report eram ignorados sistematicamente.

---

### 4. Skeleton of Thought

**O que é:** Definição antecipada de um andaime estrutural que organiza tanto o raciocínio do modelo quanto a saída gerada.

**Por que foi escolhida:** Sem estrutura obrigatória, o modelo mesclava seções de complexidades diferentes — adicionava Contexto Técnico em bugs simples ou omitia Tasks Técnicas em bugs complexos. O andaime garante que cada nível de complexidade produza exatamente o conjunto de seções esperado, eliminando variância estrutural entre execuções.

**Como foi aplicada:** O prompt define quatro blocos obrigatórios em sequência: `FORMATO OBRIGATÓRIO` (o que gerar por complexidade) → `RACIOCÍNIO PASSO A PASSO` (como analisar antes de gerar) → `EXEMPLOS` (modelos de referência) → `REGRAS IMPORTANTES` (restrições e edge cases). O modelo percorre esse andaime antes de produzir qualquer saída.

**Impacto:** Eliminou a maior fonte de variância estrutural entre execuções e garantiu consistência no formato das respostas, contribuindo diretamente para a estabilidade de Clarity e Precision.

---

## Decisões Técnicas

### Teto do ground truth

Durante os experimentos, foi identificado que parte do F1 não era recuperável via prompt. O avaliador LLM-as-Judge infere detalhes que não existem no bug report de entrada — por exemplo, "log de auditoria é boa prática", "reserva temporária de 15 minutos" ou uso de "materialized views". O modelo não tem base para reproduzir essas inferências, pois não estão no input.

Esses casos foram mapeados e aceitos como **teto do ground truth**. Tentativas de cobri-los com instruções adicionais apenas aumentavam o ruído em Precision — cada ganho de recall custava queda em Precision. Por isso, o F1 ficou em ~0.84 e não atingiu 0.90. As demais métricas (Clarity, Precision, Helpfulness) foram aprovadas.

---

### Não inclusão de exemplos do ground truth no Few-shot

Uma das formas mais diretas de elevar artificialmente as métricas seria incluir, nos exemplos Few-shot do `bug_to_user_story_v2`, os mesmos bugs e User Stories presentes no dataset de avaliação (`datasets/bug_to_user_story.jsonl`). Isso **não foi feito intencionalmente**.

Incluir exemplos do dataset de avaliação diretamente no prompt seria **data leakage**: o modelo estaria "vendo a resposta" antes da pergunta, pois os exemplos que ele usa como referência durante a geração seriam exatamente os casos pelos quais ele seria avaliado. Isso geraria **overfitting** — o prompt performaria bem apenas naqueles 15 casos específicos, sem qualquer capacidade de generalização para bugs reais fora do dataset.

A consequência direta dessa decisão é que **não foi possível atingir 0.9 em todas as métricas** — em especial F1 (0.83) e Correctness (0.87), que dependem de Recall, e Recall depende de reproduzir inferências do ground truth que não estão no input. A alternativa de usar os próprios casos de teste como exemplos resolveria o número, mas invalidaria completamente a avaliação.

Os exemplos Few-shot utilizados no prompt são **diferentes dos casos do dataset**, construídos para ensinar o formato e o nível de detalhe esperado — não para memorizar respostas específicas.

---

## Como Executar

### Pré-requisitos

- Python 3.9+
- Conta no [LangSmith](https://smith.langchain.com/) com API Key
- Chave de API do Google Gemini ([Google AI Studio](https://aistudio.google.com/app/apikey)) **ou** OpenAI ([platform.openai.com](https://platform.openai.com/api-keys))

### Instalação

```bash
git clone <url-do-repositorio>
cd mba-ia-pull-evaluation-prompt

python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### Configuração do `.env`

```bash
cp .env.example .env
```

Variáveis obrigatórias:

```env
LANGSMITH_API_KEY=<sua-api-key-langsmith>
LANGSMITH_PROJECT=prompt-optimization-challenge-resolved
USERNAME_LANGSMITH_HUB=<seu-username-no-langsmith-hub>

# Escolha um provider:
LLM_PROVIDER=google
LLM_MODEL=gemini-2.5-flash
EVAL_MODEL=gemini-2.5-flash
GOOGLE_API_KEY=<sua-api-key-google>

# Ou OpenAI:
# LLM_PROVIDER=openai
# LLM_MODEL=gpt-4o-mini
# EVAL_MODEL=gpt-4o
# OPENAI_API_KEY=<sua-api-key-openai>
```

> Para descobrir seu `USERNAME_LANGSMITH_HUB`: publique qualquer prompt no LangSmith Hub, abra-o e clique no ícone de cadeado para ver o username.

### Execução

**Fase 1 — Pull do prompt base:**
```bash
python3 src/pull_prompts.py
```

**Fase 2 — Editar o prompt otimizado:**

Edite manualmente `prompts/bug_to_user_story_v2.yml` aplicando as técnicas desejadas.

**Fase 3 — Push do prompt otimizado:**
```bash
python3 src/push_prompts.py
```

**Fase 4 — Avaliação:**
```bash
python3 src/evaluate.py
```

**Fase 5 — Testes de validação:**
```bash
pytest tests/test_prompts.py
```

---

## Desafio Original

<details>
<summary>Ver enunciado completo</summary>

### Objetivo

Você deve entregar um software capaz de:

1. **Fazer pull de prompts** do LangSmith Prompt Hub contendo prompts de baixa qualidade
2. **Refatorar e otimizar** esses prompts usando técnicas avançadas de Prompt Engineering
3. **Fazer push dos prompts otimizados** de volta ao LangSmith
4. **Avaliar a qualidade** através de métricas customizadas (Helpfulness, Correctness, F1-Score, Clarity, Precision)
5. **Atingir pontuação mínima** de 0.9 (90%) em todas as métricas de avaliação

---

### Tecnologias obrigatórias

- **Linguagem:** Python 3.9+
- **Framework:** LangChain
- **Plataforma de avaliação:** LangSmith
- **Gestão de prompts:** LangSmith Prompt Hub
- **Formato de prompts:** YAML

---

### Pacotes recomendados

```python
from langchain import hub  # Pull e Push de prompts
from langsmith import Client  # Interação com LangSmith API
from langsmith.evaluation import evaluate  # Avaliação de prompts
from langchain_openai import ChatOpenAI  # LLM OpenAI
from langchain_google_genai import ChatGoogleGenerativeAI  # LLM Gemini
```

---

### Modelos

**OpenAI:**
- LLM para responder: `gpt-4o-mini`
- LLM para avaliação: `gpt-4o`

**Gemini (modelo free):**
- LLM para responder: `gemini-2.5-flash`
- LLM para avaliação: `gemini-2.5-flash`
- Limite: 15 req/min, 1500 req/dia

---

### Requisitos

**1. Pull do prompt inicial**

- Configurar credenciais do LangSmith no `.env`
- Implementar `src/pull_prompts.py`: faz pull de `leonanluppi/bug_to_user_story_v1` e salva em `prompts/bug_to_user_story_v1.yml`

**2. Otimização do prompt**

- Analisar `prompts/bug_to_user_story_v1.yml`
- Criar `prompts/bug_to_user_story_v2.yml` aplicando obrigatoriamente **Few-shot Learning** e pelo menos uma técnica adicional (CoT, Tree of Thought, Skeleton of Thought, ReAct ou Role Prompting)

**3. Push e avaliação**

- Implementar `src/push_prompts.py`: lê `prompts/bug_to_user_story_v2.yml` e publica como `{username}/bug_to_user_story_v2`
- Verificar no dashboard do LangSmith e deixar público

**4. Iteração**

Espera-se 3–5 iterações até **TODAS as métricas >= 0.9**:

```
Helpfulness >= 0.9
Correctness >= 0.9
F1-Score    >= 0.9
Clarity     >= 0.9
Precision   >= 0.9
```

**5. Testes de validação**

Implementar em `tests/test_prompts.py` com `pytest`:

- `test_prompt_has_system_prompt`
- `test_prompt_has_role_definition`
- `test_prompt_mentions_format`
- `test_prompt_has_few_shot_examples`
- `test_prompt_no_todos`
- `test_minimum_techniques`

---

### Estrutura do projeto

```
mba-ia-pull-evaluation-prompt/
├── .env.example
├── requirements.txt
├── README.md
├── prompts/
│   ├── bug_to_user_story_v1.yml
│   └── bug_to_user_story_v2.yml
├── datasets/
│   └── bug_to_user_story.jsonl
├── src/
│   ├── pull_prompts.py
│   ├── push_prompts.py
│   ├── evaluate.py       # pronto — não alterar
│   ├── metrics.py        # pronto — não alterar
│   └── utils.py          # pronto — não alterar
└── tests/
    └── test_prompts.py
```

</details>
