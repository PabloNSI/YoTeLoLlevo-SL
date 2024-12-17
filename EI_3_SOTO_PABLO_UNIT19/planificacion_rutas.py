import math
import networkx as nx
import matplotlib.pyplot as plt
from itertools import cycle

# Coordenadas de los nodos
coordenadas = {
    'Almacen': (20, 20),  # Coordenada arbitraria para el Almacen,
    'Puerta del Sol': (10, 10), 'Plaza Mayor': (12, 11), 'Calle Arenal': (11, 9), 
    'Gran Vía': (15, 10), 'Plaza de España': (17, 9), 'Calle Mayor': (13, 12),
    'Plaza de Oriente': (14, 8), 'Ópera': (13, 9), 'Calle Preciados': (11, 11),
    'Callao': (14, 11),

    # Barrio Chamberí
    'Quevedo': (20, 15), 'Iglesia': (21, 14), 'Alonso Cano': (23, 14), 
    'Ríos Rosas': (25, 13), 'Canal': (20, 17), 'Islas Filipinas': (22, 18), 
    'San Bernardo': (19, 13), 'Argüelles': (18, 11), 'Moncloa': (18, 19), 
    'Guzmán el Bueno': (21, 16),

    # Barrio Salamanca
    'Velázquez': (30, 20), 'Serrano': (32, 19), 'Goya': (34, 18),
    'Príncipe de Vergara': (35, 17), 'Diego de León': (36, 16), 
    'Lista': (33, 19), 'Manuel Becerra': (38, 15), 'Doctor Esquerdo': (40, 14), 
    'Avenida de América': (30, 22), 'Núñez de Balboa': (31, 20),

    # Barrio Chamartín
    'Chamartín': (40, 30), 'Plaza de Castilla': (45, 31), 'Pío XII': (43, 29), 
    'Cuzco': (42, 28), 'Santiago Bernabéu': (40, 27), 'Hispanoamérica': (43, 26), 
    'Colombia': (41, 25), 'Concha Espina': (39, 26), 'Duque de Pastrana': (46, 30), 
    'Plaza de Lima': (41, 28),

    # Barrio Retiro
    'Atocha': (10, 30), 'Menéndez Pelayo': (11, 29), 'Pacífico': (12, 28), 
    'Conde de Casal': (13, 27), 'Ibiza': (15, 25), 'Sainz de Baranda': (16, 26), 
    'Retiro': (14, 28), 'Prado': (11, 31), 'Neptuno': (12, 32), 'Cibeles': (13, 30)
}

