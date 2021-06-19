#!/usr/bin/python

from gurobipy import *


def solve(mines, ores, available, unit_costs, unit_time_needed, work_hours, subsidised_ores, demand):

    model = Model('bergwerk')

    model.modelSense = GRB.MINIMIZE

    x = {}
    for m in mines:
        for o in ores:
            x[m, o] = model.addVar(obj = unit_costs[m, o], name=f'x_{m}_{o}')

    model.update()

    # 1. Nebenbedingung:
    # Menge jeden Erzes soll mindestens das Auftragsvolumen (demand) pro Erz decken.
    model.addConstrs((quicksum(x[m, o] for m in mines) >= demand[o]) for o in ores)

    # 2. Nebenbedingung:
    # Abgebaute Menge darf die maximal vorhandene Menge (available) pro Mine und Erz nicht überschreiten.
    model.addConstrs((x[m, o] <= available[m, o]) for o in ores for m in mines)

    # 3. Nebenbedingung:
    # Die Arbeitszeit darf pro Mine nur 2/3 ihrer maximalen Arbeitszeit (work_hours) betragen.
    model.addConstrs((quicksum(x[m, o] * unit_time_needed[m, o] for o in ores) <= (work_hours[m] * 2/3)) for m in mines)

    # 4. Nebenbedingung:
    # Pro Mine müssen 1/4 der abgebauten Erze subventionierte Erze sein.
    model.addConstrs((quicksum(x[m,o] for o in ores) / 4 <= quicksum(x[m,o] for o in subsidised_ores)) for m in mines)

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

    