import os
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path
from PIL import Image
import pydeck as pdk


# -------------------------------------------------------------------
# CONFIGURACIÓN BÁSICA
# -------------------------------------------------------------------

# Ruta del logo (mismo folder que este archivo)
BASE_DIR = Path(__file__).parent
logo_path = BASE_DIR / "Logo-dimex111.png"
logo = Image.open(logo_path)

st.set_page_config(
    page_title="Dimex | Tablero de Sucursales",
    page_icon=logo,   # aquí usamos el logo
    layout="wide",
    initial_sidebar_state="expanded",
)

# Paleta de colores Dimex / tech
DIMEX_COLORS = {
    "primary": "#4CAF2A",       # verde principal
    "primary_dark": "#2C7A16",
    "accent": "#FFC300",        # amarillo
    "bg": "#F5F7FA",
    "card_bg": "#FFFFFF",
    "text_main": "#24323F",
    "text_soft": "#6B7B8A",
    "danger": "#E53935",
}

# -------------------------------------------------------------------
# ESTILOS GLOBALES (CSS) PARA HACERLO MODERNO
# -------------------------------------------------------------------
CUSTOM_CSS = f"""
<style>

/* ================================
   FONDO GLOBAL TIPO APPLE + DIMEX
================================ */

/* Fondo para toda la app */
body {{
    margin: 0;
    background:
        radial-gradient(circle at 0% 0%, rgba(76, 175, 42, 0.16), transparent 55%),
        radial-gradient(circle at 100% 0%, rgba(255, 195, 0, 0.12), transparent 55%),
        linear-gradient(135deg,
            #F3F6FA 0%,
            #FFFFFF 45%,
            #E7F4EC 100%
        );
    background-attachment: fixed;
}}

/* Contenedor principal de Streamlit */
[data-testid="stAppViewContainer"] > .main {{
    background: transparent;
    backdrop-filter: blur(10px) saturate(150%);
}}

/* Contenedor interno donde van los elementos (para dar efecto glass) */
.block-container {{
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    border-radius: 24px;
    background: rgba(255, 255, 255, 0.82);
    box-shadow:
        0 24px 60px rgba(15, 23, 42, 0.16),
        0 0 0 1px rgba(148, 163, 184, 0.25);
    backdrop-filter: blur(16px);
}}

/* ================================
   ANIMACIONES SUAVES (KPIs & Charts)
================================ */
@keyframes fadeInUp {{
    0% {{
        opacity: 0;
        transform: translateY(14px) scale(0.98);
    }}
    60% {{
        opacity: 1;
        transform: translateY(-2px) scale(1.01);
    }}
    100% {{
        opacity: 1;
        transform: translateY(0) scale(1);
    }}
}}

@keyframes fadeIn {{
    0% {{ opacity: 0; transform: scale(0.96); }}
    100% {{ opacity: 1; transform: scale(1); }}
}}

/* ================================
   ENCABEZADO DIMEX
================================ */
.dimex-header {{
    padding: 1.5rem 0 0.5rem 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}
.dimex-title-block {{
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
}}
.dimex-title {{
    font-size: 2.1rem;
    font-weight: 800;
    color: {DIMEX_COLORS["text_main"]};
    letter-spacing: 0.04em;
}}
.dimex-subtitle {{
    font-size: 0.95rem;
    color: {DIMEX_COLORS["text_soft"]};
}}
.dimex-badge {{
    padding: 0.25rem 0.75rem;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 600;
    color: #fff;
    background: linear-gradient(135deg, {DIMEX_COLORS["primary_dark"]}, {DIMEX_COLORS["primary"]});
    box-shadow: 0 0 18px rgba(76, 175, 42, 0.35);
}}

/* ================================
   TARJETAS DE FILTROS
================================ */
.filter-card {{
    background: linear-gradient(135deg, #FFFFFF, #F8FFF7);
    border-radius: 18px;
    padding: 1rem 1.2rem;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
    border: 1px solid rgba(148, 163, 184, 0.25);
    backdrop-filter: blur(8px);
    margin-bottom: 0.8rem;
}}
.filter-title {{
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: {DIMEX_COLORS["text_soft"]};
    margin-bottom: 0.4rem;
}}

/* ================================
   KPI GRID
================================ */
.kpi-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin-top: 0.4rem;
}}

.kpi-card {{
    position: relative;
    padding: 1.1rem 1.2rem;
    border-radius: 18px;
    background: {DIMEX_COLORS["card_bg"]};
    overflow: hidden;
    border: 1px solid rgba(148, 163, 184, 0.35);
    box-shadow:
        0 18px 45px rgba(15, 23, 42, 0.10),
        0 0 0 1px rgba(148, 163, 184, 0.18);
    transition: all 220ms ease-out;
    cursor: default;

    /* Animación al renderizar */
    animation: fadeInUp 0.45s ease-out;
}}
.kpi-card::before {{
    content: "";
    position: absolute;
    inset: -40%;
    background: radial-gradient(circle at top, rgba(76, 175, 42, 0.12), transparent 55%);
    opacity: 0;
    transition: opacity 260ms ease-out;
}}
.kpi-card:hover {{
    transform: translateY(-4px) scale(1.01);
    box-shadow:
        0 24px 55px rgba(15, 23, 42, 0.22),
        0 0 22px rgba(76, 175, 42, 0.35); /* Glow tech verde */
}}
.kpi-card:hover::before {{
    opacity: 1;
}}

.kpi-label {{
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: {DIMEX_COLORS["text_soft"]};
    margin-bottom: 0.25rem;
}}

.kpi-value {{
    font-size: 1.6rem;
    font-weight: 800;
    color: {DIMEX_COLORS["text_main"]};
}}

.kpi-trend {{
    font-size: 0.82rem;
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    margin-top: 0.25rem;
    padding: 0.12rem 0.55rem;
    border-radius: 999px;
    background-color: rgba(76, 175, 42, 0.06);
    color: {DIMEX_COLORS["primary_dark"]};
    font-weight: 500;
}}
.kpi-trend.bad {{
    background-color: rgba(229, 57, 53, 0.06);
    color: {DIMEX_COLORS["danger"]};
}}

.kpi-caption {{
    font-size: 0.75rem;
    color: {DIMEX_COLORS["text_soft"]};
    margin-top: 0.3rem;
}}

/* ================================
   CHART CARD
================================ */
.chart-card {{
    margin-top: 1rem;
    padding: 1rem 1.2rem;
    border-radius: 18px;
    background: #FFFFFF;
    box-shadow: 0 16px 40px rgba(15, 23, 42, 0.08);
    border: 1px solid rgba(148, 163, 184, 0.3);

    /* Animación */
    animation: fadeIn 0.40s ease-out;
}}
.chart-title {{
    font-size: 0.95rem;
    font-weight: 600;
    color: {DIMEX_COLORS["text_main"]};
    margin-bottom: 0.3rem;
}}
.chart-caption {{
    font-size: 0.78rem;
    color: {DIMEX_COLORS["text_soft"]};
    margin-bottom: 0.6rem;
}}

/* ================================
   PILL DE CONTEXTO
================================ */
.context-pill {{
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    padding: 0.25rem 0.8rem;
    border-radius: 999px;
    background-color: rgba(15, 23, 42, 0.03);
    border: 1px solid rgba(148, 163, 184, 0.4);
    font-size: 0.75rem;
    color: {DIMEX_COLORS["text_soft"]};
    margin-top: 0.4rem;
}}
.context-pill span.context-strong {{
    font-weight: 600;
    color: {DIMEX_COLORS["primary_dark"]};
}}

/* ================================
   SELECTBOX más moderno (CSS hack)
================================ */
.stSelectbox > div {{
    border: 1px solid #D0D7DE !important;
    border-radius: 12px !important;
    padding: 6px !important;
    background: white !important;
    transition: all 0.2s ease-out !important;
}}
.stSelectbox > div:hover {{
    border-color: {DIMEX_COLORS["primary"]} !important;
    box-shadow: 0 0 12px rgba(76, 175, 42, 0.20);
}}
.stSelectbox label {{
    font-weight: 600 !important;
    color: {DIMEX_COLORS["text_soft"]} !important;
}}

/* ================================
   ALERTA DE CLUSTER SELECCIONADO
================================ */
.cluster-alert {{
    margin-top: 0.8rem;
    margin-bottom: 0.8rem;
    padding: 0.75rem 1rem;
    border-radius: 14px;
    border: 1px solid rgba(76, 175, 42, 0.35);
    background: linear-gradient(90deg, #ECFDF3, #F4FFF7);
    color: #14532D;
    font-size: 0.9rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
    animation: fadeIn 0.35s ease-out;
    box-shadow: 0 10px 25px rgba(22, 101, 52, 0.12);
}}

.cluster-alert-icon {{
    font-size: 1.1rem;
}}

.cluster-alert-branch {{
    font-weight: 700;
}}

.cluster-alert-cluster {{
    font-weight: 700;
    color: #15803D;
}}

</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# -------------------------------------------------------------------
# CARGA DE DATOS
# -------------------------------------------------------------------
@st.cache_data(show_spinner=True)
def load_excel(file) -> pd.DataFrame:
    return pd.read_excel(file)

def get_default_dataframe() -> pd.DataFrame:
    """
    Si el usuario no ha subido archivo, intenta cargar el Excel local
    Info_Reto_Sucursal_Excel.xlsx para pruebas.
    """
    filename = "Info_Reto_Sucursal_Excel.xlsx"
    if os.path.exists(filename):
        return load_excel(filename)
    else:
        return pd.DataFrame()

# -------------------------------------------------------------------
# FUNCIONES AUXILIARES
# -------------------------------------------------------------------
def format_currency(x: float) -> str:
    if pd.isna(x):
        return "–"
    # millones MXN
    if abs(x) >= 1_000_000:
        return f"${x/1_000_000:,.1f}M"
    return f"${x:,.0f}"

def format_percent(x: float) -> str:
    if pd.isna(x):
        return "–"
    return f"{x*100:,.1f}%" if x < 1.1 else f"{x:,.1f}%"  # por si ya viene en %

def build_filters(df: pd.DataFrame):
    st.sidebar.markdown("### 📂 Cargar base de sucursales")
    uploaded = st.sidebar.file_uploader(
        "Sube la base de sucursales Dimex (.xlsx)",
        type=["xlsx"],
        help="Debe tener las columnas Región, Zona, Sucursal y métricas numéricas.",
    )

    if uploaded is not None:
        data = load_excel(uploaded)
    else:
        data = get_default_dataframe()
        if data.empty:
            st.sidebar.warning(
                "Sube un archivo de Excel para comenzar. "
                "Mientras no haya archivo, el tablero estará vacío."
            )

    if data.empty:
        return data, None, None, None

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎯 Filtros de segmento")

    regiones = ["Todas"] + sorted(data["Región"].dropna().unique().tolist())
    region_sel = st.sidebar.selectbox("Región", regiones, index=0)

    if region_sel != "Todas":
        df_region = data[data["Región"] == region_sel]
    else:
        df_region = data.copy()

    zonas = ["Todas"] + sorted(df_region["Zona"].dropna().unique().tolist())
    zona_sel = st.sidebar.selectbox("Zona", zonas, index=0)

    if zona_sel != "Todas":
        df_zona = df_region[df_region["Zona"] == zona_sel]
    else:
        df_zona = df_region.copy()

    sucursales = ["Todas"] + sorted(df_zona["Sucursal"].dropna().unique().tolist())
    sucursal_sel = st.sidebar.selectbox("Sucursal", sucursales, index=0)

    # Aplicar filtro final
    df_filt = df_zona.copy()
    if sucursal_sel != "Todas":
        df_filt = df_filt[df_filt["Sucursal"] == sucursal_sel]

    st.sidebar.markdown("---")
    st.sidebar.caption(
        "💡 Tip: este tablero está optimizado para agrupar y comparar sucursales "
        "por Región, Zona y Sucursal usando las métricas clave de riesgo."
    )

    return df_filt, region_sel, zona_sel, sucursal_sel

# -------------------------------------------------------------------
# CÁLCULO DE MÉTRICAS PRINCIPALES
# -------------------------------------------------------------------
def compute_kpis(df: pd.DataFrame) -> dict:
    if df.empty:
        return {}

    # columnas que usaremos
    col_capital = "Capital Dispersado Actual"
    col_crec_saldo = "Crecimiento Saldo Actual"
    col_morosidad = "Morosidad Temprana Actual"
    col_fpd = "% FPD Actual"
    col_ratio_vencida = "Ratio_Cartera_Vencida Actual"
    col_saldo_vencido = "Saldo Insoluto Vencido Actual"

    result = {
        "capital_total": df[col_capital].sum(skipna=True),
        "crec_saldo_prom": df[col_crec_saldo].mean(skipna=True),
        "morosidad_prom": df[col_morosidad].mean(skipna=True),
        "fpd_prom": df[col_fpd].mean(skipna=True),
        "ratio_vencida_prom": df[col_ratio_vencida].mean(skipna=True),
        "saldo_vencido_total": df[col_saldo_vencido].sum(skipna=True),
        "num_sucursales": df["Sucursal"].nunique(),
    }

    return result

def compute_cluster_scores(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula z_0, z_1, z_2 y las probabilidades para cada sucursal,
    y asigna el cluster con mayor probabilidad.
    """

    if df.empty:
        return df

    required_cols = [
        "Capital Dispersado Actual",
        "Morosidad Temprana Actual",
        "% FPD Actual",
        "ICV",
        "Saldo Insoluto Vencido Actual",
        "Ratio_Cartera_Vencida Actual",
        "Crecimiento Saldo Actual",
    ]

    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        st.error(
            "Faltan columnas necesarias para el cálculo de clusters ML: "
            + ", ".join(missing)
        )
        return pd.DataFrame()

    df_scored = df.copy()

    # Asegurar que son numéricas
    for c in required_cols:
        df_scored[c] = pd.to_numeric(df_scored[c], errors="coerce").fillna(0.0)

    cap   = df_scored["Capital Dispersado Actual"].values
    mor   = df_scored["Morosidad Temprana Actual"].values
    fpd   = df_scored["% FPD Actual"].values
    icv   = df_scored["ICV"].values
    saldo = df_scored["Saldo Insoluto Vencido Actual"].values
    ratio = df_scored["Ratio_Cartera_Vencida Actual"].values
    crec  = df_scored["Crecimiento Saldo Actual"].values

    # ---- z-scores según tus fórmulas ----
    z0 = (
        -0.049651
        + (-0.000011 * cap)
        + (0.246301 * mor)
        + (0.068909 * fpd)
        + (0.043039 * icv)
        + (0.000006 * saldo)
        + (0.008315 * ratio)
        + (-0.356566 * crec)
    )

    z1 = (
        -0.497694
        + (0.000005 * cap)
        + (-0.012713 * mor)
        + (-0.151820 * fpd)
        + (-0.045727 * icv)
        + (-0.000001 * saldo)
        + (-0.316812 * ratio)
        + (0.071495 * crec)
    )

    z2 = (
        0.547347
        + (0.000006 * cap)
        + (-0.233585 * mor)
        + (0.082910 * fpd)
        + (0.002688 * icv)
        + (-0.000005 * saldo)
        + (0.308495 * ratio)
        + (0.285076 * crec)
    )

    Z = np.vstack([z0, z1, z2]).T  # shape (n, 3)

    # Softmax para probabilidades
    Z_shift = Z - Z.max(axis=1, keepdims=True)  # estabilidad numérica
    expZ = np.exp(Z_shift)
    probs = expZ / expZ.sum(axis=1, keepdims=True)

    df_scored["p_0_0"]   = probs[:, 0]
    df_scored["p_0_1"]   = probs[:, 1]
    df_scored["p_Main1"] = probs[:, 2]

    labels = np.array(["0_0", "0_1", "Main_1"])
    df_scored["Cluster_ML"] = labels[probs.argmax(axis=1)]

    return df_scored


