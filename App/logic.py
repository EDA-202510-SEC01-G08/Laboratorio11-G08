"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """

# ___________________________________________________
#  Importaciones
# ___________________________________________________

from DataStructures.Graph import digraph as gr
from DataStructures.Graph import dijsktra_structure as ds
from DataStructures.List import single_linked_list as lt
from DataStructures.Map import map_linear_probing as m
from DataStructures.Graph import digraph as G
from DataStructures.Graph import dijsktra_structure as dj

import csv
import time
import os

data_dir = os.path.dirname(os.path.realpath('__file__')) + '/Data/'


"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________


def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    analyzer = new_analyzer()
    return analyzer


def new_analyzer():
    """ Inicializa el analizador

   stops: Tabla de hash para guardar los vertices del grafo
   connections: Grafo para representar las rutas entre estaciones
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    try:
        analyzer = {
            'stops': None,
            'connections': None,
            'components': None,
            'paths': None
        }

        analyzer['stops'] = m.new_map(
            num_elements=14000, load_factor=0.7, prime=109345121)

        analyzer['connections'] = G.new_graph(size=14000)
        return analyzer
    except Exception as exp:
        return exp

# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________


def load_services(analyzer, servicesfile):
    """
    Carga los datos de los archivos CSV en el modelo.
    Se crea un arco entre cada par de estaciones que
    pertenecen al mismo servicio y van en el mismo sentido.

    addRouteConnection crea conexiones entre diferentes rutas
    servidas en una misma estación.
    """
    servicesfile = data_dir + servicesfile
    input_file = csv.DictReader(open(servicesfile, encoding="utf-8"),
                                delimiter=",")
    lastservice = None
    for service in input_file:
        if lastservice is not None:
            sameservice = lastservice['ServiceNo'] == service['ServiceNo']
            samedirection = lastservice['Direction'] == service['Direction']
            samebusStop = lastservice['BusStopCode'] == service['BusStopCode']
            if sameservice and samedirection and not samebusStop:
                add_stop_connection(analyzer, lastservice, service)
        lastservice = service

    return analyzer


def set_station(analyzer, station):
    """
    Establece la estación base para la consulta de caminos
    """
    try:
        station = str(station)
        vertex = G.get_vertex(analyzer['connections'], station)
        if vertex is not None:
            # TODO: Llame a la ejecucion de Dijkstra desde la estacion
            # base para calcular los caminos de costo minimo
            analyzer['paths'] = dj.dijkstra(analyzer['connections'], station)
            return True
        else:
            return False
    except Exception as exp:
        return exp
# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________


def total_stops(analyzer):
    """
    Total de paradas de autobus
    """
    return G.order(analyzer['connections'])


def total_connections(analyzer):
    """
    Total de enlaces entre las paradas
    """
    return G.size(analyzer['connections'])


# Funciones para la medición de tiempos

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(end, start):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed


# Funciones para agregar informacion al grafo

def add_stop_connection(analyzer, lastservice, service):
    """
    Adiciona las estaciones al grafo como vertices y arcos entre las
    estaciones adyacentes.

    Los vertices tienen por nombre el identificador de la estacion
    seguido de la ruta que sirve.  Por ejemplo:

    75009-10

    Si la estacion sirve otra ruta, se tiene: 75009-101
    """
    try:
        origin = format_vertex(lastservice)
        destination = format_vertex(service)
        clean_service_distance(lastservice, service)
        distance = float(service['Distance']) - float(lastservice['Distance'])
        distance = abs(distance)
        add_stop(analyzer, origin)
        add_stop(analyzer, destination)
        add_connection(analyzer, origin, destination, distance)
        add_route_stop(analyzer, service)
        add_route_stop(analyzer, lastservice)
        return analyzer
    except Exception as exp:
        return exp


def add_stop(analyzer, stopid):
    """
    Adiciona una estación como un vertice del grafo
    """

    G.insert_vertex(analyzer['connections'], stopid, stopid)
    return analyzer


def add_route_stop(analyzer, service):
    """
    Agrega a una estacion, una ruta que es servida en ese paradero
    """
    lstroutes = m.get(analyzer['stops'], service['BusStopCode'])
    if lstroutes is None:
        lstroutes = lt.new_list()
        lt.add_last(lstroutes, service['ServiceNo'])
        m.put(analyzer['stops'], service['BusStopCode'], lstroutes)
    else:
        lstroutes = lstroutes['value']
        info = service['ServiceNo']
        if not lt.is_present(lstroutes, info):
            lt.add_last(lstroutes, info)
    return analyzer


def add_connection(analyzer, origin, destination, distance):
    """
    Adiciona un arco entre dos estaciones
    """

    G.add_edge(analyzer['connections'], origin, destination, distance)


# ==============================
# Funciones Helper
# ==============================

def clean_service_distance(lastservice, service):
    """
    En caso de que el archivo tenga un espacio en la
    distancia, se reemplaza con cero.
    """
    if service['Distance'] == '':
        service['Distance'] = 0
    if lastservice['Distance'] == '':
        lastservice['Distance'] = 0


def format_vertex(service):
    """
    Se formatea el nombrer del vertice con el id de la estación
    seguido de la ruta.
    """
    name = service['BusStopCode'] + '-'
    name = name + service['ServiceNo']
    return name

def main_dijkstra():
    """
    Función para ejecutar el algoritmo de Dijkstra
    """

    grafo = gr.new_graph(5)
    gr.insert_vertex(grafo, 0, "A")
    gr.insert_vertex(grafo, 1, "B")
    gr.insert_vertex(grafo, 2, "C")
    gr.insert_vertex(grafo, 3, "D")
    gr.insert_vertex(grafo, 4, "E")
    gr.insert_vertex(grafo, 5, "F")
    gr.insert_vertex(grafo, 6, "G")
    gr.insert_vertex(grafo, 7, "H")

    gr.add_edge(grafo, 0, 1, 5)
    gr.add_edge(grafo, 0, 7, 8)
    gr.add_edge(grafo, 0, 4, 9)
    gr.add_edge(grafo, 1, 3, 15)
    gr.add_edge(grafo, 1, 2, 12)
    gr.add_edge(grafo, 1, 7, 4)
    gr.add_edge(grafo, 3, 6, 9)
    gr.add_edge(grafo, 2, 6, 11)
    gr.add_edge(grafo, 2, 3, 3)
    gr.add_edge(grafo, 7, 2, 7)
    gr.add_edge(grafo, 7, 5, 6)
    gr.add_edge(grafo, 4, 7, 5)
    gr.add_edge(grafo, 4, 5, 4)
    gr.add_edge(grafo, 4, 6, 20)
    gr.add_edge(grafo, 5, 2, 1)
    gr.add_edge(grafo, 5, 6, 13)
  

    dijk = ds.dijkstra(grafo, 0)
    print("predecesores", dijk['predecessors'])
    print(ds.path_to(6, dijk))

    print("IMPORTANTE FINAL Para ver el desarrollo ve a la funcion final de la logica")

    print("\n Para ver de donde sale el grafo, en la ultima presentacion de mod4 al final hay un grafo, este es el mismo")
    print("y como puedes ver, el camino desde 6 es el mismo y los predecesores coinciden")
