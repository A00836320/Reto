import pandas as pd
import plotly.express as px
import streamlit as st

from styles_dimex import DIMEX_COLORS
from metrics_dimex import format_currency, format_percent

def render_kpi_cards(kpis: dict):
    if not kpis:
        st.info("No hay datos para el filtro seleccionado.")
        return

    # ---------------- CSS propio (no choca con nada global) ----------------
    st.markdown(
        """
        <style>
        .kpi-mini-card {
            background: rgba(255,255,255,0.96);
            padding: 0.65rem 0.9rem 0.7rem 0.9rem;
            border-radius: 14px;
            border: 1px solid rgba(148,163,184,0.22);
            box-shadow:
                0 6px 16px rgba(15,23,42,0.05),
                0 0 0 1px rgba(148,163,184,0.10);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            min-height: 88px;    /* recortadas */
            transition: transform 0.12s ease, box-shadow 0.12s ease;
        }
        .kpi-mini-card:hover {
            transform: translateY(-1px);
            box-shadow:
                0 10px 24px rgba(15,23,42,0.10),
                0 0 0 1px rgba(148,163,184,0.22);
        }

        .kpi-mini-label {
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 700;
            color: #64748b;
            margin-bottom: 0.15rem;
        }
        .kpi-mini-value {
            font-size: 1.35rem;
            font-weight: 800;
            color: #0f172a;
            letter-spacing: -0.02em;
            margin-bottom: 0.2rem;
        }
        .kpi-mini-caption {
            font-size: 0.72rem;
            color: #6b7280;
            margin-top: 0.05rem;
        }

        .kpi-mini-trend {
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
            padding: 0.12rem 0.5rem;
            border-radius: 999px;
            font-size: 0.7rem;
            font-weight: 500;
            background: rgba(34,197,94,0.08);
            color: #15803d;
            border: 1px solid rgba(34,197,94,0.28);
        }
        .kpi-mini-trend.bad {
            background: rgba(248,113,113,0.12);
            color: #b91c1c;
            border-color: rgba(248,113,113,0.5);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # -------- Contexto arriba (igual que antes) --------
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

    # ====== FILA 1: 3 KPIs ======
    row1 = st.columns(3)

    # 1) Capital dispersado
    with row1[0]:
        st.markdown(
            f"""
            <div class="kpi-mini-card">
                <div>
                    <div class="kpi-mini-label">Capital dispersado actual</div>
                    <div class="kpi-mini-value">{format_currency(kpis["capital_total"])}</div>
                </div>
                <div class="kpi-mini-caption">
                    Suma de capital vivo en las sucursales filtradas.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 2) Crecimiento saldo
    crec = kpis["crec_saldo_prom"]
    trend_class = "kpi-mini-trend" if crec >= 0 else "kpi-mini-trend bad"
    trend_icon = "▲" if crec >= 0 else "▼"
    with row1[1]:
        st.markdown(
            f"""
            <div class="kpi-mini-card">
                <div>
                    <div class="kpi-mini-label">Crecimiento saldo actual</div>
                    <div class="kpi-mini-value">{format_percent(crec)}</div>
                    <div class="{trend_class}">
                        <span>{trend_icon}</span>
                        <span>vs histórico promedio</span>
                    </div>
                </div>
                <div class="kpi-mini-caption">
                    Variación del saldo insoluto vs último mes.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 3) Morosidad temprana
    mor = kpis["morosidad_prom"]
    trend_class = "kpi-mini-trend bad" if mor > 0.06 else "kpi-mini-trend"
    trend_icon = "⚠️" if mor > 0.06 else "✅"
    with row1[2]:
        st.markdown(
            f"""
            <div class="kpi-mini-card">
                <div>
                    <div class="kpi-mini-label">% Morosidad temprana</div>
                    <div class="kpi-mini-value">{format_percent(mor)}</div>
                    <div class="{trend_class}">
                        <span>{trend_icon}</span>
                        <span>30–89 días de atraso</span>
                    </div>
                </div>
                <div class="kpi-mini-caption">
                    Porcentaje de cartera con atraso inicial.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ====== FILA 2: otros 3 KPIs ======
    row2 = st.columns(3)

    # 4) % FPD
    fpd = kpis["fpd_prom"]
    trend_class = "kpi-mini-trend bad" if fpd > 0.08 else "kpi-mini-trend"
    trend_icon = "⚠️" if fpd > 0.08 else "✅"
    with row2[0]:
        st.markdown(
            f"""
            <div class="kpi-mini-card">
                <div>
                    <div class="kpi-mini-label">% FPD actual</div>
                    <div class="kpi-mini-value">{format_percent(fpd)}</div>
                    <div class="{trend_class}">
                        <span>{trend_icon}</span>
                        <span>Colocación con atraso</span>
                    </div>
                </div>
                <div class="kpi-mini-caption">
                    Calidad de originación reciente en el segmento filtrado.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 5) Ratio cartera vencida
    ratio = kpis["ratio_vencida_prom"]
    trend_class = "kpi-mini-trend bad" if ratio > 0.12 else "kpi-mini-trend"
    trend_icon = "⚠️" if ratio > 0.12 else "✅"
    with row2[1]:
        st.markdown(
            f"""
            <div class="kpi-mini-card">
                <div>
                    <div class="kpi-mini-label">Ratio cartera vencida</div>
                    <div class="kpi-mini-value">{format_percent(ratio)}</div>
                    <div class="{trend_class}">
                        <span>{trend_icon}</span>
                        <span>Saldo vencido / saldo total</span>
                    </div>
                </div>
                <div class="kpi-mini-caption">
                    Indicador de riesgo estructural en la cartera.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 6) Saldo insoluto vencido
    with row2[2]:
        st.markdown(
            f"""
            <div class="kpi-mini-card">
                <div>
                    <div class="kpi-mini-label">Saldo insoluto vencido</div>
                    <div class="kpi-mini-value">{format_currency(kpis["saldo_vencido_total"])}</div>
                </div>
                <div class="kpi-mini-caption">
                    Suma de saldo vencido (todas las buckets) en el segmento actual.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_risk_chart(df: pd.DataFrame, top_n: int = 8):
    """
    Top sucursales por saldo vencido, en barras horizontales,
    dentro de la tarjeta de estilo Dimex.
    """
    if df is None or df.empty:
        return

    col_vencido = "Saldo Insoluto Vencido Actual"
    if "Sucursal" not in df.columns or col_vencido not in df.columns:
        st.info("Faltan las columnas 'Sucursal' y/o 'Saldo Insoluto Vencido Actual'.")
        return

    # Top N sucursales por saldo vencido
    tmp = (
        df.groupby("Sucursal", as_index=False)[col_vencido]
        .sum()
        .sort_values(col_vencido, ascending=False)
        .head(top_n)
    )

    # Etiqueta en millones (ej. 7.5M)
    tmp["saldo_millones"] = tmp[col_vencido] / 1_000_000
    tmp["saldo_label"] = tmp["saldo_millones"].map(lambda v: f"{v:,.1f}M")

    # Color Dimex
    try:
        color_seq = [DIMEX_COLORS["primary"]]
    except NameError:
        color_seq = ["#2E7D32"]

    fig = px.bar(
        tmp,
        x=col_vencido,
        y="Sucursal",
        orientation="h",
        text="saldo_label",
        labels={
            col_vencido: "Saldo insoluto vencido (MXN)",
            "Sucursal": "Sucursal",
        },
        color_discrete_sequence=color_seq,
    )

    fig.update_traces(
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Saldo vencido: $%{x:,.0f}<extra></extra>",
        marker_line_width=0,
    )

    fig.update_layout(
        margin=dict(l=10, r=20, t=10, b=10),
        yaxis_title="",
        xaxis_title="Saldo insoluto vencido (MXN)",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(categoryorder="total ascending"),
        xaxis=dict(tickprefix="$", showgrid=True, gridcolor="rgba(0,0,0,0.06)"),
    )

    # ------- Card de estilo Dimex (lo que ya tenías) -------
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
    st.markdown("### Tabla de métricas por segmento")

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
# GRÁFICAS AVANZADAS PARA ADMINISTRADOR
# =========================

def admin_chart_bubble(df: pd.DataFrame):
    """
    Bubble chart: Capital dispersado vs % FPD, tamaño por saldo vencido.
    Si existe 'Cluster_ML' se colorea por cluster, si no, por Región.
    """
    if df is None or df.empty:
        st.info("No hay datos suficientes para la gráfica de burbujas.")
        return

    required = [
        "Sucursal",
        "Región",
        "Zona",
        "Capital Dispersado Actual",
        "% FPD Actual",
        "Saldo Insoluto Vencido Actual",
    ]
    if not all(col in df.columns for col in required):
        st.info(
            "Faltan columnas para la gráfica de burbujas "
            "(Sucursal, Región, Zona, Capital, %FPD, Saldo vencido)."
        )
        return

    agg = (
        df.groupby(["Sucursal", "Región", "Zona"], as_index=False)
        .agg(
            capital=("Capital Dispersado Actual", "sum"),
            fpd=("% FPD Actual", "mean"),
            saldo_vencido=("Saldo Insoluto Vencido Actual", "sum"),
        )
    )

    # Si existe Cluster_ML lo usamos para color, si no, usamos Región
    if "Cluster_ML" in df.columns:
        cluster_map = (
            df.groupby("Sucursal", as_index=False)["Cluster_ML"]
            .first()
            .rename(columns={"Cluster_ML": "cluster"})
        )
        agg = agg.merge(cluster_map, on="Sucursal", how="left")
        color_col = "cluster"
    else:
        color_col = "Región"

    st.markdown("### 🌐 Capital vs %FPD (tamaño = saldo vencido)")

    fig = px.scatter(
        agg,
        x="capital",
        y="fpd",
        size="saldo_vencido",
        color=color_col,
        hover_name="Sucursal",
        hover_data={
            "Región": True,
            "Zona": True,
            "capital": ":,.0f",
            "fpd": ":.2%",
            "saldo_vencido": ":,.0f",
        },
        title="Sucursales: Capital vs %FPD (tamaño = Saldo vencido)",
        size_max=40,
    )
    fig.update_layout(margin=dict(l=10, r=10, t=50, b=10))
    st.plotly_chart(fig, use_container_width=True)


def admin_chart_heatmap(df: pd.DataFrame):
    """
    Heatmap Región–Zona por %FPD promedio.
    Vista ejecutiva con título externo, hover limpio y color verde.
    """
    if df is None or df.empty:
        st.info("No hay datos suficientes para el mapa de calor.")
        return

    required = ["Región", "Zona", "% FPD Actual"]
    if not all(col in df.columns for col in required):
        st.info("Faltan columnas para el mapa de calor (Región, Zona, % FPD Actual).")
        return

    # Agregación por zona y región
    tmp = (
        df.groupby(["Región", "Zona"], as_index=False)["% FPD Actual"]
        .mean()
        .rename(columns={"% FPD Actual": "fpd_prom"})
    )

    if tmp.empty:
        st.info("No se pudieron generar datos agregados para el mapa de calor.")
        return

    # Pivot
    pivot = tmp.pivot(index="Región", columns="Zona", values="fpd_prom")

    # ---- Título elegante fuera de la figura ----
    st.markdown("### 🌿 % FPD promedio por Región y Zona")
    st.caption("Permite identificar zonas con comportamiento de riesgo elevado.")

    # ---- Gráfica ----
    fig = px.imshow(
        pivot,
        labels=dict(x="Zona", y="Región", color="% FPD"),
        aspect="auto",
        color_continuous_scale="Greens",   # << VERDE
    )

    # ---- Hover bonito ----
    fig.update_traces(
        hovertemplate="<b>Región:</b> %{y}<br>"
                      "<b>Zona:</b> %{x}<br>"
                      "<b>% FPD:</b> %{z:.2%}<extra></extra>"
    )

    # ---- Estilos y márgenes ----
    fig.update_layout(
        margin=dict(l=40, r=40, t=10, b=60),
        xaxis=dict(
            tickangle=40,
            tickfont=dict(size=10),
        ),
        yaxis=dict(
            tickfont=dict(size=11),
        ),
        coloraxis_colorbar=dict(
            title="% FPD",
            tickformat=".0%",
            thickness=12,
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(fig, use_container_width=True)


def admin_chart_rankings(df: pd.DataFrame):
    """
    3 rankings de sucursales:
    - Top 15 por saldo vencido
    - Top 15 por %FPD
    - Top 15 por morosidad temprana

    Ahora con barras horizontales, colores verdes desvanecidos y estilo ejecutivo.
    """

    if df is None or df.empty:
        return

    st.markdown("### 🏆 Rankings de sucursales (riesgo)")

    col1, col2, col3 = st.columns(3, gap="large")

    # --------- PALETA VERDE DESVANECIDA ---------
    gradient_green = [
        "#d9f2e6",  # muy claro
        "#a5e1c5",
        "#6bcc97",
        "#3aad6b",
        "#1f8a4a"   # más oscuro
    ]

    # ----------------- 1) Saldo vencido -----------------
    with col1:
        st.markdown("#### Top 15 por saldo vencido")

        if "Saldo Insoluto Vencido Actual" in df.columns:
            tmp = (
                df.groupby("Sucursal", as_index=False)["Saldo Insoluto Vencido Actual"]
                .sum()
                .sort_values("Saldo Insoluto Vencido Actual", ascending=False)
                .head(15)
            )

            fig1 = px.bar(
                tmp,
                x="Saldo Insoluto Vencido Actual",
                y="Sucursal",
                orientation="h",
                color="Saldo Insoluto Vencido Actual",
                color_continuous_scale=gradient_green,
                labels={"Saldo Insoluto Vencido Actual": "Saldo vencido (MXN)"},
            )

            fig1.update_traces(
                hovertemplate="<b>%{y}</b><br>Saldo vencido: $%{x:,.0f}<extra></extra>"
            )
            fig1.update_layout(
                margin=dict(l=0, r=0, t=10, b=10),
                xaxis_title="Saldo vencido (MXN)",
                yaxis_title="Sucursal",
                coloraxis_showscale=False,
            )
            st.plotly_chart(fig1, use_container_width=True)

    # ----------------- 2) %FPD -----------------
    with col2:
        st.markdown("#### Top 15 por % FPD")

        if "% FPD Actual" in df.columns:
            tmp = (
                df.groupby("Sucursal", as_index=False)["% FPD Actual"]
                .mean()
                .sort_values("% FPD Actual", ascending=False)
                .head(15)
            )

            fig2 = px.bar(
                tmp,
                x="% FPD Actual",
                y="Sucursal",
                orientation="h",
                color="% FPD Actual",
                color_continuous_scale=gradient_green,
                labels={"% FPD Actual": "% FPD"},
            )

            fig2.update_traces(
                hovertemplate="<b>%{y}</b><br>%FPD: %{x:.2%}<extra></extra>"
            )
            fig2.update_layout(
                margin=dict(l=0, r=0, t=10, b=10),
                xaxis_title="% FPD",
                yaxis_title="Sucursal",
                xaxis_tickformat=".0%",
                coloraxis_showscale=False,
            )
            st.plotly_chart(fig2, use_container_width=True)

    # ----------------- 3) Morosidad temprana -----------------
    with col3:
        st.markdown("#### Top 15 por morosidad temprana")

        if "Morosidad Temprana Actual" in df.columns:
            tmp = (
                df.groupby("Sucursal", as_index=False)["Morosidad Temprana Actual"]
                .mean()
                .sort_values("Morosidad Temprana Actual", ascending=False)
                .head(15)
            )

            fig3 = px.bar(
                tmp,
                x="Morosidad Temprana Actual",
                y="Sucursal",
                orientation="h",
                color="Morosidad Temprana Actual",
                color_continuous_scale=gradient_green,
                labels={"Morosidad Temprana Actual": "Morosidad temprana"},
            )

            fig3.update_traces(
                hovertemplate="<b>%{y}</b><br>Morosidad: %{x:.2f}<extra></extra>"
            )
            fig3.update_layout(
                margin=dict(l=0, r=0, t=10, b=10),
                xaxis_title="Morosidad temprana",
                yaxis_title="Sucursal",
                coloraxis_showscale=False,
            )
            st.plotly_chart(fig3, use_container_width=True)

def admin_chart_clusters(df: pd.DataFrame):
    """
    Distribución de sucursales por cluster.
    Si no existe la columna de cluster, simplemente no se muestra nada.
    """
    if df is None or df.empty:
        return

    # Aceptamos cualquiera de estas dos posibles columnas
    cluster_col = None
    for c in ["Cluster_ML", "Cluster", "Cluster_Riesgo"]:
        if c in df.columns:
            cluster_col = c
            break

    if cluster_col is None:
        # No molestamos al usuario con mensajes, solo salimos
        return

    tmp = (
        df.groupby(cluster_col, as_index=False)["Sucursal"]
        .nunique()
        .rename(columns={"Sucursal": "num_sucursales"})
    )

    st.markdown("### 🧬 Distribución de sucursales por cluster")

    fig = px.bar(
        tmp,
        x=cluster_col,
        y="num_sucursales",
        title="Sucursales por cluster",
        labels={cluster_col: "Cluster", "num_sucursales": "Número de sucursales"},
        text="num_sucursales",
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig, use_container_width=True)


def admin_chart_growth_vs_risk(df: pd.DataFrame):
    """
    Gráfica de Crecimiento de Saldo vs % FPD.
    - Eje X: Crecimiento Saldo Actual (promedio)
    - Eje Y: % FPD Actual (promedio)
    - Color: Cluster si existe, si no Región
    - Hover: bonito con región, crecimiento, FPD, capital y saldo vencido
    """
    if df is None or df.empty:
        return

    required = [
        "Sucursal",
        "Región",
        "Crecimiento Saldo Actual",
        "% FPD Actual",
    ]
    if not all(col in df.columns for col in required):
        st.info(
            "Faltan columnas para la gráfica de Crecimiento vs riesgo "
            "(Sucursal, Región, Crecimiento Saldo Actual, % FPD Actual)."
        )
        return

    # Ver si tenemos capital y saldo vencido para el hover
    has_capital = "Capital Dispersado Actual" in df.columns
    has_saldo_vencido = "Saldo Insoluto Vencido Actual" in df.columns

    agg = (
        df.groupby("Sucursal", as_index=False)
        .agg(
            crec_saldo=("Crecimiento Saldo Actual", "mean"),
            fpd=("% FPD Actual", "mean"),
            region=("Región", "first"),
            **(
                {"capital": ("Capital Dispersado Actual", "sum")}
                if has_capital
                else {}
            ),
            **(
                {"saldo_vencido": ("Saldo Insoluto Vencido Actual", "sum")}
                if has_saldo_vencido
                else {}
            ),
        )
    )

    # Determinar color: cluster si existe, si no Región
    color_col = "region"
    if "Cluster_ML" in df.columns:
        cluster_map = (
            df.groupby("Sucursal", as_index=False)["Cluster_ML"]
            .first()
            .rename(columns={"Cluster_ML": "cluster"})
        )
        agg = agg.merge(cluster_map, on="Sucursal", how="left")
        color_col = "cluster"

    # Definir qué columnas van a custom_data para el hover
    custom_cols = ["region"]
    if has_capital:
        custom_cols.append("capital")
    if has_saldo_vencido:
        custom_cols.append("saldo_vencido")

    fig = px.scatter(
        agg,
        x="crec_saldo",
        y="fpd",
        color=color_col,
        hover_name="Sucursal",
        custom_data=custom_cols,
        title="Crecimiento del saldo vs % FPD por sucursal",
    )

    # Construir hovertemplate bonito según lo que tengamos
    if has_capital and has_saldo_vencido:
        hovertemplate = (
            "<b>%{hovertext}</b><br>"
            "Región: %{customdata[0]}<br>"
            "Crecimiento: %{x:.2%}<br>"
            "FPD: %{y:.2%}<br>"
            "Capital: $%{customdata[1]:,.0f}<br>"
            "Saldo vencido: $%{customdata[2]:,.0f}"
            "<extra></extra>"
        )
    else:
        hovertemplate = (
            "<b>%{hovertext}</b><br>"
            "Región: %{customdata[0]}<br>"
            "Crecimiento: %{x:.2%}<br>"
            "FPD: %{y:.2%}"
            "<extra></extra>"
        )

    fig.update_traces(hovertemplate=hovertemplate)

    fig.update_layout(
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis_title="Crecimiento Saldo (promedio)",
        yaxis_title="% FPD (promedio)",
    )
    st.plotly_chart(fig, use_container_width=True)

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
