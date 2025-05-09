from DataStructures.List import array_list as al
from DataStructures.Priority_queue import index_pq_entry as ie

def new_heap(is_min_pq=True):
    if is_min_pq == True:
        cmp_function = default_compare_lower_value()
    else:
        cmp_function = default_compare_higher_value()
    lista = al.new_list()
    al.add_last(lista, None)
    my_heap = {"elelemts": lista,
               "size": 0,
               "cmp_function": cmp_function}
    return my_heap

def default_compare_higher_value(father_node, child_node):
    if father_node >= child_node:
        return True
    else:
        return False

def default_compare_lower_value(father_node, child_node):
    if father_node <= child_node:
        return True
    else:
        return False
    
def priority(my_heap, parent, child):
    cmp_function = my_heap["cmp_function"]
    if cmp_function(parent, child):
        return True
    else:
        return False

def insert(my_heap, element, key):
    new_entry = ie.new_pq_entry(key, element)
    al.add_last(my_heap["elements"], new_entry)
    my_heap["size"] += 1
    swim(my_heap, my_heap["size"]-1)

def swim(my_heap, pos):
    if pos == 0:
        return my_heap
    else:
        father_pos = pos // 2
        father = al.get_element(my_heap["elements"], father_pos)
        child = al.get_element(my_heap["elements"], pos)
        if priority(my_heap, ie.get_index(father), ie.get_index(child)):
            al.exchange(my_heap["elements"], father_pos, pos)
            return swim(my_heap, father_pos)
        else:
            return my_heap

def size(my_heap):
    return my_heap["size"]

def is_empty(my_heap):
    if size(my_heap) == 0:
        return True
    else: 
        return False
    
def get_first_priority(my_heap):
    if is_empty(my_heap):
        return None
    else:
        elemento = al.get_element(my_heap["elements"], 1)
        valor = ie.get_index(elemento)
        return valor

def remove (my_heap):
    if is_empty(my_heap):
        return None
    else:
        first = al.get_element(my_heap["elements"], 1)
        al.exchange(my_heap["elements"], 1, my_heap["size"])
        al.remove_last(my_heap["elements"])
        my_heap["size"] -= 1
        sink(my_heap, 1)
        return ie.get_index(first)


def sink(my_heap, pos):
    if pos >= my_heap["size"]:
        return my_heap
    else:
        left_child_pos = pos * 2
        right_child_pos = pos * 2 + 1
        father = al.get_element(my_heap["elements"], pos)
        left_child = al.get_element(my_heap["elements"], left_child_pos)
        right_child = al.get_element(my_heap["elements"], right_child_pos)
        if priority(my_heap, ie.get_index(father), ie.get_index(left_child)) and priority(my_heap, ie.get_index(father), ie.get_index(right_child)):
            return my_heap
        elif priority(my_heap, ie.get_index(left_child), ie.get_index(right_child)):
            al.exchange(my_heap["elements"], pos, left_child_pos)
            return sink(my_heap, left_child_pos)
        else:
            al.exchange(my_heap["elements"], pos, right_child_pos)
            return sink(my_heap, right_child_pos)