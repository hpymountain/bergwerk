#!/usr/bin/python

from gurobipy import *


def solve(mines, ores, available, unit_costs, unit_time_needed, work_hours, subsidised_ores, demand):

    model = Model('bergwerk')

    x = {}
    for m in mines:
        for o in ores:
            x[m, o] = model.addVar(name=f'x_{m}_{o}')

    model.modelSense = GRB.MINIMIZE

    model.update()

    # 1. Nebenbedingung:
    # Zeit pro Mine max.2/3 der work_hours
    model.addConstr(quicksum(unit_time_needed[ores] * x[ores] for o in ores)<= quicksum(2/3 * x[ores]*subsidised_ores[ores] for o in ores))

    # 2. Nebenbedingung:
    # Von jedem Erz mind. Menge von demand abbauen
    for o in ores:
        x[ores] >= demand[ores] 
     
    # 3. Nebenbedingung: 
    # Pro Mine nicht mehr als die verfügbare Menge abbauen
    for m in mines:
        x[mines] <= available[mines]
    
    # 4. Nebenbedingung: 
    # Pro Erz nicht mehr als die verfügbare Menge abbauen
    for o in ores:
        x[ores] <= available[ores]

    # 5. Nebenbedingung:
    # 1/4 der abgebauten Erze müssen subventionierte Erze sein
    model.addConstr(1/4 *quicksum(x[ores] for o in ores) <= quicksum(subsidised_ores[ores] * x[subsidised_ores] for o in ores))

    # optimize
    model.optimize()

    # Ausgabe der Loesung.
    if model.status == GRB.OPTIMAL:
        print('\nOptimaler Zielfunktionswert: %g\n' % model.ObjVal)
        for m in mines:
            for o in ores:
                print(f"Mine {m} baut {str(x[m,o].x)} Einheiten {o} ab")
            print("")
    else:
        print('Keine Optimalloesung gefunden. Status: %i' % (model.status))
    return model

    