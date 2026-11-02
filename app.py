import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

from src.data_loader import load_data

st.set_page_config(page_title="Falhas de Baterias de Veículos Elétricos", layout="wide")
st.title("Falhas de Baterias de Veículos Elétricos")
st.caption("EV Battery Failure Dataset — correlação, distribuição e indicadores")

df = load_data()

VARS_QUANT = ["manufacturing_year", "battery_capacity_kwh", "odometer_km"]
ROTULOS = {
    "manufacturing_year": "Ano de fabricação",
    "battery_capacity_kwh": "Capacidade da bateria (kWh)",
    "odometer_km": "Quilometragem (km)",
    "battery_chemistry": "Química da bateria",
    "battery_manufacturer": "Fabricante da bateria",
}
COR_DESTAQUE = "#b5322d"
COR_CONTEXTO = "#bcdff1"
FAIXAS_KM = ["< 100 mil", "100–150 mil", "150–200 mil", "200–250 mil", "≥ 250 mil"]


def limpar_selecao():
    st.session_state["versao_selecao"] = st.session_state.get("versao_selecao", 0) + 1


def resumo_falhas(dados, coluna):
    resumo = dados.groupby(coluna, observed=True).agg(
        veiculos=("battery_failure", "size"), falhas=("battery_failure", "sum")
    ).reset_index()

    resumo["proporcao_falha"] = resumo["falhas"] / resumo["veiculos"]

    return resumo


with st.sidebar:
    st.header("Filtros")

    variaveis = st.multiselect(
        "Variáveis quantitativas", VARS_QUANT, default=VARS_QUANT,
        format_func=lambda var: ROTULOS[var], on_change=limpar_selecao,
    )

    intervalos = {}

    for var in variaveis:

        if var == "manufacturing_year":
            minimo, maximo, passo = int(df[var].min()), int(df[var].max()), 1
        else:
            minimo, maximo, passo = float(df[var].min()), float(df[var].max()), 0.1

        if minimo == maximo:
            st.caption(f"{ROTULOS[var]}: todos os veículos têm o valor {minimo}.")
            continue

        intervalos[var] = st.slider(
            ROTULOS[var], min_value=minimo, max_value=maximo,
            value=(minimo, maximo), step=passo, key=f"intervalo_{var}",
            on_change=limpar_selecao,
        )

    marcas = st.multiselect(
        "Marcas de veículos", sorted(df["vehicle_brand"].unique()),
        default=sorted(df["vehicle_brand"].unique()), on_change=limpar_selecao,
    )

    tipos = st.multiselect(
        "Tipos de veículos", sorted(df["vehicle_type"].unique()),
        default=sorted(df["vehicle_type"].unique()), on_change=limpar_selecao,
    )

base = df[df["vehicle_brand"].isin(marcas) & df["vehicle_type"].isin(tipos)]

for var, (inicio, fim) in intervalos.items():
    base = base[base[var].between(inicio, fim)]

st.caption(f"{len(base):,} de {len(df):,} veículos dentro dos filtros escolhidos.")
tab1, tab2 = st.tabs(["Correlação e distribuição", "Indicadores"])

