from tortilleria import registrar_venta, mostrar_ventas, borrar_venta, modificar_venta, mostrar_compras_por_cliente, registrar_cliente, registrar_producto

def menu():
    while True:
        print("\n===🎉🎉 SISTEMA DE VENTAS - TORTILLERÍA 🎉🎉===")
        print("1.📂 Registrar venta")
        print("2.🔍 Mostrar historial de ventas por fecha")
        print("3.🗂️ Mostrar compras por cliente")
        print("4.➕ Registrar nuevo cliente")
        print("5.🗑️ Borrar una venta por ID")
        print("6.✏️ Modificar una venta por ID")
        print("7.📦 Registrar nuevo producto")
        print("8.📛 Salir")

        opcion = input("📝 Seleccione una opción: ")
        if opcion == '1':
            registrar_venta()
        elif opcion == '2':
            mostrar_ventas()
        elif opcion == '3':
            mostrar_compras_por_cliente()
        elif opcion == '4':
            registrar_cliente()
        elif opcion == '5':
            borrar_venta()
        elif opcion == '6':
            modificar_venta()
        elif opcion == "7":
            registrar_producto()
        elif opcion == "8":
            break
    else:
            print("❌Opción no válida.❌")

if __name__ == "__main__":
    menu()