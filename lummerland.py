# coding=utf-8

from gurobipy import *


def solve(places, goods, travel_distance, costs, capacities, availabilities, demands, max_travel):
    model = Model("lummerland")

    # Ziel (Minimieren oder Maximieren?)
    model.modelSense = GRB.MINIMIZE

    # Variablen erzeugen.
    x = {}
    for g in goods:
        for p in places:
            for q in places:
                x[g, p, q] = model.addVar(obj = costs[g] * travel_distance[p, q], name="x_" + g + "_" + p + "_" + q)

    # Variablen dem Modell bekannt machen.
    model.update()

    # bedarf decken
    model.addConstrs(quicksum(x[g, p, q] for p in places) >= demands[q, g] for q in places for g in goods)

    # Vierte Nebenbedingung (falls noetig):
    # kapazität checken
    model.addConstrs(availabilities[p, g] >= quicksum(x[g, p, q] for q in places) for p in places for g in goods)
    # Ungleichung: ...




    # Erste Nebenbedingung:
    # Bedeutung: Es muss von einem Gut immer mehr oder gleich viel vorhanden sein, als/wie benötigt wird.
    model.addConstrs((quicksum(availabilities[p, g] for p in places) >= quicksum(demands[p, g] for p in places)) for g in goods)


    # Zweite Nebenbedingung (falls noetig):
    # insgesamt können höchstens capacities[p, q] Chargen von Ort p zu Ort q transportiert werden.
    model.addConstrs(quicksum(x[g, p, q] for g in goods) <= capacities[p, q] for p in places for q in places)


    # Dritte Nebenbedingung (falls noetig):
    # max travel nicht überschreiten
    model.addConstr(quicksum(quicksum(x[g, p, q] for g in goods) * travel_distance[p, q] for p in places for q in places) <= max_travel)



    # Fuenfte Nebenbedingung (falls noetig):
    # Bedeutung: ...
    # Ungleichung: ...

    # Nebenbedingungen hinzugefuegt? LP loesen lassen!
    model.optimize()

    # Transportmengen ausgeben.
    if model.status == GRB.OPTIMAL:
      print('\nOptimalloesung hat Kosten von %g.\n' % (model.ObjVal))
      for k in goods:
        for s1 in places:
          for s2 in places:
            if x[k, s1, s2].x > 0.0001:
              print('Von %s nach %s werden %g Chargen von %s transportiert.' % (s1, s2, x[k, s1, s2].x, k))
    else:
      print('Keine Optimalloesung gefunden. Status: %i' % (model.status))

    return model

