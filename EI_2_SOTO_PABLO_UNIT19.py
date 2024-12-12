# INICIO Validación de Órdenes

# Recibir_orden(orden):
#     Dirección <- Extraer_dirección(orden)

#     SI Dirección EN área_cubierta:
#         Registrar_orden(orden)
#         Retornar "Orden válida y registrada"
#     SINO:
#         Retornar "Dirección fuera de cobertura"

# FIN Validación de Órdenes


# INICIO Optimización de Rutas

# Planificar_ruta(órdenes):
#     rutas <- Crear_grafo(órdenes)
    
#     destinos <- Extraer_destinos(rutas)
#     ruta_ordenada <- Quicksort(destinos)

#     Retornar ruta_ordenada

# FIN Optimización de Rutas


