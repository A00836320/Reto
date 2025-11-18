import pandas as pd
import plotly.express as px
import streamlit as st

from styles_dimex import DIMEX_COLORS
from metrics_dimex import format_currency, format_percent


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
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


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
