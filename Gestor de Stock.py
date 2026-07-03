import random
from functools import reduce
import re
import json

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

    #Se le pedirá al usuario ingresar su DNI.
    dni = input("DNI (8 digitos): ")
    #Validación de cantidad y tipo de carácteres obligatorios.
    while not re.match(r"^\d{8}$", dni):
        print("Error. DNI fuera de rango.")
        dni = input("DNI (8 digitos): ")
    dni = int(dni)
    
    #Se buscará si el DNI ingresado se encuentra registrado en el sistema. 
    existe_nombre = None
    for colaborador in stock:
        #Si el DNI se encuentra en el sistema, se registrará automáticamente con el mismo nombre.
        if colaborador["colaborador"][1] == dni:
            existe_nombre = colaborador["colaborador"][0]
            break
    
    if existe_nombre:
        print(f"¡Hola nuevamente {existe_nombre}!")
        #Se registra con el mismo nombre. 
        name = existe_nombre
    else:
        #Si el DNI no se encuentra registrado, se le pedirá el nombre por primera vez.
        name = input("Nombre del colaborador: ")
        while not re.match(r"^[a-zA-Z\s]+$", name):
            print("Error. Ingrese un nombre válido.")
            name = input("Nombre del colaborador: ")

    #Se crea la tupla en base al Nombre y DNI del colaborador      
    colaborador = tuple([name, dni])

    id = random.randint(100, 999)
    #Genera otro ID si el anterior ya existe en la matriz
    while id in [producto["id"] for producto in stock]:
        print("\nID repetido, generando otro...")
        id = random.randint(100, 999)

    nombre = input("Ingresar nombre del producto: ")
    #Verifica que el nombre no se repita
    while nombre in [producto["nombre"] for producto in stock]:
        print("Producto repetido")
        nombre = input("Reingresar nombre del producto: ")

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
        "colaborador": colaborador,
        "id": id,
        "nombre": nombre,
        "precio": precio,
        "cantidad": cantidad
    })

    #Se abre el archivo json
    archivo = open("personas.json", "w")
    json.dump(stock, archivo, indent=4)
    archivo.close()
    
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

                try:
                    opcion = int(input("\nOpcion: "))
                    
                    #Valdicaion para actualizar precio y cantidad
                    if opcion == 1:

                        print("\n===== PRECIO =====")

                        nuevo_precio = input("Nuevo precio: ")
                        #Valida el nuevo precio
                        while not re.match(r"^\d+(\.\d+)?$", nuevo_precio) or float(nuevo_precio) < 1:
                            print("Precio inválido, ingrese nuevamente")
                            nuevo_precio = input("Nuevo precio: ")
                        producto["precio"] = float(nuevo_precio)

                        archivo = open("personas.json", "w")
                        json.dump(stock, archivo, indent=4)
                        archivo.close()

                        print("Precio actualizado correctamente")

                    elif opcion == 2:

                        print("\n===== CANTIDAD =====")
                        nueva_cantidad = input("Nueva cantidad: ")
                        #Valida la nueva cantidad de productos
                        while not re.match(r"^\d+$", nueva_cantidad) or int(nueva_cantidad) < 1:
                            print("Cantidad inválida, ingrese nuevamente")
                            nueva_cantidad = input("Nueva cantidad: ")
                        producto["cantidad"] = int(nueva_cantidad)

                        archivo = open("personas.json", "w")
                        json.dump(stock, archivo, indent=4)
                        archivo.close()

                        print("Cantidad actualizada correctamente")
                    
                    elif opcion == 0:
                        print("Saliendo al menú...")
                        return

                    else:
                        print("Seleccionar una opción sugerida.")
                
                except ValueError:
                    print("Error. Ingrese valores númericos.")
            
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

        try:
            opcion = int(input("\nOpción: "))
            
            if opcion == 1:

                stock.sort(key=lambda producto: producto["precio"])

                print("== Lista ordenada - PRECIO de menor a mayor ==")

                for producto in stock:
                    print("-----------------------------")
                    nombre_colab = producto["colaborador"][0]
                    dni_colab = producto["colaborador"][1]

                    print(f"Colaborador: {nombre_colab} - DNI: {dni_colab}")
                    print(f"ID: {producto['id']} - Nombre del producto: {producto['nombre']} - Precio por unidad: {producto['precio']} - Cantidad: {producto['cantidad']} ")
                print("-----------------------------")

            elif opcion == 2:

                stock.sort(key=lambda producto: producto["cantidad"])

                print("== Lista ordenada - CANTIDAD de menor a mayor ==")

                for producto in stock:

                    print("-----------------------------")
                    nombre_colab = producto["colaborador"][0]
                    dni_colab = producto["colaborador"][1]

                    print(f"Colaborador: {nombre_colab} - DNI: {dni_colab}")
                    print(f"ID: {producto['id']} - Nombre del producto: {producto['nombre']} - Precio por unidad: {producto['precio']} - Cantidad: {producto['cantidad']} ")
                print("-----------------------------")

            elif opcion == 0:
                print("Volviendo al menú...")
                return

            else:
                print("Opción no reconocida")

        except ValueError: 
            print("Error. Ingrese valores numéricos.")

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

        nombre_colab = producto["colaborador"][0]
        dni_colab = producto["colaborador"][1]

        print(f"Colaborador: {nombre_colab} - DNI: {dni_colab}")
        print("ID:", producto["id"])
        print("Nombre del producto:", producto["nombre"])
        print("Precio por unidad:", producto["precio"])
        print("Cantidad:", producto["cantidad"])

    print("-----------------------------")


