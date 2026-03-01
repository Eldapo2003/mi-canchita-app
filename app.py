# ==========================================
# CONFIGURACIÓN DEL ESTABLECIMIENTO
# ==========================================
nombre_app = "Mi Canchita App"
precio_cancha_hora = 20.0
precio_parqueo_hora = 2.0

# Precios del Bar
precios_bar = {
    "cola": 1.50,
    "agua": 1.00,
    "cerveza": 3.00,
    "salchipapa": 5.00
}

# ==========================================
# INICIO DEL PROGRAMA (INTERFAZ)
# ==========================================
print(f"\n--- BIENVENIDO A {nombre_app.upper()} ---")
print("------------------------------------------")

# Datos del Cliente
cliente = input("Nombre del cliente: ")
horas = int(input(f"¿Cuántas horas desea reservar la cancha? ($ {precio_cancha_hora}/h): "))

# Gestión de Parqueo
usa_parqueo = input("¿Necesita espacio de parqueadero? (si/no): ").lower()

# Gestión del Bar (Ejemplo simple de un item)
print("\n--- MENÚ DEL BAR ---")
print("Productos disponibles: Cola, Agua, Cerveza, Salchipapa")
pedido_bar = input("¿Desea agregar algún producto? (Escriba el nombre o 'no'): ").lower()

# ==========================================
# LÓGICA DE CÁLCULOS
# ==========================================
subtotal_cancha = horas * precio_cancha_hora
total_parqueo = 0
total_bar = 0

if usa_parqueo == "si":
    total_parqueo = horas * precio_parqueo_hora

if pedido_bar in precios_bar:
    total_bar = precios_bar[pedido_bar]
    print(f">> {pedido_bar.capitalize()} agregada al pedido.")

total_final = subtotal_cancha + total_parqueo + total_bar

# ==========================================
# RESUMEN DE RESERVA
# ==========================================
print(f"\n==========================================")
print(f"RESUMEN DE RESERVA - {nombre_app}")
print(f"==========================================")
print(f"Cliente: {cliente}")
print(f"Tiempo: {horas} hora(s)")
print(f"Costo Cancha: ${subtotal_cancha:.2f}")

if total_parqueo > 0:
    print(f"Costo Parqueo: ${total_parqueo:.2f}")

if total_bar > 0:
    print(f"Consumo Bar ({pedido_bar}): ${total_bar:.2f}")

print(f"------------------------------------------")
print(f"TOTAL A PAGAR: ${total_final:.2f}")
print(f"==========================================\n")