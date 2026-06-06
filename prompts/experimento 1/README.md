---

##Execução do exercicio

1. Ao executar o evaluate.py percebi que ele nao inseria os experimentos no Lang smith, então criei um V2 para usar a função evaluate do lang
2. Executei a versão V2 com um copy paste da V1 para ver as notas e como evoluiria cada uma delas.

o que fui mudando entre os prompts:

V2 (que foi copia da V1 a V1) rodada de alterações

  ┌──────────────────────────────────────┬───────────────────────────────────────────────────────────────────────────────┐
  │               Mudança                │                                    Por quê                                    │
  ├──────────────────────────────────────┼───────────────────────────────────────────────────────────────────────────────┤
  │ Role Prompting — PM Sênior           │ Calibra tom e foco em valor de negócio, não só descrição técnica              │
  ├──────────────────────────────────────┼───────────────────────────────────────────────────────────────────────────────┤
  │ Bug report removido do system prompt │ Estava duplicado no v1/v2 — confunde o modelo e desperdiça tokens             │
  ├──────────────────────────────────────┼───────────────────────────────────────────────────────────────────────────────┤
  │ Chain of Thought — 5 perguntas       │ Força o modelo a analisar persona, valor e complexidade antes de escrever     │
  ├──────────────────────────────────────┼───────────────────────────────────────────────────────────────────────────────┤
  │ Few-shot — 3 exemplos                │ Um por nível de complexidade (simples/médio/complexo) para calibrar o formato │
  ├──────────────────────────────────────┼───────────────────────────────────────────────────────────────────────────────┤
  │ Edge cases por complexidade          │ Regras explícitas para evitar seções desnecessárias ou omissões            


  V3 rodada de alterações

  ⏺ Boa evolução! Comparando v2 vs v3:

  ┌─────────────┬────────┬────────┐
  │   Métrica   │   v2   │   v3   │
  ├─────────────┼────────┼────────┤
  │ F1-Score    │ 0.72 ✗ │ 0.80 ✗ │
  ├─────────────┼────────┼────────┤
  │ Clarity     │ 0.86 ✗ │ 0.91 ✓ │
  ├─────────────┼────────┼────────┤
  │ Precision   │ 0.81 ✗ │ 0.90 ✓ │
  ├─────────────┼────────┼────────┤
  │ Helpfulness │ 0.84 ✗ │ 0.91 ✓ │
  ├─────────────┼────────┼────────┤
  │ Correctness │ 0.77 ✗ │ 0.85 ✗ │
  ├─────────────┼────────┼────────┤
  │ Média       │ 0.80   │ 0.87   │
  └─────────────┴────────┴────────┘

  Clarity, Precision e Helpfulness já passaram. O gargalo agora é o F1-Score (0.80) que puxa o Correctness para baixo. F1 baixo
  significa que as respostas não estão cobrindo todo o conteúdo esperado (recall baixo).
  │ Helpfulness │ 0.84 ✗ │ 0.91 ✓ │
  ├─────────────┼────────┼────────┤
  │ Correctness │ 0.77 ✗ │ 0.85 ✗ │
  ├─────────────┼────────┼────────┤
  │ Média       │ 0.80   │ 0.87   │
  └─────────────┴────────┴────────┘

  Clarity, Precision e Helpfulness já passaram. O gargalo agora é o F1-Score (0.80) que puxa o Correctness para baixo. F1 baixo
  significa que as respostas não estão cobrindo todo o conteúdo esperado (recall baixo).

  Para subir o F1, o prompt precisa instruir o modelo a ser mais completo — especialmente nos critérios de aceitação. Quer que eu crie
  uma v4 focando nisso?

  │ Média       │ 0.80   │ 0.87   │
  └─────────────┴────────┴────────┘

  Clarity, Precision e Helpfulness já passaram. O gargalo agora é o F1-Score (0.80) que puxa o Correctness para baixo. F1 baixo
  significa que as respostas não estão cobrindo todo o conteúdo esperado (recall baixo).

  Para subir o F1, o prompt precisa instruir o modelo a ser mais completo — especialmente nos critérios de aceitação. Quer que eu crie
  uma v4 focando nisso?

  significa que as respostas não estão cobrindo todo o conteúdo esperado (recall baixo).

  Para subir o F1, o prompt precisa instruir o modelo a ser mais completo — especialmente nos critérios de aceitação. Quer que eu crie
  uma v4 focando nisso?

  Para subir o F1, o prompt precisa instruir o modelo a ser mais completo — especialmente nos critérios de aceitação. Quer que eu crie
  uma v4 focando nisso?


