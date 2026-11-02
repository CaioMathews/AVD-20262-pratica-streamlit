# Declaração de Uso de IA

**Nome:**  Caio Mathews de Farias Ferreira
**Data:** 02/11/2026
**Atividade:** Dashboards em Streamlit — Aulas 21, 22 e 23
**Dataset:** EV Battery Failure Dataset

## Ferramenta

Codex (OpenAI), utilizado no aplicativo Codex para leitura dos materiais, apoio na implementação em Python/Streamlit, elaboração dos rascunhos de layout, documentação e verificação do funcionamento.

A EDA original já possuía uma declaração de uso do Claude (Anthropic), que foi mantida no notebook. Esta declaração registra o apoio do Codex na adaptação dessa EDA para os dashboards e nas implementações das três etapas de Streamlit.

## Entrega 1 — Aula 21: estrutura do Dashboard 1

### Finalidade do uso

Leitura dos materiais, entendimento do repositório e adaptação da estrutura inicial do app para minha EDA de falhas de baterias de veículos elétricos.

### Prompts usados

> Leia e entenda as 3 aulas e o repositorio que dei fork e o clone.

Foram informados os PDFs das Aulas 21, 22 e 23 e o clone local do repositório.

> Preciso da sua ajuda para geração dos graficos e da aplicação streamlit, e me ajude a criar o png dos rascuhos para geração 


Pedidos de verificação do código:

> Verifique os arquivos para ver se eu deixei de fazer algo ou possui algo incorreto

### Aceito e por quê

- Adaptação do `app.py` para meu dataset, com seletor das variáveis quantitativas, sliders de intervalo e espaços reservados para correlação e distribuição, seguindo o escopo da primeira entrega.

- Ajuste do caminho de leitura do CSV no notebook e inclusão da exportação para `data/clean/dataset.csv`, permitindo que o app carregasse o resultado do tratamento.

- Geração inicial do CSV tratado seguindo as regras já presentes na minha EDA: mediana nas quantitativas, categoria `Desconhecido` nas qualitativas, manutenção dos outliers e das colunas derivadas.

- Criação do rascunho do Dashboard 1, para representar a disposição dos filtros e das áreas de visualização.

- Verificações automáticas de inicialização, seleção de variáveis, filtros de intervalo e contagens, para conferir o funcionamento da estrutura.

### Modificado e por quê

- O exemplo de doenças cardíacas foi substituído pelo contexto de veículos elétricos. Seus gráficos foram retirados nessa etapa, mantendo espaços reservados para respeitar a progressão da atividade.

- A pasta `notebooks/` foi reduzida à minha EDA, conforme solicitado.


### Participação e verificação

Forneci minha EDA e o dataset, solicitei a adaptação e os ajustes no layout e realizei manualmente o commit da primeira entrega. O tratamento dos dados já estava definido na EDA original; o apoio do Codex nesta etapa foi na integração com o app, na exportação e nas verificações automáticas.

## Entrega 2 — Aula 22: gráficos e indicadores

### Finalidade do uso

Completar os gráficos do Dashboard 1 e me ajudar na criação dos indicadores, dos gráficos e do rascunho do Dashboard 2, seguindo a atividade da Aula 22.

### Prompts usados

> Me ajude com a implementação do dashboard 2 e a geração do rascunho com base no que já fiz para a EDA e para a aula anterior

Pedidos de verificação do código:

> verifique se deixei algo passar despercebido ou se tem algum erro no projeto

Também pedi ajuda para corrigir o texto das justificativas das metricas e organizar melhor, além de usar para organizar e fazer a declaração de IA por entregas.

### Aceito e por quê

- Implementação do mapa de correlação de Spearman e dos histogramas, para completar as visualizações do Dashboard 1 com os dados dos veículos elétricos.

- Inclusão de cache no carregamento dos dados e criação das abas, para evitar a leitura do CSV a cada interação e separar os dois dashboards.

- Criação dos gráficos do Dashboard 2 e dos filtros de marca, tipo de veículo e seleção de segmentos, permitindo comparar os grupos e atualizar os indicadores.

- Criação do rascunho do Dashboard 2 e apoio na justificativa das métricas.

- Inclusão dos cálculos dos indicadores e das prévias dos gráficos ao final do notebook, mantendo a análise que eu já tinha feito.

- Verificação do funcionamento do app e dos cálculos.

### Modificado e por quê

- Os espaços reservados da primeira entrega foram substituídos pelos gráficos do meu dataset.

- As cores do app foram ajustadas para seguir a paleta da EDA, com vermelho para destaque e falhas e azul claro para contexto e veículos sem falha.

- Durante as verificações, foram ajustados os intervalos do histograma de ano de fabricação e as escalas dos gráficos, para facilitar a leitura.


### Participação e verificação

Solicitei a continuação da atividade, acompanhei as alterações, tirei dúvidas sobre os indicadores e fiz ajustes na documentação. O Codex ajudou na implementação, nos rascunhos, na validação da escrita das justificativas e na verificação dos cálculos e dos filtros. Também conferiu a execução completa da EDA e a interação entre os gráficos. 

## Entrega 3 — Aula 23: publicação e testes da aplicação

### Finalidade do uso

Me orientar na publicação do app no Streamlit Community Cloud e ajudar a conferir as entregas e documentação.

### Prompts usados

> como fazer o deploy

> verifique se está certo os dados do deploy, e me diga se tem alguma sugestão para o deploy

Enviei imagens das configurações de publicação para conferir o repositório, a branch, o arquivo principal e a versão do Python.


### Aceito e por quê

- Orientações para publicar o app no Streamlit Community Cloud, usando meu repositório, a branch `main` e o arquivo `app.py`.

- Conferência das configurações do deploy e sugestão de um endereço mais fácil de compartilhar. A aplicação foi publicada em `https://falhas-baterias-caio.streamlit.app/`.

- Testes das duas abas, dos filtros e dos gráficos na versão publicada, para verificar se o app funcionava fora do meu computador.

### Modificado e por quê

- Troquei o endereço automático sugerido pelo Streamlit por `falhas-baterias-caio`, para deixar o link mais simples.


### Participação e verificação

Fiz o deploy manualmente, seguindo as orientações, e enviei as configurações e o link para conferência. O Codex verificou o acesso público sem login, a navegação entre as abas, os filtros de ano, marca e tipo de veículo, a seleção simples e múltipla de segmentos e a limpeza da seleção. Também testou situações sem variáveis ou sem veículos selecionados e comparou os indicadores com os dados locais. Os testes da versão publicada não apontaram erros. A inclusão do link no README e esta seção registram a conclusão dessa etapa.