# Calcular distancia euclidiana
def calcular_distancia(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

# Crear grafo con networkx
def crear_grafo(coordenadas):
    grafo = nx.Graph()

    # Añadir nodos con posiciones
    for nodo, coord in coordenadas.items():
        grafo.add_node(nodo, pos=coord)

    # Añadir aristas según distancia
    nodos = list(coordenadas.keys())
    for i, nodo1 in enumerate(nodos):
        for j, nodo2 in enumerate(nodos):
            if i != j:
                distancia = calcular_distancia(coordenadas[nodo1], coordenadas[nodo2])
                if distancia <= 6:  # Conectar nodos cercanos (radio máximo de 6)
                    tiempo_estimado = distancia * 1.5 if nodo1 in ['Centro', 'Salamanca'] else distancia * 1.2
                    grafo.add_edge(nodo1, nodo2, weight=round(tiempo_estimado, 2))  # Redondear a 2 decimales
    return grafo

def calcular_ruta_mas_corta(grafo, origen, destino):
    # Usamos Dijkstra para encontrar la ruta más corta
    ruta = nx.dijkstra_path(grafo, source=origen, target=destino, weight='weight')
    return ruta

# Función para asignar colores a los nodos asegurando que nodos conectados no tengan el mismo color
def asignar_colores(grafo):
    # Usar una paleta de colores
    colores = list(plt.cm.tab10.colors)  # Paleta con 10 colores distintos
    colores_ciclo = cycle(colores)  # Ciclar sobre la paleta de colores

    color_nodos = {}
    for nodo in grafo.nodes:
        vecinos = list(grafo.neighbors(nodo))
        # Asignar un color único a cada nodo
        for color in colores_ciclo:
            # Verificar que el color no se repita con los vecinos
            if all(color != color_nodos.get(vecino) for vecino in vecinos):
                color_nodos[nodo] = color
                break

    return color_nodos

# Función para asignar colores a las aristas de acuerdo al nodo de origen
def asignar_colores_aristas(grafo, color_nodos):
    color_aristas = {}
    for u, v in grafo.edges:
        # Asignar el color de la arista según el nodo de origen
        color_aristas[(u, v)] = color_nodos[u]
    return color_aristas

# Añadir el nodo central 'Almacen' y conectarlo con el nodo más cercano de cada zona
def agregar_nodo_almacen(grafo, coordenadas):
    # Añadir el nodo central 'Almacen' con una posición arbitraria
    coordenadas['Almacen'] = (20, 20)  # Se coloca en el centro de las zonas

    grafo.add_node('Almacen', pos=coordenadas['Almacen'])

    # Definir las zonas
    zonas = {
        'Centro': [
            'Puerta del Sol', 'Plaza Mayor', 'Calle Arenal', 'Gran Vía', 'Plaza de España', 
            'Calle Mayor', 'Plaza de Oriente', 'Ópera', 'Calle Preciados', 'Callao'
        ],
        'Chamberí': [
            'Quevedo', 'Iglesia', 'Alonso Cano', 'Ríos Rosas', 'Canal', 'Islas Filipinas', 
            'San Bernardo', 'Argüelles', 'Moncloa', 'Guzmán el Bueno'
        ],
        'Salamanca': [
            'Velázquez', 'Serrano', 'Goya', 'Príncipe de Vergara', 'Diego de León', 
            'Lista', 'Manuel Becerra', 'Doctor Esquerdo', 'Avenida de América', 'Núñez de Balboa'
        ],
        'Chamartín': [
            'Chamartín', 'Plaza de Castilla', 'Pío XII', 'Cuzco', 'Santiago Bernabéu', 
            'Hispanoamérica', 'Colombia', 'Concha Espina', 'Duque de Pastrana', 'Plaza de Lima'
        ],
        'Retiro': [
            'Atocha', 'Menéndez Pelayo', 'Pacífico', 'Conde de Casal', 'Ibiza', 
            'Sainz de Baranda', 'Retiro', 'Prado', 'Neptuno', 'Cibeles'
        ]
    }
    # Para cada zona, conectar 'Almacen' con el nodo más cercano
    for zona, nodos_zona in zonas.items():
        nodo_cercano = min(nodos_zona, key=lambda nodo: calcular_distancia(coordenadas['Almacen'], coordenadas[nodo]))
        grafo.add_edge('Almacen', nodo_cercano, weight=round(calcular_distancia(coordenadas['Almacen'], coordenadas[nodo_cercano]), 2))  # Redondear a 2 decimales

G = crear_grafo(coordenadas)

# Agregar el nodo 'Almacen' y las conexiones
agregar_nodo_almacen(G, coordenadas)

color_nodos = asignar_colores(G)
color_aristas = asignar_colores_aristas(G, color_nodos)

# Dibujar el grafo
def dibujar_grafo(grafo, color_nodos, color_aristas, ruta_seleccionada):
    pos = nx.get_node_attributes(grafo, 'pos')  # Obtener posiciones de los nodos
    labels = nx.get_edge_attributes(grafo, 'weight')  # Obtener etiquetas de las aristas
    # Redondear las etiquetas de las aristas a 2 decimales
    labels = {k: round(v, 2) for k, v in labels.items()}  # Redondear distancias a 2 decimales
    
    # Dibujar las aristas
    for u, v, data in grafo.edges(data=True):
        if (u, v) in ruta_seleccionada or (v, u) in ruta_seleccionada:
            # Si la arista está en la ruta seleccionada, colorearla de negro y aumentar el grosor
            nx.draw_networkx_edges(grafo, pos, edgelist=[(u, v)], width=3, edge_color='black')
        else:
            # Dibujar la arista con el color predeterminado
            nx.draw_networkx_edges(grafo, pos, edgelist=[(u, v)], width=1, edge_color=color_aristas.get((u, v), 'gray'))

    # Dibujar los nodos
    nx.draw_networkx_nodes(grafo, pos, node_color=list(color_nodos.values()), node_size=500)

    # Dibujar las etiquetas de los nodos
    nx.draw_networkx_labels(grafo, pos, font_size=10, font_weight='bold')

    # Dibujar las etiquetas de las aristas (distancias)
    # nx.draw_networkx_edge_labels(grafo, pos, edge_labels=labels)

    plt.title('Grafo de Rutas de envio')
    plt.show()

destino = input("Introduce el destino desde el Almacen: ")
ruta_seleccionada = calcular_ruta_mas_corta(G, 'Almacen', destino)

# Función para calcular distancia desde el Almacen a un destino
def calcular_distancia_desde_almacen():
    # Verificar si el destino existe en las coordenadas
    if destino in coordenadas:
        # Calcular la distancia desde el Almacen
        distancia = calcular_distancia(coordenadas['Almacen'], coordenadas[destino])
        # Redondear la distancia a 2 decimales
        distancia = round(distancia, 2)

# Llamar a la función para calcular la distancia
calcular_distancia_desde_almacen()
# Imprimir la ruta más corta y los nodos por los que pasa
print(f"Ruta más corta desde 'Almacen' a {destino}: {ruta_seleccionada}")
print("Nodos por los que ha pasado la ruta:")
for nodo in ruta_seleccionada:
    print(f"- {nodo}")

# Llamar a la función de visualización con la ruta seleccionada
dibujar_grafo(G, color_nodos, color_aristas, ruta_seleccionada)


# El algoritmo de Dijkstra encuentra la ruta más corta entre un nodo de origen y otros nodos en un grafo ponderado. 
# Comienza asignando una distancia de 0 al nodo origen y distancias infinitas a los demás nodos. 
# Luego, selecciona el nodo con la menor distancia no visitado, actualiza las distancias de sus vecinos y lo marca como visitado. 
# Repite este proceso hasta encontrar la ruta más corta hacia el destino.

