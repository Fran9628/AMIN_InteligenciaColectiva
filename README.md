# Ant Colony System.
Implementación del sistema de colonia de hormigas de Marco Dorigo.

## Requerimientos:
- Python 3.6.5+
- Scipy, pandas, numpy: `python -m pip install --user numpy scipy matplotlib ipython jupyter pandas sympy nose`

## Ejecucion:
Para los comandos definidos en clase: `python acs.py`

Para valores personalizados: `python acs.py numero_hormigas alfa beta q0 iteraciones ruta_archivo`

Para valores personalizados y semilla: `python acs.py numero_hormigas alfa beta q0 iteraciones ruta_archivo semilla`

## Ejemplo con parametros:
`python acs.py 24 0.1 2.5 0.9 500 berlin52.tsp 123`

Este ejemplo fue el mejor caso que pude obtener con los siguientes datos:
```
Distancia: 7677.660844311166
Error: 0.01767%
Solucion: [45, 43, 33, 34, 35, 38, 39, 37, 36, 47, 23, 4, 14, 5, 3, 24, 11, 27, 26, 25, 46, 12, 13, 51, 10, 50, 32, 42, 9, 8, 7, 40, 18, 44, 31, 48, 0, 21, 30, 17, 2, 16, 20, 41, 6, 1, 29, 28, 49, 19, 22, 15]
```