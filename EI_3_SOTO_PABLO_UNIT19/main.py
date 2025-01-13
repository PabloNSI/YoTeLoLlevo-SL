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

        print("Tiempo estimado para llegar del almacen a "+str(destino)+": "
              + str(tiempo_estimado_minutos)+" minutos y "+str(tiempo_estimado_segundos)+" segundos.")
    
# Llamar a la función para procesar la orden con el destino importado de planificacion_rutas.py
procesar_orden(destino)
