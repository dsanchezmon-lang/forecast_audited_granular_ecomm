import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Forecast Dashboard",
    layout="wide"
)

@st.cache_data
def load_data():

    df = pd.read_parquet(
        "audited_revenue_granular.parquet"
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
    options=sorted(
        df["txt_tipo_resultado"]
        .dropna()
        .unique()
    ),
    default=sorted(
        df["txt_tipo_resultado"]
        .dropna()
        .unique()
    )
)

channel = st.sidebar.multiselect(
    "Channel",
    options=sorted(
        df["txt_channel"]
        .dropna()
        .unique()
    ),
    default=sorted(
        df["txt_channel"]
        .dropna()
        .unique()
    )
)

country = st.sidebar.multiselect(
    "Country",
    options=sorted(
        df["country"]
        .dropna()
        .unique()
    ),
    default=sorted(
        df["country"]
        .dropna()
        .unique()
    )
)

# =====================================
# FILTER DATA
# =====================================

filtered = df[
    (df["txt_tipo_resultado"].isin(tipo_resultado))
    &
    (df["txt_channel"].isin(channel))
    &
    (df["country"].isin(country))
]

# =====================================
# TITLE
# =====================================

st.title("Forecast Revenue Dashboard")

# =====================================
# KPI
# =====================================

total_revenue = filtered["revenue_usd"].sum()

st.metric(
    "Revenue USD",
    f"${total_revenue:,.0f}"
)

# =====================================
# TIMESERIES
# =====================================

timeseries = (
    filtered
    .groupby(
        ["dt_date_sale", "txt_channel"],
        as_index=False
    )
    ["revenue_usd"]
    .sum()
)

fig = px.line(
    timeseries,
    x="dt_date_sale",
    y="revenue_usd",
    color="txt_channel",
    title="Revenue Timeline"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================
# DETAIL TABLE
# =====================================

st.dataframe(
    filtered,
    use_container_width=True
)