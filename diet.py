# -*- coding: utf-8 -*-

from gurobipy import *

def solve(speisen, kalorien, fett, kosten, minMenge, minKalorien, maxFett, obst):

  # Gurobi-Modell erzeugen.
  model = Model("Diätenplanung")


  modeUNI = 2

  if (modeUNI == 0):
    # Problem ist ein Minimierungsproblem.
    model.modelSense = GRB.MINIMIZE

    # Variablen in Gurobi erzeugen und hinzufuegen.
    xKaufen = {}
    for speise in speisen:
      xKaufen[speise] = model.addVar(lb = minMenge[speise], ub = 8.0, obj = kosten[speise], name = ('x_' + speise))

    # Constraint: Maximal 8 Einheiten einer Sorte kaufen
    #for speise in speisen:
    #  model.addConstr(xKaufen[speise] <= 8)

    # muss nicht sein
    model.update()

    # Constraint: Mindestmenge an Kalorien.
    model.addConstr(quicksum(kalorien[speise] * xKaufen[speise] for speise in speisen) >= minKalorien)

    # Constraint: Maximalmenge an Fett.
    model.addConstr(quicksum(fett[speise] * xKaufen[speise] for speise in speisen) <= maxFett)

    # Constraint: Ein Drittel der Gesamtmenge muss Obst sein.
    model.addConstr(1.0/3.0 * quicksum(xKaufen[speise] for speise in speisen) <= quicksum(xKaufen[speise] for speise in obst))


  elif (modeUNI == 1):
    x_Apfel = model.addVar(lb = minMenge['Apfel'], ub = 8.0, name = 'x_Apfel')
    x_Erdnussbutter = model.addVar(lb = minMenge['Erdnussbutter'], ub = 8.0, name = 'x_Erdnussbutter')
    x_Milch = model.addVar(lb = minMenge['Milch'], ub = 8.0, name = 'x_Milch')
    x_Brot = model.addVar(lb = minMenge['Brot'], ub = 8.0, name = 'x_Brot')
    x_Birne = model.addVar(lb = minMenge['Birne'], ub = 8.0, name = 'x_Birne')

    model.setObjective(0.31 * x_Apfel + 0.82 * x_Erdnussbutter + 0.06 * x_Milch + 0.49 * x_Brot + 0.25 * x_Birne, GRB.MINIMIZE)

    # Constraint: Mindestmenge an Kalorien.
    model.addConstr(50 * x_Apfel + 627 * x_Erdnussbutter + 42 * x_Milch + 188 * x_Brot + 55 * x_Birne >= minKalorien)

    # Constraint: Maximalmenge an Fett.
    model.addConstr(0.4 * x_Apfel + 49.9 * x_Erdnussbutter + 0.1 * x_Milch + 1.0 * x_Brot + 0.3 * x_Birne <= maxFett)

    # Constraint: Ein Drittel der Gesamtmenge muss Obst sein.
    model.addConstr(x_Apfel + x_Birne >= (x_Apfel + x_Erdnussbutter + x_Milch + x_Brot + x_Birne) / 3.0)


  else:
    x_Apfel = model.addVar(lb = minMenge['Apfel'], ub = 8.0, obj = 0.31, name = 'x_Apfel')
    x_Erdnussbutter = model.addVar(lb = minMenge['Erdnussbutter'], ub = 8.0, obj = 0.82, name = 'x_Erdnussbutter')
    x_Milch = model.addVar(lb = minMenge['Milch'], ub = 8.0, obj = 0.06, name = 'x_Milch')
    x_Brot = model.addVar(lb = minMenge['Brot'], ub = 8.0, obj = 0.49, name = 'x_Brot')
    x_Birne = model.addVar(lb = minMenge['Birne'], ub = 8.0, obj = 0.25, name = 'x_Birne')

    model.modelSense = GRB.MINIMIZE

    # Constraint: Mindestmenge an Kalorien.
    model.addConstr(50 * x_Apfel + 627 * x_Erdnussbutter + 42 * x_Milch + 188 * x_Brot + 55 * x_Birne >= minKalorien)

    # Constraint: Maximalmenge an Fett.
    model.addConstr(0.4 * x_Apfel + 49.9 * x_Erdnussbutter + 0.1 * x_Milch + 1.0 * x_Brot + 0.3 * x_Birne <= maxFett)

    # Constraint: Ein Drittel der Gesamtmenge muss Obst sein.
    model.addConstr(x_Apfel + x_Birne >= (x_Apfel + x_Erdnussbutter + x_Milch + x_Brot + x_Birne) / 3.0)


  # Problem loesen lassen.
  model.optimize()

  # Ausgabe der Loesung.
  if model.status == GRB.OPTIMAL:
    print(f"\nOptimaler Zielfunktionswert: {model.ObjVal}\n")
    if (modeUNI == 0):
      for speise in speisen:
        print(f"Es werden {xKaufen[speise].x} Mengeneinheiten von {speise} gekauft.")
    else:
        print(f"Es werden {x_Apfel.x} Mengeneinheiten von Apfel gekauft.")
        print(f"Es werden {x_Erdnussbutter.x} Mengeneinheiten von Erdnussbutter gekauft.")
        print(f"Es werden {x_Milch.x} Mengeneinheiten von Milch gekauft.")
        print(f"Es werden {x_Brot.x} Mengeneinheiten von Brot gekauft.")
        print(f"Es werden {x_Birne.x} Mengeneinheiten von Birne gekauft.")
  else:
    print(f"Keine Optimalloesung gefunden. Status: {model.status}")


  return model
