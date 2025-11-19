import streamlit as st

# USUARIOS Y ROLES (login muy simple por ahora no valida password)
USERS = {
    "admin": "admin",      # usuario: rol
    "empleado": "empleado",
    # ejemplo:
    # "juan": "empleado",
    # "gerente": "admin",
}

# Contraseñas por sucursal (para vista de empleado)
# Usa EXACTAMENTE el mismo nombre de sucursal que viene en el Excel.
# Ejemplo; reemplaza/añade las tuyas reales:
BRANCH_PASSWORDS = {
    # "Nombre de sucursal en el Excel": "contraseña",
    "San Nicolás Valle BIS": "12345",
    "Valle Chalco": "12345",
    "Puente de Tlalne": "12345",
    # Agrega aquí todas las sucursales que quieras habilitar
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
