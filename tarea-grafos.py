import sys
import os
import random
import heapq
from collections import deque
import time

# Intentar importar matplotlib para visualización (opcional)
try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    import numpy as np
    from matplotlib.colors import ListedColormap
    MATPLOTLIB_DISPONIBLE = True
except ImportError:
    MATPLOTLIB_DISPONIBLE = False
    print("matplotlib no instalado. Usando visualización textual.")

# Intentar importar networkx para visualización de grafos (opcional)
try:
    import networkx as nx
    NETWORKX_DISPONIBLE = True
except ImportError:
    NETWORKX_DISPONIBLE = False

# CLASE LABERINTO

class Laberinto:
    """Clase para representar un laberinto como matriz"""
    
    def __init__(self, matriz):
        self.matriz = matriz
        self.filas = len(matriz)
        self.columnas = len(matriz[0]) if self.filas > 0 else 0
    
    def es_valida(self, fila, columna):
        """Verifica si una posición es válida (dentro de la matriz y libre)"""
        if 0 <= fila < self.filas and 0 <= columna < self.columnas:
            return self.matriz[fila][columna] == 0
        return False
    
    def obtener_vecinos(self, posicion):
        """Obtiene los vecinos válidos de una posición (4 direcciones)"""
        fila, columna = posicion
        vecinos = []
        
        # Movimientos: arriba, abajo, izquierda, derecha
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for df, dc in direcciones:
            nf, nc = fila + df, columna + dc
            if self.es_valida(nf, nc):
                vecinos.append((nf, nc))
        
        return vecinos
    
    def obtener_vecinos_con_costo(self, posicion):
        """Obtiene vecinos con costo (para UCS)"""
        vecinos = self.obtener_vecinos(posicion)
        return [(v, 1) for v in vecinos]  # Costo 1 por paso
    
    def es_objetivo(self, posicion, objetivo):
        """Verifica si la posición es el objetivo"""
        return posicion == objetivo
    
    def get_heuristica(self, posicion, objetivo):
        """Heurística para A* (distancia Manhattan)"""
        return abs(posicion[0] - objetivo[0]) + abs(posicion[1] - objetivo[1])
    
    def mostrar(self):
        """Muestra el laberinto de forma textual"""
        print("\n" + "-"*50)
        print("LABERINTO")
        print("-"*50)
        print("  " + " ".join([str(i) for i in range(self.columnas)]))
        for i, fila in enumerate(self.matriz):
            fila_str = f"{i} "
            for j, celda in enumerate(fila):
                if celda == 1:
                    fila_str += "██ "
                else:
                    fila_str += "·  "
            print(fila_str)
    
    @classmethod
    def crear_laberinto_ejemplo(cls):
        """Crea un laberinto de ejemplo"""
        matriz = [
            [0, 1, 0, 0, 0, 0, 1, 0],
            [0, 1, 0, 1, 1, 0, 1, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [1, 1, 0, 1, 0, 1, 1, 0],
            [0, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 1, 1, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 1, 0, 0]
        ]
        return cls(matriz)
    
    @classmethod
    def crear_laberinto_ejemplo2(cls):
        """Crea un laberinto más grande de ejemplo"""
        matriz = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 0, 1, 1, 0],
            [0, 1, 0, 0, 0, 1, 0, 1, 0, 0],
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [0, 1, 0, 1, 0, 0, 0, 1, 0, 0],
            [0, 1, 0, 1, 1, 1, 0, 1, 1, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        return cls(matriz)
    
    @classmethod
    def generar_aleatorio(cls, filas, columnas, densidad=0.3):
        """Genera un laberinto aleatorio"""
        matriz = [[1 if random.random() < densidad else 0 for _ in range(columnas)] for _ in range(filas)]
        
        # Asegurar que la entrada y salida estén libres
        matriz[0][0] = 0
        matriz[filas-1][columnas-1] = 0
        
        return cls(matriz)
    
    @classmethod
    def cargar_desde_archivo(cls, archivo):
        """Carga un laberinto desde archivo"""
        try:
            matriz = []
            with open(archivo, 'r') as f:
                for linea in f:
                    if linea.strip():
                        # Eliminar espacios y convertir a enteros
                        fila = [int(c) for c in linea.strip().replace(' ', '')]
                        matriz.append(fila)
            return cls(matriz)
        except Exception as e:
            print(f"❌ Error al cargar archivo: {e}")
            return None

# CLASE GRAFO

class Grafo:
    """Clase para representar un grafo ponderado"""
    
    def __init__(self):
        self.adyacencia = {}  # Diccionario de adyacencia
        self.nodos = set()
    
    def agregar_arista(self, origen, destino, peso=1):
        """Agrega una arista al grafo"""
        if origen not in self.adyacencia:
            self.adyacencia[origen] = []
        self.adyacencia[origen].append((destino, peso))
        self.nodos.add(origen)
        self.nodos.add(destino)
    
    def obtener_vecinos(self, nodo):
        """Obtiene los vecinos de un nodo"""
        return self.adyacencia.get(nodo, [])
    
    def obtener_nodos(self):
        """Obtiene todos los nodos del grafo"""
        return list(self.nodos)
    
    def crear_grafo_ejemplo(self):
        """Crea un grafo de ejemplo (versión simplificada de Rumania)"""
        # Ciudades de Rumania con distancias en km
        aristas = [
            ("Arad", "Zerind", 75),
            ("Arad", "Sibiu", 140),
            ("Arad", "Timisoara", 118),
            ("Zerind", "Oradea", 71),
            ("Oradea", "Sibiu", 151),
            ("Sibiu", "Fagaras", 99),
            ("Sibiu", "Rimnicu", 80),
            ("Rimnicu", "Pitesti", 97),
            ("Rimnicu", "Craiova", 146),
            ("Pitesti", "Bucharest", 101),
            ("Fagaras", "Bucharest", 211),
            ("Bucharest", "Giurgiu", 90),
            ("Bucharest", "Urziceni", 85),
            ("Urziceni", "Vaslui", 142),
            ("Urziceni", "Hirsova", 98),
            ("Hirsova", "Eforie", 86),
            ("Vaslui", "Iasi", 92),
            ("Iasi", "Neamt", 87),
            ("Timisoara", "Lugoj", 111),
            ("Lugoj", "Mehadia", 70),
            ("Mehadia", "Drobeta", 75),
            ("Drobeta", "Craiova", 120),
            ("Craiova", "Pitesti", 138)
        ]
        
        for origen, destino, peso in aristas:
            self.agregar_arista(origen, destino, peso)
            # Grafo no dirigido
            self.agregar_arista(destino, origen, peso)
    
    def crear_grafo_simple(self):
        """Crea un grafo simple para pruebas"""
        aristas = [
            ("A", "B", 5),
            ("A", "C", 3),
            ("B", "D", 2),
            ("B", "E", 4),
            ("C", "F", 6),
            ("D", "G", 1),
            ("E", "G", 3),
            ("F", "G", 2),
            ("A", "D", 7),
            ("C", "E", 8)
        ]
        
        for origen, destino, peso in aristas:
            self.agregar_arista(origen, destino, peso)
            self.agregar_arista(destino, origen, peso)
    
    def cargar_desde_csv(self, archivo):
        """Carga un grafo desde un archivo CSV"""
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                for linea in f:
                    if linea.strip():
                        partes = linea.strip().split(',')
                        if len(partes) >= 3:
                            origen, destino, peso = partes[0], partes[1], float(partes[2])
                            self.agregar_arista(origen, destino, peso)
                            self.agregar_arista(destino, origen, peso)
            print(f"Grafo cargado desde {archivo}")
        except Exception as e:
            print(f"Error al cargar archivo: {e}")
    
    def mostrar(self):
        """Muestra el grafo en formato legible"""
        print("\n" + "-"*50)
        print("GRAFO")
        print("-"*50)
        for nodo in sorted(self.nodos):
            vecinos = self.adyacencia.get(nodo, [])
            if vecinos:
                vecinos_str = ", ".join([f"{v}({p})" for v, p in vecinos])
                print(f"{nodo} -> {vecinos_str}")
    
    def get_heuristica(self, nodo, objetivo):
        """Heurística para A* (distancia en línea recta)"""
        # Coordenadas aproximadas de ciudades
        coordenadas = {
            "Arad": (46.17, 21.32),
            "Bucharest": (44.43, 26.10),
            "Craiova": (44.32, 23.80),
            "Drobeta": (44.63, 22.66),
            "Eforie": (44.06, 28.63),
            "Fagaras": (45.84, 24.97),
            "Giurgiu": (43.90, 25.97),
            "Hirsova": (44.69, 27.95),
            "Iasi": (47.16, 27.59),
            "Lugoj": (45.69, 21.90),
            "Mehadia": (44.90, 22.36),
            "Neamt": (46.98, 26.38),
            "Oradea": (47.05, 21.93),
            "Pitesti": (44.86, 24.88),
            "Rimnicu": (45.10, 24.37),
            "Sibiu": (45.80, 24.15),
            "Timisoara": (45.75, 21.23),
            "Urziceni": (44.72, 26.63),
            "Vaslui": (46.63, 27.73),
            "Zerind": (46.63, 21.52),
            # Para grafo simple
            "A": (0, 0), "B": (1, 1), "C": (-1, 1),
            "D": (2, 0), "E": (-2, 0), "F": (0, -2),
            "G": (0, 2)
        }
        
        import math
        if nodo in coordenadas and objetivo in coordenadas:
            x1, y1 = coordenadas[nodo]
            x2, y2 = coordenadas[objetivo]
            return math.sqrt((x1-x2)**2 + (y1-y2)**2) * 100
        return 0

# ALGORITMOS DE BÚSQUEDA

class BFS:
    """Implementación de BFS (Breadth-First Search)"""
    
    @staticmethod
    def buscar(grafo, inicio, objetivo):
        """Búsqueda en grafo"""
        visitados = set()
        cola = deque([(inicio, [inicio])])
        visitados.add(inicio)
        orden_visita = []
        
        while cola:
            nodo, camino = cola.popleft()
            orden_visita.append(nodo)
            
            if nodo == objetivo:
                return {
                    'camino': camino,
                    'visitados': orden_visita,
                    'costo': len(camino) - 1,
                    'algoritmo': 'BFS'
                }
            
            for vecino, _ in grafo.obtener_vecinos(nodo):
                if vecino not in visitados:
                    visitados.add(vecino)
                    cola.append((vecino, camino + [vecino]))
        
        return None
    
    @staticmethod
    def buscar_laberinto(laberinto, inicio, objetivo):
        """Búsqueda en laberinto"""
        visitados = set()
        cola = deque([(inicio, [inicio])])
        visitados.add(inicio)
        orden_visita = []
        
        while cola:
            pos, camino = cola.popleft()
            orden_visita.append(pos)
            
            if laberinto.es_objetivo(pos, objetivo):
                return {
                    'camino': camino,
                    'visitados': orden_visita,
                    'costo': len(camino) - 1,
                    'algoritmo': 'BFS'
                }
            
            for vecino in laberinto.obtener_vecinos(pos):
                if vecino not in visitados:
                    visitados.add(vecino)
                    cola.append((vecino, camino + [vecino]))
        
        return None


class DFS:
    """Implementación de DFS (Depth-First Search)"""
    
    @staticmethod
    def buscar(grafo, inicio, objetivo):
        """Búsqueda en grafo"""
        visitados = set()
        pila = [(inicio, [inicio])]
        orden_visita = []
        
        while pila:
            nodo, camino = pila.pop()
            
            if nodo in visitados:
                continue
            
            visitados.add(nodo)
            orden_visita.append(nodo)
            
            if nodo == objetivo:
                return {
                    'camino': camino,
                    'visitados': orden_visita,
                    'costo': len(camino) - 1,
                    'algoritmo': 'DFS'
                }
            
            vecinos = grafo.obtener_vecinos(nodo)
            for vecino, _ in reversed(vecinos):
                if vecino not in visitados:
                    pila.append((vecino, camino + [vecino]))
        
        return None
    
    @staticmethod
    def buscar_laberinto(laberinto, inicio, objetivo):
        """Búsqueda en laberinto"""
        visitados = set()
        pila = [(inicio, [inicio])]
        orden_visita = []
        
        while pila:
            pos, camino = pila.pop()
            
            if pos in visitados:
                continue
            
            visitados.add(pos)
            orden_visita.append(pos)
            
            if laberinto.es_objetivo(pos, objetivo):
                return {
                    'camino': camino,
                    'visitados': orden_visita,
                    'costo': len(camino) - 1,
                    'algoritmo': 'DFS'
                }
            
            for vecino in laberinto.obtener_vecinos(pos):
                if vecino not in visitados:
                    pila.append((vecino, camino + [vecino]))
        
        return None


class UCS:
    """Implementación de UCS (Uniform Cost Search)"""
    
    @staticmethod
    def buscar(grafo, inicio, objetivo):
        """Búsqueda en grafo"""
        visitados = set()
        cola = [(0, inicio, [inicio])]
        orden_visita = []
        
        while cola:
            costo, nodo, camino = heapq.heappop(cola)
            
            if nodo in visitados:
                continue
            
            visitados.add(nodo)
            orden_visita.append(nodo)
            
            if nodo == objetivo:
                return {
                    'camino': camino,
                    'visitados': orden_visita,
                    'costo': costo,
                    'algoritmo': 'UCS'
                }
            
            for vecino, peso in grafo.obtener_vecinos(nodo):
                if vecino not in visitados:
                    heapq.heappush(cola, (costo + peso, vecino, camino + [vecino]))
        
        return None
    
    @staticmethod
    def buscar_laberinto(laberinto, inicio, objetivo):
        """Búsqueda en laberinto"""
        visitados = set()
        cola = [(0, inicio, [inicio])]
        orden_visita = []
        
        while cola:
            costo, pos, camino = heapq.heappop(cola)
            
            if pos in visitados:
                continue
            
            visitados.add(pos)
            orden_visita.append(pos)
            
            if laberinto.es_objetivo(pos, objetivo):
                return {
                    'camino': camino,
                    'visitados': orden_visita,
                    'costo': costo,
                    'algoritmo': 'UCS'
                }
            
            for vecino in laberinto.obtener_vecinos(pos):
                if vecino not in visitados:
                    heapq.heappush(cola, (costo + 1, vecino, camino + [vecino]))
        
        return None


class AStar:
    """Implementación de A* (A-Star Search)"""
    
    @staticmethod
    def buscar(grafo, inicio, objetivo):
        """Búsqueda en grafo"""
        visitados = set()
        cola = [(0, 0, inicio, [inicio])]
        orden_visita = []
        costos = {inicio: 0}
        
        while cola:
            f, g, nodo, camino = heapq.heappop(cola)
            
            if nodo in visitados:
                continue
            
            visitados.add(nodo)
            orden_visita.append(nodo)
            
            if nodo == objetivo:
                return {
                    'camino': camino,
                    'visitados': orden_visita,
                    'costo': g,
                    'algoritmo': 'A*'
                }
            
            for vecino, peso in grafo.obtener_vecinos(nodo):
                if vecino not in visitados:
                    nuevo_g = g + peso
                    if vecino not in costos or nuevo_g < costos[vecino]:
                        costos[vecino] = nuevo_g
                        h = grafo.get_heuristica(vecino, objetivo)
                        f = nuevo_g + h
                        heapq.heappush(cola, (f, nuevo_g, vecino, camino + [vecino]))
        
        return None
    
    @staticmethod
    def buscar_laberinto(laberinto, inicio, objetivo):
        """Búsqueda en laberinto"""
        visitados = set()
        cola = [(0, 0, inicio, [inicio])]
        orden_visita = []
        costos = {inicio: 0}
        
        while cola:
            f, g, pos, camino = heapq.heappop(cola)
            
            if pos in visitados:
                continue
            
            visitados.add(pos)
            orden_visita.append(pos)
            
            if laberinto.es_objetivo(pos, objetivo):
                return {
                    'camino': camino,
                    'visitados': orden_visita,
                    'costo': g,
                    'algoritmo': 'A*'
                }
            
            for vecino in laberinto.obtener_vecinos(pos):
                if vecino not in visitados:
                    nuevo_g = g + 1
                    if vecino not in costos or nuevo_g < costos[vecino]:
                        costos[vecino] = nuevo_g
                        h = laberinto.get_heuristica(vecino, objetivo)
                        f = nuevo_g + h
                        heapq.heappush(cola, (f, nuevo_g, vecino, camino + [vecino]))
        
        return None

# VISUALIZACIÓN

class Visualizador:
    """Clase para visualizar grafos y laberintos"""
    
    @staticmethod
    def mostrar_laberinto_textual(laberinto, resultado):
        """Visualización textual del laberinto"""
        if resultado is None:
            print("No hay resultados para mostrar")
            return
        
        print("\n" + "="*60)
        print("VISUALIZACIÓN DEL LABERINTO")
        print("="*60)
        
        camino = resultado['camino']
        visitados = resultado['visitados']
        visitados_set = set(visitados)
        camino_set = set(camino)
        
        print(f"\nAlgoritmo: {resultado.get('algoritmo', '')}")
        print(f"Pasos: {len(camino)}")
        print(f"Nodos visitados: {len(visitados)}")
        print("\n")
        
        print("Leyenda:")
        print("  · = Libre")
        print("  █ = Barrera")
        print("  * = Visitado")
        print("  # = Camino")
        print("  S = Inicio")
        print("  G = Objetivo")
        print("\n")
        
        # Mostrar laberinto con el camino
        for i in range(laberinto.filas):
            fila_str = f"{i:2} "
            for j in range(laberinto.columnas):
                if laberinto.matriz[i][j] == 1:
                    fila_str += "██ "
                elif (i, j) == camino[0]:
                    fila_str += "S  "
                elif (i, j) == camino[-1]:
                    fila_str += "G  "
                elif (i, j) in camino_set:
                    fila_str += "#  "
                elif (i, j) in visitados_set:
                    fila_str += "*  "
                else:
                    fila_str += "·  "
            print(fila_str)
        
        print("\n" + "-"*60)
        print("Camino encontrado:")
        for i, paso in enumerate(camino):
            print(f"  Paso {i}: {paso}")
    
    @staticmethod
    def mostrar_laberinto_grafico(laberinto, resultado):
        """Visualización gráfica del laberinto usando matplotlib"""
        if not MATPLOTLIB_DISPONIBLE:
            Visualizador.mostrar_laberinto_textual(laberinto, resultado)
            return
        
        if resultado is None:
            print("No hay resultados para mostrar")
            return
        
        matriz = np.array(laberinto.matriz)
        filas, columnas = matriz.shape
        
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # Crear matriz para visualización
        visual = matriz.copy()
        visitados = resultado['visitados']
        camino = resultado['camino']
        
        # Marcar visitados (2)
        for pos in visitados:
            if pos not in camino:
                visual[pos[0]][pos[1]] = 2
        
        # Marcar camino (3)
        for pos in camino:
            visual[pos[0]][pos[1]] = 3
        
        # Marcar inicio (4) y objetivo (5)
        inicio = camino[0]
        objetivo = camino[-1]
        visual[inicio[0]][inicio[1]] = 4
        visual[objetivo[0]][objetivo[1]] = 5
        
        # Colores personalizados
        cmap = ListedColormap(['white', 'black', 'yellow', 'red', 'green', 'lightgreen'])
        
        # Mostrar matriz
        im = ax.imshow(visual, cmap=cmap, interpolation='nearest')
        
        # Agregar grid
        ax.set_xticks(np.arange(-0.5, columnas, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, filas, 1), minor=True)
        ax.grid(which="minor", color="gray", linestyle='-', linewidth=0.5)
        
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Título
        titulo = f"Laberinto - {resultado.get('algoritmo', '')}\n"
        titulo += f"Camino: {len(camino)} pasos | Visitados: {len(visitados)}"
        ax.set_title(titulo, fontsize=14, fontweight='bold')
        
        # Leyenda
        legend_elements = [
            plt.Rectangle((0,0),1,1, facecolor='white', edgecolor='black', label='Libre'),
            plt.Rectangle((0,0),1,1, facecolor='black', edgecolor='black', label='Barrera'),
            plt.Rectangle((0,0),1,1, facecolor='yellow', edgecolor='black', label='Visitado'),
            plt.Rectangle((0,0),1,1, facecolor='red', edgecolor='black', label='Camino'),
            plt.Rectangle((0,0),1,1, facecolor='green', edgecolor='black', label='Inicio'),
            plt.Rectangle((0,0),1,1, facecolor='lightgreen', edgecolor='black', label='Objetivo')
        ]
        ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.15, 1))
        
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def mostrar_grafo(grafo, resultado):
        """Visualiza el grafo con el camino encontrado"""
        if resultado is None:
            print("No hay resultados para mostrar")
            return
        
        if NETWORKX_DISPONIBLE and MATPLOTLIB_DISPONIBLE:
            # Crear grafo de networkx
            G = nx.Graph()
            
            for nodo, vecinos in grafo.adyacencia.items():
                for vecino, peso in vecinos:
                    G.add_edge(nodo, vecino, weight=peso)
            
            pos = nx.spring_layout(G, seed=42)
            
            fig, ax = plt.subplots(figsize=(12, 8))
            
            # Dibujar todos los nodos y aristas
            nx.draw_networkx_nodes(G, pos, node_color='lightblue', 
                                  node_size=500, ax=ax)
            nx.draw_networkx_edges(G, pos, edge_color='gray', width=1, ax=ax)
            nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold', ax=ax)
            
            # Resaltar camino
            camino = resultado['camino']
            aristas_camino = [(camino[i], camino[i+1]) for i in range(len(camino)-1)]
            
            # Dibujar aristas del camino en rojo
            nx.draw_networkx_edges(G, pos, edgelist=aristas_camino, 
                                  edge_color='red', width=3, ax=ax)
            
            # Resaltar nodos del camino
            nx.draw_networkx_nodes(G, pos, nodelist=camino, 
                                  node_color='orange', node_size=600, ax=ax)
            
            # Resaltar inicio y objetivo
            nx.draw_networkx_nodes(G, pos, nodelist=[camino[0]], 
                                  node_color='green', node_size=700, ax=ax)
            nx.draw_networkx_nodes(G, pos, nodelist=[camino[-1]], 
                                  node_color='red', node_size=700, ax=ax)
            
            # Título
            titulo = f"Grafo - {resultado.get('algoritmo', '')}\n"
            titulo += f"Camino: {' → '.join(camino)}"
            ax.set_title(titulo, fontsize=14, fontweight='bold')
            
            plt.tight_layout()
            plt.show()
        else:
            # Visualización textual
            print("\n" + "="*60)
            print("VISUALIZACIÓN DEL GRAFO")
            print("="*60)
            print(f"\nAlgoritmo: {resultado.get('algoritmo', '')}")
            print(f"Camino: {' -> '.join(resultado['camino'])}")
            print(f"Costo: {resultado.get('costo', 0)}")
            print(f"Nodos visitados: {len(resultado['visitados'])}")
            print(f"Orden de visita: {' -> '.join(resultado['visitados'])}")