with tab1:

    separar_classes = st.toggle("Distinguir por status da bateria", value=False)
    col_correlacao, col_distribuicao = st.columns([1, 1.5])

    with col_correlacao:

        st.subheader("Correlação (Spearman)")

        if len(variaveis) < 2:
            st.warning("Selecione pelo menos 2 variáveis para analisar a correlação.")
        elif len(base) < 2:
            st.warning("São necessários pelo menos 2 veículos para calcular a correlação.")
        else:
            matriz = base[variaveis].corr(method="spearman")
            corr = (
                matriz.rename_axis(index="var_y")
                .reset_index()
                .melt(
                    id_vars="var_y", value_vars=variaveis,
                    var_name="var_x", value_name="correlacao",
                )
                .dropna(subset=["correlacao"])
            )

            if corr.empty:
                st.warning("A correlação é indefinida: as variáveis selecionadas não variam neste recorte.")
            else:

                if base[variaveis].nunique().lt(2).any():
                    st.caption("Células de variáveis sem variação ficam vazias.")

                grade = alt.Chart(corr).encode(
                    x=alt.X("var_x:N", title=None, sort=variaveis, axis=alt.Axis(labelAngle=-30, labelExpr="""
                        datum.label === 'manufacturing_year' ? 'Ano' :
                        datum.label === 'battery_capacity_kwh' ? 'Capacidade' : 'Km'
                    """)),

                    y=alt.Y("var_y:N", title=None, sort=variaveis, axis=alt.Axis(labelExpr="""
                        datum.label === 'manufacturing_year' ? 'Ano' :
                        datum.label === 'battery_capacity_kwh' ? 'Capacidade' : 'Km'
                    """)),
                )

                cores = grade.mark_rect().encode(
                    color=alt.Color("correlacao:Q", title="Spearman", scale=alt.Scale(scheme="redblue", domain=[-1, 1])),
                    tooltip=[alt.Tooltip("var_x:N", title="Variável"), alt.Tooltip("var_y:N", title="Variável"),
                             alt.Tooltip("correlacao:Q", title="Correlação", format=".2f")],
                )

                valores = grade.mark_text(fontSize=17).encode(
                    text=alt.Text("correlacao:Q", format=".2f"),
                    color=alt.condition("abs(datum.correlacao) > 0.5", alt.value("white"), alt.value("#30343b")),
                )

                st.altair_chart((cores + valores).properties(height=360), width="stretch")
                st.caption("Correlação indica associação entre as variáveis; não demonstra causa.")

    with col_distribuicao:

        st.subheader("Distribuição")

        if not variaveis:
            st.warning("Selecione pelo menos 1 variável para analisar a distribuição.")
        elif base.empty:
            st.warning("Nenhum veículo dentro dos filtros escolhidos.")
        else:

            for var in variaveis:

                limites = (
                    np.arange(df[var].min() - 0.5, df[var].max() + 1.5, 1)
                    if var == "manufacturing_year"
                    else np.histogram_bin_edges(df[var], bins=20)
                )

                linhas = []
                grupos = base.groupby("status_bateria") if separar_classes else [("Todos", base)]

                for classe, dados in grupos:
                    contagens, _ = np.histogram(dados[var], bins=limites)

                    for inicio, fim, quantidade in zip(limites[:-1], limites[1:], contagens):
                        linhas.append({"inicio": inicio, "fim": fim, "veiculos": int(quantidade), "status": classe})

                hist = alt.Chart(pd.DataFrame(linhas)).mark_bar(color=COR_DESTAQUE).encode(
                    x=alt.X(
                        "inicio:Q", bin="binned", title=ROTULOS[var],
                        axis=alt.Axis(format="d", tickMinStep=1) if var == "manufacturing_year" else alt.Axis(),
                    ), x2="fim:Q",

                    y=alt.Y("veiculos:Q", title="Veículos", stack="zero"),
                    tooltip=[alt.Tooltip("inicio:Q", title="De", format=".1f"),
                             alt.Tooltip("fim:Q", title="Até", format=".1f"),
                             alt.Tooltip("veiculos:Q", title="Veículos", format=",.0f")],
                )

                if separar_classes:
                    hist = hist.encode(
                        color=alt.Color("status:N", title="Status", scale=alt.Scale(domain=["OK", "Falha"], range=[COR_CONTEXTO, COR_DESTAQUE])),
                        tooltip=["status:N", "inicio:Q", "fim:Q", "veiculos:Q"],
                    )

                st.altair_chart(hist.properties(height=185), width="stretch")

