#########################
# LIBRERÍAS Y FUNCIONES #
#########################

# Se importan las librerías y funciones usadas
import csv # Para leer archivos csv
from scipy.stats import t # Para hacer pruebas t de Student

# Para crear una submatriz del dataframe a partir de una lista de columnas
# de interés
def matriz_con_frecuencias_y_ganancias(df, columnas, modo="single"):
  # Un conjunto para guardar los elementos únicos
  elementos = set()

  # Una matriz para guardar los elementos únicos, el número de veces
  # que aparecen en el dataframe y la ganancia total que genera ese elemento
  elementos_info = []

  for i in range(1, len(df)): # Para no iterar la fila del nombre de las columnas

    if modo=="single":# Se da una sola con las columnas dadas
      # Se define el elemento a estudiar
      if len(columnas)==1:
        elemento = df[i][columnas[0]]
      else:
        elemento = frozenset({df[i][columnas[0]], df[i][columnas[1]]})

      # Cuando un elemento aparece por primera vez, se agrega
      # a la lista de elementos
      if elemento not in elementos:
        elementos.add(elemento)
        elementos_info.append([elemento, 1, float(df[i][9])])

      # Cuando no es la primera vez que aparece, se suma
      # a su frecuencia de aparición
      else:
        for j in range(len(elementos_info)):
          if elementos_info[j][0]==elemento:
            elementos_info[j][1]+=1
            elementos_info[j][2]+=float(df[i][9])
    
    else:# Se dan dos pasadas con las columnas dadas
      # Se da una pasada sobre el primer índice de la columna
      elemento = df[i][columnas[0]]

      if elemento not in elementos:
        elementos.add(elemento)
        elementos_info.append([elemento, 0.5, float(df[i][9])/2])

      else:
        for j in range(len(elementos_info)):
          if elementos_info[j][0]==elemento:
            elementos_info[j][1]+=0.5
            elementos_info[j][2]+=float(df[i][9])/2
      
      # Se da una segunda pasada sobre el segundo índice de la columna
      elemento = df[i][columnas[1]]
      
      if elemento not in elementos:
        elementos.add(elemento)
        elementos_info.append([elemento, 0.5, float(df[i][9])/2])

      else:
        for j in range(len(elementos_info)):
          if elementos_info[j][0]==elemento:
            elementos_info[j][1]+=0.5
            elementos_info[j][2]+=float(df[i][9])/2

  return elementos_info[:][:]

# Para hacer un sort de una matriz
def ordenar_matriz(matriz, columna_pivote, orden="descendente"):
  matriz_dummy = [fila[:] for fila in matriz]
  numero = len(matriz_dummy)

  # Se hace un ordenamiento
  for i in range(numero):
    for j in range(numero-1):
      
      # Se define si el ordenamiento es ascendente o descendente
      if orden=="descendente":
        condicional = matriz_dummy[j][columna_pivote] < matriz_dummy[j+1][columna_pivote]
      else:
        condicional = matriz_dummy[j][columna_pivote] > matriz_dummy[j+1][columna_pivote]
      
      # Se hace el ordenamineto
      if condicional:
        matriz_dummy[j+1][:], matriz_dummy[j][:] = matriz_dummy[j][:], matriz_dummy[j+1][:]

  return matriz_dummy

# Se cuentan las ganancias de la matriz
def ganancias_de_matriz(matriz):
  suma=0
  # Se suman las ganancias de todos los registros de la matriz
  for i in range(len(matriz)):
    suma+=matriz[i][-1]
  return suma

# Se cuentan las frecuencias de la matriz
def frecuencias_de_matriz(matriz):
  suma=0
  # Se suman las frecuencias de todos los registros de la matriz
  for i in range(len(matriz)):
    suma+=matriz[i][1]
  return suma

# Se toma una columna de la matriz
def extraer_columna(matriz, columna):
  lista = [matriz[i][columna] for i in range(len(matriz))]
  return lista

# Se hace una prueba t de Student (varianzas iguales)
def prueba_t(matriz_1, matriz_2, columna):

  # Se extraen las filas de interés
  lista_1 = extraer_columna(matriz_1, columna)
  lista_2 = extraer_columna(matriz_2, columna)

  # Se obtienen los promedios
  promedio_1 = sum(lista_1)/len(lista_1)
  promedio_2 = sum(lista_2)/len(lista_2)

  # El tamaño de las muestras
  n_1 = len(lista_1)
  n_2 = len(lista_2)

  # Se obtienen las varianzas
  var_1 = sum([(valor-promedio_1)**2 for valor in lista_1])/(n_1-1)
  var_2 = sum([(valor-promedio_2)**2 for valor in lista_2])/(n_2-1)

  # Se calculan los parámetros de la prueba
  d_f = n_1+n_2-1
  error = (var_1/n_1 + var_2/n_2)**0.5

  # Se devuelve el valor acumulativo de la distribución t
  return t.cdf((promedio_1-promedio_2)/error, d_f)
  

#################################
# PROCESAMIENTO DE LOS ENCARGOS #
#################################

# LECTURA DE DATOS

# Se guardan los registros del archivo csv en un "dataframe"
df = []

with open("synergy_logistics_database.csv", "r") as archivo_csv:
  lector = csv.reader(archivo_csv)
  for linea in lector:
    df.append(linea)

# RUTAS DE IMPORTACIÓN Y EXPORTACIÓN

# Como no es relevante el orden de las rutas, sino sólo
# los lugares que conecta, se guardaran los pares de lugares
# en conjuntos, pues éstos son estructuras no ordenadas
rutas_info = matriz_con_frecuencias_y_ganancias(df, [2, 3])

