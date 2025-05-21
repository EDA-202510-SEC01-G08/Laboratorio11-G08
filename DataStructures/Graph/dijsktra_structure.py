from DataStructures.Map import map_linear_probing as mp
from DataStructures.Priority_queue import priority_queue as pq


def new_dijsktra_structure(source, g_order):
    """

    Crea una estructura de busqueda usada en el algoritmo **dijsktra**.

    Se crea una estructura de busqueda con los siguientes atributos:

    - **source**: Vertice de origen. Se inicializa en ``source``
    - **visited**: Mapa con los vertices visitados. Se inicializa en ``None``
    - **pq**: Cola indexada con los vertices visitados. Se inicializa en ``None``

    :returns: Estructura de busqueda
    :rtype: dijsktra_search
    """
    structure = {
        "source": source,
        "visited": mp.new_map(
            g_order, 0.5),
        "pq": pq.new_heap(),
        "predecessors": {}
        }
    return structure

def dijkstra(my_graph, source):
    
    if my_graph["order"] == 0:
        raise Exception("El grafo está vacío, no se puede ejecutar Dijkstra.")
    else:
        aux_structure = new_dijsktra_structure(source, my_graph["order"])
        pq.insert(aux_structure["pq"], source, 0)
        mp.put(aux_structure["visited"], source, 0)
        while not pq.is_empty(aux_structure["pq"]):
            vertex = pq.remove(aux_structure["pq"])
            adjacents = my_graph["vertices"][vertex]["adjacents"]
            for i in adjacents:
                if i is not None and i["key"] not in aux_structure["visited"]["elements"]:
                    new_distance = i["weight"] + dist_to(vertex, aux_structure)
                    if new_distance < dist_to(i["key"], aux_structure):
                        pq.insert(aux_structure["pq"], i["key"], new_distance)
                        mp.put(aux_structure["visited"], i["key"], new_distance)
                        aux_structure["predecessor"][i["key"]] = vertex  
        return aux_structure
    
def dist_to(key_v, aux_structure):
    
    if key_v in aux_structure["visited"]["elements"]:
        return aux_structure["visited"]["elements"][key_v]
    else:
        raise Exception("No existe una distancia registrada para el vértice dado.")
    
def has_path_to(key_v, aux_structure):

    if key_v in aux_structure["visited"]["elements"]:
        return True
    else:
        raise Exception("No existe un camino desde el vértice fuente hasta el vértice dado.")

def path_to(key_v, aux_structure):
    
    if not has_path_to(key_v, aux_structure):
        raise Exception("No existe un camino desde el vértice fuente hasta el vértice dado.")
    
    path = []
    current = key_v
    while current != aux_structure["source"]:
        path.append(current)
        current = aux_structure["predecessor"][current]
    path.append(aux_structure["source"])
    path.reverse()  
    return path