with tab2:
    st.subheader("Indicadores da frota")
    st.caption("Resultados descritivos do recorte selecionado, sem previsão de falhas futuras.")

    metricas = st.container()

    grupo = st.selectbox(
        "Agrupar veículos por", ["battery_chemistry", "battery_manufacturer"],
        format_func=lambda coluna: ROTULOS[coluna], on_change=limpar_selecao,
    )

    st.button("Limpar seleção do gráfico", on_click=limpar_selecao)

    if base.empty:
        st.info("Nenhum veículo dentro dos filtros escolhidos. Ajuste os filtros para ver os indicadores.")
    else:
        st.subheader("Veículos por segmento")

        segmentos = resumo_falhas(base, grupo).rename(columns={grupo: "categoria"})
        clique = alt.selection_point(name="segmento", fields=["categoria"], clear="dblclick")

        barras = alt.Chart(segmentos).mark_bar(color=COR_CONTEXTO).encode(
            x=alt.X("veiculos:Q", title="Veículos"),

            y=alt.Y("categoria:N", title=ROTULOS[grupo], sort="-x"),
            opacity=alt.condition(clique, alt.value(1), alt.value(0.3)),
            tooltip=[alt.Tooltip("categoria:N", title=ROTULOS[grupo]),
                     alt.Tooltip("veiculos:Q", title="Veículos", format=",.0f"),
                     alt.Tooltip("falhas:Q", title="Veículos com falha", format=",.0f"),
                     alt.Tooltip("proporcao_falha:Q", title="Proporção com falha", format=".1%")],
        ).add_params(clique).properties(height=max(240, len(segmentos) * 30))

        evento = st.altair_chart(
            barras, width="stretch", on_select="rerun",
            key=f"segmentos_{st.session_state.get('versao_selecao', 0)}", selection_mode="segmento",
        )

        categorias = [item["categoria"] for item in evento.selection.get("segmento", [])]
        selecionado = base[base[grupo].isin(categorias)] if categorias else base

        st.caption("Clique em uma barra para filtrar os indicadores e os gráficos abaixo. Shift + clique seleciona mais de uma; duplo clique limpa.")

        if categorias:
            st.caption("Segmentos selecionados: " + ", ".join(categorias))

        if selecionado.empty:
            st.info("A seleção não contém veículos. Limpe a seleção do gráfico.")
        else:

            with metricas:
                cards = st.columns(4)
                cards[0].metric("Veículos analisados", f"{len(selecionado):,}")
                cards[1].metric("Veículos com falha", f"{selecionado['battery_failure'].mean():.1%}")
                cards[2].metric("Quilometragem mediana", f"{selecionado['odometer_km'].median():,.0f} km")
                cards[3].metric("Capacidade mediana", f"{selecionado['battery_capacity_kwh'].median():.1f} kWh")

            selecionado = selecionado.copy()

            selecionado["faixa_km"] = pd.cut(
                selecionado["odometer_km"], bins=[0, 100000, 150000, 200000, 250000, np.inf],
                labels=FAIXAS_KM, right=False,
            )

            resumos = {campo: resumo_falhas(selecionado, campo) for campo in ["faixa_km", "manufacturing_year"]}
            limite_y = min(1, max(0.1, max(r["proporcao_falha"].max() for r in resumos.values()) * 1.15))
            col_km, col_ano = st.columns(2)

            for coluna, campo, titulo, rotulo in [
                (col_km, "faixa_km", "Falhas por quilometragem", "Quilometragem (km)"),
                (col_ano, "manufacturing_year", "Falhas por ano", "Ano de fabricação"),
            ]:
                with coluna:

                    st.subheader(titulo)
                    resumo = resumos[campo]

                    grafico = alt.Chart(resumo).mark_bar(color=COR_DESTAQUE).encode(
                        x=alt.X(f"{campo}:O", title=rotulo, sort=FAIXAS_KM if campo == "faixa_km" else "ascending", axis=alt.Axis(labelAngle=-30)),

                        y=alt.Y("proporcao_falha:Q", title="Veículos com falha", axis=alt.Axis(format=".0%"), scale=alt.Scale(domain=[0, limite_y])),
                        tooltip=[alt.Tooltip(f"{campo}:O", title=rotulo),
                                 alt.Tooltip("veiculos:Q", title="Veículos", format=",.0f"),
                                 alt.Tooltip("falhas:Q", title="Veículos com falha", format=",.0f"),
                                 alt.Tooltip("proporcao_falha:Q", title="Proporção com falha", format=".1%")],
                    ).properties(height=300)

                    st.altair_chart(grafico, width="stretch")

            st.caption("Proporção com falha = veículos com battery_failure = 1 ÷ veículos do grupo. Os tooltips mostram o tamanho de cada grupo.")

            st.caption("Os dados tratados preservam as imputações da EDA: mediana nas quantitativas e 'Desconhecido' nas categorias.")
