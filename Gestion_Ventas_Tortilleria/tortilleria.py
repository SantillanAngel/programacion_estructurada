from datetime import datetime
from db_conexion import conectar
from decimal import Decimal

def obtener_clientes():
    conexion = conectar()
    clientes = []
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT id, nombre FROM clientes")
            clientes = cursor.fetchall()
        except Exception as e:
            print(f"❌Error al obtener clientes: {e}")
        finally:
            cursor.close()
            conexion.close()
    return clientes

def seleccionar_cliente_automatico():
    clientes = obtener_clientes()
    if not clientes:
        print("No hay clientes registrados. Debes registrar uno primero.")
        return registrar_cliente()

    print("\n--- Clientes disponibles ---")
    for cliente in clientes:
        print(f"- {cliente['nombre']}")

    while True:
        nombre = input("Ingrese el nombre del cliente o 'N' para registrar uno nuevo: ").strip()
        if nombre.lower() == 'n':
            return registrar_cliente()
        for cliente in clientes:
            if cliente['nombre'].lower() == nombre.lower():
                return cliente['id']
        print("Cliente no encontrado. Intente de nuevo o registre uno nuevo (N).")

def registrar_cliente():
    conexion = conectar()
    if conexion:
        try:
            nombre = input("Ingrese el nombre del cliente: ").strip()
            telefono = input("Ingrese teléfono (opcional): ").strip()
            email = input("Ingrese email (opcional): ").strip()

            cursor = conexion.cursor()
            sql = "INSERT INTO clientes (nombre, telefono, email) VALUES (%s, %s, %s)"
            cursor.execute(sql, (nombre, telefono or None, email or None))
            conexion.commit()
            print(f"✅ Cliente '{nombre}' registrado correctamente con ID {cursor.lastrowid}.")
            return cursor.lastrowid
        except Exception as e:
            print(f"❌Error al registrar cliente: {e}")
        finally:
            cursor.close()
            conexion.close()
    return None

def obtener_productos():
    conexion = conectar()
    productos = {}
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre, precio FROM productos")
            resultados = cursor.fetchall()
            for id, nombre, precio in resultados:
                productos[id] = {"nombre": nombre, "precio": float(precio)}
        except Exception as e:
            print(f"❌Error al obtener productos: {e}")
        finally:
            cursor.close()
            conexion.close()
    return productos

def registrar_venta():
    cliente_id = seleccionar_cliente_automatico()
    if cliente_id is None:
        print("❌No se pudo seleccionar ni registrar cliente. Venta cancelada.")
        return

    carrito = []
    productos = obtener_productos()
    if not productos:
        print("❌No hay productos disponibles para la venta.❌")
        return

    while True:
        print("\n---📂 PRODUCTOS DISPONIBLES 📂---")
        for pid, prod in productos.items():
            print(f"{pid}. {prod['nombre']} - ${prod['precio']} por kilo")
        try:
            producto_id = int(input("📝 Seleccione el número del producto: "))
            if producto_id not in productos:
                print("❌Producto no válido.❌")
                continue

            kilos = float(input("📝 Ingrese la cantidad en kilos: "))
            if kilos <= 0:
                print("❌Cantidad no válida.❌")
                continue

            producto = productos[producto_id]
            total = kilos * producto["precio"]

            carrito.append({
                "producto_id": producto_id,
                "producto": producto["nombre"],
                "kilos": kilos,
                "precio_unitario": producto["precio"],
                "total": total
            })

            seguir = input("¿Desea agregar otro producto? (Si/No): ").lower()
            if seguir != 'si':
                break
        except ValueError:
            print("❌Entrada no válida.❌")

    if not carrito:
        print("❌No hay productos para registrar.❌")
        return

    print("\n--- Resumen de la venta ---")
    total_general = 0
    for i, item in enumerate(carrito, 1):
        print(f"{i}. {item['producto']}: {item['kilos']} kg x ${item['precio_unitario']} = ${item['total']:.2f}")
        total_general += item['total']
    print(f"Total general: ${total_general:.2f}")

    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            fecha = datetime.now()
            for item in carrito:
                sql = "INSERT INTO ventas (fecha, cliente_id, producto_id, kilos, precio_unitario, total) VALUES (%s, %s, %s, %s, %s, %s)"
                valores = (fecha, cliente_id, item['producto_id'], item['kilos'], item['precio_unitario'], item['total'])
                cursor.execute(sql, valores)
            conexion.commit()
            print("✅ Venta registrada correctamente.")
        except Exception as e:
            print(f"❌Error al registrar la venta: {e}")
        finally:
            cursor.close()
            conexion.close()


