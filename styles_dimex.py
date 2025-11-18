import streamlit as st

# Paleta de colores Dimex / tech
DIMEX_COLORS = {
    "primary": "#4CAF2A",       # verde principal
    "primary_dark": "#2C7A16",
    "accent": "#FFC300",        # amarillo
    "bg": "#F5F7FA",
    "card_bg": "#FFFFFF",
    "text_main": "#24323F",
    "text_soft": "#6B7B8A",
    "danger": "#E53935",
}

# Estilos globales
CUSTOM_CSS = f"""
<style>

/* ================================
   FONDO GLOBAL TIPO APPLE + DIMEX
================================ */

/* Fondo para toda la app */
body {{
    margin: 0;
    background:
        radial-gradient(circle at 0% 0%, rgba(76, 175, 42, 0.16), transparent 55%),
        radial-gradient(circle at 100% 0%, rgba(255, 195, 0, 0.12), transparent 55%),
        linear-gradient(135deg,
            #F3F6FA 0%,
            #FFFFFF 45%,
            #E7F4EC 100%
        );
    background-attachment: fixed;
}}

/* Contenedor principal de Streamlit */
[data-testid="stAppViewContainer"] > .main {{
    background: transparent;
    backdrop-filter: blur(10px) saturate(150%);
}}

/* Contenedor interno donde van los elementos (para dar efecto glass) */
.block-container {{
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    border-radius: 24px;
    background: rgba(255, 255, 255, 0.82);
    box-shadow:
        0 24px 60px rgba(15, 23, 42, 0.16),
        0 0 0 1px rgba(148, 163, 184, 0.25);
    backdrop-filter: blur(16px);
}}

/* ================================
   ANIMACIONES SUAVES (KPIs & Charts)
================================ */
@keyframes fadeInUp {{
    0% {{
        opacity: 0;
        transform: translateY(14px) scale(0.98);
    }}
    60% {{
        opacity: 1;
        transform: translateY(-2px) scale(1.01);
    }}
    100% {{
        opacity: 1;
        transform: translateY(0) scale(1);
    }}
}}

@keyframes fadeIn {{
    0% {{ opacity: 0; transform: scale(0.96); }}
    100% {{ opacity: 1; transform: scale(1); }}
}}

/* ================================
   ENCABEZADO DIMEX
================================ */
.dimex-header {{
    padding: 1.5rem 0 0.5rem 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}
.dimex-title-block {{
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
}}
.dimex-title {{
    font-size: 2.1rem;
    font-weight: 800;
    color: {DIMEX_COLORS["text_main"]};
    letter-spacing: 0.04em;
}}
.dimex-subtitle {{
    font-size: 0.95rem;
    color: {DIMEX_COLORS["text_soft"]};
}}
.dimex-badge {{
    padding: 0.25rem 0.75rem;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 600;
    color: #fff;
    background: linear-gradient(135deg, {DIMEX_COLORS["primary_dark"]}, {DIMEX_COLORS["primary"]});
    box-shadow: 0 0 18px rgba(76, 175, 42, 0.35);
}}

/* ================================
   TARJETAS DE FILTROS
================================ */
.filter-card {{
    background: linear-gradient(135deg, #FFFFFF, #F8FFF7);
    border-radius: 18px;
    padding: 1rem 1.2rem;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
    border: 1px solid rgba(148, 163, 184, 0.25);
    backdrop-filter: blur(8px);
    margin-bottom: 0.8rem;
}}
.filter-title {{
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: {DIMEX_COLORS["text_soft"]};
    margin-bottom: 0.4rem;
}}

/* ================================
   KPI GRID
================================ */
.kpi-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin-top: 0.4rem;
}}

.kpi-card {{
    position: relative;
    padding: 1.1rem 1.2rem;
    border-radius: 18px;
    background: {DIMEX_COLORS["card_bg"]};
    overflow: hidden;
    border: 1px solid rgba(148, 163, 184, 0.35);
    box-shadow:
        0 18px 45px rgba(15, 23, 42, 0.10),
        0 0 0 1px rgba(148, 163, 184, 0.18);
    transition: all 220ms ease-out;
    cursor: default;

    /* Animación al renderizar */
    animation: fadeInUp 0.45s ease-out;
}}
.kpi-card::before {{
    content: "";
    position: absolute;
    inset: -40%;
    background: radial-gradient(circle at top, rgba(76, 175, 42, 0.12), transparent 55%);
    opacity: 0;
    transition: opacity 260ms ease-out;
}}
.kpi-card:hover {{
    transform: translateY(-4px) scale(1.01);
    box-shadow:
        0 24px 55px rgba(15, 23, 42, 0.22),
        0 0 22px rgba(76, 175, 42, 0.35); /* Glow tech verde */
}}
.kpi-card:hover::before {{
    opacity: 1;
}}

.kpi-label {{
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: {DIMEX_COLORS["text_soft"]};
    margin-bottom: 0.25rem;
}}

.kpi-value {{
    font-size: 1.6rem;
    font-weight: 800;
    color: {DIMEX_COLORS["text_main"]};
}}

.kpi-trend {{
    font-size: 0.82rem;
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    margin-top: 0.25rem;
    padding: 0.12rem 0.55rem;
    border-radius: 999px;
    background-color: rgba(76, 175, 42, 0.06);
    color: {DIMEX_COLORS["primary_dark"]};
    font-weight: 500;
}}
.kpi-trend.bad {{
    background-color: rgba(229, 57, 53, 0.06);
    color: {DIMEX_COLORS["danger"]};
}}

.kpi-caption {{
    font-size: 0.75rem;
    color: {DIMEX_COLORS["text_soft"]};
    margin-top: 0.3rem;
}}

/* ================================
   CHART CARD
================================ */
.chart-card {{
    margin-top: 1rem;
    padding: 1rem 1.2rem;
    border-radius: 18px;
    background: #FFFFFF;
    box-shadow: 0 16px 40px rgba(15, 23, 42, 0.08);
    border: 1px solid rgba(148, 163, 184, 0.3);

    /* Animación */
    animation: fadeIn 0.40s ease-out;
}}
.chart-title {{
    font-size: 0.95rem;
    font-weight: 600;
    color: {DIMEX_COLORS["text_main"]};
    margin-bottom: 0.3rem;
}}
.chart-caption {{
    font-size: 0.78rem;
    color: {DIMEX_COLORS["text_soft"]};
    margin-bottom: 0.6rem;
}}

/* ================================
   PILL DE CONTEXTO
================================ */
.context-pill {{
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    padding: 0.25rem 0.8rem;
    border-radius: 999px;
    background-color: rgba(15, 23, 42, 0.03);
    border: 1px solid rgba(148, 163, 184, 0.4);
    font-size: 0.75rem;
    color: {DIMEX_COLORS["text_soft"]};
    margin-top: 0.4rem;
}}
.context-pill span.context-strong {{
    font-weight: 600;
    color: {DIMEX_COLORS["primary_dark"]};
}}

/* ================================
   SELECTBOX más moderno (CSS hack)
================================ */
.stSelectbox > div {{
    border: 1px solid #D0D7DE !important;
    border-radius: 12px !important;
    padding: 6px !important;
    background: white !important;
    transition: all 0.2s ease-out !important;
}}
.stSelectbox > div:hover {{
    border-color: {DIMEX_COLORS["primary"]} !important;
    box-shadow: 0 0 12px rgba(76, 175, 42, 0.20);
}}
.stSelectbox label {{
    font-weight: 600 !important;
    color: {DIMEX_COLORS["text_soft"]} !important;
}}

/* ================================
   ALERTA DE CLUSTER SELECCIONADO
================================ */
.cluster-alert {{
    margin-top: 0.8rem;
    margin-bottom: 0.8rem;
    padding: 0.75rem 1rem;
    border-radius: 14px;
    border: 1px solid rgba(76, 175, 42, 0.35);
    background: linear-gradient(90deg, #ECFDF3, #F4FFF7);
    color: #14532D;
    font-size: 0.9rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
    animation: fadeIn 0.35s ease-out;
    box-shadow: 0 10px 25px rgba(22, 101, 52, 0.12);
}}

.cluster-alert-icon {{
    font-size: 1.1rem;
}}

.cluster-alert-branch {{
    font-weight: 700;
}}

.cluster-alert-cluster {{
    font-weight: 700;
    color: #15803D;
}}

</style>
"""

def inject_css():
    """Inyecta los estilos globales en la app."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
