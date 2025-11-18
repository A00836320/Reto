import streamlit as st
from pathlib import Path
from PIL import Image

from styles_dimex import inject_css
from auth_dimex import show_login
from dashboards_dimex import render_admin_dashboard, render_employee_dashboard


# -------------------------------------------------------------------
# CONFIGURACIÓN BÁSICA
# -------------------------------------------------------------------
BASE_DIR = Path(__file__).parent
logo_path = BASE_DIR / "Logo-dimex111.png"
logo = Image.open(logo_path)

st.set_page_config(
    page_title="Dimex | Tablero de Sucursales",
    page_icon=logo,
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inyectar estilos globales
inject_css()


# -------------------------------------------------------------------
# LAYOUT PRINCIPAL CON LOGIN Y ROLES
# -------------------------------------------------------------------
def main():
    # 1. Encabezado
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

    # 2. Inicializar session_state
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
        st.session_state["user"] = None
        st.session_state["role"] = None

    # 3. Si NO está logueado → mostrar login
    if not st.session_state["logged_in"]:
        show_login()
        return

    # 4. Si SÍ está logueado → botón de logout
    col_user, col_logout = st.columns([4, 1])
    with col_user:
        st.caption(
            f"👤 Usuario: **{st.session_state['user']}** · "
            f"Rol: **{st.session_state['role']}**"
        )
    with col_logout:
        if st.button("Cerrar sesión", key="logout_button"):
            for k in ["logged_in", "user", "role"]:
                st.session_state.pop(k, None)
            st.rerun()

    # 5. Dashboard según rol
    if st.session_state["role"] == "Administrador":
        render_admin_dashboard()
    else:
        render_employee_dashboard()


if __name__ == "__main__":
    main()
