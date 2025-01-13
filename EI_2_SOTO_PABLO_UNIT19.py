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