# COMPARADOR DE ALGORITMOS

class Comparador:
    """Clase para comparar el rendimiento de los algoritmos"""
    
    @staticmethod
    def comparar_en_laberinto(laberinto, inicio, objetivo):
        """Compara todos los algoritmos en un laberinto"""
        print("\n" + "="*70)
        print("   COMPARACIÓN DE ALGORITMOS EN LABERINTO")
        print("="*70)
        
        algoritmos = [
            ("BFS", BFS.buscar_laberinto),
            ("DFS", DFS.buscar_laberinto),
            ("UCS", UCS.buscar_laberinto),
            ("A*", AStar.buscar_laberinto)
        ]
        
        resultados = []
        
        for nombre, algoritmo in algoritmos:
            print(f"\n▶ Ejecutando {nombre}...")
            start = time.time()
            resultado = algoritmo(laberinto, inicio, objetivo)
            end = time.time()
            
            if resultado:
                tiempo = end - start
                resultado['tiempo'] = tiempo
                resultados.append((nombre, resultado))
                print(f"  Encontrado en {tiempo:.4f}s | {len(resultado['camino'])} pasos | {len(resultado['visitados'])} visitados")
            else:
                print(f"  No se encontró solución")
        
        # Mostrar tabla comparativa
        print("\n" + "="*70)
        print("   TABLA COMPARATIVA")
        print("="*70)
        print(f"{'Algoritmo':<10} {'Pasos':<8} {'Visitados':<10} {'Tiempo (s)':<12} {'Costo':<8}")
        print("-"*70)
        for nombre, resultado in resultados:
            if resultado:
                print(f"{nombre:<10} {len(resultado['camino']):<8} {len(resultado['visitados']):<10} {resultado['tiempo']:.4f}     {resultado.get('costo', 0):<8}")
        
        # Visualizar el mejor resultado
        if resultados:
            mejor = min(resultados, key=lambda x: x[1]['costo'])
            print(f"\n✅ Mejor algoritmo: {mejor[0]} con costo {mejor[1]['costo']}")
            Visualizador.mostrar_laberinto_grafico(laberinto, mejor[1])
    
    @staticmethod
    def comparar_en_grafo(grafo, inicio, objetivo):
        """Compara todos los algoritmos en un grafo"""
        print("\n" + "="*70)
        print("   COMPARACIÓN DE ALGORITMOS EN GRAFO")
        print("="*70)
        
        algoritmos = [
            ("BFS", BFS.buscar),
            ("DFS", DFS.buscar),
            ("UCS", UCS.buscar),
            ("A*", AStar.buscar)
        ]
        
        resultados = []
        
        for nombre, algoritmo in algoritmos:
            print(f"\n▶ Ejecutando {nombre}...")
            start = time.time()
            resultado = algoritmo(grafo, inicio, objetivo)
            end = time.time()
            
            if resultado:
                tiempo = end - start
                resultado['tiempo'] = tiempo
                resultados.append((nombre, resultado))
                print(f"  Encontrado en {tiempo:.4f}s | {len(resultado['camino'])} pasos | {len(resultado['visitados'])} visitados")
            else:
                print(f"  No se encontró solución")
        
        # Mostrar tabla comparativa
        print("\n" + "="*70)
        print("   TABLA COMPARATIVA")
        print("="*70)
        print(f"{'Algoritmo':<10} {'Pasos':<8} {'Visitados':<10} {'Tiempo (s)':<12} {'Costo':<8}")
        print("-"*70)
        for nombre, resultado in resultados:
            if resultado:
                print(f"{nombre:<10} {len(resultado['camino']):<8} {len(resultado['visitados']):<10} {resultado['tiempo']:.4f}     {resultado.get('costo', 0):<8}")
        
        # Visualizar el mejor resultado
        if resultados:
            mejor = min(resultados, key=lambda x: x[1]['costo'])
            print(f"\n✅ Mejor algoritmo: {mejor[0]} con costo {mejor[1]['costo']}")
            Visualizador.mostrar_grafo(grafo, mejor[1])

