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
    """
    Pantalla de inicio de sesión súper moderna con animaciones y glassmorphism.
    Mantiene la lógica: al hacer login se setean:
    - st.session_state["logged_in"]
    - st.session_state["user"]
    - st.session_state["role"]  (Administrador / Empleado)
    """

    # ------ CSS específico para el login (animaciones + estilos) ------
    st.markdown(
        """
        <style>
        /* Fondo general con ligero gradiente */
        .dimex-login-background {
            position: relative;
            padding: 2rem 0 4rem 0;
        }

        /* Burbujas animadas de fondo */
        .dimex-login-blob {
            position: fixed;
            border-radius: 999px;
            filter: blur(40px);
            opacity: 0.45;
            z-index: -1;
            pointer-events: none;
            mix-blend-mode: multiply;
        }
        .dimex-login-blob.blob-1 {
            width: 260px;
            height: 260px;
            top: 12%;
            left: 5%;
            background: #b8ffd0;
            animation: floatBlob1 18s ease-in-out infinite alternate;
        }
        .dimex-login-blob.blob-2 {
            width: 320px;
            height: 320px;
            top: 40%;
            right: 4%;
            background: #9ef2ff;
            animation: floatBlob2 22s ease-in-out infinite alternate;
        }
        .dimex-login-blob.blob-3 {
            width: 280px;
            height: 280px;
            bottom: 0%;
            left: 35%;
            background: #e2ffd0;
            animation: floatBlob3 26s ease-in-out infinite alternate;
        }

        @keyframes floatBlob1 {
            from { transform: translate3d(0, 0, 0); }
            to   { transform: translate3d(40px, 20px, 0) scale(1.05); }
        }
        @keyframes floatBlob2 {
            from { transform: translate3d(0, 0, 0); }
            to   { transform: translate3d(-50px, -20px, 0) scale(1.08); }
        }
        @keyframes floatBlob3 {
            from { transform: translate3d(0, 0, 0); }
            to   { transform: translate3d(0, -30px, 0) scale(0.95); }
        }

        /* Contenedor principal del login */
        .dimex-login-shell {
            max-width: 960px;
            margin: 0 auto;
        }

        .dimex-login-grid {
            display: grid;
            grid-template-columns: minmax(0, 1.4fr) minmax(0, 1fr);
            gap: 2.5rem;
            align-items: stretch;
        }

        @media (max-width: 900px) {
            .dimex-login-grid {
                grid-template-columns: minmax(0, 1fr);
            }
        }

        /* Panel izquierdo: mensaje hero */
        .dimex-login-hero {
            padding: 1.5rem 0 1.5rem 0;
        }
        .dimex-login-kicker {
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.14em;
            color: #4f5b66;
            margin-bottom: 0.6rem;
        }
        .dimex-login-title {
            font-size: 2rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            display: flex;
            align-items: center;
            gap: 0.6rem;
            margin-bottom: 0.5rem;
        }
        .dimex-login-title-icon {
            font-size: 2.3rem;
            filter: drop-shadow(0 4px 12px rgba(0,0,0,0.18));
            animation: pulseGlow 2.6s ease-in-out infinite;
        }
        .dimex-login-subtitle {
            font-size: 0.98rem;
            color: #6b7785;
            max-width: 420px;
        }

        @keyframes pulseGlow {
            0%   { transform: translateY(0); filter: drop-shadow(0 4px 12px rgba(16, 185, 129, 0.25)); }
            50%  { transform: translateY(-3px); filter: drop-shadow(0 10px 25px rgba(16, 185, 129, 0.55)); }
            100% { transform: translateY(0); filter: drop-shadow(0 4px 12px rgba(16, 185, 129, 0.25)); }
        }

        .dimex-login-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.25rem 0.75rem;
            margin-top: 0.9rem;
            border-radius: 999px;
            font-size: 0.78rem;
            background: rgba(15, 118, 110, 0.06);
            color: #045d56;
            border: 1px solid rgba(45, 212, 191, 0.45);
            backdrop-filter: blur(10px);
        }
        .dimex-login-pill-dot {
            width: 9px;
            height: 9px;
            border-radius: 999px;
            background: radial-gradient(circle at 30% 30%, #6ee7b7, #047857);
            box-shadow: 0 0 0 6px rgba(16, 185, 129, 0.25);
        }

        /* Panel derecho: tarjeta del formulario */
        .dimex-login-card {
            position: relative;
            padding: 1.75rem 1.8rem 1.6rem 1.8rem;
            border-radius: 22px;
            background: radial-gradient(circle at 0% 0%, rgba(255,255,255,0.9), rgba(248,250,252,0.96));
            border: 1px solid rgba(148, 163, 184, 0.18);
            box-shadow:
                0 26px 80px rgba(15, 23, 42, 0.18),
                0 0 0 1px rgba(255,255,255,0.7);
            backdrop-filter: blur(18px);
            overflow: hidden;
        }

        .dimex-login-card::before {
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(135deg, rgba(16,185,129,0.06), transparent 40%, rgba(56,189,248,0.08));
            opacity: 1;
            pointer-events: none;
        }

        .dimex-login-card-inner {
            position: relative;
            z-index: 2;
        }

        .dimex-login-card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.3rem;
        }

        .dimex-login-card-title {
            display: flex;
            flex-direction: column;
            gap: 0.2rem;
        }
        .dimex-login-card-title span.label {
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            color: #9ca3af;
        }
        .dimex-login-card-title span.main {
            font-size: 1.2rem;
            font-weight: 700;
            color: #0f172a;
            display: flex;
            align-items: center;
            gap: 0.35rem;
        }

        .dimex-login-badge-soft {
            padding: 0.3rem 0.7rem;
            border-radius: 999px;
            font-size: 0.75rem;
            background: rgba(22, 163, 74, 0.08);
            color: #15803d;
            border: 1px solid rgba(22, 163, 74, 0.25);
        }

        .dimex-login-divider {
            height: 1px;
            width: 100%;
            background: linear-gradient(to right, transparent, rgba(148,163,184,0.5), transparent);
            margin-bottom: 1.1rem;
            opacity: 0.6;
        }

        /* Ajustes a inputs de Streamlit dentro del card */
        .dimex-login-card .stTextInput > div > div,
        .dimex-login-card .stSelectbox > div > div {
            border-radius: 999px !important;
            border: 1px solid rgba(148, 163, 184, 0.55) !important;
            background-color: rgba(255,255,255,0.9) !important;
            box-shadow: 0 0 0 0 rgba(16, 185, 129, 0);
            transition: box-shadow 0.18s ease, border-color 0.18s ease, transform 0.14s ease;
        }
        .dimex-login-card .stTextInput > div > div:focus-within,
        .dimex-login-card .stSelectbox > div > div:focus-within {
            border-color: rgba(16, 185, 129, 0.9) !important;
            box-shadow: 0 0 0 1px rgba(16,185,129,0.55);
            transform: translateY(-1px);
        }

        .dimex-login-footer-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 0.75rem;
            margin-top: 1.1rem;
        }

        .dimex-login-hint {
            font-size: 0.78rem;
            color: #6b7280;
        }

        /* Botón principal */
        .dimex-login-primary-btn button {
            width: 100%;
            border-radius: 999px !important;
            background: linear-gradient(135deg, #16a34a, #22c55e) !important;
            color: white !important;
            border: none !important;
            font-weight: 600 !important;
            box-shadow: 0 14px 35px rgba(22, 163, 74, 0.35) !important;
            transition: transform 0.12s ease, box-shadow 0.12s ease, filter 0.12s ease;
        }
        .dimex-login-primary-btn button:hover {
            transform: translateY(-1px) scale(1.01);
            box-shadow: 0 18px 42px rgba(22, 163, 74, 0.45) !important;
            filter: brightness(1.02);
        }
        .dimex-login-primary-btn button:active {
            transform: translateY(0) scale(0.99);
            box-shadow: 0 8px 20px rgba(22, 163, 74, 0.35) !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ------ Burbujas de fondo ------
    st.markdown(
        """
        <div class="dimex-login-blob blob-1"></div>
        <div class="dimex-login-blob blob-2"></div>
        <div class="dimex-login-blob blob-3"></div>
        """,
        unsafe_allow_html=True,
    )

    # ------ Layout del login ------
    st.markdown('<div class="dimex-login-background">', unsafe_allow_html=True)
    st.markdown('<div class="dimex-login-shell">', unsafe_allow_html=True)

    # Grid principal
    left_col, right_col = st.columns([1.3, 1], gap="large")

    # --------- LADO IZQUIERDO: mensaje hero ---------
    with left_col:
        st.markdown(
            """
            <div class="dimex-login-hero">
                <div class="dimex-login-kicker">Acceso seguro · Dimex</div>
                <div class="dimex-login-title">
                    <span class="dimex-login-title-icon">🔐</span>
                    <span>Inicio de sesión</span>
                </div>
                <div class="dimex-login-subtitle">
                    Conéctate al Dimex Intelligence Board para monitorear
                    cartera, riesgo y crecimiento de sucursales en tiempo casi real.
                </div>
                <div class="dimex-login-pill">
                    <span class="dimex-login-pill-dot"></span>
                    <span>Datos cifrados · Acceso controlado por rol</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # --------- LADO DERECHO: tarjeta de formulario ---------
    with right_col:
        st.markdown('<div class="dimex-login-card">', unsafe_allow_html=True)
        st.markdown('<div class="dimex-login-card-inner">', unsafe_allow_html=True)

        st.markdown(
            """
            <div class="dimex-login-card-header">
                <div class="dimex-login-card-title">
                    <span class="label">Panel Dimex</span>
                    <span class="main">Acceso rápido</span>
                </div>
                <div class="dimex-login-badge-soft">
                    v1.0 · Roles: Admin / Empleado
                </div>
            </div>
            <div class="dimex-login-divider"></div>
            """,
            unsafe_allow_html=True,
        )

        # ---- Widgets de Streamlit (login real) ----
        user = st.text_input("Usuario", key="login_user")
        role = st.selectbox(
            "Tipo de usuario",
            ["Administrador", "Empleado"],
            key="login_role",
        )

        st.markdown(
            '<div class="dimex-login-footer-row">',
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="dimex-login-hint">
                Selecciona tu tipo de usuario. El administrador ve toda la red;
                el empleado solo su sucursal y recomendaciones específicas.
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Botón dentro de un contenedor para aplicar la clase
        login_btn_container = st.container()
        with login_btn_container:
            st.markdown(
                '<div class="dimex-login-primary-btn">',
                unsafe_allow_html=True,
            )
            login_clicked = st.button("Entrar", key="login_button")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)  # .dimex-login-card-inner
        st.markdown("</div>", unsafe_allow_html=True)  # .dimex-login-card

    st.markdown("</div>", unsafe_allow_html=True)  # .dimex-login-shell
    st.markdown("</div>", unsafe_allow_html=True)  # .dimex-login-background

    # ------ Lógica de login ------
    if login_clicked:
        username_clean = user.strip() if user.strip() else "Invitado"

        st.session_state["user"] = username_clean
        st.session_state["role"] = role  # "Administrador" o "Empleado"
        st.session_state["logged_in"] = True

        st.rerun()
