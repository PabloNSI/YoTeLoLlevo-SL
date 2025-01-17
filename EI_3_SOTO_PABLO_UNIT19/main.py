from planificacion_rutas import crear_grafo, calcular_distancia, destino_validado as destino
from datos import coordenadas

# Crear el grafo utilizando el callejero proporcionado por planificacion_rutas.py
G = crear_grafo(coordenadas)

# Función para calcular el tiempo estimado desde un destino al 'Almacen'
def calcular_tiempo_desde_destino(destino):
    # Verificar si el destino está en el callejero
    if destino not in coordenadas:
        print("El destino "+str(destino)+" no está cubierto por el servicio.")
        return None
    
    # Calcular la distancia entre el destino y 'Almacen'
    distancia = calcular_distancia(coordenadas['Almacen'], coordenadas[destino])
    
    # Calcular el tiempo estimado (ajustado por distancia)
    tiempo_estimado = distancia * 1.5  # Usamos el mismo factor de tiempo por distancia
    
    # Convertir el tiempo estimado en minutos y segundos
    tiempo_estimado_minutos = int(tiempo_estimado)
    tiempo_estimado_segundos = round((tiempo_estimado - tiempo_estimado_minutos) * 60)
    
    return tiempo_estimado_minutos, tiempo_estimado_segundos

# Función para procesar las órdenes
def procesar_orden(destino):
    
    # Calcular el tiempo desde el destino al 'Almacen'
    tiempo_estimado = calcular_tiempo_desde_destino(destino)
    
    if tiempo_estimado:
        tiempo_estimado_minutos, tiempo_estimado_segundos = tiempo_estimado

        print("Hemos generado una orden de entrega.")
        print("\nTiempo estimado para ir desde el almacen a "+str(destino)+": "
              + str(tiempo_estimado_minutos)+" minutos y "+str(tiempo_estimado_segundos)+" segundos.")

# Llamar a la función para procesar la orden con el destino importado de planificacion_rutas.py
procesar_orden(destino)

def guardar_orden(destino):
    # Leer el archivo para cargar los destinos y sus contadores
    with open("EI_3_SOTO_PABLO_UNIT19\\ordenes_envio.txt", "r") as archivo:
        lineas = archivo.readlines()

    # Crear un diccionario para almacenar los destinos y sus contadores
    destinos_dict = {}
    for linea in lineas:
        destino_nombre, contador = linea.strip().split(" : ")
        destinos_dict[destino_nombre] = int(contador)

    # Actualizar el contador para el destino
    if destino in destinos_dict:
        destinos_dict[destino] += 1
    else:
        destinos_dict[destino] = 1

    # Escribir de nuevo todos los destinos con los contadores actualizados
    with open("EI_3_SOTO_PABLO_UNIT19\\ordenes_envio.txt", "w") as archivo:
        for destino_nombre, contador in sorted(destinos_dict.items()):
            archivo.write(f"{destino_nombre} : {contador}\n")

# Llamamos a la función para guardar la orden
guardar_orden(destino)