# -------------------------------------------------------------------
# COMPONENTE: TARJETAS KPI
# -------------------------------------------------------------------
def render_kpi_cards(kpis: dict):
    if not kpis:
        st.info("No hay datos para el filtro seleccionado.")
        return

    # Contexto arriba de las tarjetas
    st.markdown(
        f"""
        <div class="context-pill">
            <span>Resumen de cartera</span>
            <span class="context-strong">{kpis["num_sucursales"]} sucursales</span>
            <span>incluidas en la vista actual</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Grid de tarjetas
    st.markdown('<div class="kpi-grid">', unsafe_allow_html=True)

    # 1) Capital Dispersado
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Capital dispersado actual</div>
            <div class="kpi-value">{format_currency(kpis["capital_total"])}</div>
            <div class="kpi-caption">
                Suma de capital vivo en las sucursales filtradas.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 2) Crecimiento de saldo
    crec = kpis["crec_saldo_prom"]
    trend_class = "kpi-trend" if crec >= 0 else "kpi-trend bad"
    trend_icon = "▲" if crec >= 0 else "▼"
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Crecimiento saldo actual</div>
            <div class="kpi-value">{format_percent(crec)}</div>
            <div class="{trend_class}">
                <span>{trend_icon}</span>
                <span>vs histórico promedio</span>
            </div>
            <div class="kpi-caption">
                Variación relativa del saldo insoluto respecto a los últimos 12 meses.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 3) Morosidad temprana
    mor = kpis["morosidad_prom"]
    trend_class = "kpi-trend bad" if mor > 0.06 else "kpi-trend"
    trend_icon = "⚠️" if mor > 0.06 else "✅"
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">% Morosidad temprana</div>
            <div class="kpi-value">{format_percent(mor)}</div>
            <div class="{trend_class}">
                <span>{trend_icon}</span>
                <span>Nivel promedio de atraso 30-89 días</span>
            </div>
            <div class="kpi-caption">
                Porcentaje de cartera con atraso inicial en las sucursales seleccionadas.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 4) % FPD
    fpd = kpis["fpd_prom"]
    trend_class = "kpi-trend bad" if fpd > 0.08 else "kpi-trend"
    trend_icon = "⚠️" if fpd > 0.08 else "✅"
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">% FPD actual</div>
            <div class="kpi-value">{format_percent(fpd)}</div>
            <div class="{trend_class}">
                <span>{trend_icon}</span>
                <span>Colocación con atraso en primer pago</span>
            </div>
            <div class="kpi-caption">
                Medida de calidad de originación reciente en el segmento filtrado.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 5) Ratio cartera vencida
    ratio = kpis["ratio_vencida_prom"]
    trend_class = "kpi-trend bad" if ratio > 0.12 else "kpi-trend"
    trend_icon = "⚠️" if ratio > 0.12 else "✅"
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Ratio cartera vencida</div>
            <div class="kpi-value">{format_percent(ratio)}</div>
            <div class="{trend_class}">
                <span>{trend_icon}</span>
                <span>Saldo vencido / saldo total</span>
            </div>
            <div class="kpi-caption">
                Indicador clave de riesgo estructural en la cartera.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 6) Saldo insoluto vencido
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Saldo insoluto vencido</div>
            <div class="kpi-value">{format_currency(kpis["saldo_vencido_total"])}</div>
            <div class="kpi-caption">
                Suma de saldo vencido (todas las buckets) en el segmento actual.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)  # cierra grid


# -------------------------------------------------------------------
# COMPONENTE: GRÁFICO “TOP SUCURSALES EN RIESGO”
# -------------------------------------------------------------------
def render_risk_chart(df: pd.DataFrame):
    if df.empty:
        return

    # Top 8 sucursales por Saldo Insoluto Vencido Actual
    col_vencido = "Saldo Insoluto Vencido Actual"
    tmp = (
        df.groupby("Sucursal", as_index=False)[col_vencido]
        .sum()
        .sort_values(col_vencido, ascending=False)
        .head(8)
    )

    fig = px.bar(
        tmp,
        x="Sucursal",
        y=col_vencido,
        text=col_vencido,
    )
    fig.update_traces(
        marker_color=DIMEX_COLORS["primary"],
        marker_line_width=0,
        texttemplate="%{text:.2s}",
        hovertemplate="<b>%{x}</b><br>Saldo vencido: $%{y:,.0f}<extra></extra>",
    )
    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        yaxis_title="Saldo insoluto vencido (MXN)",
        xaxis_title="Sucursal",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="chart-title">Top sucursales por saldo vencido</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="chart-caption">Ayuda a priorizar gestión de cobranza en sucursales críticas.</div>',
        unsafe_allow_html=True,
    )
    st.plotly_chart(fig, width='content')
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------------------
# TABLA DE MÉTRICAS POR SEGMENTO (REGIÓN / ZONA / SUCURSAL)
# -------------------------------------------------------------------
def render_metrics_tab(df: pd.DataFrame):
    st.markdown("### 📑 Tabla de métricas por segmento")

    if df.empty:
        st.info("No hay datos para mostrar con el filtro actual.")
        return

    # Nivel de agregación elegido por el usuario
    nivel = st.radio(
        "Nivel de agregación",
        ["Región", "Zona", "Sucursal"],
        horizontal=True,
        key="nivel_tabla_metricas",
    )

    if nivel == "Región":
        group_cols = ["Región"]
    elif nivel == "Zona":
        group_cols = ["Región", "Zona"]
    else:  # "Sucursal"
        group_cols = ["Región", "Zona", "Sucursal"]

    # Agregación: sumas vs promedios
    agg = (
        df.groupby(group_cols)
        .agg(
            capital_disper=("Capital Dispersado Actual", "sum"),
            saldo_vencido=("Saldo Insoluto Vencido Actual", "sum"),
            morosidad=("Morosidad Temprana Actual", "mean"),
            fpd=("% FPD Actual", "mean"),
            icv=("ICV", "mean"),
            ratio_vencida=("Ratio_Cartera_Vencida Actual", "mean"),
            crec_saldo=("Crecimiento Saldo Actual", "mean"),
            n_suc=("Sucursal", "nunique"),
        )
        .reset_index()
    )

    # Pasar ratios a porcentaje (0–100) con 1 decimal
    perc_cols = ["morosidad", "fpd", "icv", "ratio_vencida", "crec_saldo"]
    agg[perc_cols] = agg[perc_cols].apply(lambda s: (s * 100).round(1))

    st.dataframe(agg, use_container_width=True)

# Vista para lo de ML"
def render_cluster_tab(df: pd.DataFrame):
    st.markdown("### 🧠 Score de riesgo por sucursal (modelo ML)")

    if df.empty:
        st.info("No hay datos para calcular los clusters ML con el filtro actual.")
        return

    df_scored = compute_cluster_scores(df)
    if df_scored.empty:
        return

    # Selector de sucursales
    sucursales_opts = sorted(df_scored["Sucursal"].dropna().unique().tolist())
    seleccionadas = st.multiselect(
        "Selecciona una o varias sucursales para revisar su cluster:",
        options=sucursales_opts,
        default=sucursales_opts,      # 👉 ahora, por defecto, TODAS las sucursales filtradas
    )

    if seleccionadas:
        df_view = df_scored[df_scored["Sucursal"].isin(seleccionadas)].copy()
    else:
        df_view = df_scored.copy()

    # ---------- Tarjetas resumen por cluster ----------
    cluster_counts = (
        df_view["Cluster_ML"]
        .value_counts()
        .reindex(["0_0", "0_1", "Main_1"])
        .fillna(0)
        .astype(int)
    )

    # OJO: el HTML va SIN espacios al inicio, pegado a la izquierda
    kpi_html = f"""<div class="kpi-grid">
<div class="kpi-card">
    <div class="kpi-label">Cluster 0_0</div>
    <div class="kpi-value">{cluster_counts["0_0"]}</div>
    <div class="kpi-caption">
        Sucursales consolidadas / menor riesgo relativo.
    </div>
</div>

<div class="kpi-card">
    <div class="kpi-label">Cluster 0_1</div>
    <div class="kpi-value">{cluster_counts["0_1"]}</div>
    <div class="kpi-caption">
        Sucursales en riesgo / cartera más tensa.
    </div>
</div>

<div class="kpi-card">
    <div class="kpi-label">Cluster Main_1</div>
    <div class="kpi-value">{cluster_counts["Main_1"]}</div>
    <div class="kpi-caption">
        Sucursales con potencial de crecimiento controlado.
    </div>
</div>
</div>"""

    st.markdown(kpi_html, unsafe_allow_html=True)

    # ---------- Banner bonito para UNA sola sucursal ----------
    if len(seleccionadas) == 1 and not df_view.empty:
        suc = seleccionadas[0]
        cluster = df_view.iloc[0]["Cluster_ML"]

        banner_html = f"""<div class="cluster-alert">
<span class="cluster-alert-icon">📌</span>
La sucursal <span class="cluster-alert-branch">{suc}</span>
se clasifica en el cluster
<span class="cluster-alert-cluster">{cluster}</span>
según el modelo ML.
</div>"""

        st.markdown(banner_html, unsafe_allow_html=True)

    # ---------- Tabla de detalle ----------
    df_table = df_view[
        [
            "Región",
            "Zona",
            "Sucursal",
            "Cluster_ML",
            "p_0_0",
            "p_0_1",
            "p_Main1",
        ]
    ].copy()

    df_table["p_0_0"] = (df_table["p_0_0"] * 100).round(1)
    df_table["p_0_1"] = (df_table["p_0_1"] * 100).round(1)
    df_table["p_Main1"] = (df_table["p_Main1"] * 100).round(1)

    df_table = df_table.rename(
        columns={
            "Cluster_ML": "Cluster asignado",
            "p_0_0": "% Prob. 0_0",
            "p_0_1": "% Prob. 0_1",
            "p_Main1": "% Prob. Main_1",
        }
    )

    st.markdown("#### 📋 Detalle de sucursales y probabilidad por cluster")
    st.dataframe(
        df_table,
        use_container_width=True,
    )

# -------------------------------------------------------------------
# LAYOUT PRINCIPAL
# -------------------------------------------------------------------
def main():
    # Encabezado tipo Dimex (lo dejamos igual)
    col_left, col_right = st.columns([3, 1], gap="large")

    with col_left:
        st.markdown(
            """
            <div class="dimex-header">
                <div class="dimex-title-block">
                    <div class="dimex-title">Dimex Intelligence Board</div>
                    <div class="dimex-subtitle">
                        Visibilidad ejecutiva de cartera por región, zona y sucursal.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_right:
        st.markdown(
            """
            <div class="dimex-header" style="justify-content:flex-end;">
                <div class="dimex-badge">
                    BETA · Riesgo & Originación
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Filtros (sidebar) y datos filtrados
    df_filtered, region_sel, zona_sel, sucursal_sel = build_filters(
        get_default_dataframe()
    )

    if df_filtered is None or df_filtered.empty:
        st.info("Carga una base y/o ajusta los filtros para ver información.")
        st.stop()

    # Tabs principales del dashboard
    tab_resumen, tab_ml, tab_table = st.tabs(
        [
            "📊 Resumen cartera",
            "🧠 Clusters ML por sucursal",
            "📑 Tabla detallada",
        ]
    )

    # ---------- TAB 1: Resumen cartera ----------
    with tab_resumen:
        with st.container():
            kpis = compute_kpis(df_filtered)
            render_kpi_cards(kpis)

            # Subtítulo contextual pequeño
            region_txt = region_sel if region_sel != "Todas" else "todas las regiones"
            zona_txt = zona_sel if zona_sel != "Todas" else "todas las zonas"
            suc_txt = (
                sucursal_sel if sucursal_sel != "Todas" else "todas las sucursales"
            )

            st.caption(
                f"Vista actual: **{region_txt}** · **{zona_txt}** · **{suc_txt}** "
                f"— datos agregados directamente de la base de sucursales."
            )

            render_risk_chart(df_filtered)

    # ---------- TAB 2: Clusters ML ----------
    with tab_ml:
        render_cluster_tab(df_filtered)

    # ---------- TAB 3: Tabla detallada ----------
    with tab_table:
        render_metrics_tab(df_filtered)

if __name__ == "__main__":
    main()
