import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Forecast Dashboard",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_parquet(
        "audited_revenue_granular.parquet"
    )

df = load_data()

st.sidebar.title("Filtros")

tipo_resultado = st.sidebar.multiselect(
    "Tipo Resultado",
    sorted(df["txt_tipo_resultado"].dropna().unique()),
    default=sorted(df["txt_tipo_resultado"].dropna().unique())
)

channel = st.sidebar.multiselect(
    "Channel",
    sorted(df["txt_channel"].dropna().unique()),
    default=sorted(df["txt_channel"].dropna().unique())
)

country = st.sidebar.multiselect(
    "Country",
    sorted(df["country"].dropna().unique()),
    default=sorted(df["country"].dropna().unique())
)

filtered = df[
    (df["txt_tipo_resultado"].isin(tipo_resultado)) &
    (df["txt_channel"].isin(channel)) &
    (df["country"].isin(country))
]

    )["revenue_usd"]
    .sum()
    color="txt_channel",
    title="Revenue Timeline"
)
    use_container_width=True
)

st.dataframe(
    filtered,
    use_container_width=True
)
st.plotly_chart(
    fig,
    timeseries,
    x="dt_date_sale",
    y="revenue_usd",
)

fig = px.line(
st.title("Forecast Revenue Dashboard")

st.metric(
    "Revenue USD",
    f"${filtered['revenue_usd'].sum():,.0f}"
        as_index=False
)

        ["dt_date_sale", "txt_channel"],
timeseries = (
    filtered
    .groupby(

