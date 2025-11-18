import streamlit as st

from data_dimex import build_filters
from metrics_dimex import compute_kpis
from components_dimex import render_kpi_cards, render_risk_chart, render_metrics_tab
from ml_clusters_dimex import render_cluster_tab


def render_admin_dashboard():
    # Filtros (sidebar) y datos filtrados
    df_filtered, region_sel, zona_sel, sucursal_sel = build_filters()

    if df_filtered is None or df_filtered.empty:
        st.info("Carga una base y/o ajusta los filtros para ver información.")
        return

    # Tabs principales del dashboard
    tab_resumen, tab_ml, tab_table = st.tabs(
        [
            "📊 Resumen cartera",
            "🧠 Clusters ML por sucursal",
            "📑 Tabla detallada",
        ]
    )

    # TAB 1: Resumen cartera
    with tab_resumen:
        with st.container():
            kpis = compute_kpis(df_filtered)
            render_kpi_cards(kpis)

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

    # TAB 2: Clusters ML
    with tab_ml:
        render_cluster_tab(df_filtered)

    # TAB 3: Tabla detallada
    with tab_table:
        render_metrics_tab(df_filtered)


def render_employee_dashboard():
    st.markdown("### 👷 Vista empleado")

    st.write(
        "Carga tu archivo para continuar. "
        "La visualización estará disponible más adelante."
    )

    archivo = st.file_uploader(
        "Subir archivo de sucursales (Excel o CSV)",
        type=["xlsx", "csv"],
        help="Selecciona el archivo que te hayan proporcionado."
    )

    if archivo is not None:
        st.success(
            "✅ Archivo cargado correctamente. "
            "El panel para empleados estará disponible próximamente."
        )
        # Por ahora NO hacemos nada con el archivo.
