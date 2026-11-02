# Justificativa das métricas — Dashboard 2

A ideia do dashboard é ajudar gestores de frota e equipes de manutenção a entender os dados do EV Battery Failure Dataset. Ele mostra como estão os veículos da amostra e permite comparar grupos, mas não prevê quais baterias vão falhar nem comprova o que causou as falhas.

## Métrica 1: Veículos analisados
- **Variável:** `vehicle_id` (uma linha por veículo).

- **O que ela mede:** a quantidade de veículos após os filtros e a seleção do gráfico.

- **Por que foi escolhida:** porque ela serve para informar a quantidade de veículos e dados que temos.

- **Público-alvo:** gestores de frota e analistas de manutenção.

- **Qual decisão pode ser apoiada por essa métrica?** Verificar se há veículos suficientes no dataset antes de fazer qualquer coisa.

- **O que comunica ao público-alvo:** quantos veículos estão sendo considerados, evitando interpretar uma proporção sem conhecer sua base.

## Métrica 2: Veículos com falha

- **Variável:** `battery_failure`, em que 0 significa sem falha registrada e 1 significa com falha registrada.

- **O que ela mede:** a porcentagem de veículos com falha entre os que estão selecionados. Para calcular, divido a quantidade de veículos com falha pelo total de veículos do grupo.

- **Por que foi escolhida:** porque só olhar a quantidade de falhas pode dar uma impressão errada ao comparar grupos de tamanhos diferentes. A porcentagem ajuda a entender quanto as falhas representam em cada um deles.

- **Público-alvo:** gestores de frota e equipes de manutenção.

- **Qual decisão pode ser apoiada por essa métrica?** Escolher quais grupos vale a pena investigar melhor, olhando a porcentagem de falhas junto com a quantidade de veículos.

- **O que comunica ao público-alvo:** de todos os veículos selecionados, qual parte teve uma falha registrada. Isso descreve o que aparece nos dados, não a chance de um veículo falhar no futuro.

## Métrica 3: Quilometragem mediana

- **Variável:** `odometer_km`.

- **O que ela mede:** o valor que fica no meio quando organizamos as quilometragens dos veículos selecionados, da menor para a maior.

- **Por que foi escolhida:** porque na EDA vimos que alguns veículos rodaram muito mais do que os outros. Esses valores puxam a média para cima, então escolhi a mediana para representar melhor a quilometragem central do grupo.

- **Público-alvo:** gestores de frota e responsáveis pelo planejamento de manutenção.

- **Qual decisão pode ser apoiada por essa métrica?** Comparar o nível de uso dos grupos e escolher quais merecem uma análise mais detalhada sobre manutenção.

- **O que comunica ao público-alvo:** uma referência da quilometragem dos veículos selecionados. Pelo menos metade deles tem uma quilometragem menor ou igual à mediana, e pelo menos metade tem uma quilometragem maior ou igual.

## Métrica 4: Capacidade mediana

- **Variável:** `battery_capacity_kwh`.

- **O que ela mede:** o valor central da capacidade das baterias dos veículos selecionados, em kWh.

- **Por que foi escolhida:** porque ajuda a entender o perfil das baterias do grupo. Na EDA, essa variável não apresentou diferença significativa entre veículos com e sem falha, então ela entra como uma informação para conhecer a frota.

- **Público-alvo:** gestores de frota e equipes de planejamento técnico.

- **Qual decisão pode ser apoiada por essa métrica?** Verificar se os grupos têm baterias de capacidades parecidas antes de comparar suas porcentagens de falha.

- **O que comunica ao público-alvo:** qual é a capacidade central das baterias selecionadas. Esse valor não informa a carga atual, a autonomia ou o estado de saúde da bateria.

## Filtros e interação

Os dois dashboards usam os mesmos filtros da barra lateral: marca, tipo de veículo e intervalos das variáveis quantitativas. Se eu desmarcar uma variável, o filtro de intervalo dela deixa de ser aplicado. Se retirar todas as marcas ou todos os tipos, o app avisa que não há veículos selecionados.

No Dashboard 2, posso escolher entre agrupar os veículos pela química ou pelo fabricante da bateria. Ao clicar em uma barra, os quatro indicadores e os dois gráficos de baixo passam a considerar só aquele grupo. Também dá para selecionar mais de uma barra com Shift + clique.

Sem nenhuma barra selecionada, os indicadores mostram todos os veículos que passaram pelos filtros da barra lateral. O botão de limpar seleção volta para essa visão. Mudar os filtros ou a opção de agrupamento também limpa a seleção anterior.

## Visuais

1. **Veículos por segmento:** mostra quantos veículos temos de cada química ou fabricante de bateria. Esse é o gráfico em que podemos clicar para selecionar os grupos. Ao passar o mouse, aparecem a quantidade de veículos, a quantidade com falha e a porcentagem com falha.

2. **Falhas por faixa de quilometragem:** mostra a porcentagem de veículos com falha em cada faixa: menos de 100 mil km, de 100 a menos de 150 mil, de 150 a menos de 200 mil, de 200 a menos de 250 mil e de 250 mil em diante. Por exemplo, um veículo com exatamente 150 mil km entra na faixa de 150 a menos de 200 mil.

3. **Falhas por ano de fabricação:** mostra a porcentagem de veículos com falha em cada ano de fabricação. A ideia é comparar veículos mais antigos e mais recentes. O ano é o de fabricação do veículo, não o ano em que a falha aconteceu, porque essa data não está no dataset.

Nos dois gráficos de porcentagem, a conta é feita dentro de cada grupo, considerando os filtros aplicados. Uma faixa sem veículos não aparece como se tivesse zero falhas. As quantidades ficam disponíveis ao passar o mouse para ajudar a interpretar os resultados: uma porcentagem alta em um grupo pequeno pode ter um peso diferente da mesma porcentagem em um grupo grande. Os gráficos mostram essas diferenças, mas não fazem um teste estatístico para dizer se elas são significativas.

## Tratamento e identidade visual

O app usa o arquivo tratado `data/clean/dataset.csv`. O carregamento tem cache para não precisar ler o arquivo de novo a cada interação.

Os tratamentos são os mesmos da atividade da EDA, onde valores numéricos ausentes foram preenchidos com a mediana e categorias ausentes receberam o nome `Desconhecido`, sem excluir linhas. Esses preenchimentos também entram nos cálculos do dashboard, então parte dos valores foi estimada durante o tratamento.

Para as cores, segui a mesma ideia da EDA: vermelho `#b5322d` para destacar as falhas e azul claro `#bcdff1` para contexto e veículos sem falha. O app tem fundo branco, barra lateral cinza claro e fonte sem serifa. O rascunho desse layout está em `entregas/rascunho-dashboard2.png`.
