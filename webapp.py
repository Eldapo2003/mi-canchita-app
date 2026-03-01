import streamlit as st
import pandas as pd
from datetime import time

st.set_page_config(page_title="Mi Canchita App", page_icon="⚽", layout="wide")

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

# ─── ESTRUCTURA MULTI-COMPLEJO ────────────────────────────────────────────────
# Cada complejo tiene su propio ID, info, canchas, bar y horarios.
# Cuando un nuevo dueño se registre, se agrega un nuevo entry aqui.
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
                {"id": 1, "nombre": "Cancha Techada (Futbol)",    "tipo": "Futbol", "precio_tipo": "hora",    "precio": 40.0, "descripcion": "Cancha cubierta con iluminacion LED", "activa": True},
                {"id": 2, "nombre": "Cancha Descubierta (Futbol)","tipo": "Futbol", "precio_tipo": "hora",    "precio": 30.0, "descripcion": "Cancha al aire libre",               "activa": True},
                {"id": 3, "nombre": "Cancha Padel #1",            "tipo": "Padel",  "precio_tipo": "persona", "precio":  5.0, "descripcion": "Cancha de padel profesional",         "activa": True},
                {"id": 4, "nombre": "Cancha Padel #2",            "tipo": "Padel",  "precio_tipo": "persona", "precio":  5.0, "descripcion": "Cancha de padel profesional",         "activa": True},
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
# 2. SISTEMA DE LOGIN Y REGISTRO
# ==========================================
if st.session_state.usuario_conectado is None:
    col_l, col_c, col_r = st.columns([1, 1.5, 1])
    with col_c:
        st.title("⚽ Mi Canchita App")
        opcion = st.radio("Selecciona una opcion", ["Ingresar", "Registrarse como Cliente"], horizontal=True)

        if opcion == "Ingresar":
            with st.container(border=True):
                u = st.text_input("Usuario (Nombre Completo)")
                p = st.text_input("Contrasena", type="password")
                if st.button("Entrar", use_container_width=True, type="primary"):
                    if u in st.session_state.usuarios and st.session_state.usuarios[u]["clave"] == p:
                        st.session_state.usuario_conectado = dict(st.session_state.usuarios[u])
                        st.session_state.usuario_conectado["id"] = u
                        st.rerun()
                    else:
                        st.error("Credenciales incorrectas")
        else:
            with st.container(border=True):
                new_u  = st.text_input("Tu Nombre Completo")
                new_p  = st.text_input("Crea una Contrasena", type="password")
                conf_p = st.text_input("Confirma tu Contrasena", type="password")
                if st.button("Finalizar Registro", use_container_width=True):
                    if new_u and new_p == conf_p:
                        st.session_state.usuarios[new_u] = {"clave": new_p, "tipo": "cliente", "nombre": new_u}
                        st.success("Registro exitoso! Ahora puedes ingresar.")
                    else:
                        st.error("Las contrasenas no coinciden o faltan datos.")

        st.divider()
        st.markdown(
            """
            <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border: 1px solid #25d366;
                        padding: 24px; border-radius: 12px; text-align: center;">
                <h4 style="color:#ffffff; margin-bottom:8px; font-size:1.1rem;">🏟️ Eres dueno de un complejo deportivo?</h4>
                <p style="color:#cccccc; margin-bottom:16px; font-size:0.9rem;">Unete a nuestra red y gestiona tus reservas de forma profesional.</p>
                <a href="https://wa.me/593984347607?text=Hola,%20me%20interesa%20contratar%20los%20servicios%20de%20Mi%20Canchita%20App"
                   target="_blank"
                   style="display:inline-block; background-color:#25d366; color:white; padding:12px 28px;
                          text-decoration:none; border-radius:8px; font-weight:bold; font-size:0.95rem;">
                    💬 Contratar Servicios (WhatsApp)
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.stop()

# ==========================================
# 3. INTERFAZ SEGUN ROL
# ==========================================
user = st.session_state.usuario_conectado

st.sidebar.title("Bienvenido")
st.sidebar.write(f"👤 {user['nombre']}")
if st.sidebar.button("Cerrar Sesion"):
    st.session_state.usuario_conectado = None
    st.rerun()

# ==========================================
# VISTA CLIENTE
# ==========================================
if user["tipo"] == "cliente":
    st.header("⚽ Mi Canchita App")

    # ── Dropdown de complejos disponibles ─────────────────────────
    complejos_disponibles = {
        cid: data for cid, data in st.session_state.complejos.items()
    }

    nombres_complejos = {cid: data["info"]["nombre"] for cid, data in complejos_disponibles.items()}

    if not nombres_complejos:
        st.warning("No hay complejos disponibles por el momento.")
        st.stop()

    complejo_seleccionado_nombre = st.selectbox(
        "🏟️ Selecciona un Complejo Deportivo",
        options=list(nombres_complejos.values()),
        index=0
    )

    # Obtener el ID del complejo seleccionado
    complejo_id = next(cid for cid, nom in nombres_complejos.items() if nom == complejo_seleccionado_nombre)
    complejo = complejos_disponibles[complejo_id]
    cfg = complejo["info"]

    # Info del complejo
    with st.container(border=True):
        col_info1, col_info2, col_info3 = st.columns(3)
        col_info1.write(f"**{cfg['nombre']}**")
        col_info1.caption(cfg.get("descripcion", ""))
        col_info2.write(f"📍 {cfg.get('direccion', '')}")
        col_info3.write(f"📞 {cfg.get('telefono', '')}")

    st.divider()

    # ── Reserva ───────────────────────────────────────────────────
    st.subheader("Reserva tu Cancha")
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

        # ── Bar ───────────────────────────────────────────────────
        st.divider()
        st.subheader("🍺 Agregar del Bar (opcional)")
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

        # ── Resumen y confirmar ───────────────────────────────────
        st.divider()
        _, col_res = st.columns([2, 1])
        with col_res:
            with st.container(border=True):
                st.write("**Resumen**")
                st.write(f"Cancha: ${p_base:.2f}")
                if parq:
                    st.write("Parqueadero: $2.00")
                if total_bar > 0:
                    st.write(f"Bar: ${total_bar:.2f}")
                st.subheader(f"Total: ${total:.2f}")

        if st.button("✅ Confirmar Reserva", type="primary"):
            st.session_state.base_reservas.append({
                "Complejo": cfg["nombre"],
                "Cliente":  user["nombre"],
                "Cancha":   cancha_nombre,
                "Fecha":    str(fec),
                "Hora":     str(hor),
                "Total":    total,
                "Estado":   "Pendiente"
            })
            st.success("Reserva enviada correctamente!")
            st.balloons()

# ==========================================
# VISTA ADMINISTRADOR
# ==========================================
else:
    # El admin gestiona el complejo asociado a su cuenta
    complejo_id = user.get("complejo_id", list(st.session_state.complejos.keys())[0])

    # Si por alguna razon no existe, crearlo vacio
    if complejo_id not in st.session_state.complejos:
        st.session_state.complejos[complejo_id] = {
            "info": {"nombre": "Mi Complejo", "direccion": "", "telefono": "", "descripcion": ""},
            "canchas": [], "bar": [], "horarios": {
                "Lunes":     {"abierto": True, "apertura": "08:00", "cierre": "22:00"},
                "Martes":    {"abierto": True, "apertura": "08:00", "cierre": "22:00"},
                "Miercoles": {"abierto": True, "apertura": "08:00", "cierre": "22:00"},
                "Jueves":    {"abierto": True, "apertura": "08:00", "cierre": "22:00"},
                "Viernes":   {"abierto": True, "apertura": "08:00", "cierre": "23:00"},
                "Sabado":    {"abierto": True, "apertura": "07:00", "cierre": "23:00"},
                "Domingo":   {"abierto": True, "apertura": "08:00", "cierre": "20:00"},
            },
            "next_cancha_id": 1, "next_bar_id": 1,
        }

    complejo = st.session_state.complejos[complejo_id]
    cfg      = complejo["info"]

    st.header(f"🛠️ Panel Administrativo — {cfg['nombre']}")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Reservas",
        "🏟️ Establecimiento",
        "⚽ Canchas",
        "🍺 Bar y Productos",
        "🕐 Horarios"
    ])

    # TAB 1: RESERVAS ─────────────────────────────────────────────
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

    # TAB 2: ESTABLECIMIENTO ──────────────────────────────────────
    with tab2:
        st.subheader("Informacion del Establecimiento")
        with st.form("form_establecimiento"):
            nuevo_nombre = st.text_input("Nombre del Establecimiento", value=cfg["nombre"])
            nuevo_dir    = st.text_input("Direccion",                  value=cfg.get("direccion", ""))
            nuevo_tel    = st.text_input("Telefono de Contacto",       value=cfg.get("telefono", ""))
            nueva_desc   = st.text_area("Descripcion del Complejo",    value=cfg.get("descripcion", ""), height=100)

            if st.form_submit_button("💾 Guardar Cambios", type="primary"):
                st.session_state.complejos[complejo_id]["info"].update({
                    "nombre": nuevo_nombre, "direccion": nuevo_dir,
                    "telefono": nuevo_tel,  "descripcion": nueva_desc
                })
                st.success("Informacion actualizada correctamente.")
                st.rerun()

        st.divider()
        st.caption("Vista previa para clientes:")
        with st.container(border=True):
            st.markdown(f"### 🏟️ {cfg['nombre']}")
            st.write(cfg.get("descripcion", ""))
            ci, cd = st.columns(2)
            ci.write(f"📍 {cfg.get('direccion', '')}")
            cd.write(f"📞 {cfg.get('telefono', '')}")

    # TAB 3: CANCHAS ──────────────────────────────────────────────
    with tab3:
        st.subheader("Gestion de Canchas")

        with st.expander("➕ Agregar Nueva Cancha", expanded=False):
            with st.form("form_nueva_cancha"):
                c1, c2 = st.columns(2)
                with c1:
                    nc_nombre      = st.text_input("Nombre de la Cancha")
                    nc_tipo        = st.selectbox("Tipo de Deporte", ["Futbol", "Padel", "Basket", "Tenis", "Volley", "Otro"])
                    nc_desc        = st.text_input("Descripcion corta")
                with c2:
                    nc_precio_tipo = st.selectbox("Tipo de Precio", ["hora", "persona"])
                    nc_precio      = st.number_input("Precio ($)", min_value=0.0, value=20.0, step=0.5)
                    nc_activa      = st.checkbox("Cancha activa", value=True)

                if st.form_submit_button("Agregar Cancha", type="primary"):
                    if nc_nombre:
                        nid = complejo["next_cancha_id"]
                        st.session_state.complejos[complejo_id]["canchas"].append({
                            "id": nid, "nombre": nc_nombre, "tipo": nc_tipo,
                            "precio_tipo": nc_precio_tipo, "precio": nc_precio,
                            "descripcion": nc_desc, "activa": nc_activa
                        })
                        st.session_state.complejos[complejo_id]["next_cancha_id"] += 1
                        st.success(f"Cancha '{nc_nombre}' agregada.")
                        st.rerun()
                    else:
                        st.error("El nombre es obligatorio.")

        st.divider()
        tipos_list = ["Futbol", "Padel", "Basket", "Tenis", "Volley", "Otro"]
        icono_map  = {"Futbol": "⚽", "Padel": "🎾", "Tenis": "🎾", "Basket": "🏀", "Volley": "🏐"}

        for i, cancha in enumerate(complejo["canchas"]):
            with st.container(border=True):
                c_info, c_precio, c_estado, c_accion = st.columns([3, 1.5, 1, 1])
                with c_info:
                    icono = icono_map.get(cancha["tipo"], "🏟️")
                    st.write(f"{icono} **{cancha['nombre']}**")
                    st.caption(f"{cancha['tipo']} | {cancha.get('descripcion','')}")
                with c_precio:
                    st.write(f"💲 **${cancha['precio']:.2f}** / {cancha['precio_tipo']}")
                with c_estado:
                    st.write("🟢 Activa" if cancha["activa"] else "🔴 Inactiva")
                with c_accion:
                    if st.button("✏️ Editar", key=f"ed_c_{complejo_id}_{cancha['id']}"):
                        key = f"show_ec_{complejo_id}_{cancha['id']}"
                        st.session_state[key] = not st.session_state.get(key, False)

            if st.session_state.get(f"show_ec_{complejo_id}_{cancha['id']}", False):
                with st.container(border=True):
                    st.markdown(f"**Editando: {cancha['nombre']}**")
                    with st.form(f"form_ec_{complejo_id}_{cancha['id']}"):
                        ec1, ec2 = st.columns(2)
                        with ec1:
                            e_nom  = st.text_input("Nombre", value=cancha["nombre"])
                            e_tipo = st.selectbox("Tipo", tipos_list,
                                                  index=tipos_list.index(cancha["tipo"]) if cancha["tipo"] in tipos_list else 0)
                            e_desc = st.text_input("Descripcion", value=cancha.get("descripcion", ""))
                        with ec2:
                            e_pt   = st.selectbox("Tipo Precio", ["hora", "persona"],
                                                  index=0 if cancha["precio_tipo"] == "hora" else 1)
                            e_prec = st.number_input("Precio ($)", min_value=0.0, value=cancha["precio"], step=0.5)
                            e_act  = st.checkbox("Activa", value=cancha["activa"])
                        cs, cd_ = st.columns(2)
                        with cs:
                            if st.form_submit_button("💾 Guardar", type="primary", use_container_width=True):
                                st.session_state.complejos[complejo_id]["canchas"][i].update({
                                    "nombre": e_nom, "tipo": e_tipo, "descripcion": e_desc,
                                    "precio_tipo": e_pt, "precio": e_prec, "activa": e_act
                                })
                                st.session_state[f"show_ec_{complejo_id}_{cancha['id']}"] = False
                                st.success("Cancha actualizada.")
                                st.rerun()
                        with cd_:
                            if st.form_submit_button("🗑️ Eliminar", use_container_width=True):
                                st.session_state.complejos[complejo_id]["canchas"].pop(i)
                                st.session_state[f"show_ec_{complejo_id}_{cancha['id']}"] = False
                                st.rerun()

    # TAB 4: BAR Y PRODUCTOS ──────────────────────────────────────
    with tab4:
        st.subheader("Gestion del Bar y Productos")

        with st.expander("➕ Agregar Nuevo Producto", expanded=False):
            with st.form("form_nuevo_prod"):
                p1, p2 = st.columns(2)
                with p1:
                    np_nom    = st.text_input("Nombre del Producto")
                    np_cat    = st.selectbox("Categoria", ["Bebidas", "Comidas", "Snacks", "Otro"])
                    np_precio = st.number_input("Precio ($)", min_value=0.0, value=2.0, step=0.25)
                with p2:
                    np_stock  = st.number_input("Stock Inicial", min_value=0, value=10)
                    np_activo = st.checkbox("Producto activo", value=True)
                    np_img    = st.file_uploader("Foto del Producto (opcional)", type=["png","jpg","jpeg"])

                if st.form_submit_button("Agregar Producto", type="primary"):
                    if np_nom:
                        img_bytes = np_img.read() if np_img else None
                        nid = complejo["next_bar_id"]
                        st.session_state.complejos[complejo_id]["bar"].append({
                            "id": nid, "nombre": np_nom, "categoria": np_cat,
                            "precio": np_precio, "stock": np_stock,
                            "activo": np_activo, "imagen": img_bytes
                        })
                        st.session_state.complejos[complejo_id]["next_bar_id"] += 1
                        st.success(f"Producto '{np_nom}' agregado.")
                        st.rerun()
                    else:
                        st.error("El nombre es obligatorio.")

        st.divider()
        cats_list   = ["Bebidas", "Comidas", "Snacks", "Otro"]
        categorias  = sorted(set(p["categoria"] for p in complejo["bar"]))

        for cat in categorias:
            st.markdown(f"#### {cat}")
            for prod in [p for p in complejo["bar"] if p["categoria"] == cat]:
                idx_g = next(k for k, x in enumerate(complejo["bar"]) if x["id"] == prod["id"])

                with st.container(border=True):
                    cp1, cp2, cp3, cp4, cp5 = st.columns([0.7, 2.5, 1.2, 2, 0.8])
                    with cp1:
                        if prod.get("imagen"):
                            st.image(prod["imagen"], width=55)
                        else:
                            st.markdown("<div style='font-size:1.8rem;text-align:center'>🛒</div>", unsafe_allow_html=True)
                    with cp2:
                        badge = "🟢" if prod["activo"] else "🔴"
                        st.write(f"{badge} **{prod['nombre']}**")
                        st.caption(prod["categoria"])
                    with cp3:
                        st.write(f"💲 **${prod['precio']:.2f}**")
                    with cp4:
                        nuevo_stock = st.number_input(
                            f"Stock {prod['nombre']}", min_value=0, value=prod["stock"],
                            key=f"sk_{complejo_id}_{prod['id']}", label_visibility="collapsed"
                        )
                        if nuevo_stock != prod["stock"]:
                            st.session_state.complejos[complejo_id]["bar"][idx_g]["stock"] = nuevo_stock
                        st.caption(f"Stock: {prod['stock']} uds")
                    with cp5:
                        if st.button("✏️", key=f"ed_p_{complejo_id}_{prod['id']}", help="Editar"):
                            key = f"show_ep_{complejo_id}_{prod['id']}"
                            st.session_state[key] = not st.session_state.get(key, False)

                if st.session_state.get(f"show_ep_{complejo_id}_{prod['id']}", False):
                    with st.container(border=True):
                        st.markdown(f"**Editando: {prod['nombre']}**")
                        with st.form(f"form_ep_{complejo_id}_{prod['id']}"):
                            ep1, ep2 = st.columns(2)
                            with ep1:
                                e_pn   = st.text_input("Nombre", value=prod["nombre"])
                                e_pc   = st.selectbox("Categoria", cats_list,
                                                      index=cats_list.index(prod["categoria"]) if prod["categoria"] in cats_list else 3)
                                e_pp   = st.number_input("Precio ($)", min_value=0.0, value=prod["precio"], step=0.25)
                            with ep2:
                                e_ps   = st.number_input("Stock", min_value=0, value=prod["stock"])
                                e_pa   = st.checkbox("Activo", value=prod["activo"])
                                e_pimg = st.file_uploader("Cambiar Foto", type=["png","jpg","jpeg"])
                            eps, epd = st.columns(2)
                            with eps:
                                if st.form_submit_button("💾 Guardar", type="primary", use_container_width=True):
                                    img_nueva = e_pimg.read() if e_pimg else prod.get("imagen")
                                    st.session_state.complejos[complejo_id]["bar"][idx_g].update({
                                        "nombre": e_pn, "categoria": e_pc, "precio": e_pp,
                                        "stock": e_ps, "activo": e_pa, "imagen": img_nueva
                                    })
                                    st.session_state[f"show_ep_{complejo_id}_{prod['id']}"] = False
                                    st.success("Producto actualizado.")
                                    st.rerun()
                            with epd:
                                if st.form_submit_button("🗑️ Eliminar", use_container_width=True):
                                    st.session_state.complejos[complejo_id]["bar"].pop(idx_g)
                                    st.session_state[f"show_ep_{complejo_id}_{prod['id']}"] = False
                                    st.rerun()

    # TAB 5: HORARIOS ─────────────────────────────────────────────
    with tab5:
        st.subheader("Horarios de Atencion")
        st.caption("Define los dias y horarios en que tu complejo esta disponible para reservas.")
        horarios = complejo["horarios"]

        with st.form("form_horarios"):
            hdr1, hdr2, hdr3, hdr4 = st.columns([1.5, 1, 1.5, 1.5])
            hdr1.markdown("**Dia**"); hdr2.markdown("**Abierto**")
            hdr3.markdown("**Apertura**"); hdr4.markdown("**Cierre**")
            st.divider()
            cambios = {}
            for dia, datos in horarios.items():
                cd1, cd2, cd3, cd4 = st.columns([1.5, 1, 1.5, 1.5])
                with cd1: st.write(f"**{dia}**")
                with cd2: abierto  = st.checkbox("", value=datos["abierto"], key=f"ho_{complejo_id}_{dia}")
                with cd3: apertura = st.text_input("", value=datos["apertura"], key=f"hap_{complejo_id}_{dia}", placeholder="08:00")
                with cd4: cierre   = st.text_input("", value=datos["cierre"],   key=f"hci_{complejo_id}_{dia}", placeholder="22:00")
                cambios[dia] = {"abierto": abierto, "apertura": apertura, "cierre": cierre}
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
                        st.markdown(
                            f"<div style='text-align:center;color:#25d366;font-size:0.75rem'>"
                            f"{datos['apertura']}<br>↕<br>{datos['cierre']}</div>",
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            "<div style='text-align:center;color:#ff4b4b;font-size:0.8rem'>Cerrado</div>",
                            unsafe_allow_html=True
                        )
