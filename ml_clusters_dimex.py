import numpy as np
import pandas as pd
import streamlit as st


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


def render_cluster_tab(df: pd.DataFrame):
    st.markdown("### Score de riesgo por sucursal (modelo ML)")

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
        default=sucursales_opts,      # por defecto, todas las sucursales filtradas
    )

    if seleccionadas:
        df_view = df_scored[df_scored["Sucursal"].isin(seleccionadas)].copy()
    else:
        df_view = df_scored.copy()

    # Tarjetas resumen por cluster
    cluster_counts = (
        df_view["Cluster_ML"]
        .value_counts()
        .reindex(["0_0", "0_1", "Main_1"])
        .fillna(0)
        .astype(int)
    )

    kpi_html = f"""<div class="kpi-grid">
<div class="kpi-card">
    <div class="kpi-label">Sucursales consolidadas / menor riesgo relativo.</div>
    <div class="kpi-value">{cluster_counts["0_0"]}</div>
    <div class="kpi-caption">
        Cluster 0_0
    </div>
</div>

<div class="kpi-card">
    <div class="kpi-label">Sucursales en riesgo / cartera más tensa.</div>
    <div class="kpi-value">{cluster_counts["0_1"]}</div>
    <div class="kpi-caption">
        Cluster 0_1
    </div>
</div>

<div class="kpi-card">
    <div class="kpi-label">Sucursales con potencial de crecimiento controlado.</div>
    <div class="kpi-value">{cluster_counts["Main_1"]}</div>
    <div class="kpi-caption">
        Cluster Main_1
    </div>
</div>
</div>"""

    st.markdown(kpi_html, unsafe_allow_html=True)

    # Banner bonito para UNA sola sucursal
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

    # Tabla de detalle
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

    st.markdown("####  Detalle de sucursales y probabilidad por cluster")
    st.dataframe(
        df_table,
        use_container_width=True,
    )