def obtener_productos():
    conexion = conectar()
    productos = {}
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre, precio FROM productos")
            resultados = cursor.fetchall()
            for id, nombre, precio in resultados:
                productos[id] = {"nombre": nombre, "precio": float(precio)}
        except Exception as e:
            print(f"❌Error al obtener productos: {e}")
        finally:
            cursor.close()
            conexion.close()
    return productos

def mostrar_ventas():
    conexion = conectar()
    if conexion:
        cursor = conexion.cursor()
        fecha_input = input("Ingrese la fecha (YYYY-MM-DD) para consultar ventas: ").strip()
        try:
            cursor.execute("SELECT id, fecha, producto_id, kilos, precio_unitario, total FROM ventas WHERE DATE(fecha) = %s", (fecha_input,))
            resultados = cursor.fetchall()
            if resultados:
                total_general = 0
                print("\n---🕒 HISTORIAL DE VENTAS ---")
                print("IDs de ventas encontradas ese día:")
                for venta in resultados:
                    id_venta, fecha, producto_id, kilos, precio_unitario, total = venta
                    print(f"ID: {id_venta}")
                print("\nDetalles:")
                for venta in resultados:
                    id_venta, fecha, producto_id, kilos, precio_unitario, total = venta
                    print(f"{id_venta}. {fecha} - Producto ID {producto_id}: {kilos} kg a ${precio_unitario}/kg = ${total}")
                    total_general += total
                print(f"\nTotal vendido ese día: ${total_general:.2f}")
            else:
                print("❌No hay ventas en esa fecha.❌")
        except Exception as e:
            print(f"❌Error al consultar ventas: {e}")
        finally:
            cursor.close()
            conexion.close()

def borrar_venta():
    conexion = conectar()
    if conexion:
        cursor = conexion.cursor()
        try:
            print("=== IDs de ventas disponibles ===")
            cursor.execute("SELECT id FROM ventas")
            ids_disponibles = cursor.fetchall()

            if not ids_disponibles:
                print("No hay ventas registradas.")
                return

            print(" ".join([str(id_venta[0]) for id_venta in ids_disponibles]))
            print("---------------------------------")

            id_venta = int(input("Ingrese el ID de la venta a borrar: "))
            
            # Nuevo: Confirmación antes de borrar
            confirmacion = input(f"¿Está seguro que desea borrar la venta con ID {id_venta}? (s/n): ")
            if confirmacion.lower() == 's':
                cursor.execute("DELETE FROM ventas WHERE id = %s", (id_venta,))
                if cursor.rowcount > 0:
                    conexion.commit()
                    print("✅Venta eliminada correctamente.")
                else:
                    print("❌No se encontró la venta.❌")
            else:
                print("Operación cancelada.")

        except Exception as e:
            print(f"❌Error: {e}")
        finally:
            cursor.close()
            conexion.close()

def modificar_venta():
    conexionBD = conectar()
    if conexionBD:
        try:
            cursor = conexionBD.cursor()
            
            print("=== IDs de ventas disponibles ===")
            cursor.execute("SELECT id FROM ventas")
            ids_disponibles = cursor.fetchall()
            
            if not ids_disponibles:
                print("No hay ventas registradas.")
                return

            print(" ".join([str(id_venta[0]) for id_venta in ids_disponibles]))
            print("---------------------------------")

            id_venta = int(input("Ingrese el ID de la venta a modificar: "))
            
            cursor.execute("SELECT * FROM ventas WHERE id = %s", (id_venta,))
            venta = cursor.fetchone()

            if venta:
                print("\n=== Información de la venta actual ===")
                print(f"ID venta: {venta[0]}")
                print(f"Fecha: {venta[1]}")
                print(f"Cliente ID: {venta[2]}")
                print(f"Producto ID: {venta[3]}")
                print(f"Kilos: {venta[4]}")
                print(f"Precio unitario: {venta[5]}")
                print(f"Total: {venta[6]}")

                try:
                    nuevo_kilos = Decimal(input("Nuevo valor de kilos: "))
                    precio_unitario = Decimal(venta[5])
                    nuevo_total = nuevo_kilos * precio_unitario
                except (ValueError, TypeError):
                    print("❌ Entrada no válida para los kilos. Por favor, ingrese un número.")
                    return

                cursor.execute("UPDATE ventas SET kilos=%s, total=%s WHERE id=%s",
                               (nuevo_kilos, nuevo_total, id_venta))
                conexionBD.commit()
                print("✅ Venta modificada correctamente.")
            else:
                print("❌ No se encontró la venta con ese ID.")
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            if conexionBD:
                conexionBD.close()

