# sequencia de execuçao

esse experimento foi guiado por alterações somente do Claude

1. apos dois experimenros com mais de 10 versoes de prompts cada, criei um novo experimento agora pedindo para o Claude gerar um novo prompt com todos aprendizados que tive. Pegou o melhor prompt com as melhores notas e vai corrigir o Recall baixo que afeta o F1
    - executou mas piorou a meterica de precisão

2. o Claude vai tentar mais alguns ajustes de criterios de race condition e exemplos de bugs complexos.
    - aumentou o F1 adicionando os exemplos especificos

3. Agora vamos adicionar exemplos para casos de Android e Mobile
    - Regredi com 5 exemplos — o prompt ficou longo demais. Vou voltar para 4 exemplos (o melhor resultado) e focar em dois problemas específicos detectados:

    1. Persona errada: o bug "Dashboard mostra contagem errada de usuários ativos" tem como persona "administrador" na referência, mas minha regra mapeia "dashboard" para "gerente/executivo" — isso prejudica F1 e Precision
    2. Bugs complexos: a regra de "Métricas de Sucesso" e organização por sprint precisa de mais clareza

4. voltamos para 4 exemplos e outras alterçaões no prompt