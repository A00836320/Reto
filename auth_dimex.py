import streamlit as st

# USUARIOS Y ROLES (login muy simple por ahora no valida password)
USERS = {
    "admin": "admin",      # usuario: rol
    "empleado": "empleado",
    # ejemplo:
    # "juan": "empleado",
    # "gerente": "admin",
}


def show_login():
    st.markdown("## 🔐 Inicio de sesión")

    col1, col2 = st.columns(2)

    with col1:
        user = st.text_input("Usuario", key="login_user")

    with col2:
        role = st.selectbox(
            "Tipo de usuario",
            ["Administrador", "Empleado"],
            key="login_role"
        )

    login_btn = st.button("Entrar", key="login_button")

    if login_btn:
        if user.strip() == "":
            st.warning("Escribe un usuario para continuar.")
        else:
            st.session_state["logged_in"] = True
            st.session_state["user"] = user.strip()
            st.session_state["role"] = role
            st.rerun()
