from DataStructures.Map import map_linear_probing as lp
from DataStructures.Graph import edge as edg
from DataStructures.Graph import vertex as ve

def new_graph(order):
    graph = {"vertices": lp.new_map(order, 0.5, 109345121),
             "num_edges": 0}
    return graph

def instert_vertex(my_graph, key_u, info_u):
    vertex = ve.new_vertex(key_u, info_u)
    lp.put(my_graph["vertices"], key_u, vertex)
    return my_graph

def update_vertex_info(my_graph, key_u, new_info_u):
    vertex = lp.get(my_graph["vertices"], key_u)
    ve.set_value(vertex, new_info_u)
    return my_graph

def remove_vertex(my_graph, key_u):
    vertex = lp.get(my_graph["elements"], key_u)
    if vertex == None:
        return None
    else:
        adjacents = ve.get_adjacents(vertex)
        for edge in adjacents["elements"]:
            lp.remove(adjacents, edge)
        lp.remove(my_graph["vertices"], key_u)
        return my_graph

def add_edge(my_graph, key_u, key_v, weight=1.0):
    vertex_u = lp.get(my_graph["vertices"], key_u)
    vertex_v = lp.get(my_graph["vertices"], key_v)
    if vertex_u == None
        raise Exception("El vertice u no existe")
    elif vertex_v == None:
        raise Exception("El vertice v no existe")
    else:
        pass
    pass