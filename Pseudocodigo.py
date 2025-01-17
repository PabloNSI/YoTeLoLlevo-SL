# Algoritmo Dijkstra (calcular_ruta_mas_corta):
# 1. Inicializar un conjunto de nodos no visitados
# 2. Establecer la distancia a todos los nodos como infinita, excepto al nodo de inicio (establecer distancia a 0)
# 3. Mientras haya nodos no visitados:
#     a. Seleccionar el nodo con la distancia mínima
#     b. Para cada vecino del nodo seleccionado:
#         i. Calcular la distancia desde el nodo actual hasta el vecino
#         ii. Si la distancia calculada es menor que la distancia previamente registrada, actualizar la distancia
#     c. Marcar el nodo como visitado
# 4. Repetir hasta que todos los nodos hayan sido visitados o se haya encontrado el nodo de destino
# 5. Reconstruir el camino más corto siguiendo los nodos desde el destino hasta el origen

# INICIO Validación de Órdenes

# Recibir_orden(orden):
#     Dirección <- Extraer_dirección(orden)

#     SI Dirección EN área_cubierta:
#         SI Dirección válida:
#             Registrar_orden(orden)
#             Retornar "Orden válida y registrada"
#         SINO:
#             Retornar "Dirección inválida"
#     SINO:
#         Retornar "Dirección fuera de cobertura"

# FIN Validación de Órdenes

# INICIO Optimización de Rutas

# Planificar_ruta(órdenes):
#     grafo <- Crear_grafo(órdenes)  // Construir el grafo de rutas

#     destinos <- Extraer_destinos(órdenes)  // Extraer destinos desde las órdenes
#     rutas_ordenadas <- Ordenar_por_prioridad(destinos)  // Ordenar destinos por prioridad (o tiempo)

#     ruta_optimizada <- Generar_rutas_optimizada(grafo, rutas_ordenadas)  // Generar la ruta óptima utilizando el grafo

#     Retornar ruta_optimizada

# FIN Optimización de Rutas
