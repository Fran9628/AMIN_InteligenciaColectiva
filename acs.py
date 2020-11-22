import sys
import numpy as np
import pandas as pd
from funciones import *
from operator import attrgetter
from numpy.random import RandomState
from scipy.spatial import distance_matrix


class ACS():

    def __init__(self, n, alpha, beta, rho, max_it, dm, eta, prng):
        self.n = n
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.max_it = max_it
        self.dm = dm
        self.eta = eta
        self.prng = prng
        # Solucion inicial y feromonas.
        self.ruta_global = generar_solucion(len(dm), prng)
        self.costo_global = calcular_costo(dm, self.ruta_global)
        self.tau_cero = np.reciprocal(self.costo_global)
        #self.tau_cero = 0.01
        self.tau = np.full(dm.shape, self.tau_cero)
        # Hormigas.
        self.hormigas = []
        self.mejor_hormiga = None

    def _init_hormigas(self):
        """ Asigna randomicamente una y solo una hormiga en cualquiera de los vertices de la solucion. """
        self.hormigas = []
        muestra = self.prng.choice(self.ruta_global, self.n, replace=False)
        for nodo_inicial in muestra:
            nk = list(self.ruta_global)
            nk.pop(nk.index(nodo_inicial))
            nueva_hormiga = Hormiga(self, nk, nodo_inicial)
            self.hormigas.append(nueva_hormiga)

    def _actualizacion_local(self, hormiga):
        """ Agrega feromonas solamente en el tramo seleccionado (Ecuacion 4). """
        a = (1 - self.alpha) * self.tau[hormiga.actual][hormiga.proximo]
        b = self.alpha * self.tau_cero
        self.tau[hormiga.actual][hormiga.proximo] = a + b

    def _actualizar_solucion(self):
        """ Actualiza si hay una nueva mejor solucion global. """
        if self.mejor_hormiga.costo < self.costo_global:
            self.ruta_global = self.mejor_hormiga.ruta
            self.costo_global = self.mejor_hormiga.costo
            print("Nuevo costo global:", self.mejor_hormiga.costo)

    def _actualizacion_global(self):
        """ Evapora todas las feromonas y agrega a las de la mejor ruta. """
        # Evaporacion a todas las feromonas.
        self.tau = np.multiply(self.tau, (1 - self.alpha))
        # Agrega feromonas en la ruta seleccionada.
        ruta = self.mejor_hormiga.ruta
        delta = np.reciprocal(self.mejor_hormiga.costo)
        for i in range(1, len(self.ruta_global) - 1):
            self.tau[ruta[i - 1]][ruta[i]] += self.alpha * delta

    def run(self):
        """ Se ejecutara hasta que se cumple la condicion de termino. """
        for it in range(self.max_it):
            # Asignacion de hormigas.
            self._init_hormigas()
            # Para cada vertice del grafo.
            for _ in range(len(self.dm) - 1):
                # Seleccionar el proximo segmento en el grafo.
                for hormiga in self.hormigas:
                    hormiga.run()
                # Actualizacion local.
                for hormiga in self.hormigas:
                    self._actualizacion_local(hormiga)
                    hormiga._avanzar()
            # Sumar el retorno a el nodo inicial y obtener la mejor hormiga.
            for hormiga in self.hormigas:
                hormiga.costo += self.dm[hormiga.nodo_inicial][hormiga.actual]
            self.mejor_hormiga = min(self.hormigas, key=attrgetter('costo'))
            # Actualizar la solucion global de ser necesario.
            self._actualizar_solucion()
            # Actualizacion global.
            self._actualizacion_global()
            print("Iteracion:", it)

    def __str__(self):
        """ Retorna el resultado final. """
        return f'Distancia: {self.costo_global}\nSolucion: {self.ruta_global}'


class Hormiga():

    def __init__(self, acs, nk, nodo_inicial):
        self.acs = acs
        self.nk = nk
        self.nodo_inicial = nodo_inicial
        # Ruta de hormiga
        self.actual = nodo_inicial
        self.proximo = 0
        self.ruta = [nodo_inicial]
        self.costo = 0

    def _explotar(self):
        """ (Primera ecuacion). """
        maximo = 0
        for vecino in self.nk:
            tau = self.acs.tau[self.actual][vecino]
            nb = self.acs.eta[self.actual][vecino] ** self.acs.beta
            if maximo < tau * nb:
                maximo = tau * nb
                self.proximo = vecino

    def _explorar(self):
        """ (Segunda ecuacion). """
        valores = []
        for vecino in self.nk:
            tau = self.acs.tau[self.actual][vecino]
            nb = self.acs.eta[self.actual][vecino] ** self.acs.beta
            valores.append(tau * nb)
        suma_valores = sum(valores)
        relativo = [x / suma_valores for x in valores]
        probabilidades = [sum(relativo[:i + 1]) for i in range(len(relativo))]
        seleccion = seleccion_ruleta(self.nk, probabilidades, 1, self.acs.prng)
        self.proximo = seleccion[0]

    def _avanzar(self):
        """ Permite a la hormiga avanzar en el grafo. """
        self.costo += self.acs.dm[self.actual][self.proximo]
        self.ruta.append(self.proximo)
        self.nk.pop(self.nk.index(self.proximo))
        self.actual = self.proximo
        self.proximo = 0

    def run(self):
        """ Regla de transicion, decide en que forma se eligira el proximo nodo. """
        r = self.acs.prng.rand()
        if r <= self.acs.rho:
            self._explotar()
        else:
            self._explorar()


if __name__ == '__main__':
    np.seterr(divide='ignore')
    # python acs.py 24 0.1 2.5 0.9 500 berlin52.tsp 123
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
        alpha = float(sys.argv[2])
        beta = float(sys.argv[3])
        rho = float(sys.argv[4])
        max_it = int(sys.argv[5])
        tsp = leer_archivo_tsp(sys.argv[6])
        # Si no contiene semilla se realizara de forma aleatorea.
        if len(sys.argv) > 7:
            prng = RandomState(int(sys.argv[7]))
        else:
            prng = RandomState()
    # python acs.py
    else:
        n = 10
        alpha = 0.1
        beta = 2.5
        rho = 0.9
        max_it = 100
        tsp = leer_archivo_tsp("berlin52.tsp")
        prng = RandomState()
    # Coordenadas, Matriz de Distancia y Heuristica
    coord = pd.DataFrame(tsp, columns=['x_coord', 'y_coord'])
    dm = pd.DataFrame(distance_matrix(coord.values, coord.values))
    eta = np.where(dm != 0, np.reciprocal(dm), 0)
    acs = ACS(n, alpha, beta, rho, max_it, dm, eta, prng)
    acs.run()
    print(acs)
