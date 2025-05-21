from DataStructures.Queue import queue as q
from DataStructures.Stack import stack as st
from DataStructures.Map import map_linear_probing as lp
from DataStructures.Graph import digraph as dg
from DataStructures.Graph import vertex as ve

def bfs(my_graph, source):
    visited = st.new_stack()
    queue_vertices = q.new_queue()
    if dg.order(my_graph) == 0:
        return None
    else:
        q.enqueue(queue_vertices, source)
        bfs_vertex(my_graph, source, visited, queue_vertices)
        return visited


def bfs_vertex(my_graph, vertex, search, queue):
    if q.is_empty(queue):
        return None
    else:
        vertex = q.dequeue(queue)
        st.push(search, vertex)
        adjacents = ve.get_adjacents(lp.get(my_graph["vertices"], vertex))
        if adjacents == None:
            return bfs_vertex(my_graph, vertex, search, queue)
        else:
            for i in adjacents["table"]["elements"]:
                if i != None and i["key"] not in search["elements"]:
                    q.enqueue(queue, i["key"])
        return bfs_vertex(my_graph, vertex, search, queue)
    
def has_path_to(key_v, visited_map):
    if key_v in visited_map["elements"]:
        return True
    else:
        return False

def path_to(key_v, visited_map):
    if key_v in visited_map["elements"]:
        return visited_map["elements"][key_v]
    else:
        return None