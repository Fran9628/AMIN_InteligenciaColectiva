from numpy.random import RandomState


def generar_solucion(n, prng):
    """ Retorna una representacion vectorial pseudoaleatorea de un problema.

    Parameters
    ----------
    n : int
        Largo del vector a obtener.
    prng : RandomState
        Generador de numeros pseudoaleatoreos.
    Returns
    -------
    list
        Un vector de cero a n desordenado.
    """

    solucion = list(range(n))
    prng.shuffle(solucion)
    return solucion


def calcular_costo(dm, solucion):
    """ Retorna el costo total de recorrer un grafo.

    Parameters
    ----------
    dm : DataFrame
        Matriz con los costos entre dos nodos del grafo.
    solucion : list
        Vector con el orden a recorrer el grafo.
    Returns
    -------
    float
        Costo de recorrer la solucion y volver al nodo de origen.
    """

    costo = 0.0
    for i in range(0, len(solucion) - 1):
        costo += dm[solucion[i]][solucion[i + 1]]
    costo += dm[solucion[-1]][solucion[0]]
    return costo


def seleccion_ruleta(poblacion, probabilidades, n, prng):
    """ Retorna una cantidad n de individuos desde una poblacion en forma aleatorea.

    Parameters
    ----------
    poblacion : list
        Elementos de la poblacion.
    probabilidades : list
        Probabilidades respectivas a los elementos de poblacion.
    n : int
        Numero de individuos a obtener desde la ruleta.
    prng : RandomState
        Generador de numeros pseudoaleatoreos.
    Returns
    -------
    list
        Listado de individuos.
    """

    seleccionados = []
    for _ in range(n):
        r = prng.rand()
        for (i, individuo) in enumerate(poblacion):
            if r <= probabilidades[i]:
                seleccionados.append(individuo)
                break
    return seleccionados


def leer_archivo_tsp(path):
    """ Funcion que retorna las coordenadas desde un archivo .tsp

    Parameters
    ----------
    path : String
        Direccion relativa del archivo TSP
    Returns
    -------
    list
        Lista con las coordenadas
    """

    data = []
    with open(path) as f:
        for line in f.readlines()[6:-1]:
            _, *b = line.split()
            data.append((float(i) for i in b))
    return data