# MENÚ PRINCIPAL

def menu_principal():
    """Menú principal del programa"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*70)
    print("   IMPLEMENTACIÓN Y VISUALIZACIÓN DE ALGORITMOS DE BÚSQUEDA")
    print("="*70)
    print("\n" + "="*70)
    print("   ALGORITMOS DISPONIBLES: BFS, DFS, UCS, A*")
    print("="*70)
    print("\n1. Búsqueda en Grafo/Árbol")
    print("2. Búsqueda en Laberinto")
    print("3. Comparación automática de algoritmos")
    print("4. Salir")
    
    opcion = input("\nSeleccione una opción: ")
    return opcion

def menu_algoritmo():
    """Menú para seleccionar algoritmo"""
    print("\n" + "-"*50)
    print("ALGORITMOS DE BÚSQUEDA")
    print("-"*50)
    print("1. BFS (Breadth-First Search)")
    print("2. DFS (Depth-First Search)")
    print("3. UCS (Uniform Cost Search)")
    print("4. A* (A-Star Search)")
    
    opcion = input("\nSeleccione algoritmo: ")
    return opcion

def menu_laberinto():
    """Menú para seleccionar laberinto"""
    print("\n" + "-"*50)
    print("SELECCIÓN DE LABERINTO")
    print("-"*50)
    print("1. Laberinto pequeño (7x8)")
    print("2. Laberinto mediano (10x10)")
    print("3. Generar laberinto aleatorio")
    print("4. Cargar desde archivo")
    
    opcion = input("\nSeleccione: ")
    return opcion

def menu_grafo():
    """Menú para seleccionar grafo"""
    print("\n" + "-"*50)
    print("SELECCIÓN DE GRAFO")
    print("-"*50)
    print("1. Grafo de Rumania (clásico)")
    print("2. Grafo simple para pruebas")
    print("3. Cargar desde archivo CSV")
    
    opcion = input("\nSeleccione: ")
    return opcion

def ejecutar_grafo():
    """Ejecuta búsqueda en grafo"""
    print("\n" + "="*60)
    print("   BÚSQUEDA EN GRAFO")
    print("="*60)
    
    grafo = Grafo()
    opcion = menu_grafo()
    
    if opcion == "1":
        grafo.crear_grafo_ejemplo()
    elif opcion == "2":
        grafo.crear_grafo_simple()
    elif opcion == "3":
        archivo = input("Nombre del archivo CSV: ")
        if os.path.exists(archivo):
            grafo.cargar_desde_csv(archivo)
        else:
            print("Archivo no encontrado. Usando grafo de ejemplo.")
            grafo.crear_grafo_ejemplo()
    else:
        print("Opción no válida. Usando grafo de ejemplo.")
        grafo.crear_grafo_ejemplo()
    
    grafo.mostrar()
    
    # Seleccionar nodos
    nodos = grafo.obtener_nodos()
    print(f"\nNodos disponibles: {', '.join(nodos)}")
    inicio = input("Nodo inicial (Enter para usar primero): ").strip()
    objetivo = input("Nodo objetivo (Enter para usar último): ").strip()
    
    if not inicio or inicio not in nodos:
        inicio = nodos[0] if nodos else "A"
        print(f"Usando nodo inicial: {inicio}")
    
    if not objetivo or objetivo not in nodos:
        objetivo = nodos[-1] if nodos else "G"
        print(f"Usando nodo objetivo: {objetivo}")
    
    opcion_algo = menu_algoritmo()
    
    if opcion_algo == "1":
        resultado = BFS.buscar(grafo, inicio, objetivo)
    elif opcion_algo == "2":
        resultado = DFS.buscar(grafo, inicio, objetivo)
    elif opcion_algo == "3":
        resultado = UCS.buscar(grafo, inicio, objetivo)
    elif opcion_algo == "4":
        resultado = AStar.buscar(grafo, inicio, objetivo)
    else:
        print("Opción no válida")
        return
    
    if resultado:
        Visualizador.mostrar_grafo(grafo, resultado)
    else:
        print("No se encontró solución")

def ejecutar_laberinto():
    """Ejecuta búsqueda en laberinto"""
    print("\n" + "="*60)
    print("   BÚSQUEDA EN LABERINTO")
    print("="*60)
    
    opcion = menu_laberinto()
    laberinto = None
    
    if opcion == "1":
        laberinto = Laberinto.crear_laberinto_ejemplo()
    elif opcion == "2":
        laberinto = Laberinto.crear_laberinto_ejemplo2()
    elif opcion == "3":
        try:
            filas = int(input("Número de filas: "))
            columnas = int(input("Número de columnas: "))
            densidad = float(input("Densidad de obstáculos (0-1, ej: 0.3): "))
            laberinto = Laberinto.generar_aleatorio(filas, columnas, densidad)
        except:
            print("Valores inválidos. Usando laberinto de ejemplo.")
            laberinto = Laberinto.crear_laberinto_ejemplo()
    elif opcion == "4":
        archivo = input("Nombre del archivo: ")
        if os.path.exists(archivo):
            laberinto = Laberinto.cargar_desde_archivo(archivo)
        else:
            print("Archivo no encontrado. Usando laberinto de ejemplo.")
            laberinto = Laberinto.crear_laberinto_ejemplo()
    else:
        laberinto = Laberinto.crear_laberinto_ejemplo()
    
    if laberinto is None:
        laberinto = Laberinto.crear_laberinto_ejemplo()
    
    laberinto.mostrar()
    
    # Seleccionar posiciones
    print(f"\nDimensiones: {laberinto.filas}x{laberinto.columnas}")
    print("Formato: fila,columna (ej: 0,0)")
    inicio_str = input("Posición inicial (Enter para usar 0,0): ").strip()
    objetivo_str = input("Posición objetivo (Enter para usar final): ").strip()
    
    try:
        if inicio_str:
            inicio = tuple(map(int, inicio_str.split(',')))
        else:
            inicio = (0, 0)
        
        if objetivo_str:
            objetivo = tuple(map(int, objetivo_str.split(',')))
        else:
            objetivo = (laberinto.filas-1, laberinto.columnas-1)
        
        if not laberinto.es_valida(inicio[0], inicio[1]):
            print("Posición inicial no válida. Usando (0,0)")
            inicio = (0, 0)
        
        if not laberinto.es_valida(objetivo[0], objetivo[1]):
            print("Posición objetivo no válida. Usando final")
            objetivo = (laberinto.filas-1, laberinto.columnas-1)
            
    except:
        print("Formato incorrecto. Usando posiciones por defecto.")
        inicio = (0, 0)
        objetivo = (laberinto.filas-1, laberinto.columnas-1)
    
    opcion_algo = menu_algoritmo()
    
    if opcion_algo == "1":
        resultado = BFS.buscar_laberinto(laberinto, inicio, objetivo)
    elif opcion_algo == "2":
        resultado = DFS.buscar_laberinto(laberinto, inicio, objetivo)
    elif opcion_algo == "3":
        resultado = UCS.buscar_laberinto(laberinto, inicio, objetivo)
    elif opcion_algo == "4":
        resultado = AStar.buscar_laberinto(laberinto, inicio, objetivo)
    else:
        print("Opción no válida")
        return
    
    if resultado:
        Visualizador.mostrar_laberinto_grafico(laberinto, resultado)
    else:
        print("No se encontró solución")

def ejecutar_comparacion():
    """Ejecuta comparación automática de algoritmos"""
    print("\n" + "="*60)
    print("   COMPARACIÓN AUTOMÁTICA DE ALGORITMOS")
    print("="*60)
    
    print("\nComparar en:")
    print("1. Laberinto")
    print("2. Grafo")
    
    opcion = input("\nSeleccione: ")
    
    if opcion == "1":
        laberinto = Laberinto.crear_laberinto_ejemplo2()
        inicio = (0, 0)
        objetivo = (laberinto.filas-1, laberinto.columnas-1)
        Comparador.comparar_en_laberinto(laberinto, inicio, objetivo)
    elif opcion == "2":
        grafo = Grafo()
        grafo.crear_grafo_ejemplo()
        nodos = grafo.obtener_nodos()
        inicio = nodos[0] if nodos else "A"
        objetivo = nodos[-1] if nodos else "G"
        Comparador.comparar_en_grafo(grafo, inicio, objetivo)
    else:
        print("Opción no válida")

def main():
    """Función principal"""
    while True:
        opcion = menu_principal()
        
        if opcion == "1":
            ejecutar_grafo()
        elif opcion == "2":
            ejecutar_laberinto()
        elif opcion == "3":
            ejecutar_comparacion()
        elif opcion == "4":
            print("\n👋 ¡Hasta luego!")
            break
        else:
            print("Opción no válida")
        
        input("\nPresione Enter para continuar...")

# PUNTO DE ENTRADA

if __name__ == "__main__":
    # Verificar dependencias
    if not MATPLOTLIB_DISPONIBLE:
        print("\nPara visualización gráfica instale:")
        print("   pip install matplotlib numpy")
        print("   (La visualización textual seguirá funcionando)\n")
    
    if not NETWORKX_DISPONIBLE:
        print("Para visualización de grafos instale:")
        print("   pip install networkx")
        print("   (La visualización textual seguirá funcionando)\n")
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n¡Programa terminado por el usuario!")
        sys.exit(0)
        