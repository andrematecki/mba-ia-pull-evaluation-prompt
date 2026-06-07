# Passos

apos tres experiementos, peguei o melhor prompt e fiz uma extração excel para identificar as oportunidades que temos para chegar a nota desejada.

1. Vou executar o mlehor prompt ate agora e coletar as evidencias de melhoras. coloquei as evidencias de melhoria no excel e com o Claude ele me deu o que mudou e pq

O que mudei e por quê
#	Onde	O que mudou	Por que
M1	Passo 6 do raciocínio + Regras	Instrução explícita para reutilizar implementações técnicas do bug report (CRDTs, chunked upload, CSP, etc.)	Causa mais frequente de f1 baixo — afetava 8/15 casos. O modelo descartava detalhes que já estavam no bug
M2	Passo 1 + Regras	Persona deve ser extraída do bug report, não inventada	Exemplos 2 e 13 geraram personas genéricas ignorando quem o bug citava explicitamente
M3	Formato complexo + Regras	Tasks Técnicas passam a ser condicionais ("apenas se o bug report já as listar")	O modelo adicionava tasks mesmo quando a resposta esperada não as tinha, prejudicando precision
M4	Exemplo 3 (checkout)	Critérios de aceitação expandidos com todas as condições "E"	O exemplo era o principal professor do modelo — estava ensinando critérios rasos. Agora mostra o nível de detalhe correto
M5	Regras	Nova regra: bugs UI/UX → seção obrigatória de Critérios de Acessibilidade	Exemplos 4, 5, 12 omitiam ESC / foco / backdrop consistentemente por falta de instrução


2. fiz as alterações e vamos executar
    - subou um pouco a metricas mas F1 ainda nao
    - a inclusao de sessao de UX opara todos casos que tenha a ver poiorou alguns itens, precisa entrar somente se mencionar explicitamente no BUG
    - reverter as 3 regressões (ex 7, 11, 14) sem perder os 5 casos que melhoraram com o v3, levando o f1 de ~0,799 para ~0,82–0,84.

3. A execução melhoou foi boa a estrategia de analisar somente os que pioraram, pq mudando eles os que melhoraram continuaram certo. Ponto importante sempre analisar o detalhe dos casos, se for somente no percentual geral ficamos tentaiva e erro. Usar a propria IA para analisar os casos, seria bom o Lang smith ter isso. Estou gerando Excel e analisando caso a caso

4. Nova execução, alterações :
    M1 — Checklist de completude no passo de raciocínio (novo)
    O passo 6 do raciocínio atual é uma pergunta aberta. Vira um checklist explícito que o modelo deve marcar antes de escrever:
    "Verifique: ✓ Detalhes técnicos do bug (CRDTs, HTTP codes, algoritmos, limites) → nos critérios. ✓ Logs/auditoria mencionados → no critério 'E'. ✓ Alternativas de negócio (remover/aguardar) → como opção 'OU'."
    Impacto esperado: ex 1, 2, 8, 10 (4 casos, f1 médio 0,74 → ~0,85)

    M2 — Few-shot Exemplo 2 (bug médio) enriquecido
    O exemplo atual tem critérios rasos. Adicionar ao Então: "E deve retornar HTTP 200", "E deve logar o event para auditoria". O modelo aprende por imitação — se o exemplo tem 2 condições "E", ele gera 2; se tem 5, gera 5.
    Impacto esperado: ex 8 e 10 (que repetem exatamente esse padrão de omissão)

    M3 — Trigger words explícitas para acessibilidade (refinamento M5)
    A regra atual diz "mencionar explicitamente" mas o modelo não reconhece "foco" e "ESC" como gatilhos. Adicionar lista: foco, ESC, teclado, tab, leitor de tela, backdrop, sobreposição bloqueando.
    Impacto esperado: ex 4 (f1 0,62 → ~0,75+, o pior caso atual)

    M4 — Regra de alternativas de negócio (nova)
    Se o bug mencionar opções alternativas ("remover o item" ou "aguardar reposição"), incluí-las nos critérios como "OU [alternativa]" em vez de omitir.

5. executei e regrediu, ficou mais permissivo e pemitiu coisas que nao eram esperadas no ground truth, vou voltar a versao anterior e cexecutar nvovamente

6. Alterações propostas pelo Claude, piorou. deixamos o prompt mais permissivo para trazer mais casos no user stories pensando em cobrir o recall o que faltava, mas isso reduziu precision, pois trouxe mais coisa que não precisava

7. Alterações dessa execução: P1 — completude de critérios agora condicional por complexidade (simples=2-4 critérios, médio/complexo=cobrir tudo), para evitar que bugs simples recebam seções desnecessárias que penalizavam Precision. P2 — persona "sistema" virou PASSO 0 obrigatório antes de qualquer análise, com heurística mecânica e exemplo dedicado, porque a "EXCEÇÃO" no passo 1 estava sendo ignorada pelo modelo.
    - execução pioroi, cada nova mexida esta piorando, melhor voltar a iteraçãço que melhor resultou no score alto

8. Quanto mais mexe nos prompts mais bagunça a partir de agora. Vou fazer um novo experimento com os dois melhores prompts.

