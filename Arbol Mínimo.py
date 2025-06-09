import networkx as nx  # Importa la librería para trabajar con grafos
import matplotlib.pyplot as plt  # Importa la librería para graficar

# Clase para representar conjuntos disjuntos (Union-Find)
class UnionFind:
    def __init__(self, elementos):
        # Inicializa cada elemento como su propio padre
        self.padre = {e: e for e in elementos}

    def encontrar(self, elemento):
        # Encuentra la raíz del conjunto al que pertenece el elemento (con compresión de caminos)
        if self.padre[elemento] != elemento:
            self.padre[elemento] = self.encontrar(self.padre[elemento])
        return self.padre[elemento]

    def unir(self, a, b):
        # Une los conjuntos de 'a' y 'b' si son diferentes
        raiz_a = self.encontrar(a)
        raiz_b = self.encontrar(b)
        if raiz_a != raiz_b:
            self.padre[raiz_b] = raiz_a
            return True  # Se unieron
        return False  # Ya estaban unidos

# Algoritmo de Kruskal para encontrar el Árbol de Expansión Mínima (MST)
def kruskal(grafo):
    aristas = []
    # Recorre cada nodo y sus vecinos para obtener todas las aristas
    for nodo in grafo:
        for vecino, peso in grafo[nodo]:
            # Evita duplicar aristas en grafos no dirigidos
            if (vecino, nodo, peso) not in aristas:
                aristas.append((nodo, vecino, peso))
    
    # Ordena las aristas por peso (de menor a mayor)
    aristas.sort(key=lambda x: x[2])
    conjuntos = UnionFind(grafo.keys())  # Inicializa Union-Find con los nodos
    mst = []  # Lista para almacenar las aristas del MST

    print("Paso a paso del Árbol de Expansión Mínima (Kruskal):\n")

    # Recorre las aristas ordenadas
    for u, v, peso in aristas:
        # Si unir u y v no forma un ciclo, agrega la arista al MST
        if conjuntos.unir(u, v):
            mst.append((u, v, peso))
            print(f"Agregando arista ({u}, {v}) con peso {peso}")
        else:
            print(f"Descartando arista ({u}, {v}) con peso {peso} - forma un ciclo")

    return mst  # Devuelve las aristas del MST

# Función para graficar el grafo y resaltar el MST
def graficar(grafo, mst):
    G = nx.Graph()  # Crea un grafo vacío de NetworkX
    # Agrega todas las aristas al grafo
    for nodo in grafo:
        for vecino, peso in grafo[nodo]:
            G.add_edge(nodo, vecino, weight=peso)

    pos = nx.spring_layout(G)  # Calcula posiciones para los nodos
    edge_labels = nx.get_edge_attributes(G, 'weight')  # Obtiene los pesos de las aristas

    # Dibuja todos los nodos y aristas en gris claro
    nx.draw(G, pos, with_labels=True, node_color='lightgray', node_size=800)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)  # Dibuja los pesos

    # Dibuja solo las aristas del MST en rojo y más gruesas
    mst_edges = [(u, v) for u, v, w in mst]
    nx.draw_networkx_edges(G, pos, edgelist=mst_edges, edge_color='red', width=3)

    plt.title("Árbol de Expansión Mínima (Kruskal)")  # Título del gráfico
    plt.show()  # Muestra el gráfico

# Grafo de ejemplo representado como diccionario de listas de adyacencia
grafo = {
    'A': [('B', 3), ('D', 1)],
    'B': [('A', 3), ('D', 3), ('E', 1)],
    'C': [('E', 5)],
    'D': [('A', 1), ('B', 3), ('E', 6)],
    'E': [('B', 1), ('D', 6), ('C', 5)]
}

mst = kruskal(grafo)  # Calcula el MST usando Kruskal
graficar(grafo, mst)  # Grafica el grafo y el MST
