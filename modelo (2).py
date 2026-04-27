import pulp

def optimizar_paneles(consumos, areas_techo):
    """
    consumos: lista con consumo mensual de cada casa [kWh]
    areas_techo: lista con área disponible en cada casa [m2]
    """

    # Datos de paneles
    paneles = {
        "A": {"costo": 190, "energia": 54, "area": 1.9},
        "B": {"costo": 205, "energia": 60.75, "area": 2.1},
        "C": {"costo": 255, "energia": 74.25, "area": 2.5},
    }

    # Modelo
    modelo = pulp.LpProblem("Optimizacion_Paneles", pulp.LpMinimize)

    # Variables de decisión: número de paneles por casa
    x = pulp.LpVariable.dicts("Paneles", 
                              [(casa, tipo) for casa in range(len(consumos)) for tipo in paneles.keys()],
                              lowBound=0, cat="Integer")

    # Función objetivo: minimizar inversión total
    modelo += pulp.lpSum([paneles[tipo]["costo"] * x[(casa, tipo)] 
                          for casa in range(len(consumos)) for tipo in paneles.keys()])

    # Restricciones: energía mínima por casa
    for casa in range(len(consumos)):
        modelo += pulp.lpSum([paneles[tipo]["energia"] * x[(casa, tipo)] for tipo in paneles.keys()]) >= consumos[casa]

    # Restricciones: área máxima por casa
    for casa in range(len(consumos)):
        modelo += pulp.lpSum([paneles[tipo]["area"] * x[(casa, tipo)] for tipo in paneles.keys()]) <= areas_techo[casa]

    # Resolver
    modelo.solve()

    # Resultados
    solucion = {f"Casa {casa+1}": {tipo: int(x[(casa, tipo)].value()) for tipo in paneles.keys()} 
                for casa in range(len(consumos))}
    costo_total = pulp.value(modelo.objective)

    return solucion, costo_total
