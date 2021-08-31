from lifestore_file import lifestore_products, lifestore_sales, lifestore_searches

####################
# FUNCIONES ÚTILES #
####################


# Esta función genera un bucle while para inciar sesión.
# Se sale del bucle sólo saliendo del programa o haciendo un
# inicio de sesión correcto.
def login():
    # Esta variable será de utilidad para saber si se ejecuta el programa o no
    # Si es "s", no se ejecutará el programa. De lo contrario, sí.
    salir = ""

    while True:
        # Para colocar la información de inicio de sesión
        username = input("Introduzca su nombre de usuario: ")
        password = input("Introduzca su contraseña: ")

        # Si el inicio de sesión es correcto
        if username == "admin" and password == "12345":
            print("Inicio de sesión satisfactorio!")
            break

        # Si el inicio de sesión es incorrecto
        # Si el nombre no es correcto
        if username != "admin":
            print("Su nombre de usuario es incorrecto")

        # Si lo que falló es la contraseña
        else:
            print("Su contraseña es incorrecta")

        # Para salir del programa sin iniciar sesión
        salir = input("¿Desea salir del programa? (s/n): ")

        if salir == "s":
            print("Hasta luego!")
            return salir


###############################################################################


# Función para ordenar la lista de productos al ordenar una lista asociada.
# Esta función es para hacer rankings de productos más o menos vendidos, por ejemplo.
def ordenar_lista_productos(lista_para_ordenar, orden="descendente"):
    lista_dummy_productos = productos[:]
    lista_dummy = lista_para_ordenar[:]

    # Se hace un ordenamiento
    for i in range(numero_productos):
        for j in range(numero_productos - 1):

            # Se define si el ordenamiento es ascendente o descendente
            if orden == "descendente":
                condicional = lista_dummy[j] < lista_dummy[j + 1]
            else:
                condicional = lista_dummy[j] > lista_dummy[j + 1]

            # Se hace el ordenamiento subiendo o bajando el elemento presente
            if condicional:
                # Se acomoda el valor de la lista que se ordena
                variable_dummy = lista_dummy[j + 1]
                lista_dummy[j + 1] = lista_dummy[j]
                lista_dummy[j] = variable_dummy

                # Se acomoda su id de producto correspondiente
                variable_dummy = lista_dummy_productos[j + 1]
                lista_dummy_productos[j + 1] = lista_dummy_productos[j]
                lista_dummy_productos[j] = variable_dummy

    # Se regresa la lista de id's ordenada
    return lista_dummy_productos[:]


#############################################################################


# Esta función ordena la lista de productos usando otra como criterio (usando la función anterior).
# Luego, filtra los productos que cumplen con una condición de filtro.
def ordenar_y_filtrar_productos(valor_filtro,
                                posicion,
                                lista_para_ordenar,
                                orden="descendente"):

    # Se ordenan los id's de los productos de acuerdo a los parámetros dados
    productos_ordenados = ordenar_lista_productos(lista_para_ordenar, orden)

    # Se hace una lista con los id's de los productos que pertenecen a la categoría dada
    lista_filtro = []

    for i in range(numero_productos):
        if lifestore_products[i][posicion] == valor_filtro:
            lista_filtro.append(lifestore_products[i][0])

    # Se obtiene de la lista de id's ordenados, únicamente aquellos productos que
    # se encuentren en la lista_filtro
    lista_filtrada = []

    for i in range(numero_productos):
        if productos_ordenados[i] in lista_filtro:
            lista_filtrada.append(productos_ordenados[i])

    # Se devuelve la lista de id's ordenada y filtrada
    return lista_filtrada[:]


###############################################################################


# Esta función sirve igual que ordenar_lista_productos con la diferencia de
# que esta ordena una lista de meses.
def ordenar_lista_meses(lista_para_ordenar, orden="descendente"):
    lista_dummy_meses = meses[:]
    lista_dummy = lista_para_ordenar[:]

    # Se hace un ordenamiento
    for i in range(12):
        for j in range(11):

            # Se define si el ordenamiento es ascendente o descendente
            if orden == "descendente":
                condicional = lista_dummy[j] < lista_dummy[j + 1]
            else:
                condicional = lista_dummy[j] > lista_dummy[j + 1]

            # Se hace el ordenamineto
            if condicional:
                # Se ordena la lista guía
                variable_dummy = lista_dummy[j + 1]
                lista_dummy[j + 1] = lista_dummy[j]
                lista_dummy[j] = variable_dummy

                # Se reajusta la lista de meses acorde a la lista guía
                variable_dummy = lista_dummy_meses[j + 1]
                lista_dummy_meses[j + 1] = lista_dummy_meses[j]
                lista_dummy_meses[j] = variable_dummy

    # Se devuelve tanto la lista de meses ordenadas como su correspondiente lista
    # guía ordenada
    return [lista_dummy_meses[:], lista_dummy[:]]