def buscar_producto(stock):
    """
    Función: buscar_producto
    Propósito: buscar un producto por su ID usando la lista en memoria y mostrarlo si existe.
    """
    print("\n===== BUSCAR PRODUCTOS =====")
    
    # Verificamos con la lista que ya tenemos en memoria
    if not stock:
        print("No hay productos")
        return
    
    id_buscar = input("ID a buscar: ")
    #Validación 
    while not re.match(r"^\d+$", id_buscar):
        print("ID inválido")
        id_buscar = input("ID: ")
    id_buscar = int(id_buscar)

    #Recorremos la matriz para mostrar el producto
    for producto in stock:

        if producto["id"] == id_buscar:

            nombre_colab = producto["colaborador"][0]
            dni_colab = producto["colaborador"][1]

            print(f"Colaborador: {nombre_colab} - DNI: {dni_colab}")
            print(f"Nombre del producto: {producto['nombre']}")
            print(f"Precio por unidad: {producto['precio']}")
            print(f"Cantidad: {producto['cantidad']}")
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
    print("\n===== ESTADISTICAS =====")
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

            nombre_colab = p["colaborador"][0]
            dni_colab = p["colaborador"][1]

            print(f"Colaborador: {nombre_colab} - DNI: {dni_colab}")
            print(f"ID: {p['id']} - Nombre del producto: {p['nombre']} - Precio por unidad: {p['precio']} - Cantidad: {p['cantidad']} ")

    else:
        print("No hay productos con cantidad menor a 5")


def dnis_unicos(stock):
    """
    Función: DNIs_unicos
    Propósito: mostrar los DNIs únicos registrados en el sistema.
    Utiliza un set para almacenar los DNIs sin repetición.
    """

    print("\n===== DNIs UNICOS =====")

    # Verifica que existan productos cargados
    if not stock:
        print("No hay productos")
        return

    # Se crea un set para almacenar los DNIs únicos
    dnis = set()

    for producto in stock:
        dni = producto["colaborador"]
        dnis.add(dni)

    for dni in dnis:
        print("Colaborador:", dni[0], "- DNI:", dni[1])
        

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

        try:
            deseo = int(input("¿Desea eliminar un producto? 1 = Sí / 0 = No: "))

            if deseo == 1:

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

                    archivo = open("personas.json", "w")
                    json.dump(nuevo, archivo, indent=4)
                    archivo.close()

                return nuevo

            elif deseo == 0:
                return stock
            
            else:
                print("Comando no reconocido")
        
        except ValueError:
            print("Error. Ingresar valores numéricos.")


def prueba_calculo_precios():
    
    #Se creará dos diccionarios ficticios para el test.
    stock_prueba = [{
        "colaborador": ("Axel", 44123456),
        "id": 101, 
        "nombre": "Teclado", 
        "precio": 1500.0, 
        "cantidad": 2
        },
        {
        "colaborador": ("Ale", 44123457),
        "id": 102, 
        "nombre": "Mouse", 
        "precio": 500.0, 
        "cantidad": 5,        
    }]
    
    #Se llamará a la función obtener precios ejecutado con el stock de prueba.
    resultado = obtener_precios(stock_prueba)
    
    #Si los resultados coinciden, la prueba finalizó con éxito.
    if resultado == [1500.0, 500.0]:
        print("Prueba Cálculo de Precios: CORRECTA")
    #Si se cambió el valor inicial, el resultado finalizó con éxito operando con el Error. 
    else:
        print("Prueba Cálculo de Precios: ERROR")

