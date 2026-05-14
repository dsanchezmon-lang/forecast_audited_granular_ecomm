import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Forecast Dashboard",
    layout="wide"
)

# =====================================
# LOAD DATA
# =====================================

@st.cache_data
def load_data():

    cols = [
        "dt_date_sale",
        "txt_channel",
        "txt_tipo_resultado",
        "country",
        "revenue_usd"
    ]

    df = pd.read_parquet(
        "audited_revenue_granular.parquet",
        columns=cols
    )

    df["dt_date_sale"] = pd.to_datetime(
        df["dt_date_sale"]
    )

    return df

df = load_data()

# =====================================
# SIDEBAR
# =====================================

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
    sorted(df["country"].dropna().unique())[:50]
)

# =====================================
# FILTER
# =====================================

filtered = df[
    (df["txt_tipo_resultado"].isin(tipo_resultado))
    &
    (df["txt_channel"].isin(channel))
]

if len(country) > 0:

    filtered = filtered[
        filtered["country"].isin(country)
    ]

# =====================================
# KPI
# =====================================

st.title("Forecast Revenue Dashboard")

st.metric(
    "Revenue USD",
    f"${filtered['revenue_usd'].sum():,.0f}"
)

# =====================================
# GRAPH
# =====================================

timeseries = (
    filtered
    .groupby(
        ["dt_date_sale", "txt_channel"],
        as_index=False
    )["revenue_usd"]
    .sum()
)

fig = px.line(
    timeseries,
    x="dt_date_sale",
    y="revenue_usd",
    color="txt_channel"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================
# SAMPLE TABLE
# =====================================

st.dataframe(
    filtered.head(1000),
    use_container_width=True
)