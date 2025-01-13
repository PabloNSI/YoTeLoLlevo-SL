import math
import networkx as nx
import matplotlib.pyplot as plt
from itertools import cycle
from datos import coordenadas, zonas, colores
import unicodedata

def normalizar_texto(texto):
    # Elimina tildes, convierte a minúsculas y elimina espacios innecesarios
    texto = ''.join(
        (c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
    )
    return texto.strip().lower()

# Calcular distancia euclidiana
def calcular_distancia(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

# Crear grafo con networkx
def crear_grafo(coordenadas):
    grafo = nx.Graph()

    # Añadir nodos con posiciones
    for nodo, coord in coordenadas.items():
        grafo.add_node(nodo, pos=coord)

    # Asignar colores a las zonas
    zona_colores = {zona: colores[i % len(colores)] for i, zona in enumerate(zonas)}

    # Añadir nodos con posiciones
    for nodo, coord in coordenadas.items():
        grafo.add_node(nodo, pos=coord)

    # Añadir aristas según distancia
    nodos = list(coordenadas.keys())
    for i, nodo1 in enumerate(nodos):
        for j, nodo2 in enumerate(nodos):
            if i != j:
                distancia = calcular_distancia(coordenadas[nodo1], coordenadas[nodo2])
                if distancia <= 3:  # Conectar nodos cercanos (radio máximo de 3)
                    tiempo_estimado = distancia * 1.5 if nodo1 in ['Centro', 'Salamanca'] else distancia * 1.2
                    grafo.add_edge(nodo1, nodo2, weight=round(tiempo_estimado, 2))  # Redondear a 2 decimales
    return grafo

def calcular_ruta_mas_corta(grafo, origen, destino):
    # Usamos Dijkstra para encontrar la ruta más corta
    try:
        ruta = nx.dijkstra_path(grafo, source=origen, target=destino, weight='weight')
        return ruta
    except nx.NetworkXNoPath:
        print("No existe una ruta entre el origen y el destino.")
        return None

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

def validar_destino(destino):
    destino_normalizado = normalizar_texto(destino)
    for nodo in coordenadas.keys():
        if normalizar_texto(nodo) == destino_normalizado:
            return nodo
    return None

# Añadir el nodo central 'Almacen' y conectarlo con el nodo más cercano de cada zona
def agregar_nodo_almacen(grafo, coordenadas):
    # Añadir el nodo central 'Almacen' con una posición arbitraria
    coordenadas['Almacen'] = (20, 20)  # Se coloca en el centro de las zonas

    grafo.add_node('Almacen', pos=coordenadas['Almacen'])
    # Para cada zona, conectar 'Almacen' con el nodo más cercano
    for zona, nodos_zona in zonas.items():
        nodo_cercano = min(nodos_zona, key=lambda nodo: calcular_distancia(coordenadas['Almacen'], coordenadas[nodo]))
        grafo.add_edge('Almacen', nodo_cercano, weight=round(calcular_distancia(coordenadas['Almacen'], coordenadas[nodo_cercano]), 2))  # Redondear a 2 decimales

G = crear_grafo(coordenadas)

# Agregar el nodo 'Almacen' y las conexiones
agregar_nodo_almacen(G, coordenadas)
color_nodos = asignar_colores(G)

def dibujar_grafo(grafo, color_nodos, ruta_seleccionada):
    pos = nx.get_node_attributes(grafo, 'pos')  # Obtener posiciones de los nodos
    edge_colors = [grafo[u][v].get('color', 'grey') for u, v in grafo.edges()]
    labels = nx.get_edge_attributes(grafo, 'weight')  # Obtener etiquetas de las aristas
    labels = {k: round(v, 2) for k, v in labels.items()}  # Redondear distancias a 2 decimales

    # Dibujar nodos
    nx.draw_networkx_nodes(grafo, pos, node_size=500)

    # Dibujar aristas con colores
    nx.draw_networkx_edges(grafo, pos, edge_color=edge_colors)

    # Dibujar las aristas (ruta óptima)
    for u, v, data in grafo.edges(data=True):
        if (u, v) in ruta_seleccionada or (v, u) in ruta_seleccionada:
            # Si la arista está en la ruta seleccionada, colorearla de negro y aumentar el grosor
            nx.draw_networkx_edges(grafo, pos, edgelist=[(u, v)], width=3, edge_color='black')
        else:
            # Dibujar la arista con el color predeterminado
            nx.draw_networkx_edges(grafo, pos, edgelist=[(u, v)], width=1, edge_color=grafo[u][v].get('color', 'grey'))

    # Dibujar los nodos
    nx.draw_networkx_nodes(grafo, pos, node_color=list(color_nodos.values()), node_size=500)

    # Dibujar las etiquetas de los nodos
    nx.draw_networkx_labels(grafo, pos, font_size=10, font_weight='bold')

    # Resaltar la ruta seleccionada
    if ruta_seleccionada:
        path_edges = list(zip(ruta_seleccionada, ruta_seleccionada[1:]))
        nx.draw_networkx_edges(grafo, pos, edgelist=path_edges, edge_color='black', width=2)

    plt.show()


# Lógica principal para obtener y validar el destino
while True:
    destino = input("Introduce el destino desde el Almacen: ")
    nodo_destino = validar_destino(destino)

    if nodo_destino:
        print("La ruta hacia "+str(nodo_destino)+ " es válida.")
        break
    else:
        print("Destino no válido. Por favor, inténtalo nuevamente.")

# Calcular la ruta más corta
ruta_seleccionada = calcular_ruta_mas_corta(G, 'Almacen', nodo_destino)

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
print("Ruta más corta desde el almacen a "+str(destino)+": "+str(ruta_seleccionada))
print("Nodos por los que ha pasado la ruta:")
for nodo in ruta_seleccionada:
    print("- "+str(nodo))

# Dibujar el grafo con la ruta seleccionada
if ruta_seleccionada:
    dibujar_grafo(G, color_nodos, ruta_seleccionada)
else:
    print("No se puede dibujar la ruta porque no existe un camino válido.")

# Variable global para el destino validado
destino_validado = nodo_destino


# El algoritmo de Dijkstra encuentra la ruta más corta entre un nodo de origen y otros nodos en un grafo ponderado. 
# Comienza asignando una distancia de 0 al nodo origen y distancias infinitas a los demás nodos. 
# Luego, selecciona el nodo con la menor distancia no visitado, actualiza las distancias de sus vecinos y lo marca como visitado. 
# Repite este proceso hasta encontrar la ruta más corta hacia el destino.

