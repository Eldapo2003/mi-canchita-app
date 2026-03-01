import streamlit as st
import pandas as pd
from datetime import time
import streamlit.components.v1 as components

st.set_page_config(page_title="Mi Canchita App", page_icon="⚽", layout="wide")

# ==========================================
# INYECCION DE CSS GLOBAL (diseño oscuro)
# ==========================================
st.html("""
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet"/>
<style>
  /* ─── Variables ─── */
  :root {
    --bg-deep:    #050e1a;
    --bg-card:    #081828;
    --bg-panel:   #0a1e30;
    --green:      #00e676;
    --green-dim:  #00c853;
    --green-glow: rgba(0,230,118,0.18);
    --border:     rgba(0,230,118,0.12);
    --teal:       #00bcd4;
    --text:       #e8f4f8;
    --muted:      #7a9ab0;
  }

  /* ─── Fondo general ─── */
  .stApp, [data-testid="stAppViewContainer"] {
    background: var(--bg-deep) !important;
    font-family: 'Outfit', sans-serif !important;
  }
  [data-testid="stHeader"] {
    background: rgba(5,14,26,0.9) !important;
    backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--border);
  }
  [data-testid="stSidebar"] {
    background: #060f1c !important;
    border-right: 1px solid var(--border) !important;
  }

  /* ─── Sidebar ─── */
  [data-testid="stSidebar"] * { color: var(--text) !important; }
  [data-testid="stSidebar"] .stButton > button {
    background: rgba(0,230,118,0.08) !important;
    border: 1px solid var(--border) !important;
    color: var(--green) !important;
    border-radius: 8px !important;
    font-family: 'Outfit', sans-serif !important;
  }
  [data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(0,230,118,0.18) !important;
    border-color: var(--green) !important;
  }

  /* ─── Texto general ─── */
  h1,h2,h3,h4,p,label,span,div { color: var(--text) !important; font-family: 'Outfit', sans-serif !important; }
  h1,h2 { font-family: 'Bebas Neue', sans-serif !important; letter-spacing: 1.5px !important; }
  .stMarkdown p { color: var(--muted) !important; }

  /* ─── Inputs ─── */
  .stTextInput input, .stSelectbox select, .stNumberInput input, .stTextArea textarea {
    background: #0c1f30 !important;
    border: 1px solid rgba(0,230,118,0.2) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
    font-family: 'Outfit', sans-serif !important;
  }
  .stTextInput input:focus, .stSelectbox select:focus {
    border-color: var(--green) !important;
    box-shadow: 0 0 0 2px var(--green-glow) !important;
  }
  [data-baseweb="select"] > div {
    background: #0c1f30 !important;
    border: 1px solid rgba(0,230,118,0.2) !important;
    border-radius: 8px !important;
  }
  [data-baseweb="select"] span { color: var(--text) !important; }

  /* ─── Botones ─── */
  .stButton > button {
    background: rgba(0,230,118,0.08) !important;
    border: 1px solid rgba(0,230,118,0.3) !important;
    color: var(--green) !important;
    border-radius: 8px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    transition: all .2s !important;
  }
  .stButton > button:hover {
    background: rgba(0,230,118,0.18) !important;
    border-color: var(--green) !important;
    box-shadow: 0 0 20px var(--green-glow) !important;
    transform: translateY(-1px) !important;
  }
  .stButton > button[kind="primary"] {
    background: linear-gradient(135deg,#003d1f,#006633) !important;
    border-color: var(--green) !important;
    color: var(--green) !important;
    font-size: 15px !important;
    padding: 10px 20px !important;
  }
  .stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg,#005c2d,#009944) !important;
    box-shadow: 0 0 30px rgba(0,230,118,0.4) !important;
    color: #fff !important;
  }

  /* ─── Radio buttons ─── */
  .stRadio label { color: var(--text) !important; }
  .stRadio [data-baseweb="radio"] span { border-color: var(--green) !important; }

  /* ─── Checkbox ─── */
  .stCheckbox label span { color: var(--text) !important; }

  /* ─── Containers / cards ─── */
  [data-testid="stVerticalBlock"] > [data-testid="element-container"] > div[data-testid="stVerticalBlock"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
  }
  div[data-testid="stExpander"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
  }

  /* ─── Tabs ─── */
  .stTabs [data-baseweb="tab-list"] {
    background: var(--bg-card) !important;
    border-radius: 10px !important;
    padding: 4px !important;
    border-bottom: 1px solid var(--border) !important;
  }
  .stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--muted) !important;
    border-radius: 8px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
  }
  .stTabs [aria-selected="true"] {
    background: rgba(0,230,118,0.12) !important;
    color: var(--green) !important;
    border-bottom: 2px solid var(--green) !important;
  }

  /* ─── Métricas ─── */
  [data-testid="stMetricValue"] {
    color: var(--green) !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 2rem !important;
  }
  [data-testid="stMetricLabel"] { color: var(--muted) !important; }

  /* ─── Dataframe ─── */
  [data-testid="stDataFrameContainer"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
  }

  /* ─── Divider ─── */
  hr { border-color: var(--border) !important; }

  /* ─── Info/success/error boxes ─── */
  [data-testid="stAlert"] {
    background: rgba(0,230,118,0.06) !important;
    border: 1px solid rgba(0,230,118,0.2) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
  }

  /* ─── Ocultar barra top de Streamlit ─── */
  #MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; }

  /* ─── Quitar padding excesivo ─── */
  .block-container { padding-top: 0 !important; max-width: 100% !important; }
  [data-testid="stVerticalBlock"] { gap: 0.5rem !important; }
  @keyframes float {
    0%,100% { transform:translateY(0); }
    50%      { transform:translateY(-12px); }
  }
</style>
""")

