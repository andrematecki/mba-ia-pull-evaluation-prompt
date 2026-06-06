# Passos do experimento - projeto bug_to_user-story-experimento-2



1. Executar o bug_to_user_story_v2 como o mesmo conteudo do bug_to_user_story_v1 para coletar metricas iniciais
2. Melhorias no prompt: role prompt e criterios claros de execução
3. Converte bugs em User Stories com role-prompting, classificação de complexidade (simples/médio/complexo), few-shot por nível, critérios Given-When-Then obrigatórios e regras anti-alucinação
4. Vamos aumentar criterio por criterio agora e ver como os demais se comportam. vamos começar pelo criterio "clareza" pegando 3 exemplos das piores avaliações e vendo oportunidades.
    - Linhas 38–42 (REGRAS OBRIGATÓRIAS): adicionadas 3 novas regras — classificação não aparece na saída, critérios de aceite descrevem comportamento genérico/desejado, Contexto Técnico como síntese no padrão "atual → esperado"
    - Linhas 138–140 (O QUE NÃO FAZER): 3 novos bullets espelhando as mesmas regras no negativo para reforço
5. Aumentou muito pouco a clareza, executando o passo 4. O modelo não esta transformando os bugs em regras sistemicas. adicionado para extração da regra sistemica no passo 5.
6. com o passo 5 atingimos o criterio de "clareza", maior GAP e o F1, podemos aumentar Precisao pq afeta diretamente F1, correctiness e o proprio precision. o que foi feito nessa versão: inferência de persona pelo contexto do bug (para resolver o "cliente" genérico que derrubava o foco na pergunta) e mapeamento de seção complementar por tipo de bug médio (para cobrir o conteúdo omitido que derrubava a correção factual do Precision).
7. a execução do passo 6 derrubou as metricas. Vou alterar o script para rpdar cada metrica separadamente no lang smith executar de novo e capturar todos os reasonings dos resultado e pedir para avaliar o que pode ser melhorado com base no prompt atual.
8. com a analise chegamos alteramos o item abaixo, mas nao variou os scores:
    - Regra 7 — adicionado mapeamento relatório/BI/analytics → gerente/executivo para corrigir persona errada em bugs de dashboard
    (precision 0.67)
    - Regra 8 — gatilho de acessibilidade ampliado de "navega por teclado" para "qualquer modal/overlay/componente interativo de UI", e
    explicitado que bugs SIMPLES nunca recebem seção complementar (F1 0.61, precision 0.67)
    - Regra 9 (nova) — valores numéricos do bug são sintomas, não metas: o critério deve descrever o comportamento desejado, não
    reproduzir o valor atual quebrado (F1 0.54, o gap mais crítico do dataset)

9. Simplificação do prompt devido ao modelo ser o gpt 4. estava muito verboso