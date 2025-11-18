import os
import pandas as pd
import streamlit as st

from typing import Tuple, Optional


@st.cache_data(show_spinner=True)
def load_excel(file) -> pd.DataFrame:
    """Carga un archivo de Excel con cache de Streamlit."""
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


def build_filters() -> Tuple[pd.DataFrame, Optional[str], Optional[str], Optional[str]]:
    """
    Construye los filtros de sidebar (Región, Zona, Sucursal) y regresa:
    df_filtrado, region_sel, zona_sel, sucursal_sel
    """
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