# ==========================================
# SVG CONSTANTS
# ==========================================
FIELD_BALL_SVG = """
<svg viewBox="0 0 700 420" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;display:block;">
  <defs>
    <radialGradient id="bG" cx="36%" cy="30%" r="65%">
      <stop offset="0%"   stop-color="#1e3f62"/>
      <stop offset="55%"  stop-color="#0a1b2e"/>
      <stop offset="100%" stop-color="#040c18"/>
    </radialGradient>
    <radialGradient id="bS" cx="28%" cy="22%" r="45%">
      <stop offset="0%"   stop-color="white" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="white" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="sL" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%"   stop-color="#001208"/>
      <stop offset="100%" stop-color="#002818"/>
    </linearGradient>
    <linearGradient id="sR" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%"   stop-color="#001e12"/>
      <stop offset="100%" stop-color="#000a06"/>
    </linearGradient>
    <linearGradient id="sFr" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%"   stop-color="#002818"/>
      <stop offset="100%" stop-color="#000c06"/>
    </linearGradient>
    <filter id="lG" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="1.8" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="bGF" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="8" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="gGF" x="-25%" y="-25%" width="150%" height="150%">
      <feGaussianBlur stdDeviation="2.5" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <clipPath id="fC">
      <polygon points="60,345 570,345 640,120 130,120"/>
    </clipPath>
    <clipPath id="bC">
      <circle cx="350" cy="25" r="58"/>
    </clipPath>
  </defs>

  <!-- 3D SIDE FACES -->
  <polygon points="60,345 130,120 130,148 60,370"   fill="url(#sL)"/>
  <polygon points="570,345 640,120 640,148 570,370"  fill="url(#sR)"/>
  <polygon points="60,345 570,345 570,370 60,370"    fill="url(#sFr)"/>
  <line x1="60"  y1="345" x2="60"  y2="370" stroke="#00e676" stroke-width="0.9" opacity="0.4"/>
  <line x1="570" y1="345" x2="570" y2="370" stroke="#00e676" stroke-width="0.9" opacity="0.3"/>
  <line x1="60"  y1="370" x2="570" y2="370" stroke="#00e676" stroke-width="0.9" opacity="0.25"/>
  <line x1="130" y1="120" x2="130" y2="148" stroke="#00e676" stroke-width="0.7" opacity="0.25"/>
  <line x1="640" y1="120" x2="640" y2="148" stroke="#00e676" stroke-width="0.7" opacity="0.2"/>

  <!-- FIELD TOP FACE -->
  <polygon points="60,345 570,345 640,120 130,120" fill="#003d22"/>
  <g clip-path="url(#fC)">
    <polygon points="60,345  124,345  194,120  130,120" fill="#004e2c" opacity="0.78"/>
    <polygon points="188,345 252,345  322,120  258,120" fill="#004e2c" opacity="0.78"/>
    <polygon points="315,345 379,345  449,120  385,120" fill="#004e2c" opacity="0.78"/>
    <polygon points="443,345 506,345  576,120  513,120" fill="#004e2c" opacity="0.78"/>
  </g>

  <!-- FIELD MARKINGS -->
  <polygon points="60,345 570,345 640,120 130,120" fill="none" stroke="#00ff88" stroke-width="2.2" filter="url(#lG)" opacity="0.92"/>
  <line x1="315" y1="345" x2="385" y2="120" stroke="#00ff88" stroke-width="1.9" filter="url(#lG)" opacity="0.9"/>
  <circle cx="350" cy="233" r="3.5" fill="#00ff88" filter="url(#lG)" opacity="0.9"/>
  <polygon points="394,233 393,217 381,206 359,202 336,206 316,217 306,233 307,248 319,259 341,263 364,259 384,248"
           fill="none" stroke="#00ff88" stroke-width="1.9" filter="url(#lG)" opacity="0.88"/>

  <!-- LEFT PENALTY AREA -->
  <polygon points="74,299 154,299 196,166 116,166" fill="none" stroke="#00ff88" stroke-width="1.7" filter="url(#lG)" opacity="0.86"/>
  <polygon points="86,263 112,263 131,202 105,202" fill="none" stroke="#00ff88" stroke-width="1.4" filter="url(#lG)" opacity="0.76"/>
  <circle cx="149" cy="233" r="3" fill="#00ff88" opacity="0.82"/>

  <!-- RIGHT PENALTY AREA -->
  <polygon points="504,299 584,299 626,166 546,166" fill="none" stroke="#00ff88" stroke-width="1.7" filter="url(#lG)" opacity="0.86"/>
  <polygon points="569,263 596,263 615,202 588,202" fill="none" stroke="#00ff88" stroke-width="1.4" filter="url(#lG)" opacity="0.76"/>
  <circle cx="552" cy="233" r="3" fill="#00ff88" opacity="0.82"/>

  <!-- CORNER ARCS -->
  <path d="M60,345  Q73,339 79,327"    fill="none" stroke="#00ff88" stroke-width="1.3" opacity="0.65"/>
  <path d="M570,345 Q572,332 562,325"  fill="none" stroke="#00ff88" stroke-width="1.3" opacity="0.65"/>
  <path d="M130,120 Q140,131 151,139"  fill="none" stroke="#00ff88" stroke-width="1.3" opacity="0.65"/>
  <path d="M640,120 Q638,133 628,140"  fill="none" stroke="#00ff88" stroke-width="1.3" opacity="0.65"/>

  <!-- LEFT GOAL -->
  <polygon points="91,245 99,220 87,220 80,245" fill="#001a0d" opacity="0.85"/>
  <line x1="84" y1="245" x2="83" y2="220" stroke="#004020" stroke-width="0.9" opacity="0.55"/>
  <line x1="87" y1="245" x2="86" y2="220" stroke="#004020" stroke-width="0.9" opacity="0.55"/>
  <line x1="91" y1="245" x2="99" y2="220" stroke="#00ff88" stroke-width="4"   filter="url(#gGF)"/>
  <line x1="99" y1="220" x2="87" y2="220" stroke="#00ff88" stroke-width="2.8" filter="url(#gGF)" opacity="0.95"/>
  <line x1="91" y1="245" x2="80" y2="245" stroke="#00ff88" stroke-width="2.8" filter="url(#gGF)" opacity="0.9"/>
  <line x1="80" y1="245" x2="87" y2="220" stroke="#00ff88" stroke-width="2.2" filter="url(#gGF)" opacity="0.8"/>

  <!-- RIGHT GOAL -->
  <polygon points="601,245 609,220 621,220 613,245" fill="#001a0d" opacity="0.85"/>
  <line x1="616" y1="245" x2="617" y2="220" stroke="#004020" stroke-width="0.9" opacity="0.55"/>
  <line x1="613" y1="245" x2="614" y2="220" stroke="#004020" stroke-width="0.9" opacity="0.55"/>
  <line x1="601" y1="245" x2="609" y2="220" stroke="#00ff88" stroke-width="4"   filter="url(#gGF)"/>
  <line x1="609" y1="220" x2="621" y2="220" stroke="#00ff88" stroke-width="2.8" filter="url(#gGF)" opacity="0.95"/>
  <line x1="601" y1="245" x2="613" y2="245" stroke="#00ff88" stroke-width="2.8" filter="url(#gGF)" opacity="0.9"/>
  <line x1="613" y1="245" x2="621" y2="220" stroke="#00ff88" stroke-width="2.2" filter="url(#gGF)" opacity="0.8"/>

  <!-- SOCCER BALL -->
  <g filter="url(#bGF)">
    <ellipse cx="350" cy="168" rx="52" ry="18" fill="black" opacity="0.36"/>
    <circle cx="350" cy="25" r="58" fill="url(#bG)"/>
    <g clip-path="url(#bC)">
      <polygon points="350,3 371,18 363,43 337,43 329,18" fill="#050d1a" opacity="0.88"/>
      <polygon points="350,-33 371,-30 371,18 350,3 329,18 330,-30" fill="#07111f" opacity="0.7"/>
      <polygon points="405,7 371,18 363,43 395,52 416,25"  fill="#07111f" opacity="0.68"/>
      <polygon points="384,72 363,43 337,43 315,72 350,88"  fill="#07111f" opacity="0.65"/>
      <polygon points="295,7 329,18 337,43 305,52 284,25"   fill="#07111f" opacity="0.68"/>
    </g>
    <g clip-path="url(#bC)" fill="none" stroke="#00e676" stroke-width="1.6" opacity="0.88">
      <line x1="350" y1="3"  x2="350" y2="-65"/>
      <line x1="371" y1="18" x2="412" y2="3"/>
      <line x1="363" y1="43" x2="392" y2="80"/>
      <line x1="337" y1="43" x2="308" y2="80"/>
      <line x1="329" y1="18" x2="288" y2="3"/>
      <path d="M350,-33 Q391,-31 405,7"/>
      <path d="M405,7   Q416,46  384,72"/>
      <path d="M384,72  Q350,94  316,72"/>
      <path d="M316,72  Q284,46  295,7"/>
      <path d="M295,7   Q309,-31 350,-33"/>
    </g>
    <circle cx="350" cy="25" r="58" fill="none" stroke="#00e676" stroke-width="1.6" opacity="0.7"/>
    <text x="350" y="33" text-anchor="middle"
          font-family="'Bebas Neue', sans-serif" font-size="30"
          fill="#00e676" filter="url(#lG)" opacity="0.98">M</text>
    <ellipse cx="330" cy="4" rx="18" ry="11" fill="url(#bS)" transform="rotate(-28,330,4)"/>
  </g>
</svg>
"""

