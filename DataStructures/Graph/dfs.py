from DataStructures.Stack import stack as st
from DataStructures.List import array_list as al
from DataStructures.Graph import digraph as dg
from DataStructures.Graph import vertex as ve

def dfs(my_graph, source):
    visited = st.new_stack()
    stack_vertices = st.new_stack()
    if dg.order(my_graph) == 0:
        return None
    else:
        st.push(stack_vertices, source)
        dfs_vertex(my_graph, source, visited, stack_vertices)
        return visited


def dfs_vertex(my_graph, vertex, search, stack):
    if st.is_empty(stack):
        return None
    else:
        vertex = st.pop(stack)
        st.push(search, vertex)
        adjacents = ve.get_adjacents(vertex)
        for i in adjacents["table"]["elements"]:
            if i != None and i["key"] not in search["elements"]:
                st.push(stack, i["key"])
        return dfs_vertex(my_graph, vertex, search, stack)