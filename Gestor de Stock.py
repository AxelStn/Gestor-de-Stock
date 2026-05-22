import random
from functools import reduce
import re

#Funcion Para añadur un correo
def validar_usuario():
    """
    Función: validar_usuario
    Propósito: Asegura que el usuario ingrese una cadena de texto con una estructura 
    válida antes de permitir el despliegue del menú principal del programa.
    """

    print("\n===== INICIO DE SESION =====")

    #Se le pide un correo electrónico al usuario
    mail = input("Ingrese su correo electrónico: ")
    patron = r"^\w+@\w+\.[a-z]{2,}$" 

    #Valida que los datos de ingreso, concuerden con los caracteres de una cuenta oficial. 
    while not re.match(patron, mail):
        print("Correo inválido. Intente nuevamente.")
        mail = input("Ingrese su correo electrónico: ")

    print("\nCorreo validado correctamente")
    return mail


def cargar_datos(stock):
    """
    Función: cargar_datos
    Propósito: cargar un nuevo producto en la matriz stock.
    Genera un ID aleatorio y valida los datos ingresados.
    """    

    print("\n===== CARGAR DATOS =====")

    id = random.randint(100, 999)

    #Genera otro ID si el anterior ya existe en la matriz
    while id in [producto["id"] for producto in stock]:
        print("\nID repetido, generando otro...")
        id = random.randint(100, 999)

    nombre = input("Ingresar nombre: ")

    #Verifica que el nombre no se repita
    while nombre in [producto["nombre"] for producto in stock]:
        print("Nombre repetido")
        nombre = input("Reingresar nombre: ")

    precio = input("Precio por unidad: ")

    #Validación de precio en float con expresiones regulares
    while not re.match(r"^\d+(\.\d+)?$", precio) or float(precio) < 1:
        print("El precio es invalido")
        precio = input("Precio por unidad: ")

    precio = float(precio)

    cantidad = input("Cantidad: ")

    #Validación de cantidad con expresiones regulares
    while not re.match(r"^\d+$", cantidad) or int(cantidad) < 1:
        print("La cantidad debe ser un número entero mayor a 0")
        cantidad = input("Cantidad: ")

    cantidad = int(cantidad)
    
    #Agrega el producto al diccionario
    stock.append({
        "id": id,
        "nombre": nombre,
        "precio": precio,
        "cantidad": cantidad
    })

    print(f"\nProducto cargado correctamente - ID: {id}")


def actualizar_producto(stock):
    """
    Función: actualizar_producto
    Propósito: buscar un producto por ID y permitir actualizar
    su precio o su cantidad.
    """

    print("\n===== ACTUALIZAR DATOS =====")

    #Verifica que existan productos cargados
    if len(stock) == 0:
        print("No hay productos")
        return

    id_buscar = input("ID a modificar: ")

    #Validacion ID con expresiones regulares
    while not re.match(r"^\d+$", id_buscar):
        print("ID inválido")
        id_buscar = input("ID a modificar: ")

    id_buscar = int(id_buscar)

    #Recorre la matriz para encontrar el producto
    for producto in stock:

        if producto["id"] == id_buscar:

            while True:

                print("1. Actualizar precio")
                print("2. Actualizar cantidad")
                print("0. Salir al menú principal")

                opcion = input("\nOpcion: ")
                
                #Valdicaion para actualizar precio y cantidad
                if opcion == "1":

                    print("\n===== PRECIO =====")

                    nuevo_precio = input("Nuevo precio: ")

                    #Valida el nuevo precio
                    while not re.match(r"^\d+(\.\d+)?$", nuevo_precio) or float(nuevo_precio) < 1:
                        print("Precio inválido, ingrese nuevamente")
                        nuevo_precio = input("Nuevo precio: ")

                    producto["precio"] = float(nuevo_precio)

                    print("Precio actualizado correctamente")

                elif opcion == "2":

                    print("\n===== CANTIDAD =====")

                    nueva_cantidad = input("Nueva cantidad: ")

                    #Valida la nueva cantidad de productos
                    while not re.match(r"^\d+$", nueva_cantidad) or int(nueva_cantidad) < 1:
                        print("Cantidad inválida, ingrese nuevamente")
                        nueva_cantidad = input("Nueva cantidad: ")

                    producto["cantidad"] = int(nueva_cantidad)

                    print("Cantidad actualizada correctamente")
                
                elif opcion == "0":
                    print("Saliendo al menú...")
                    return

                else:
                    print("Opción no reconocida")

    print("ID no encontrado")


