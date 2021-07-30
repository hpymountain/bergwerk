from gurobipy import quicksum, Model, GRB
from gurobipy import *

def solve(days, routes, length, visitors, min_rest_days, min_length, hard_routes):
    
    model = Model('tour')

    model.modelSense = GRB.MAXIMIZE

    assignment = {}
    for day in range(days): # Achtung: day nimmt alle Werte von 0 bis days-1 an.
        for route in routes:
            assignment[day, route] = model.addVar(vtype=GRB.BINARY, obj=visitors[route], name=f"assignment_{day}_{route}")
    model.update()



    # 1. tag darf kein rest tag
    model.addConstr(quicksum(assignment[0, route] for route in routes) >= 0)

    # am letzten tag darf und muss nur les champs gefahren werden
    model.addConstrs(assignment[days - 1, route] == (1 if route == 'Les Champs' else 0) for route in routes)

    # jeden tag darf nur eine route gewählt werden
    model.addConstrs(quicksum(assignment[day, route] for route in routes) <= 1 for day in range(days))

    # jede route darf nur an einem tag vorkommen
    model.addConstrs(quicksum(assignment[day, route] for day in range(days)) <= 1 for route in routes)

    # es muss mindestens strecke x gefahren werden
    model.addConstr(quicksum(assignment[day, route] * length[route] for route in routes for day in range(days)) >= min_length)

    # es müssen mindestens x ruhe tage eingehalten werden
    model.addConstr(quicksum(assignment[day, route] for day in range(days) for route in routes) <= days - min_rest_days)

    # keine zwei schweren routen an aufeinander folgenden tagen
    model.addConstrs(quicksum(assignment[day, route] + assignment[day + 1, route] for route in hard_routes) <= 1 for day in range(days - 1))



    model.optimize()


    if model.status == GRB.OPTIMAL:
        print(f"\nObjective value: {model.ObjVal}\n")
        for day in range(days):
            assign = None
            for route in routes:
                if (assignment[day, route].x >= 0.1):
                    assign = route
            if assign == None:
                print(f'Day {day+1} will be a rest day')
            else:
                print(f'Day {day+1} will include the route: {assign}')
    else:
        print(f"No solution was found. Status {model.status}")

    return model