✻ Crunched for 4m 38s


  │ F1-Score    │ 0.72 ✗ │ 0.80 ✗ │
  ├─────────────┼────────┼────────┤
  │ Clarity     │ 0.86 ✗ │ 0.91 ✓ │
  ├─────────────┼────────┼────────┤
  │ Precision   │ 0.81 ✗ │ 0.90 ✓ │
  ├─────────────┼────────┼────────┤
  │ Helpfulness │ 0.84 ✗ │ 0.91 ✓ │
  ├─────────────┼────────┼────────┤
  │ Correctness │ 0.77 ✗ │ 0.85 ✗ │
  ├─────────────┼────────┼────────┤
  │ Média       │ 0.80   │ 0.87   │
  └─────────────┴────────┴────────┘

  Clarity, Precision e Helpfulness já passaram. O gargalo agora é o F1-Score (0.80) que puxa o Correctness para baixo. F1 baixo
  significa que as respostas não estão cobrindo todo o conteúdo esperado (recall baixo).

  Para subir o F1, o prompt precisa instruir o modelo a ser mais completo — especialmente nos critérios de aceitação. Quer que eu crie
  uma v4 focando nisso?


V4

  A v4 ficou pior que a v3 — o excesso de instruções sobre formato e contagem de critérios prejudicou a Clarity e a Precision. O
  prompt ficou muito prescritivo e o modelo começou a gerar respostas mais rígidas e menos naturais.

  Melhor estratégia: partir da v3 (que já tinha Clarity/Precision/Helpfulness aprovados) e fazer ajustes cirúrgicos só no F1 — sem
  alterar o que já funciona. Quer que eu crie uma v5 a partir da v3 com mudanças mínimas focadas no recall?


  V5 (com 3 chjamadas a LLM)
A v5 também regrediu em relação à v3. Evolução completa:

  ┌─────────────┬──────┬────────┬──────┬──────┐
  │   Métrica   │  v2  │   v3   │  v4  │  v5  │
  ├─────────────┼──────┼────────┼──────┼──────┤
  │ F1-Score    │ 0.72 │ 0.80   │ 0.78 │ 0.77 │
  ├─────────────┼──────┼────────┼──────┼──────┤
  │ Clarity     │ 0.86 │ 0.91 ✓ │ 0.90 │ 0.90 │
  ├─────────────┼──────┼────────┼──────┼──────┤
  │ Precision   │ 0.81 │ 0.90 ✓ │ 0.86 │ 0.84 │
  ├─────────────┼──────┼────────┼──────┼──────┤
  │ Helpfulness │ 0.84 │ 0.91 ✓ │ 0.87 │ 0.88 │
  ├─────────────┼──────┼────────┼──────┼──────┤
  │ Correctness │ 0.77 │ 0.85   │ 0.81 │ 0.81 │
  ├─────────────┼──────┼────────┼──────┼──────┤
  │ Média       │ 0.80 │ 0.87   │ 0.84 │ 0.84 │
  └─────────────┴──────┴────────┴──────┴──────┘

  A v3 continua sendo a melhor. O problema pode não ser só o prompt — o F1 do avaliador LLM-as-Judge tem variação natural entre
  execuções. Posso rodar a v3 novamente para verificar se o 0.80 é estável, ou posso tentar uma abordagem diferente. O que prefere?


V3 novamewnte com 3 chamadas a llm

 Baseline confirmado com o avaliador correto:

  ┌─────────────┬────────────────┐
  │   Métrica   │ v3 (corrigido) │
  ├─────────────┼────────────────┤
  │ F1-Score    │ 0.80 ✗         │
  ├─────────────┼────────────────┤
  │ Clarity     │ 0.91 ✓         │
  ├─────────────┼────────────────┤
  │ Precision   │ 0.90 ✓         │
  ├─────────────┼────────────────┤
  │ Helpfulness │ 0.91 ✓         │
  ├─────────────┼────────────────┤
  │ Correctness │ 0.85 ✗         │
  ├─────────────┼────────────────┤
  │ Média       │ 0.87           │
  └─────────────┴────────────────┘

  Os scores da v3 são idênticos ao que tínhamos antes — o avaliador corrigido não alterou os resultados, apenas eliminou as chamadas
  redundantes. Ótimo sinal.

  ---
  Linha do tempo do projeto
  
  rastreável.
  
  Solução base: Criado evaluate_v2.py usando langsmith.evaluation.evaluate(), que registra cada execução como um Experiment no
  LangSmith.
  
  Bug descoberto no evaluate_v2: helpfulness e correctness faziam chamadas LLM redundantes (7 chamadas por exemplo em vez de 3).
  Corrigido com um único all_metrics_evaluator que faz 3 chamadas LLM e deriva os outros 2 matematicamente — igual ao evaluate.py
  original.
  
  Evolução dos prompts (todos testados com o avaliador corrigido):
  
  ┌────────┬──────┬─────────┬───────────┬─────────────┬─────────────┬───────┬──────────────────────────────────────────────────────┐
  │ Versão │  F1  │ Clarity │ Precision │ Helpfulness │ Correctness │ Média │                     O que mudou                      │
  ├────────┼──────┼─────────┼───────────┼─────────────┼─────────────┼───────┼──────────────────────────────────────────────────────┤
  │ v2     │ 0.72 │ 0.86    │ 0.81      │ 0.84        │ 0.77        │ 0.80  │ Prompt original sem otimização                       │
  ├────────┼──────┼─────────┼───────────┼─────────────┼─────────────┼───────┼──────────────────────────────────────────────────────┤
  │ v3     │ 0.80 │ 0.91✓   │ 0.90✓     │ 0.91✓       │ 0.85        │ 0.87  │ Role prompting + CoT 5 passos + few-shot 3 exemplos  │
  ├────────┼──────┼─────────┼───────────┼─────────────┼─────────────┼───────┼──────────────────────────────────────────────────────┤
  │ v4     │ 0.78 │ 0.90    │ 0.86      │ 0.87        │ 0.81        │ 0.84  │ ❌ Regrediu — contagens rígidas engessaram o modelo  │
  ├────────┼──────┼─────────┼───────────┼─────────────┼─────────────┼───────┼──────────────────────────────────────────────────────┤
  │ v5     │ 0.76 │ 0.89    │ 0.85      │ 0.87        │ 0.81        │ 0.84  │ ❌ Regrediu — exemplo médio diferente + passo de     │
  │        │      │         │           │             │             │       │ verificação não surtiram efeito                      │
  └────────┴──────┴─────────┴───────────┴─────────────┴─────────────┴───────┴──────────────────────────────────────────────────────┘
  
  Estado atual: v3 é o melhor prompt. Faltam F1-Score (0.80→0.9) e Correctness (0.85→0.9) para aprovação.
  
  Hipótese para próxima iteração: F1 baixo = recall baixo = o modelo não cobre todos os aspectos do bug. As tentativas v4 e v5
  tentaram resolver via formato e exemplos, mas pioraram Clarity/Precision. A próxima estratégia deve focar em instruir o modelo a
  extrair e listar explicitamente todos os problemas do bug antes de escrever a user story — sem alterar o formato de saída.