def ordenar_productos(stock):
    """
    Función: ordenar_productos
    Propósito: ordenar los productos de menor a mayor
    según precio o cantidad.
    """

    print("\n ==== ORDENAR STOCK ====")

    # Verifica que existan productos cargados
    if not stock:
        print("No hay productos ingresados")
        return
    
    while True:

        print("\n== ORDENAR DE MENOR A MAYOR ==")
        print("1. Ordenar precio por unidad")
        print("2. Ordenar por cantidad")
        print("0. Volver al menú")

        opcion = input("Opción: ")

        if opcion == "1":

            stock.sort(key=lambda producto: producto["precio"])

            print("== Lista ordenada - PRECIO de menor a mayor ==")

            for producto in stock:

                print(f"ID: {producto['id']} - Nombre: {producto['nombre']} - Precio por unidad: {producto['precio']} - Cantidad: {producto['cantidad']} ")

        elif opcion == "2":

            stock.sort(key=lambda producto: producto["cantidad"])

            print("== Lista ordenada - CANTIDAD de menor a mayor ==")

            for producto in stock:

                print(f"ID: {producto['id']} - Nombre: {producto['nombre']} - Precio por unidad: {producto['precio']} - Cantidad: {producto['cantidad']} ")

        elif opcion == "0":
            print("Volviendo al menú...")
            return

        else:
            print("Opción no reconocida")


def mostrar_productos(stock):
    """
    Función: mostrar_productos
    Propósito: mostrar todos los productos cargados en la matriz.
    """
    
    #Verifica que existan productos cargados
    if not stock:
        print("No hay productos")
        return

    print("\n===== LISTA DE PRODUCTOS =====")

    for producto in stock:

        print("-----------------------------")
        print("ID:", producto["id"])
        print("Nombre:", producto["nombre"])
        print("Precio por unidad:", producto["precio"])
        print("Cantidad:", producto["cantidad"])

    print("-----------------------------")


def buscar_producto(stock):
    """
    Función: buscar_producto
    Propósito: buscar un producto por su ID y mostrarlo si existe.
    """

    print("\n===== BUSCAR PRODUCTOS =====")
    
    #Verifica que existan productos cargados
    if not stock:
        print("No hay productos")
        return
    
    id_buscar = input("ID a buscar: ")

    #Validacion while para actualizar un producto 
    while not re.match(r"^\d+$", id_buscar):
        print("ID inválido")
        id_buscar = input("ID: ")

    id_buscar = int(id_buscar)

    #Recorre la matriz para buscar el producto
    for producto in stock:

        if producto["id"] == id_buscar:

            print("ID:", producto["id"])
            print("Nombre:", producto["nombre"])
            print("Precio por unidad:", producto["precio"])
            print("Cantidad:", producto["cantidad"])

            return

    print("No encontrado")


def obtener_precios(stock):
    """
    Función: obtener_precios
    Propósito: generar una lista con los precios de todos los productos.
    Utiliza map y lambda para recorrer la matriz y extraer la columna de precios.
    """

    return list(map(lambda p: p["precio"], stock))


def estadisticas(stock):
    """
    Función: estadisticas
    Propósito: calcular y mostrar estadísticas básicas del sistema.
    Incluye suma total, precio mínimo, máximo y promedio.
    """

    # Verifica que existan productos cargados
    if not stock:
        print("No hay datos")
        return

    # Obtiene la lista de precios usando la función anterior
    precios = obtener_precios(stock)

    # Calcula la suma total de precios usando reduce
    # acc = acumulador, x = valor actual
    suma = reduce(lambda acc, x: acc + x, precios, 0)

    # Obtiene el precio mínimo y máximo
    minimo = min(precios)
    maximo = max(precios)

    # Calcula el promedio de precios
    promedio = suma / len(precios)

    # Muestra los resultados
    print("===== ESTADISTICAS =====")
    print("Precio minimo:", minimo)
    print("Precio maximo:", maximo)
    print("Promedio:", int(promedio))
    print("Suma de precios:", suma)


