# aumentar criterio clareza

## Exemplo 1
PERGUNTA DO USUÁRIO:
Relatório de vendas demora mais de 2 minutos para gerar quando filtro ultrapassa 1000 registros.

Detalhes:
- Query SQL está sem index na coluna data_venda
- Timeout do navegador após 120 segundos
- Usuários reclamando de lentidão no horário comercial

RESPOSTA GERADA PELO MODELO:
Como um usuário do sistema de relatórios, eu quero que os relatórios de vendas sejam gerados rapidamente, para que eu possa analisar os dados sem atrasos e tomar decisões informadas.

Critérios de Aceitação:
- Dado que estou aplicando um filtro que retorna mais de 1000 registros
- Quando solicito a geração do relatório de vendas
- Então o relatório deve ser gerado em menos de 120 segundos
- E não deve ocorrer timeout no navegador

Contexto Técnico:
- Query SQL está sem index na coluna data_venda
- Timeout do navegador após 120 segundos
- Usuários reclamando de lentidão no horário comercial

RESPOSTA ESPERADA (Referência):
Como um gerente de vendas, eu quero gerar relatórios de vendas rapidamente mesmo com grandes volumes de dados, para que eu possa analisar informações sem esperar longos períodos.

Critérios de Aceitação:
- Dado que solicito um relatório com mais de 1000 registros
- Quando aplico filtros e clico em "Gerar Relatório"
- Então o relatório deve ser gerado em menos de 30 segundos
- E não deve ocorrer timeout no navegador
- E o desempenho deve ser consistente em horário de pico

Contexto Técnico:
- Problema identificado: falta de índice na coluna data_venda
- Performance atual: >120s para 1000+ registros
- Performance esperada: <30s para qualquer volume
- Sugestão: adicionar índice e otimizar query SQL

### Raciocinio 
{
  "score": 0.75,
  "reasoning": "A resposta gerada é bem organizada, com uma estrutura lógica que segue o formato de critérios de aceitação e contexto técnico. A linguagem é clara e direta, mas poderia ser mais simples, evitando a repetição desnecessária de informações já mencionadas. Não há ambiguidades significativas, mas a resposta poderia ser mais concisa, especialmente ao evitar a repetição do contexto técnico. A comparação com a resposta esperada mostra que a resposta gerada poderia ser mais específica em termos de desempenho esperado e soluções propostas, o que melhoraria a clareza geral."
}

## Exemplo 2
PERGUNTA DO USUÁRIO:
Botão de adicionar ao carrinho não funciona no produto ID 1234.

RESPOSTA GERADA PELO MODELO:
Como um cliente navegando na loja, eu quero adicionar produtos ao meu carrinho de compras, para que eu possa continuar comprando e finalizar minha compra depois.

Critérios de Aceitação:
- Dado que estou visualizando o produto com ID 1234
- Quando clico no botão "Adicionar ao Carrinho"
- Então o produto deve ser adicionado ao carrinho
- E devo ver uma confirmação visual
- E o contador do carrinho deve ser atualizado

RESPOSTA ESPERADA (Referência):
Como um cliente navegando na loja, eu quero adicionar produtos ao meu carrinho de compras, para que eu possa continuar comprando e finalizar minha compra depois.

Critérios de Aceitação:
- Dado que estou visualizando um produto
- Quando clico no botão "Adicionar ao Carrinho"
- Então o produto deve ser adicionado ao carrinho
- E devo ver uma confirmação visual
- E o contador do carrinho deve ser atualizado

### Raciocinio
{
  "score": 0.75,
  "reasoning": "A resposta gerada é bem organizada, com uma estrutura lógica clara, refletindo um cenário de uso típico. No entanto, a linguagem poderia ser mais direta, pois a inclusão do ID do produto específico pode ser desnecessária para a clareza geral. A ausência de ambiguidade é boa, mas a especificidade do ID pode causar confusão se não for relevante para todos os casos. A concisão é adequada, mas a menção ao ID do produto pode ser vista como redundante, já que a resposta esperada não o inclui. A média dos critérios resulta em um score de 0.75."
}

## Exemplo 3
PERGUNTA DO USUÁRIO:
Pipeline de vendas calcula valor total errado quando há desconto.

Cenário:
- Produto A: R$ 1.000
- Produto B: R$ 500
- Desconto: 10%
- Valor esperado: R$ 1.350
- Valor mostrado: R$ 1.400

O sistema aplica desconto só no primeiro produto.

RESPOSTA GERADA PELO MODELO:
Como um vendedor utilizando o pipeline de vendas, eu quero que o valor total da venda seja calculado corretamente com a aplicação de descontos, para que eu possa fornecer informações precisas aos meus clientes e evitar confusões.

Critérios de Aceitação:
- Dado que estou adicionando o Produto A ao pipeline de vendas com valor de R$ 1.000
- E estou adicionando o Produto B ao pipeline de vendas com valor de R$ 500
- E aplico um desconto de 10%
- Quando o sistema calcula o valor total
- Então o valor total deve ser R$ 1.350
- E o sistema não deve mostrar R$ 1.400 como valor total

Contexto Técnico:
- Produto A: R$ 1.000
- Produto B: R$ 500
- Desconto: 10%
- Valor esperado: R$ 1.350
- Valor mostrado: R$ 1.400

--- 

Este bug é classificado como SIMPLES, pois trata-se de um problema isolado sem logs ou impacto crítico mencionado.

RESPOSTA ESPERADA (Referência):
Como um vendedor gerenciando oportunidades no pipeline, eu quero que o valor total seja calculado corretamente quando aplico descontos, para que eu possa apresentar propostas precisas aos clientes.

Critérios de Aceitação:
- Dado que tenho uma oportunidade com múltiplos produtos
- Quando aplico um desconto percentual
- Então o desconto deve ser aplicado no valor total de todos os produtos
- E o valor final deve ser: (soma dos produtos) × (1 - desconto%)
- E o detalhamento deve mostrar: subtotal, desconto e total

Exemplo de Cálculo:
- Produto A: R$ 1.000
- Produto B: R$ 500
- Subtotal: R$ 1.500
- Desconto 10%: -R$ 150
- Total: R$ 1.350

Contexto Técnico:
- Bug atual: desconto sendo aplicado apenas no primeiro produto
- Resultado incorreto: R$ 1.400 (deveria ser R$ 1.350)

### Raciocinio
{
    "score": 0.8,
    "reasoning": "A resposta gerada é bem organizada, com uma estrutura lógica que segue o fluxo de um cenário de usuário e critérios de aceitação. A linguagem é clara e direta, facilitando a compreensão. No entanto, há uma leve ambiguidade na explicação do cálculo do valor total, pois não detalha explicitamente como o desconto deve ser aplicado em todos os produtos. A resposta é concisa, mas poderia ser mais direta ao ponto, eliminando algumas repetições. No geral, a clareza é boa, mas há espaço para melhorias na explicação do cálculo do desconto."
}