# ==========================================
# 1. ESTADO INICIAL / BASE DE DATOS
# ==========================================
if "usuarios" not in st.session_state:
    st.session_state.usuarios = {
        "admin": {"clave": "admin", "tipo": "admin", "nombre": "Administrador", "complejo_id": "xsports"},
        "David Paredes": {"clave": "1234", "tipo": "cliente", "nombre": "David Paredes"}
    }

if "usuario_conectado" not in st.session_state:
    st.session_state.usuario_conectado = None

if "base_reservas" not in st.session_state:
    st.session_state.base_reservas = []

if "complejos" not in st.session_state:
    st.session_state.complejos = {
        "xsports": {
            "info": {
                "nombre": "Xsports Complejo Deportivo",
                "direccion": "Av. Principal 123, Quito",
                "telefono": "+593984347607",
                "descripcion": "El mejor complejo deportivo de la ciudad."
            },
            "canchas": [
                {"id": 1, "nombre": "Cancha Techada (Futbol)",     "tipo": "Futbol", "precio_tipo": "hora",    "precio": 40.0, "descripcion": "Cancha cubierta con iluminacion LED", "activa": True},
                {"id": 2, "nombre": "Cancha Descubierta (Futbol)", "tipo": "Futbol", "precio_tipo": "hora",    "precio": 30.0, "descripcion": "Cancha al aire libre",               "activa": True},
                {"id": 3, "nombre": "Cancha Padel #1",             "tipo": "Padel",  "precio_tipo": "persona", "precio":  5.0, "descripcion": "Cancha de padel profesional",         "activa": True},
                {"id": 4, "nombre": "Cancha Padel #2",             "tipo": "Padel",  "precio_tipo": "persona", "precio":  5.0, "descripcion": "Cancha de padel profesional",         "activa": True},
            ],
            "bar": [
                {"id": 1, "nombre": "Cola",       "categoria": "Bebidas", "precio": 1.50, "stock":  50, "activo": True, "imagen": None},
                {"id": 2, "nombre": "Agua",       "categoria": "Bebidas", "precio": 1.00, "stock": 100, "activo": True, "imagen": None},
                {"id": 3, "nombre": "Cerveza",    "categoria": "Bebidas", "precio": 3.00, "stock":  30, "activo": True, "imagen": None},
                {"id": 4, "nombre": "Salchipapa", "categoria": "Comidas", "precio": 5.00, "stock":  20, "activo": True, "imagen": None},
            ],
            "horarios": {
                "Lunes":     {"abierto": True,  "apertura": "08:00", "cierre": "22:00"},
                "Martes":    {"abierto": True,  "apertura": "08:00", "cierre": "22:00"},
                "Miercoles": {"abierto": True,  "apertura": "08:00", "cierre": "22:00"},
                "Jueves":    {"abierto": True,  "apertura": "08:00", "cierre": "22:00"},
                "Viernes":   {"abierto": True,  "apertura": "08:00", "cierre": "23:00"},
                "Sabado":    {"abierto": True,  "apertura": "07:00", "cierre": "23:00"},
                "Domingo":   {"abierto": True,  "apertura": "08:00", "cierre": "20:00"},
            },
            "next_cancha_id": 5,
            "next_bar_id": 5,
        }
    }

