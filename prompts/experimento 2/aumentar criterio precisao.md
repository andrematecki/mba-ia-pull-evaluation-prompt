# aumentar criterio precisão

## Exemplo 1
PERGUNTA DO USUÁRIO:
Botão de adicionar ao carrinho não funciona no produto ID 1234.

RESPOSTA GERADA PELO MODELO:
Como um cliente navegando na loja, eu quero adicionar produtos ao meu carrinho de compras, para que eu possa continuar comprando e finalizar minha compra depois.

Critérios de Aceitação:
- Dado que estou visualizando um produto
- Quando clico no botão "Adicionar ao Carrinho"
- Então o produto deve ser adicionado ao carrinho
- E devo ver uma confirmação visual
- E o contador do carrinho deve ser atualizado

RESPOSTA ESPERADA (Ground Truth):
Como um cliente navegando na loja, eu quero adicionar produtos ao meu carrinho de compras, para que eu possa continuar comprando e finalizar minha compra depois.

Critérios de Aceitação:
- Dado que estou visualizando um produto
- Quando clico no botão "Adicionar ao Carrinho"
- Então o produto deve ser adicionado ao carrinho
- E devo ver uma confirmação visual
- E o contador do carrinho deve ser atualizado

### Raciocinio
{
  "score": 0.33,
  "reasoning": "A resposta gerada não contém alucinações, pois é uma descrição padrão de um fluxo de usuário comum em e-commerce, portanto, recebe 1.0 em ausência de alucinações. No entanto, a resposta não está focada na pergunta, que é sobre um problema específico com o botão de adicionar ao carrinho para um produto específico (ID 1234), resultando em 0.0 em foco na pergunta. Em termos de correção factual, a resposta é correta, mas não aborda o problema específico mencionado, resultando em 0.0. A média dos critérios é 0.33."
}



## Exemplo 2
PERGUNTA DO USUÁRIO:
Carrinho permite finalizar compra mesmo com produto fora de estoque.

Fluxo do bug:
1. Produto tem 2 unidades em estoque
2. Cliente A adiciona 2 unidades ao carrinho
3. Estoque fica zerado
4. Cliente B ainda consegue adicionar ao carrinho
5. Cliente B finaliza compra
6. Sistema gera pedido mas não tem estoque para enviar

RESPOSTA GERADA PELO MODELO:
Como um cliente comprando na loja, eu quero que o sistema impeça a finalização da compra quando não houver estoque disponível, para que eu não enfrente problemas com pedidos não atendidos.

Critérios de Aceitação:
- Dado que um produto está em estoque
- Quando um cliente adiciona o produto ao carrinho
- Então o sistema deve atualizar o estoque disponível
- E deve impedir que outros clientes adicionem o produto ao carrinho quando o estoque chegar a zero

- Dado que um cliente está finalizando a compra
- Quando o produto no carrinho não está mais disponível em estoque
- Então o sistema deve impedir a finalização da compra
- E deve exibir uma mensagem informando que o produto está fora de estoque

Contexto Técnico:
- Situação atual: O sistema permite que múltiplos clientes finalizem compras de produtos que estão fora de estoque.
- Situação esperada: O sistema deve bloquear a finalização da compra quando o estoque do produto estiver zerado.

RESPOSTA ESPERADA (Ground Truth):
Como o sistema de e-commerce, eu quero validar disponibilidade de estoque antes de permitir finalização de compra, para que não sejam criados pedidos que não podem ser atendidos.

Critérios de Aceitação:
- Dado que um produto está no carrinho
- Quando o cliente tenta finalizar a compra
- Então o sistema deve validar estoque disponível em tempo real
- E se o produto estiver fora de estoque, deve bloquear a compra
- E deve exibir mensagem clara sobre a indisponibilidade
- E deve sugerir remover o item ou aguardar reposição

Critérios de Prevenção:
- Quando produto ficar sem estoque
- E houver itens em carrinhos de outros clientes
- Então deve exibir aviso "estoque limitado" ao adicionar
- E deve reservar estoque temporariamente (15 minutos) ao ir para checkout

Contexto do Bug:
- Problema: validação de estoque não é feita no checkout
- Impacto: pedidos criados sem possibilidade de atendimento
- Cenário crítico: múltiplos clientes comprando último item


### Raciocinio
{
  "score": 0.67,
  "reasoning": "A resposta gerada é precisa em termos de critério de aceitação, mas falta detalhamento sobre a prevenção de problemas de estoque, como sugerido na resposta esperada. Não há alucinações, pois todas as informações são baseadas em práticas comuns de e-commerce. A resposta está focada na pergunta, mas não aborda completamente o contexto do bug e as medidas preventivas necessárias. A correção factual é alta, mas a resposta poderia ser mais completa ao incluir sugestões de prevenção, como a reserva temporária de estoque. Assim, a média dos critérios resulta em um score de 0.67."
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
Como um cliente utilizando o pipeline de vendas, eu quero que o valor total da minha compra seja calculado corretamente com todos os descontos aplicados, para que eu possa ter certeza de que estou pagando o valor correto.

Critérios de Aceitação:
- Dado que estou adicionando produtos ao meu carrinho
- Quando aplico um desconto sobre o valor total da compra
- Então o desconto deve ser aplicado sobre o valor total de todos os produtos
- E o valor total exibido deve ser o correto após a aplicação do desconto

Contexto Técnico:
- Situação atual: O sistema aplica desconto apenas no primeiro produto.
- Situação esperada: O desconto deve ser aplicado sobre o valor total de todos os produtos no carrinho.

RESPOSTA ESPERADA (Ground Truth):
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
  "score": 0.67,
  "reasoning": "A resposta gerada não contém alucinações, pois todas as informações são baseadas no cenário apresentado, resultando em uma pontuação de 1.0 para ausência de alucinações. No entanto, a resposta não está totalmente focada na pergunta, pois adota a perspectiva do cliente em vez do vendedor, como na resposta esperada, resultando em 0.5 para foco na pergunta. A correção factual é 0.5, pois a resposta não fornece o cálculo detalhado do valor total esperado, como na resposta esperada. A média dos critérios é 0.67."
}