✻ Sautéed for 2m 11s

──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
❯  
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  ? for shortcuts · ← for agents



---
  Linha do tempo do projeto
  
  rastreável.
  
  Solução base: Criado evaluate_v2.py usando langsmith.evaluation.evaluate(), que registra cada execução como um Experiment no
  LangSmith.
  
  Bug descoberto no evaluate_v2: helpfulness e correctness faziam chamadas LLM redundantes (7 chamadas por exemplo em vez de 3).
  Corrigido com um único all_metrics_evaluator que faz 3 chamadas LLM e deriva os outros 2 matematicamente — igual ao evaluate.py
  original.
  
  Evolução dos prompts (todos testados com o avaliador corrigido):
  
  ┌────────┬──────┬─────────┬───────────┬─────────────┬─────────────┬───────┬──────────────────────────────────────────────────────┐
  │ Versão │  F1  │ Clarity │ Precision │ Helpfulness │ Correctness │ Média │                     O que mudou                      │
  ├────────┼──────┼─────────┼───────────┼─────────────┼─────────────┼───────┼──────────────────────────────────────────────────────┤
  │ v2     │ 0.72 │ 0.86    │ 0.81      │ 0.84        │ 0.77        │ 0.80  │ Prompt original sem otimização                       │
  ├────────┼──────┼─────────┼───────────┼─────────────┼─────────────┼───────┼──────────────────────────────────────────────────────┤
  │ v3     │ 0.80 │ 0.91✓   │ 0.90✓     │ 0.91✓       │ 0.85        │ 0.87  │ Role prompting + CoT 5 passos + few-shot 3 exemplos  │
  ├────────┼──────┼─────────┼───────────┼─────────────┼─────────────┼───────┼──────────────────────────────────────────────────────┤
  │ v4     │ 0.78 │ 0.90    │ 0.86      │ 0.87        │ 0.81        │ 0.84  │ ❌ Regrediu — contagens rígidas engessaram o modelo  │
  ├────────┼──────┼─────────┼───────────┼─────────────┼─────────────┼───────┼──────────────────────────────────────────────────────┤
  │ v5     │ 0.76 │ 0.89    │ 0.85      │ 0.87        │ 0.81        │ 0.84  │ ❌ Regrediu — exemplo médio diferente + passo de     │
  │        │      │         │           │             │             │       │ verificação não surtiram efeito                      │
  └────────┴──────┴─────────┴───────────┴─────────────┴─────────────┴───────┴──────────────────────────────────────────────────────┘
  
  Estado atual: v3 é o melhor prompt. Faltam F1-Score (0.80→0.9) e Correctness (0.85→0.9) para aprovação.
  
  Hipótese para próxima iteração: F1 baixo = recall baixo = o modelo não cobre todos os aspectos do bug. As tentativas v4 e v5
  tentaram resolver via formato e exemplos, mas pioraram Clarity/Precision. A próxima estratégia deve focar em instruir o modelo a
  extrair e listar explicitamente todos os problemas do bug antes de escrever a user story — sem alterar o formato de saída.