def estadisticas_especificas(stock):
    """
    Función: estadisticas_especificas
    Propósito: mostrar los productos cuya cantidad sea menor a 5.
    Utiliza filter y lambda para filtrar la matriz.
    """

    print("\n===== PRODUCTOS MENORES A 5 =====")
    
    #Verifica que existan productos cargados
    if not stock:
        print("No hay productos")
        return

    # Se filtran los productos cuya cantidad es menor a 5
    menores = list(filter(lambda p: p["cantidad"] < 5, stock))

    if len(menores) > 0:

        print("Productos con cantidad menor a 5:")

        for p in menores:

            print(f"ID: {p['id']} - Nombre: {p['nombre']} - Precio por unidad: {p['precio']} - Cantidad: {p['cantidad']} ")

    else:
        print("No hay productos con cantidad menor a 5")


def eliminar_producto(stock):
    """
    Función: eliminar_producto
    Propósito: eliminar un producto de la matriz según su ID.
    Utiliza filter para generar una nueva lista sin el producto indicado.
    """

    print("\n===== ELIMINAR PRODUCTOS =====")
    
    # Verifica que existan productos cargados
    if not stock:
        print("No hay productos")
        return
    
    while True: 

        deseo = input("¿Desea eliminar un producto? 1 = Sí / 0 = No: ")

        if deseo == "1":

            #Validacion con expresiones regulares para eliminar un producto buscando el id
            dato = input("ID a eliminar: ")

            while not re.match(r"^\d+$", dato):
                print("ID inválido")
                dato = input("ID a eliminar: ")

            dato = int(dato)
                
            nuevo = list(filter(lambda p: p["id"] != dato, stock))

            if len(nuevo) == len(stock):
                print("No encontrado")
            else:
                print("Producto eliminado")

            return nuevo

        elif deseo == "0":
            return stock
        
        else:
            print("Comando no reconocido")


def info_funciones():
    """
    Función: info_funciones
    Propósito: mostrar información de las funciones del sistema
    utilizando help().
    """

    print("===== INFORMACION DE FUNCIONES =====")
    print("0. validar_usuario")
    print("1. cargar_datos")
    print("2. actualizar_producto")
    print("3. ordenar_productos")
    print("4. mostrar_productos")
    print("5. buscar_producto")
    print("6. obtener_precios")
    print("7. estadisticas")
    print("8. estadisticas_especificas")
    print("9. eliminar_producto")

    opcion = input("Elija una función: ")

    if opcion == "0":
        help(validar_usuario)
    elif opcion == "1":
        help(cargar_datos)
    elif opcion == "2":
        help(actualizar_producto)
    elif opcion == "3":
        help(ordenar_productos)
    elif opcion == "4":
        help(mostrar_productos)
    elif opcion == "5":
        help(buscar_producto)
    elif opcion == "6":
        help(obtener_precios)
    elif opcion == "7":
        help(estadisticas)
    elif opcion == "8":
        help(estadisticas_especificas)
    elif opcion == "9":
        help(eliminar_producto)
    else:
        print("Opción inválida")


def main():

    #Se crea la lista de stocks
    stock = []

    #Guarda el email ingresado
    usuario_mail = validar_usuario()

    print(f"Bienvenido, {usuario_mail}")

    #Bucle principal del programa que mantiene activo el menu
    while True:

        print("\n====== MENU ======")
        print("1. Cargar producto")
        print("2. Actualizar producto")
        print("3. Ordenar productos (Menor a Mayor)")
        print("4. Mostrar productos")
        print("5. Buscar producto")
        print("6. Estadisticas")
        print("7. Ver productos con cantidad < 5")
        print("8. Eliminar producto")
        print("9. Informacion de funciones")
        print("0. Salir")

        opcion = input("Opcion: ")

        if opcion == "1":
            cargar_datos(stock)

        elif opcion == "2":
            actualizar_producto(stock)

        elif opcion == "3":
            ordenar_productos(stock)

        elif opcion == "4":
            mostrar_productos(stock)

        elif opcion == "5":
            buscar_producto(stock)

        elif opcion == "6":
            estadisticas(stock)

        elif opcion == "7":
            estadisticas_especificas(stock)

        elif opcion == "8":
            stock = eliminar_producto(stock)

        elif opcion == "9":
            info_funciones()
            
        elif opcion == "0":
            print("Programa cerrado")
            break

        else:
            print("Use opciones del menu")

main()