def prueba_busqueda_producto():
    
    #Se creará un diccionario ficticio para el test.
    stock_prueba = [{
        "colaborador": ("Angel", 44123456),
        "id": 101, 
        "nombre": "Teclado", 
        "precio": 1500.0, 
        "cantidad": 2,    
    }]
    
    #Se buscará el ID a encontrar.
    id_falso = 999
    encontrado = False
    for p in stock_prueba:
        if p["id"] == id_falso:
            encontrado = True
    
    #Si el ID ficticio coincide con el id falso, la prueba resultó conrrectamente mostrando en la terminal CORRECTO. 
    if encontrado == False:
        print("Prueba Búsqueda (ID Inexistente): CORRECTA")
    #Si el ID ficticio no coincide con el id falso, la prueba resultadó correctamente mostrando en la terminal ERROR. 
    else:
        print("Prueba Búsqueda (ID Inexistente): ERROR")

def ejecutar_todas_las_pruebas():
    """
    Función: ejecutar_todas_las_pruebas
    Propósito: correr de forma automática las pruebas unitarias, 
    evaluando escenarios tanto positivos como negativos mediante 
    la comparación. Simula las funciones de CÁLCULO DE PRECIO y BUSCAR POR ID.
    """

    print("\n===== CORRIENDO PRUEBAS AUTOMÁTICAS =====")
    prueba_calculo_precios()
    prueba_busqueda_producto()
    print("=========================================")


def info_funciones():
    """
    Función: info_funciones
    Propósito: mostrar información de las funciones del sistema
    utilizando help().
    """

    print("\n===== INFORMACION DE FUNCIONES =====")
    print("0. validar_usuario")
    print("1. cargar_datos")
    print("2. actualizar_producto")
    print("3. ordenar_productos")
    print("4. mostrar_productos")
    print("5. buscar_producto")
    print("6. obtener_precios")
    print("7. estadisticas")
    print("8. estadisticas_especificas")
    print("9. dnis_unicos")
    print("10. eliminar_producto")
    print("11. ejecutar_todas_las_pruebas")

    try:
        opcion = int(input("\nElija una función: "))

        if opcion == 0:
            help(validar_usuario)
        elif opcion == 1:
            help(cargar_datos)
        elif opcion == 2:
            help(actualizar_producto)
        elif opcion == 3:
            help(ordenar_productos)
        elif opcion == 4:
            help(mostrar_productos)
        elif opcion == 5:
            help(buscar_producto)
        elif opcion == 6:
            help(obtener_precios)
        elif opcion == 7:
            help(estadisticas)
        elif opcion == 8:
            help(estadisticas_especificas)
        elif opcion == 9:
            help(dnis_unicos)
        elif opcion == 10:
            help(eliminar_producto)
        elif opcion == 11:
            help(ejecutar_todas_las_pruebas)
        else:
            print("Opción inválida")
    
    except ValueError:
        print("Error. Ingresar valores numéricos.")


def main():

    #Se carga el archivo json
    try: 
        archivo = open("personas.json", "r")
        stock = json.load(archivo)
        archivo.close()
        #Se genera como tupla nuevamente.
        for producto in stock: 
            producto["colaborador"] = tuple(producto["colaborador"])
        print("Stock cargado correctamente.")
        
    #Si es la 1ra vez que se ingresa, se crea la lista desde 0
    except FileNotFoundError: 
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
        print("9. DNIs unicos")
        print("10. Informacion de funciones")
        print("11. Ejecutar pruebas unitarias")
        print("0. Salir")

        try:
            opcion = int(input("\nOpción: "))

            if opcion == 1:
                cargar_datos(stock)

            elif opcion == 2:
                actualizar_producto(stock)

            elif opcion == 3:
                ordenar_productos(stock)

            elif opcion == 4:
                mostrar_productos(stock)

            elif opcion == 5:
                buscar_producto(stock)

            elif opcion == 6:
                estadisticas(stock)

            elif opcion == 7:
                estadisticas_especificas(stock)

            elif opcion == 8:
                stock = eliminar_producto(stock)

            elif opcion==9:
                dnis_unicos(stock)
                
            elif opcion == 10:
                info_funciones()

            elif opcion == 11:
                ejecutar_todas_las_pruebas()
                
            elif opcion == 0:
                print("Programa cerrado")
                break

            else:
                print("Use opciones del menu")
                
        except ValueError:
            print("Error. Ingrese valores numéricos.")
main()
