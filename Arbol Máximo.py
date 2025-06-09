import networkx as nx           # Importa la librería NetworkX para trabajar con grafos
import matplotlib.pyplot as plt  # Importa Matplotlib para graficar

# Clase para conjuntos disjuntos (Union-Find)
class UnionFind:
    def __init__(self, elementos):
        self.padre = {e: e for e in elementos}  # Inicializa cada elemento como su propio padre

    def encontrar(self, elemento):
        if self.padre[elemento] != elemento:    # Si el elemento no es su propio padre
            self.padre[elemento] = self.encontrar(self.padre[elemento])  # Compresión de caminos
        return self.padre[elemento]             # Devuelve el representante del conjunto

    def unir(self, a, b):
        raiz_a = self.encontrar(a)              # Encuentra la raíz de a
        raiz_b = self.encontrar(b)              # Encuentra la raíz de b
        if raiz_a != raiz_b:                    # Si son de conjuntos diferentes
            self.padre[raiz_b] = raiz_a         # Une los conjuntos
            return True                         # Indica que se unieron
        return False                            # Indica que ya estaban unidos

# Algoritmo de Kruskal (versión Máximo Costo)
def kruskal_maximo(grafo):
    aristas = []                               # Lista para almacenar todas las aristas
    for nodo in grafo:
        for vecino, peso in grafo[nodo]:       # Recorre los vecinos y pesos de cada nodo
            if (vecino, nodo, peso) not in aristas:  # Evita duplicar aristas no dirigidas
                aristas.append((nodo, vecino, peso)) # Agrega la arista

    aristas.sort(key=lambda x: x[2], reverse=True)  # Ordena aristas por peso descendente
    conjuntos = UnionFind(grafo.keys())             # Inicializa Union-Find con los nodos
    maxst = []                                      # Lista para el árbol de máximo coste

    print("\nPaso a paso del Árbol de Expansión de Máximo Costo (Kruskal Inverso):\n")

    for u, v, peso in aristas:                      # Recorre las aristas ordenadas
        if conjuntos.unir(u, v):                    # Si unir no forma ciclo
            maxst.append((u, v, peso))              # Agrega la arista al árbol
            print(f"Agregando arista ({u}, {v}) con peso {peso}")
        else:
            print(f"Descartando arista ({u}, {v}) con peso {peso} - forma un ciclo")

    return maxst                                    # Devuelve el árbol de máximo coste

# Visualización del Árbol de Máximo Costo
def graficar_maxst(grafo, maxst):
    G = nx.Graph()                                  # Crea un grafo vacío de NetworkX
    for nodo in grafo:
        for vecino, peso in grafo[nodo]:            # Agrega todas las aristas al grafo
            G.add_edge(nodo, vecino, weight=peso)

    pos = nx.spring_layout(G)                       # Calcula posiciones para los nodos
    edge_labels = nx.get_edge_attributes(G, 'weight') # Obtiene etiquetas de peso

    nx.draw(G, pos, with_labels=True, node_color='lightyellow', node_size=800) # Dibuja nodos y aristas
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)              # Dibuja etiquetas de aristas

    maxst_edges = [(u, v) for u, v, w in maxst]      # Extrae solo los nodos de las aristas del árbol
    nx.draw_networkx_edges(G, pos, edgelist=maxst_edges, edge_color='green', width=3) # Dibuja las aristas del árbol en verde

    plt.title("Árbol de Expansión de Máximo Costo (Kruskal Inverso)")          # Título del gráfico
    plt.show()                                                                 # Muestra el gráfico

# Grafo de ejemplo
grafo = {
    'A': [('B', 3), ('D', 1)],            # Lista de adyacencia con pesos
    'B': [('A', 3), ('D', 3), ('E', 1)],
    'C': [('E', 5)],
    'D': [('A', 1), ('B', 3), ('E', 6)],
    'E': [('B', 1), ('D', 6), ('C', 5)]
}

maxst = kruskal_maximo(grafo)             # Ejecuta Kruskal para árbol de máximo coste
graficar_maxst(grafo, maxst)              # Grafica el resultado
