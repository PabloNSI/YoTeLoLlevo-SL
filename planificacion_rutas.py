import math
import networkx as nx
import matplotlib.pyplot as plt
from itertools import cycle
from datos import coordenadas, zonas, colores  # Importar datos externos para nodos, zonas y colores

# Función para normalizar el texto
def normalizar_texto(texto):
    # Tabla de mapeo de caracteres con tildes a caracteres sin tildes
    mapeo_tildes = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'a', 'É': 'e', 'Í': 'i', 'Ó': 'o', 'Ú': 'u',
        'ñ': 'n', 'Ñ': 'n', 'ü': 'u', 'Ü': 'u'
    }
    # Reemplaza caracteres con tildes por sus equivalentes sin tildes
    texto_normalizado = ''.join(mapeo_tildes.get(c, c) for c in texto)
    # Elimina espacios innecesarios y convierte a minúsculas
    return texto_normalizado.strip().lower()

# Calcular distancia euclidiana (en línea recta) entre dos nodos
def calcular_distancia(coord1, coord2):
    # Usar la fórmula de distancia euclidiana entre dos coordenadas x e y
    return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

# Crear grafo con networkx
def crear_grafo(coordenadas):
    grafo = nx.Graph()  # Crear un grafo vacío

    # Añadir nodos con posiciones
    for nodo, coord in coordenadas.items():
        grafo.add_node(nodo, pos=coord)  # Agregar cada nodo con su posición

    # Añadir aristas según distancia
    nodos = list(coordenadas.keys())  # Obtener la lista de nodos
    for i, nodo1 in enumerate(nodos): # Iterar sobre cada nodo (indice, nodo)
        for j, nodo2 in enumerate(nodos):
            if i != j:  # Evitar agregar aristas de un nodo consigo mismo
                distancia = calcular_distancia(coordenadas[nodo1], coordenadas[nodo2])
                if distancia <= 3:  # Conectar nodos cercanos (radio máximo de 3)
                    grafo.add_edge(nodo1, nodo2, weight=round(distancia * 1.2, 2))  # Redondear a 2 decimales
    return grafo

G = crear_grafo(coordenadas)  # Crear el grafo utilizando las coordenadas

# Función que calcula la ruta más corta
def calcular_ruta_mas_corta(grafo, origen, destino):
    # Usamos Dijkstra con networkx para encontrar la ruta más corta
    try:
        return nx.dijkstra_path(grafo, source=origen, target=destino, weight='weight')
    except nx.NetworkXNoPath:  # Manejar el caso en el que no exista un camino
        print("No existe una ruta entre el almacen y el destino.")
        return None

# Función para asignar colores a los nodos asegurando que nodos conectados no tengan el mismo color
def asignar_colores(grafo):
    colores_ciclo = cycle(colores)  # Crear un ciclo infinito sobre la paleta

    color_nodos = {}
    for nodo in grafo.nodes:
        vecinos = list(grafo.neighbors(nodo))  # Obtener los vecinos del nodo
        # Asignar un color único a cada nodo
        for color in colores_ciclo:
            # Verificar que el color no se repita con los vecinos
            if all(color != color_nodos.get(vecino) for vecino in vecinos):
                color_nodos[nodo] = color  # Asignar color al nodo actual
                break

    return color_nodos

color_nodos = asignar_colores(G)  # Asignar colores a los nodos del grafo

# Función para validar el destino
def validar_destino(destino):
    for nodo in coordenadas.keys():
        if normalizar_texto(nodo) == normalizar_texto(destino):
            return nodo  # Retornar el nodo correspondiente si se encuentra una coincidencia
    return None  # Retornar None si no se encuentra el destino

# Añadir el nodo central 'Almacen' y conectarlo con el nodo más cercano de cada zona
def agregar_nodo_almacen(grafo, coordenadas):
    coordenadas['Almacen'] = (20, 20)  # Asignar una posición fija para el nodo 'Almacen'

    grafo.add_node('Almacen', pos=coordenadas['Almacen'])  # Añadir el nodo 'Almacen' al grafo
    for zona, nodos_zona in zonas.items():
        print("Procesando zona: "+str(zona)) 
        # Encontrar el nodo más cercano al 'Almacen' en cada zona
        nodo_cercano = min(nodos_zona, key=lambda nodo: calcular_distancia(coordenadas['Almacen'], coordenadas[nodo]))
          # Conectar con el nodo más cercano
        grafo.add_edge('Almacen', nodo_cercano, weight=round(calcular_distancia(coordenadas['Almacen'], coordenadas[nodo_cercano]), 2))

# Agregar el nodo 'Almacen'
agregar_nodo_almacen(G, coordenadas)

# Función para dibujar el grafo
def dibujar_grafo(grafo, color_nodos, ruta_seleccionada):
    pos = nx.get_node_attributes(grafo, 'pos')  # Obtener posiciones de los nodos
    labels = nx.get_edge_attributes(grafo, 'weight')  # Obtener etiquetas de las aristas
    labels = {k: round(v, 2) for k, v in labels.items()}  # Redondear distancias a 2 decimales

    # Dibujar nodos con sus colores
    nx.draw_networkx_nodes(grafo, pos, node_size=500, node_color=[color_nodos.get(nodo, 'grey') for nodo in grafo.nodes])

    # Dibujar las aristas (ruta óptima)
    for u, v in grafo.edges():
        if (u, v) in ruta_seleccionada or (v, u) in ruta_seleccionada: #ruta_seleccionada en Linea 134
            # Resaltar ruta óptima
            nx.draw_networkx_edges(grafo, pos, edgelist=[(u, v)], width=5, edge_color='black')  
        else:
            # Dibujar con color predeterminado
            nx.draw_networkx_edges(grafo, pos, edgelist=[(u, v)], width=1, edge_color=grafo[u][v].get('color', 'grey'))  

    # Dibujar las etiquetas de los nodos
    nx.draw_networkx_labels(grafo, pos, font_size=10, font_weight='bold')

    # Resaltar la ruta seleccionada
    if ruta_seleccionada:
        path_edges = list(zip(ruta_seleccionada, ruta_seleccionada[1:]))
        nx.draw_networkx_edges(grafo, pos, edgelist=path_edges, edge_color='black', width=6)

    plt.show()

# Lógica principal para obtener y validar el destino
while True:
    destino = input("Introduce el destino desde el Almacen: ")
    nodo_destino = validar_destino(destino)

    if nodo_destino: # Si el destino es válido
        print("La ruta hacia "+str(nodo_destino)+ " es válida.")
        break
    else:
        print("Destino no válido. Por favor, inténtalo nuevamente.")

# Calcular la ruta más corta
ruta_seleccionada = calcular_ruta_mas_corta(G, 'Almacen', nodo_destino)

# Imprimir la ruta más corta y los nodos por los que pasa
print("Ruta más corta desde el almacen a "+str(destino)+": "+str(ruta_seleccionada))
print("Nodos por los que ha pasado la ruta:")

# Imprimir los nodos por los que pasa la ruta
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