###############################################################################


# Esta función sirve para obtener el nombre del producto dado su id de producto
def obtener_nombre_producto(id_producto):
    # En toda la lista de productos se busca el nombre del producto correspondiente
    # al id de producto dado
    for i in range(numero_productos):
        if id_producto == lifestore_products[i][0]:
            return lifestore_products[i][1]


###############################################################################

########################
# EJECUCIÓN DEL CÓDIGO #
########################

# Inicio de sesión
salir_del_programa = login()

# Sólo si el inicio de sesión es correcto se corre el resto del código
if salir_del_programa != "s":

    ###############################################################################

    # PROCESAMIENTO PARA: PRODUCTOS MÁS VENDIDOS Y PRODUCTOS REZAGADOS

    # Números de registros en cada lista
    numero_productos = len(lifestore_products)
    numero_busquedas = len(lifestore_searches)
    numero_ventas = len(lifestore_sales)

    # Se obtiene el vector de id's de productos
    productos = []
    for i in range(numero_productos):
        productos.append(lifestore_products[i][0])

    # Se cuenta cuántas veces aparece cada producto en las ventas
    ventas_por_producto = []
    for i in range(numero_productos):
        contador_ventas = 0

        for j in range(numero_ventas):
            if lifestore_sales[j][1] == productos[i]:
                contador_ventas += 1

        ventas_por_producto.append(contador_ventas)

    # Se cuentan las veces que aparece cada producto en las búsquedas
    busquedas_por_producto = []
    for i in range(numero_productos):
        contador_busquedas = 0

        for j in range(numero_busquedas):
            if lifestore_searches[j][1] == productos[i]:
                contador_busquedas += 1

        busquedas_por_producto.append(contador_busquedas)

    # Se extraen todas las categorías de productos existentes
    categorias = []
    for i in range(numero_productos):
        # Aquí se verifica que la categoría presente no se vaya a repetir en la lista
        if lifestore_products[i][3] not in categorias:
            categorias.append(lifestore_products[i][3])

    # Se cuentan las menores ventas y búsquedas por categorías
    menores_ventas_por_categoria = []
    menores_busquedas_por_categoria = []

    for categoria in categorias:
        # Se intenta hacer el top 50 de menos ventas, si no alcanzan los items, hace el top de los que hayan
        try:
            ranking_ventas = ordenar_y_filtrar_productos(
                categoria, 3, ventas_por_producto, "ascendente")[:50]
        except:
            ranking_ventas = ordenar_y_filtrar_productos(
                categoria, 3, ventas_por_producto, "ascendente")

        # Se intenta hacer el top 50 de menos búsquedas, si no alcanzan los items, hace el top de los que hayan
        try:
            ranking_busquedas = ordenar_y_filtrar_productos(
                categoria, 3, busquedas_por_producto, "ascendente")[:100]
        except:
            ranking_busquedas = ordenar_y_filtrar_productos(
                categoria, 3, busquedas_por_producto, "ascendente")

        # Se asignan los tops a los arreglos por categoría
        menores_ventas_por_categoria.append(ranking_ventas)
        menores_busquedas_por_categoria.append(ranking_busquedas)

    ###############################################################################

    # PROCESAMIENTO PARA: PRODUCTOS POR RESEÑA EN EL SERVICIO

    # Se hace la lista de scores promedio para el ranking de mayores scores
    score_por_producto = []

    for i in range(numero_productos):
        contador_scores = 0
        score_total = 0

        for j in range(numero_ventas):
            if lifestore_sales[j][1] == productos[i]:
                contador_scores += 1
                score_total += lifestore_sales[j][2]

        # Como existen productos que no han sido comprados y, por ende, no tiene
        # sentido asignarles un score, en este caso se les asigna un valor fuera del rango de calificaciones
        # que no vaya a influir en el ordenamiento para sacar los productos mejor rankeados
        if contador_scores != 0:
            score_por_producto.append(score_total / contador_scores)
        else:
            score_por_producto.append(-1)

    # Los 20 productos con mejores reseñas
    mejores_scores = ordenar_lista_productos(score_por_producto)[:20]


    # Se hace la lista de scores promedio para hacer el ranking de menores scores
    score_por_producto = []

    for i in range(numero_productos):
        contador_scores = 0
        score_total = 0

        for j in range(numero_ventas):
            if lifestore_sales[j][1] == productos[i]:
                contador_scores += 1
                score_total += lifestore_sales[j][2]

        # Como existen productos que no han sido comprados y, por ende, no tiene
        # sentido asignarles un score, en este caso se les asigna un valor fuera del rango de calificaciones
        # que no vaya a influir en el ordenamiento para sacar los productos peor rankeados
        if contador_scores != 0:
            score_por_producto.append(score_total / contador_scores)
        else:
            score_por_producto.append(1000)

    # Los 20 productos con menores reseñas
    peores_scores = ordenar_lista_productos(score_por_producto,
                                            "ascendente")[:20]

    ###############################################################################

    # PROCESAMIENTO PARA: GANANCIAS Y VENTAS

    # Número de ventas sin refund del 2020
    ventas_2020 = 0
    for i in range(numero_ventas):
        # Se verifica que la venta sea del 2020 y que no se haya devuelto el dinero
        if lifestore_sales[i][3][6:] == "2020" and lifestore_sales[i][-1] == 0:
            ventas_2020 += 1

    # Número de ventas mensuales promedio del 2020
    ventas_promedio_mensuales = ventas_2020 / 12

    # Ganancias del 2020
    ganancias_2020 = 0
    for i in range(numero_ventas):
        # Se verifica que la venta sea del 2020 y que no se haya devuelto el dinero
        if lifestore_sales[i][3][6:] == "2020" and lifestore_sales[i][-1] == 0:
            # Se bsuca el costo del producto en la lista de precios y se agrega a la ganancia total
            for j in range(numero_productos):
                if lifestore_sales[i][1] == lifestore_products[j][0]:
                    ganancias_2020 += lifestore_products[j][2]

    # Ganancias mensuales promedio del 2020
    ganancias_promedio_mensuales = ganancias_2020 / 12

    # Lista de todos los meses
    meses = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
        "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]

    # Ganancias mensuales reales del 2020
    ganancias_mensuales = []

    for k in range(1, 13):

        ganancias_mes = 0

        for i in range(numero_ventas):
            # Este filtro es para estudiar sólo valores correspondientes
            # al mes de la iteración.
            # La primera posibilidad ocurre si se trata de un entero de dos
            # cifras (10, 11 o 12). La segunda posibilidad es válida si se trata de
            # un entero de una sola cifra (del 1 al 9).
            filtro_mes = (str(k) == lifestore_sales[i][3][3:5]) or (
                str(k) == lifestore_sales[i][3][4:5])
            
            # Lo siguiente verifica que sea el mes y año correcto así como
            # que no sea una venta cuyo dinero haya sido devuelto
            if filtro_mes and lifestore_sales[i][3][
                    6:] == "2020" and lifestore_sales[i][-1] == 0:
                
                # Se busca el costo del producto en la lista de productos con su id de producto
                for j in range(numero_productos):
                    if lifestore_sales[i][1] == lifestore_products[j][0]:
                        ganancias_mes += lifestore_products[j][2]

        ganancias_mensuales.append(ganancias_mes)

    # Se rankean los meses con más ganancias
    meses_con_mas_ventas, ventas_meses_mas_ventas = ordenar_lista_meses(
        ganancias_mensuales)

    ################################################################################

    ##############
    # RESULTADOS #
    ##############

    ###############################################################################

    # PRODUCTOS MÁS VENDIDOS Y PRODUCTOS REZAGADOS

    # Los 50 más vendidos (rankeado de más vendido a menos vendido)
    mas_vendidos = ordenar_lista_productos(ventas_por_producto)[:50]
    print("-------------------------------------")
    print("\n\nLOS 50 PRODUCTOS MÁS VENDIDOS\n")
    rank_contador = 0
    for id in mas_vendidos:
        rank_contador += 1
        nombre_producto = obtener_nombre_producto(id)
        print(f"{rank_contador})\tid={id}\t{nombre_producto}")

    # Los 100 más buscados (rankeado de más vendido a menos vendido)
    # Intenta obtener los 100 productos más buscados
    try:
      mas_buscados = ordenar_lista_productos(busquedas_por_producto)[:100]
    # Si no hay suficientes productos, se usan los que hayan
    except:
      mas_buscados = ordenar_lista_productos(busquedas_por_producto)
    print("-------------------------------------")
    print(f"\n\nLOS {len(mas_buscados)} PRODUCTOS MÁS BUSCADOS\n")
    rank_contador = 0
    for id in mas_buscados:
        rank_contador += 1
        nombre_producto = obtener_nombre_producto(id)
        print(f"{rank_contador})\tid={id}\t{nombre_producto}")

    # Los menos comprados (rankeado de menos vendido a más vendido) por categoría
    print("-------------------------------------")
    print("\n\nLOS MENOS VENDIDOS POR CATEGORÍA\n")
    contador_categoria = 0
    for categoria in categorias:
        rank_contador = 0
        print(f"\n{categoria.upper()}:")

        for id in menores_ventas_por_categoria[contador_categoria]:
            rank_contador += 1
            nombre_producto = obtener_nombre_producto(id)
            print(f"{rank_contador})\tid={id}\t{nombre_producto}")

        contador_categoria += 1

    # Los menos comprados (rankeado de menos vendido a más vendido) por categoría
    print("-------------------------------------")
    print("\n\nLOS MENOS BUSCADOS POR CATEGORÍA\n")
    contador_categoria = 0
    for categoria in categorias:
        rank_contador = 0
        print(f"\n{categoria.upper()}:")

        for id in menores_busquedas_por_categoria[contador_categoria]:
            rank_contador += 1
            nombre_producto = obtener_nombre_producto(id)
            print(f"{rank_contador})\tid={id}\t{nombre_producto}")

        contador_categoria += 1

    ###############################################################################

    # PRODUCTOS POR RESEÑA EN EL SERVICIO

    # Los 20 productos con mejores reseñas
    print("-------------------------------------")
    print("\n\nLOS 20 PRODUCTOS CON MEJORES CALIFICACIONES\n")
    rank_contador = 0
    for id in mejores_scores:
        rank_contador += 1
        nombre_producto = obtener_nombre_producto(id)
        print(f"{rank_contador})\tid={id}\t{nombre_producto}")

    # Los 20 productos con peores reseñas
    print("-------------------------------------")
    print("\n\nLOS 20 PRODUCTOS CON PEORES CALIFICACIONES\n")
    rank_contador = 0
    for id in peores_scores:
        rank_contador += 1
        nombre_producto = obtener_nombre_producto(id)
        print(f"{rank_contador})\tid={id}\t{nombre_producto}")

    ###############################################################################

    # GANANCIAS Y VENTAS

    # Los meses con más ventas
    print("-------------------------------------")
    print("\n\nLOS MESES CON MÁS GANANCIAS EN 2020\n")
    rank_contador = 0
    for i in range(12):
        rank_contador += 1

        # Lo siguiente es sólo para que el formato de la tabla
        # sea bueno y todos las ganancias estén alineadas
        # Para meses con nombre "corto"
        if len(meses_con_mas_ventas[i])<=7:
          print(
              f"{rank_contador})\t{meses_con_mas_ventas[i].upper()}\t\t${ventas_meses_mas_ventas[i]}"
          )
        # Para meses con nombre "largo", con 8 o más caracteres
        else:
          print(
              f"{rank_contador})\t{meses_con_mas_ventas[i].upper()}\t${ventas_meses_mas_ventas[i]}"
          )

    # Ganancias del 2020
    print("-------------------------------------")
    print(f"\n\nLAS GANANCIAS DE 2020:\t${ganancias_2020}")
    print(f"LAS VENTAS DE 2020:\t{ventas_2020} ventas")
    print("-------------------------------------")
    print(
        f"LAS GANANCIAS MENSUALES PROMEDIO DE 2020:\t${ganancias_promedio_mensuales}"
    )
    print(
        f"LAS VENTAS MENSUALES PROMEDIO DE 2020:\t\t{ventas_promedio_mensuales} ventas/mes"
    )
