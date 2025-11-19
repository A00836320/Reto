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
                Variación relativa del saldo insoluto respecto al último mes.
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

# =========================
# VISTA PARA EMPLEADOS
# =========================

# Mapeo simple de descripción de clusters para sucursales
CLUSTER_EMPLOYEE_TEXT = {
    "0_1": {
        "title": "⚠️ Sucursal en alerta (Cluster 0_1 · Cartera en riesgo)",
        "summary": (
            "Presenta indicadores de morosidad y FPD por arriba del promedio. "
            "La prioridad es contener el riesgo y reforzar la cobranza."
        ),
        "bullets": [
            "Revisar diariamente la lista de créditos en atraso y priorizar los mayores saldos.",
            "Contactar primero a clientes con FPD reciente (0–30 días) para evitar que escalen a mora dura.",
            "Reforzar políticas de originación: reducir montos y plazos para nuevos créditos de alto riesgo.",
        ],
    },
    "Main_1": {
        "title": "📈 Potencial de crecimiento (Main_1 · Riesgo medio)",
        "summary": (
            "La sucursal tiene una cartera con riesgo controlado y espacio para crecer. "
            "Se pueden impulsar colocaciones cuidando la calidad."
        ),
        "bullets": [
            "Identificar clientes con buen comportamiento para ofrecer incrementos de línea o nuevos productos.",
            "Monitorear semanalmente indicadores de morosidad y FPD para no salir del rango objetivo.",
            "Coordinarse con originación para campañas específicas en segmentos de menor riesgo.",
        ],
    },
    "0_0": {
        "title": "✅ Sucursal consolidada (0_0 · Menor riesgo relativo)",
        "summary": (
            "La sucursal muestra buen control de riesgo y cartera sana. "
            "Es un referente para compartir buenas prácticas."
        ),
        "bullets": [
            "Documentar prácticas exitosas de cobranza y originación para replicarlas en otras sucursales.",
            "Mantener seguimiento preventivo a cuentas con primeros días de atraso.",
            "Explorar crecimiento en clientes similares al perfil actual de buena cartera.",
        ],
    },
}


def render_cluster_badge(cluster_label: str):
    """
    Muestra una tarjetita con el cluster de la sucursal y su resumen.
    """
    info = CLUSTER_EMPLOYEE_TEXT.get(cluster_label)

    if info is None:
        st.info(f"Cluster asignado a la sucursal: **{cluster_label}**")
        return

    st.markdown(
        f"""
        <div class="kpi-grid">
          <div class="kpi-card" style="border-left: 4px solid {DIMEX_COLORS['primary']};">
            <div class="kpi-label">Cluster sucursal</div>
            <div class="kpi-value">{info['title']}</div>
            <div class="kpi-caption">{info['summary']}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_employee_risk_charts(df_suc):
    """
    Gráficas sencillas e interactivas para que el empleado vea
    el perfil de riesgo de su sucursal.
    Espera un DataFrame filtrado a UNA sola sucursal.
    """
    if df_suc is None or df_suc.empty:
        st.info("No hay información para la sucursal seleccionada.")
        return

    row = df_suc.iloc[0]

    capital = row.get("Capital Dispersado Actual")
    saldo_vencido = row.get("Saldo Insoluto Vencido Actual")
    morosidad = row.get("Morosidad Temprana Actual")
    fpd = row.get("% FPD Actual")
    ratio = row.get("Ratio_Cartera_Vencida Actual")

    st.markdown("### 📊 Comportamiento de la sucursal")

    col1, col2 = st.columns(2)

    # Gráfica 1: capital vs saldo vencido
    with col1:
        data_montos = pd.DataFrame(
            {
                "Concepto": ["Capital dispersado", "Saldo vencido"],
                "Monto": [capital, saldo_vencido],
            }
        )
        fig1 = px.bar(
            data_montos,
            x="Concepto",
            y="Monto",
            title="Capital vs saldo vencido",
            labels={"Monto": "Monto (MXN)"},
        )
        fig1.update_layout(margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig1, use_container_width=True)

    # Gráfica 2: morosidad, FPD y ratio
    with col2:
        data_riesgo = pd.DataFrame(
            {
                "Indicador": ["Morosidad temprana", "FPD", "Ratio cartera vencida"],
                "Valor": [morosidad, fpd, ratio],
            }
        )
        fig2 = px.bar(
            data_riesgo,
            x="Indicador",
            y="Valor",
            title="Indicadores clave de riesgo",
            labels={"Valor": "Porcentaje"},
        )
        fig2.update_layout(margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig2, use_container_width=True)


def render_branch_recommendations(cluster_label: str):
    """
    Lista de recomendaciones operativas dependiendo del cluster.
    """
    info = CLUSTER_EMPLOYEE_TEXT.get(cluster_label)

    st.markdown("### 🧭 Recomendaciones para la sucursal")

    if info is None:
        st.write(
            "Por ahora no hay recomendaciones específicas para este cluster. "
            "Consulta con el área de Riesgos para lineamientos adicionales."
        )
        return

    st.markdown(f"**{info['summary']}**")

    for bullet in info["bullets"]:
        st.markdown(f"- {bullet}")