# ==========================================
# 2. NAVBAR VISUAL
# ==========================================
def render_navbar(nombre_usuario=None):
    if nombre_usuario:
        avatar_html = f"""
        <div style="display:flex;align-items:center;gap:10px;">
          <div style="width:36px;height:36px;border-radius:50%;background:rgba(0,230,118,0.1);
                      border:1px solid rgba(0,230,118,0.25);display:flex;align-items:center;
                      justify-content:center;color:#00e676;font-size:14px;">
            👤
          </div>
          <span style="color:#e8f4f8;font-size:13px;font-weight:500;">{nombre_usuario}</span>
        </div>"""
    else:
        avatar_html = """
        <div style="width:40px;height:40px;border-radius:50%;background:rgba(0,230,118,0.08);
                    border:2px solid rgba(0,230,118,0.25);display:flex;align-items:center;
                    justify-content:center;color:#7a9ab0;font-size:18px;">👤</div>"""

    st.markdown(f"""
    <div style="background:rgba(5,14,26,0.95);backdrop-filter:blur(16px);
                border-bottom:1px solid rgba(0,230,118,0.12);
                padding:14px 32px;margin-bottom:0;
                display:flex;align-items:center;gap:16px;position:sticky;top:0;z-index:999;">
      <div style="display:flex;align-items:center;gap:10px;flex-shrink:0;">
        <div style="width:42px;height:42px;border-radius:50%;
                    background:linear-gradient(135deg,#00e676,#00897b);
                    display:flex;align-items:center;justify-content:center;
                    font-family:'Bebas Neue',sans-serif;font-size:20px;color:#050e1a;
                    box-shadow:0 0 18px rgba(0,230,118,0.5);flex-shrink:0;">M</div>
        <span style="font-family:'Bebas Neue',sans-serif;font-size:24px;
                     color:#e8f4f8;letter-spacing:1px;">Mi Canchita</span>
      </div>
      <div style="display:flex;gap:32px;margin:0 auto;">
        <span style="color:#00bcd4;font-weight:500;font-size:15px;cursor:pointer;">Inicio</span>
        <span style="color:#00bcd4;font-weight:500;font-size:15px;cursor:pointer;">Reservas</span>
        <span style="color:#00bcd4;font-weight:500;font-size:15px;cursor:pointer;">Estadísticas</span>
      </div>
      {avatar_html}
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 3. LOGIN / REGISTRO
# ==========================================
if st.session_state.usuario_conectado is None:
    render_navbar()

    # Hero section con cancha y formulario
    col_field, col_form = st.columns([1.4, 1])

    with col_field:
        # Campo SVG con animación float
        st.markdown(f"""
        <div style="padding:32px 16px 0 32px;">
            {FIELD_BALL_SVG}
        </div>
        """, unsafe_allow_html=True)

    with col_form:
        st.markdown("<div style='padding:40px 24px 0 16px;'>", unsafe_allow_html=True)
        st.markdown("""
        <h1 style="font-family:'Bebas Neue',sans-serif;font-size:2.8rem;
                   color:#e8f4f8;letter-spacing:2px;margin-bottom:4px;">
          BIENVENIDO
        </h1>
        <p style="color:#7a9ab0;margin-bottom:24px;font-size:14px;">
          Reserva tu cancha favorita en segundos
        </p>
        """, unsafe_allow_html=True)

        opcion = st.radio("", ["Ingresar", "Registrarse"], horizontal=True, label_visibility="collapsed")

        if opcion == "Ingresar":
            u = st.text_input("Usuario", placeholder="Nombre completo")
            p = st.text_input("Contraseña", type="password", placeholder="••••••••")
            if st.button("ENTRAR", use_container_width=True, type="primary"):
                if u in st.session_state.usuarios and st.session_state.usuarios[u]["clave"] == p:
                    st.session_state.usuario_conectado = dict(st.session_state.usuarios[u])
                    st.session_state.usuario_conectado["id"] = u
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas")
        else:
            new_u  = st.text_input("Nombre completo", placeholder="Tu nombre")
            new_p  = st.text_input("Contraseña", type="password", placeholder="Mínimo 4 caracteres")
            conf_p = st.text_input("Confirmar contraseña", type="password", placeholder="Repite la contraseña")
            if st.button("REGISTRARSE", use_container_width=True, type="primary"):
                if new_u and new_p == conf_p and len(new_p) >= 4:
                    st.session_state.usuarios[new_u] = {"clave": new_p, "tipo": "cliente", "nombre": new_u}
                    st.success("Registro exitoso! Ahora puedes ingresar.")
                else:
                    st.error("Verifica que los datos sean correctos.")

        st.markdown("</div>", unsafe_allow_html=True)

    # Feature cards
    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    cards = [
        ("📅", "Reservas",      "Haz tu reserva de cancha fácilmente desde cualquier lugar."),
        ("📊", "Estadísticas",  "Consulta tus estadísticas de partidos y rendimiento."),
        ("🏆", "Torneos",       "Participa en torneos y competencias de tu ciudad."),
    ]
    for col, (ico, titulo, desc) in zip([c1,c2,c3], cards):
        col.markdown(f"""
        <div style="background:#081828;border:1px solid rgba(0,230,118,0.12);border-radius:14px;
                    padding:24px 20px;display:flex;align-items:flex-start;gap:16px;
                    transition:all .25s;cursor:pointer;"
             onmouseover="this.style.borderColor='rgba(0,230,118,0.4)';this.style.transform='translateY(-4px)'"
             onmouseout="this.style.borderColor='rgba(0,230,118,0.12)';this.style.transform='none'">
          <div style="width:46px;height:46px;flex-shrink:0;background:rgba(0,230,118,0.08);
                      border:1px solid rgba(0,230,118,0.25);border-radius:10px;
                      display:flex;align-items:center;justify-content:center;font-size:20px;">
            {ico}
          </div>
          <div>
            <div style="font-size:17px;font-weight:700;color:#e8f4f8;margin-bottom:5px;">{titulo}</div>
            <div style="font-size:13px;color:#7a9ab0;line-height:1.5;">{desc}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # Disclaimer WhatsApp
    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:linear-gradient(135deg,#1a1a2e,#16213e);border:1px solid #25d366;
                padding:24px;border-radius:12px;text-align:center;max-width:600px;margin:0 auto;">
      <h4 style="color:#ffffff;margin-bottom:8px;font-size:1.1rem;">
        🏟️ ¿Eres dueño de un complejo deportivo?
      </h4>
      <p style="color:#cccccc;margin-bottom:16px;font-size:0.9rem;">
        Únete a nuestra red y gestiona tus reservas de forma profesional.
      </p>
      <a href="https://wa.me/593984347607?text=Hola,%20me%20interesa%20contratar%20los%20servicios%20de%20Mi%20Canchita%20App"
         target="_blank"
         style="display:inline-block;background-color:#25d366;color:white;padding:12px 28px;
                text-decoration:none;border-radius:8px;font-weight:bold;font-size:0.95rem;">
        💬 Contratar Servicios (WhatsApp)
      </a>
    </div>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div style="text-align:center;padding:32px;color:#3a5a70;font-size:13px;margin-top:40px;
                border-top:1px solid rgba(0,230,118,0.08);">
      © 2024 Mi Canchita · Todos los derechos reservados
    </div>
    """, unsafe_allow_html=True)

    st.stop()

# ==========================================
# 4. INTERFAZ POST-LOGIN
# ==========================================
user = st.session_state.usuario_conectado
render_navbar(user["nombre"])

# Sidebar simplificado
with st.sidebar:
    st.markdown(f"""
    <div style="padding:16px 0;">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px;">
        <div style="width:40px;height:40px;border-radius:50%;background:rgba(0,230,118,0.1);
                    border:1px solid rgba(0,230,118,0.3);display:flex;align-items:center;
                    justify-content:center;font-size:18px;">👤</div>
        <div>
          <div style="font-weight:600;font-size:14px;color:#e8f4f8;">{user['nombre']}</div>
          <div style="font-size:11px;color:#00e676;text-transform:uppercase;letter-spacing:1px;">
            {'Admin' if user['tipo']=='admin' else 'Cliente'}
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🚪 Cerrar Sesión", use_container_width=True):
        st.session_state.usuario_conectado = None
        st.rerun()

# ==========================================
# VISTA CLIENTE
# ==========================================
if user["tipo"] == "cliente":

    # Hero con cancha (más pequeño en vista cliente)
    complejos_disponibles = {cid: data for cid, data in st.session_state.complejos.items()}
    nombres_complejos = {cid: data["info"]["nombre"] for cid, data in complejos_disponibles.items()}

    if not nombres_complejos:
        st.warning("No hay complejos disponibles por el momento.")
        st.stop()

    col_hero, col_right = st.columns([1.3, 1])

    with col_hero:
        st.markdown(f"""
        <div style="padding:16px 0 0 8px;max-width:480px;">
            {FIELD_BALL_SVG}
        </div>
        """, unsafe_allow_html=True)

        # Botón RESERVAR visual
        st.markdown("""
        <div style="display:flex;justify-content:center;margin-top:8px;">
          <div style="background:linear-gradient(135deg,#003d1f,#006633);
                      border:2px solid #00e676;color:#00e676;
                      font-family:'Bebas Neue',sans-serif;font-size:28px;letter-spacing:3px;
                      padding:14px 80px;border-radius:12px;text-align:center;
                      box-shadow:0 0 30px rgba(0,230,118,0.3);">
            RESERVAR
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown("<div style='padding:24px 8px 0 16px;'>", unsafe_allow_html=True)
        st.markdown("""
        <h2 style="font-family:'Bebas Neue',sans-serif;font-size:1.8rem;
                   color:#e8f4f8;letter-spacing:1px;margin-bottom:4px;">
          PRÓXIMOS PARTIDOS
        </h2>
        """, unsafe_allow_html=True)

        # Lista de reservas recientes como "partidos"
        reservas_recientes = st.session_state.base_reservas[-4:] if st.session_state.base_reservas else []
        if reservas_recientes:
            for r in reversed(reservas_recientes):
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:12px;padding:12px 0;
                            border-bottom:1px solid rgba(0,230,118,0.08);">
                  <div style="width:32px;height:32px;background:rgba(0,230,118,0.08);
                              border:1px solid rgba(0,230,118,0.25);border-radius:8px;
                              display:flex;align-items:center;justify-content:center;font-size:14px;">⚽</div>
                  <div>
                    <div style="font-size:13px;font-weight:600;color:#00e676;">{r['Cancha']}</div>
                    <div style="font-size:11px;color:#7a9ab0;">{r['Fecha']} · {r['Hora']}</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            for i, item in enumerate([("20 de abril","Cancha Techada"),("22 de abril","Cancha Padel #1"),("25 de abril","Cancha Descubierta"),("30 de abril","Cancha Padel #2")]):
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:12px;padding:12px 0;
                            border-bottom:1px solid rgba(0,230,118,0.08);">
                  <div style="width:32px;height:32px;background:rgba(0,230,118,0.08);
                              border:1px solid rgba(0,230,118,0.25);border-radius:8px;
                              display:flex;align-items:center;justify-content:center;font-size:14px;">
                    {'🏆' if i%2==0 else '⚽'}
                  </div>
                  <div>
                    <div style="font-size:13px;font-weight:600;color:#00e676;">{item[1]}</div>
                    <div style="font-size:11px;color:#7a9ab0;">{item[0]}</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    st.divider()
    st.subheader("Reserva tu Cancha")

    complejo_nombre = st.selectbox("🏟️ Selecciona un Complejo", list(nombres_complejos.values()))
    complejo_id = next(cid for cid, nom in nombres_complejos.items() if nom == complejo_nombre)
    complejo = complejos_disponibles[complejo_id]
    cfg = complejo["info"]

    canchas_activas = {c["nombre"]: c for c in complejo["canchas"] if c["activa"]}
    if not canchas_activas:
        st.info("Este complejo no tiene canchas disponibles por el momento.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            cancha_nombre = st.selectbox("Cancha", list(canchas_activas.keys()))
            info_cancha = canchas_activas[cancha_nombre]
            if info_cancha["precio_tipo"] == "persona":
                jugs = st.number_input("Jugadores", 1, 4, 4)
                p_base = jugs * info_cancha["precio"]
                st.caption(f"${info_cancha['precio']:.2f} por persona")
            else:
                p_base = info_cancha["precio"]
                st.caption(f"${info_cancha['precio']:.2f} por hora")
        with col2:
            fec  = st.date_input("Fecha")
            hor  = st.time_input("Hora", value=time(18, 0))
            parq = st.checkbox("Parqueadero (+$2)")

        st.divider()
        st.subheader("🍺 Agregar del Bar")
        productos_activos = [p for p in complejo["bar"] if p["activo"] and p["stock"] > 0]
        pedidos_bar = []
        if productos_activos:
            cols_bar = st.columns(min(4, len(productos_activos)))
            for i, prod in enumerate(productos_activos):
                with cols_bar[i % 4]:
                    with st.container(border=True):
                        if prod.get("imagen"):
                            st.image(prod["imagen"], use_container_width=True)
                        else:
                            st.markdown("<div style='text-align:center;font-size:2rem'>🛒</div>", unsafe_allow_html=True)
                        st.write(f"**{prod['nombre']}**")
                        st.caption(f"${prod['precio']:.2f} | Stock: {prod['stock']}")
                        cant = st.number_input("Cantidad", 0, prod["stock"], 0, key=f"bar_{complejo_id}_{prod['id']}")
                        if cant > 0:
                            pedidos_bar.append({"nombre": prod["nombre"], "cantidad": cant, "precio": prod["precio"]})

        total_bar = sum(p["cantidad"] * p["precio"] for p in pedidos_bar)
        total = p_base + (2.0 if parq else 0.0) + total_bar

        st.divider()
        _, col_res = st.columns([2, 1])
        with col_res:
            with st.container(border=True):
                st.write("**Resumen**")
                st.write(f"Cancha: ${p_base:.2f}")
                if parq: st.write("Parqueadero: $2.00")
                if total_bar > 0: st.write(f"Bar: ${total_bar:.2f}")
                st.subheader(f"Total: ${total:.2f}")

        if st.button("✅ Confirmar Reserva", type="primary"):
            st.session_state.base_reservas.append({
                "Complejo": cfg["nombre"], "Cliente": user["nombre"],
                "Cancha": cancha_nombre,   "Fecha": str(fec),
                "Hora": str(hor),          "Total": total, "Estado": "Pendiente"
            })
            st.success("¡Reserva enviada correctamente!")
            st.balloons()

# ==========================================
# VISTA ADMINISTRADOR
# ==========================================
else:
    complejo_id = user.get("complejo_id", list(st.session_state.complejos.keys())[0])
    if complejo_id not in st.session_state.complejos:
        st.session_state.complejos[complejo_id] = {
            "info": {"nombre": "Mi Complejo", "direccion": "", "telefono": "", "descripcion": ""},
            "canchas": [], "bar": [],
            "horarios": {
                "Lunes":{"abierto":True,"apertura":"08:00","cierre":"22:00"},
                "Martes":{"abierto":True,"apertura":"08:00","cierre":"22:00"},
                "Miercoles":{"abierto":True,"apertura":"08:00","cierre":"22:00"},
                "Jueves":{"abierto":True,"apertura":"08:00","cierre":"22:00"},
                "Viernes":{"abierto":True,"apertura":"08:00","cierre":"23:00"},
                "Sabado":{"abierto":True,"apertura":"07:00","cierre":"23:00"},
                "Domingo":{"abierto":True,"apertura":"08:00","cierre":"20:00"},
            },
            "next_cancha_id": 1, "next_bar_id": 1,
        }

    complejo = st.session_state.complejos[complejo_id]
    cfg = complejo["info"]

    st.markdown(f"""
    <div style="padding:24px 32px 8px;">
      <h1 style="font-family:'Bebas Neue',sans-serif;font-size:2.2rem;color:#e8f4f8;
                 letter-spacing:1.5px;margin:0;">🛠️ PANEL ADMINISTRATIVO</h1>
      <p style="color:#00e676;font-size:13px;margin:0;">{cfg['nombre']}</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Reservas", "🏟️ Establecimiento", "⚽ Canchas", "🍺 Bar y Productos", "🕐 Horarios"
    ])

    with tab1:
        st.subheader("Listado de Reservas")
        reservas_complejo = [r for r in st.session_state.base_reservas if r.get("Complejo") == cfg["nombre"]]
        if reservas_complejo:
            df = pd.DataFrame(reservas_complejo)
            m1, m2, m3 = st.columns(3)
            m1.metric("Total Reservas", len(df))
            m2.metric("Ingresos Totales", f"${df['Total'].sum():.2f}")
            m3.metric("Pendientes", len(df[df["Estado"] == "Pendiente"]))
            st.divider()
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No hay reservas para este complejo aun.")

    with tab2:
        st.subheader("Informacion del Establecimiento")
        with st.form("form_establecimiento"):
            nuevo_nombre = st.text_input("Nombre del Establecimiento", value=cfg["nombre"])
            nuevo_dir    = st.text_input("Direccion",                  value=cfg.get("direccion",""))
            nuevo_tel    = st.text_input("Telefono",                   value=cfg.get("telefono",""))
            nueva_desc   = st.text_area("Descripcion",                 value=cfg.get("descripcion",""), height=100)
            if st.form_submit_button("💾 Guardar Cambios", type="primary"):
                st.session_state.complejos[complejo_id]["info"].update({
                    "nombre":nuevo_nombre,"direccion":nuevo_dir,"telefono":nuevo_tel,"descripcion":nueva_desc
                })
                st.success("Informacion actualizada.")
                st.rerun()
        st.divider()
        st.caption("Vista previa para clientes:")
        with st.container(border=True):
            st.markdown(f"### 🏟️ {cfg['nombre']}")
            st.write(cfg.get("descripcion",""))
            ci, cd = st.columns(2)
            ci.write(f"📍 {cfg.get('direccion','')}")
            cd.write(f"📞 {cfg.get('telefono','')}")

    with tab3:
        st.subheader("Gestion de Canchas")
        with st.expander("➕ Agregar Nueva Cancha", expanded=False):
            with st.form("form_nueva_cancha"):
                c1, c2 = st.columns(2)
                with c1:
                    nc_nombre      = st.text_input("Nombre")
                    nc_tipo        = st.selectbox("Tipo", ["Futbol","Padel","Basket","Tenis","Volley","Otro"])
                    nc_desc        = st.text_input("Descripcion")
                with c2:
                    nc_precio_tipo = st.selectbox("Precio por", ["hora","persona"])
                    nc_precio      = st.number_input("Precio ($)", min_value=0.0, value=20.0, step=0.5)
                    nc_activa      = st.checkbox("Activa", value=True)
                if st.form_submit_button("Agregar Cancha", type="primary"):
                    if nc_nombre:
                        nid = complejo["next_cancha_id"]
                        st.session_state.complejos[complejo_id]["canchas"].append({
                            "id":nid,"nombre":nc_nombre,"tipo":nc_tipo,
                            "precio_tipo":nc_precio_tipo,"precio":nc_precio,
                            "descripcion":nc_desc,"activa":nc_activa
                        })
                        st.session_state.complejos[complejo_id]["next_cancha_id"] += 1
                        st.success(f"Cancha '{nc_nombre}' agregada.")
                        st.rerun()
                    else:
                        st.error("El nombre es obligatorio.")
        st.divider()
        tipos_list = ["Futbol","Padel","Basket","Tenis","Volley","Otro"]
        icono_map  = {"Futbol":"⚽","Padel":"🎾","Tenis":"🎾","Basket":"🏀","Volley":"🏐"}
        for i, cancha in enumerate(complejo["canchas"]):
            with st.container(border=True):
                ci, cp, ce, ca = st.columns([3,1.5,1,1])
                with ci:
                    st.write(f"{icono_map.get(cancha['tipo'],'🏟️')} **{cancha['nombre']}**")
                    st.caption(f"{cancha['tipo']} | {cancha.get('descripcion','')}")
                with cp:
                    st.write(f"💲 **${cancha['precio']:.2f}** / {cancha['precio_tipo']}")
                with ce:
                    st.write("🟢 Activa" if cancha["activa"] else "🔴 Inactiva")
                with ca:
                    if st.button("✏️ Editar", key=f"ed_c_{complejo_id}_{cancha['id']}"):
                        k = f"show_ec_{complejo_id}_{cancha['id']}"
                        st.session_state[k] = not st.session_state.get(k, False)
            if st.session_state.get(f"show_ec_{complejo_id}_{cancha['id']}", False):
                with st.container(border=True):
                    st.markdown(f"**Editando: {cancha['nombre']}**")
                    with st.form(f"form_ec_{complejo_id}_{cancha['id']}"):
                        ec1, ec2 = st.columns(2)
                        with ec1:
                            e_nom  = st.text_input("Nombre", value=cancha["nombre"])
                            e_tipo = st.selectbox("Tipo", tipos_list, index=tipos_list.index(cancha["tipo"]) if cancha["tipo"] in tipos_list else 0)
                            e_desc = st.text_input("Descripcion", value=cancha.get("descripcion",""))
                        with ec2:
                            e_pt   = st.selectbox("Precio por", ["hora","persona"], index=0 if cancha["precio_tipo"]=="hora" else 1)
                            e_prec = st.number_input("Precio ($)", min_value=0.0, value=cancha["precio"], step=0.5)
                            e_act  = st.checkbox("Activa", value=cancha["activa"])
                        cs, cd_ = st.columns(2)
                        with cs:
                            if st.form_submit_button("💾 Guardar", type="primary", use_container_width=True):
                                st.session_state.complejos[complejo_id]["canchas"][i].update({
                                    "nombre":e_nom,"tipo":e_tipo,"descripcion":e_desc,
                                    "precio_tipo":e_pt,"precio":e_prec,"activa":e_act
                                })
                                st.session_state[f"show_ec_{complejo_id}_{cancha['id']}"] = False
                                st.success("Cancha actualizada.")
                                st.rerun()
                        with cd_:
                            if st.form_submit_button("🗑️ Eliminar", use_container_width=True):
                                st.session_state.complejos[complejo_id]["canchas"].pop(i)
                                st.session_state[f"show_ec_{complejo_id}_{cancha['id']}"] = False
                                st.rerun()

    with tab4:
        st.subheader("Gestion del Bar y Productos")
        with st.expander("➕ Agregar Nuevo Producto", expanded=False):
            with st.form("form_nuevo_prod"):
                p1, p2 = st.columns(2)
                with p1:
                    np_nom    = st.text_input("Nombre")
                    np_cat    = st.selectbox("Categoria", ["Bebidas","Comidas","Snacks","Otro"])
                    np_precio = st.number_input("Precio ($)", min_value=0.0, value=2.0, step=0.25)
                with p2:
                    np_stock  = st.number_input("Stock Inicial", min_value=0, value=10)
                    np_activo = st.checkbox("Activo", value=True)
                    np_img    = st.file_uploader("Foto (opcional)", type=["png","jpg","jpeg"])
                if st.form_submit_button("Agregar Producto", type="primary"):
                    if np_nom:
                        img_bytes = np_img.read() if np_img else None
                        nid = complejo["next_bar_id"]
                        st.session_state.complejos[complejo_id]["bar"].append({
                            "id":nid,"nombre":np_nom,"categoria":np_cat,
                            "precio":np_precio,"stock":np_stock,"activo":np_activo,"imagen":img_bytes
                        })
                        st.session_state.complejos[complejo_id]["next_bar_id"] += 1
                        st.success(f"Producto '{np_nom}' agregado.")
                        st.rerun()
                    else:
                        st.error("El nombre es obligatorio.")
        st.divider()
        cats_list  = ["Bebidas","Comidas","Snacks","Otro"]
        categorias = sorted(set(p["categoria"] for p in complejo["bar"]))
        for cat in categorias:
            st.markdown(f"#### {cat}")
            for prod in [p for p in complejo["bar"] if p["categoria"] == cat]:
                idx_g = next(k for k, x in enumerate(complejo["bar"]) if x["id"] == prod["id"])
                with st.container(border=True):
                    cp1,cp2,cp3,cp4,cp5 = st.columns([0.7,2.5,1.2,2,0.8])
                    with cp1:
                        if prod.get("imagen"): st.image(prod["imagen"], width=55)
                        else: st.markdown("<div style='font-size:1.8rem;text-align:center'>🛒</div>", unsafe_allow_html=True)
                    with cp2:
                        st.write(f"{'🟢' if prod['activo'] else '🔴'} **{prod['nombre']}**")
                        st.caption(prod["categoria"])
                    with cp3:
                        st.write(f"💲 **${prod['precio']:.2f}**")
                    with cp4:
                        nuevo_stock = st.number_input(f"Stock {prod['nombre']}", min_value=0, value=prod["stock"],
                                                      key=f"sk_{complejo_id}_{prod['id']}", label_visibility="collapsed")
                        if nuevo_stock != prod["stock"]:
                            st.session_state.complejos[complejo_id]["bar"][idx_g]["stock"] = nuevo_stock
                        st.caption(f"Stock: {prod['stock']} uds")
                    with cp5:
                        if st.button("✏️", key=f"ed_p_{complejo_id}_{prod['id']}", help="Editar"):
                            k = f"show_ep_{complejo_id}_{prod['id']}"
                            st.session_state[k] = not st.session_state.get(k, False)
                if st.session_state.get(f"show_ep_{complejo_id}_{prod['id']}", False):
                    with st.container(border=True):
                        st.markdown(f"**Editando: {prod['nombre']}**")
                        with st.form(f"form_ep_{complejo_id}_{prod['id']}"):
                            ep1,ep2 = st.columns(2)
                            with ep1:
                                e_pn  = st.text_input("Nombre", value=prod["nombre"])
                                e_pc  = st.selectbox("Categoria", cats_list, index=cats_list.index(prod["categoria"]) if prod["categoria"] in cats_list else 3)
                                e_pp  = st.number_input("Precio ($)", min_value=0.0, value=prod["precio"], step=0.25)
                            with ep2:
                                e_ps  = st.number_input("Stock", min_value=0, value=prod["stock"])
                                e_pa  = st.checkbox("Activo", value=prod["activo"])
                                e_pi  = st.file_uploader("Cambiar Foto", type=["png","jpg","jpeg"])
                            eps, epd = st.columns(2)
                            with eps:
                                if st.form_submit_button("💾 Guardar", type="primary", use_container_width=True):
                                    img_nueva = e_pi.read() if e_pi else prod.get("imagen")
                                    st.session_state.complejos[complejo_id]["bar"][idx_g].update({
                                        "nombre":e_pn,"categoria":e_pc,"precio":e_pp,
                                        "stock":e_ps,"activo":e_pa,"imagen":img_nueva
                                    })
                                    st.session_state[f"show_ep_{complejo_id}_{prod['id']}"] = False
                                    st.success("Producto actualizado.")
                                    st.rerun()
                            with epd:
                                if st.form_submit_button("🗑️ Eliminar", use_container_width=True):
                                    st.session_state.complejos[complejo_id]["bar"].pop(idx_g)
                                    st.session_state[f"show_ep_{complejo_id}_{prod['id']}"] = False
                                    st.rerun()

    with tab5:
        st.subheader("Horarios de Atencion")
        horarios = complejo["horarios"]
        with st.form("form_horarios"):
            h1,h2,h3,h4 = st.columns([1.5,1,1.5,1.5])
            h1.markdown("**Dia**"); h2.markdown("**Abierto**")
            h3.markdown("**Apertura**"); h4.markdown("**Cierre**")
            st.divider()
            cambios = {}
            for dia, datos in horarios.items():
                d1,d2,d3,d4 = st.columns([1.5,1,1.5,1.5])
                with d1: st.write(f"**{dia}**")
                with d2: abierto  = st.checkbox("", value=datos["abierto"], key=f"ho_{complejo_id}_{dia}")
                with d3: apertura = st.text_input("", value=datos["apertura"], key=f"hap_{complejo_id}_{dia}", placeholder="08:00")
                with d4: cierre   = st.text_input("", value=datos["cierre"],   key=f"hci_{complejo_id}_{dia}", placeholder="22:00")
                cambios[dia] = {"abierto":abierto,"apertura":apertura,"cierre":cierre}
            st.divider()
            if st.form_submit_button("💾 Guardar Horarios", type="primary"):
                st.session_state.complejos[complejo_id]["horarios"] = cambios
                st.success("Horarios actualizados.")
                st.rerun()
        st.divider()
        st.caption("**Resumen semanal:**")
        cols_h = st.columns(7)
        for idx, (dia, datos) in enumerate(horarios.items()):
            with cols_h[idx]:
                with st.container(border=True):
                    st.markdown(f"<div style='text-align:center'><b>{dia[:3]}</b></div>", unsafe_allow_html=True)
                    if datos["abierto"]:
                        st.markdown(f"<div style='text-align:center;color:#00e676;font-size:0.75rem'>{datos['apertura']}<br>↕<br>{datos['cierre']}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown("<div style='text-align:center;color:#ff4b4b;font-size:0.8rem'>Cerrado</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align:center;padding:24px;color:#3a5a70;font-size:12px;
            border-top:1px solid rgba(0,230,118,0.08);margin-top:40px;">
  © 2024 Mi Canchita · Todos los derechos reservados
</div>
""", unsafe_allow_html=True)