def registrar_producto():
    conexionBD = conectar()
    if conexionBD:
        try:
            nombre = input("Ingrese el nombre del nuevo producto: ").strip()
            precio = Decimal(input("Ingrese el precio por kilo: "))
            cursor = conexionBD.cursor()
            cursor.execute("INSERT INTO productos (nombre, precio) VALUES (%s, %s)",
                           (nombre, precio))
            conexionBD.commit()
            print("✅ Producto registrado correctamente.")
        except Exception as e:
            print(f"❌ Error al registrar producto: {e}")
        finally:
            conexionBD.close()

def registrar_cliente():
    conexion = conectar()
    if conexion:
        try:
            nombre = input("Ingrese el nombre del cliente: ").strip()
            telefono = input("Ingrese teléfono (opcional): ").strip()
            email = input("Ingrese email (opcional): ").strip()

            cursor = conexion.cursor()
            sql = "INSERT INTO clientes (nombre, telefono, email) VALUES (%s, %s, %s)"
            cursor.execute(sql, (nombre, telefono or None, email or None))
            conexion.commit()
            print(f"✅ Cliente '{nombre}' registrado correctamente con ID {cursor.lastrowid}.")
            return cursor.lastrowid
        except Exception as e:
            print(f"❌Error al registrar cliente: {e}")
        finally:
            cursor.close()
            conexion.close()
    return None

def seleccionar_cliente():
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre FROM clientes")
            clientes = cursor.fetchall()
            if not clientes:
                print("No hay clientes registrados. Debes registrar uno primero.")
                return registrar_cliente()

            print("\n--- Clientes disponibles ---")
            for cid, nombre in clientes:
                print(f"{cid}. {nombre}")

            while True:
                opcion = input("Ingrese el ID del cliente o 'N' para registrar uno nuevo: ").strip()
                if opcion.lower() == 'n':
                    return registrar_cliente()
                elif opcion.isdigit():
                    cliente_id = int(opcion)
                    if any(c[0] == cliente_id for c in clientes):
                        return cliente_id
                    else:
                        print("ID no válido, intente de nuevo.")
                else:
                    print("Entrada no válida.")
        except Exception as e:
            print(f"❌Error al consultar clientes: {e}")
        finally:
            cursor.close()
            conexion.close()
    return None

def mostrar_compras_por_cliente():
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT id, nombre FROM clientes")
            clientes = cursor.fetchall()
            if not clientes:
                print("No hay clientes registrados.")
                return

            print("\n--- Clientes disponibles ---")
            for cliente in clientes:
                print(f"- {cliente['nombre']}")

            while True:
                nombre_cliente = input("Ingrese el nombre del cliente para ver sus compras o 'N' para registrar uno nuevo: ").strip()
                if nombre_cliente.lower() == 'n':
                    cliente_id = registrar_cliente()
                    if cliente_id is None:
                        print("No se pudo registrar el cliente.")
                        return
                    break
                else:
                    cliente = next((c for c in clientes if c['nombre'].lower() == nombre_cliente.lower()), None)
                    if cliente:
                        cliente_id = cliente['id']
                        break
                    else:
                        print("Cliente no encontrado. Intente de nuevo o registre uno nuevo (N).")

            cursor.execute("""
                SELECT fecha, producto_id, kilos, precio_unitario, total 
                FROM ventas WHERE cliente_id = %s ORDER BY fecha DESC
            """, (cliente_id,))
            ventas = cursor.fetchall()

            if ventas:
                print(f"\nCompras del cliente '{nombre_cliente}':")
                for venta in ventas:
                    print(f"{venta['fecha']} - Producto ID {venta['producto_id']}: {venta['kilos']} kg x ${venta['precio_unitario']} = ${venta['total']}")

            else:
                print("El cliente no tiene compras registradas.")
        except Exception as e:
            print(f"❌Error al consultar compras: {e}")
        finally:
            cursor.close()
            conexion.close()