rank_rutas_frecuencia = ordenar_matriz(rutas_info, 1)[:10] # Las rutas más frecuentes

# Las ganancias totales de la lista completa de rutas y las de las rutas más frecuentes
ganancias_totales = ganancias_de_matriz(rutas_info)
ganancias_rutas_frecuentes = ganancias_de_matriz(rank_rutas_frecuencia)

# Las ganancias por ruta de la lista completa de rutas y las de las rutas más frecuentes
ganancias_totales_promedio = ganancias_totales/len(rutas_info)
ganancias_rutas_frecuentes_promedio = ganancias_rutas_frecuentes/len(rank_rutas_frecuencia)

# Las frecuencias totales de la lista completa de rutas y las de las rutas frecuentes
frecuencias_totales = frecuencias_de_matriz(rutas_info)
frecuencias_rutas_frecuentes = frecuencias_de_matriz(rank_rutas_frecuencia)

print(f"Las proporción de frecuencias de las 10 rutas más frecuentes y las totales es: {round(frecuencias_rutas_frecuentes/frecuencias_totales, 4)}")
print(f"Las proporción de ganancias que proporcionan las 10 rutas más frecuentes y las ganancias totales es: {round(ganancias_rutas_frecuentes/ganancias_totales, 4)}")
print(f"Las proporción de las ganancias promedio de las 10 rutas más frecuentes y el total de las rutas es: {round(ganancias_rutas_frecuentes_promedio/ganancias_totales_promedio, 4)}")
print(f"El p-value de una prueba unilateral de hipótesis sobre las ganancias promedio es: {round(1-prueba_t(rank_rutas_frecuencia, rutas_info, 2), 6)}")

print(f"\nLas 10 rutas más frecuentes (de un total de {len(rutas_info)}):")
print("Ruta\t\t\t\tFrecuencia\tGanancias\tGanancia/Traslado")
for fila in rank_rutas_frecuencia:
  print(f"{str(fila[0])[11:-2]:30}\t{fila[1]}\t\t{fila[2]}\t{round(fila[2]/fila[1],4)}")

# MEDIOS DE TRANSPORTE

transportes_info = matriz_con_frecuencias_y_ganancias(df, [7])

rank_transportes = ordenar_matriz(transportes_info, 2) # Los transportes más frecuentes

ganancias_transportes = ganancias_de_matriz(rank_transportes[:3])
ganancias_transportes_promedio = ganancias_transportes/len(rank_transportes[:3])
frecuencias_transportes = frecuencias_de_matriz(rank_transportes[:3])

print(f"\n\n\n\nLas proporción de frecuencias de los 3 transportes más valiosos y las totales es: {round(frecuencias_transportes/frecuencias_totales, 4)}")
print(f"Las proporción de ganancias que proporcionan los 3 transportes más valiosos y las ganancias totales es: {round(ganancias_transportes/ganancias_totales, 4)}")
print(f"Las proporción de las ganancias promedio de los 3 transportes más valiosos y el total de las rutas es: {round(ganancias_transportes_promedio/ganancias_totales_promedio, 4)}")
print(f"El p-value de una prueba unilateral de hipótesis sobre las ganancias promedio es: {round(1-prueba_t(rank_transportes[:3], transportes_info, 2), 6)}")

print("\nLos transportes rankeados por orden de valor:")
print("Transporte\tFrecuencia\tGanancias\tGanancia/Traslado")
for fila in rank_transportes:
  print(f"{fila[0]:10}\t{fila[1]}\t\t{fila[2]}\t{round(fila[2]/fila[1],4)}")

# VALOR TOTAL DE IMPORTACIONES Y EXPORTACIONES

# Note que con el ciclo de matriz_con_frecuencias_y_gancias, se contaron dos veces
# las ganancias y las frecuencias totales de viajes. Por lo tanto, se van a
# dividir entre dos ambas cantidades.
paises_info = matriz_con_frecuencias_y_ganancias(df, [2, 3], "double")
rank_paises = ordenar_matriz(paises_info, 2)

# Se buscan los países que están involucrados en el 80% de las ganancias totales
suma = 0
indice = 0
while suma<=0.8*ganancias_totales:
  suma+=rank_paises[indice][2]
  indice+=1

rank_paises_slice = rank_paises[:indice]

ganancias_paises = ganancias_de_matriz(rank_paises_slice)
ganancias_paises_promedio = ganancias_paises/len(rank_paises_slice)
frecuencias_paises = frecuencias_de_matriz(rank_paises_slice)

print(f"\n\n\n\nLas proporción de frecuencias de los {indice} países más valioso y las totales es: {round(frecuencias_paises/frecuencias_totales, 4)}")
print(f"Las proporción de ganancias que proporcionan los {indice} países más valiosos y las ganancias totales es: {round(ganancias_paises/ganancias_totales, 4)}")
print(f"Las proporción de las ganancias promedio de los {indice} países más valiosos y el total de las rutas es: {round(ganancias_paises_promedio/ganancias_totales_promedio, 4)}")
print(f"El p-value de una prueba unilateral de hipótesis sobre las ganancias promedio es: {round(1-prueba_t(rank_paises_slice, paises_info, 2), 6)}")

print(f"\nLos {indice} países más valiosos (de un total de {len(paises_info)}):")
print("País\t\tFrecuencia\tGanancias\tGanancia/Traslado")
for fila in rank_paises_slice:
  print(f"{fila[0]:10}\t{fila[1]}\t\t{fila[2]}\t{round(fila[2]/fila[1],4)}")