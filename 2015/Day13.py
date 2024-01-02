# learnings:
# - seating arrangement is circular, so different rotations are effectively the same
# - fix one person's position and permute the rest to significantly reduce the number of permutations
# - iter() is a built-in function that returns an iterator for the given iterable
# - next() is built-in function that retrieves the next/first item from an iterator
# - next(iter(person_master)) gets the first element from a set or any other iterable that doesn't support direct indexing like list
# - using pyomo yielded alternative solution where it divided people into 2 groups
# - not able to figure out circular constraint in pyomo
# - networkx.draw() helps with visulaization of graphs
# - networkx.spring_layout() helps simplify visual positioning of nodes in a graph

# %%
import re
import itertools
import math
import pyomo.environ as pyo
import matplotlib.pyplot as plt
import networkx as nx
# %%
puzzle_input = \
"""Alice would gain 2 happiness units by sitting next to Bob.
Alice would gain 26 happiness units by sitting next to Carol.
Alice would lose 82 happiness units by sitting next to David.
Alice would lose 75 happiness units by sitting next to Eric.
Alice would gain 42 happiness units by sitting next to Frank.
Alice would gain 38 happiness units by sitting next to George.
Alice would gain 39 happiness units by sitting next to Mallory.
Bob would gain 40 happiness units by sitting next to Alice.
Bob would lose 61 happiness units by sitting next to Carol.
Bob would lose 15 happiness units by sitting next to David.
Bob would gain 63 happiness units by sitting next to Eric.
Bob would gain 41 happiness units by sitting next to Frank.
Bob would gain 30 happiness units by sitting next to George.
Bob would gain 87 happiness units by sitting next to Mallory.
Carol would lose 35 happiness units by sitting next to Alice.
Carol would lose 99 happiness units by sitting next to Bob.
Carol would lose 51 happiness units by sitting next to David.
Carol would gain 95 happiness units by sitting next to Eric.
Carol would gain 90 happiness units by sitting next to Frank.
Carol would lose 16 happiness units by sitting next to George.
Carol would gain 94 happiness units by sitting next to Mallory.
David would gain 36 happiness units by sitting next to Alice.
David would lose 18 happiness units by sitting next to Bob.
David would lose 65 happiness units by sitting next to Carol.
David would lose 18 happiness units by sitting next to Eric.
David would lose 22 happiness units by sitting next to Frank.
David would gain 2 happiness units by sitting next to George.
David would gain 42 happiness units by sitting next to Mallory.
Eric would lose 65 happiness units by sitting next to Alice.
Eric would gain 24 happiness units by sitting next to Bob.
Eric would gain 100 happiness units by sitting next to Carol.
Eric would gain 51 happiness units by sitting next to David.
Eric would gain 21 happiness units by sitting next to Frank.
Eric would gain 55 happiness units by sitting next to George.
Eric would lose 44 happiness units by sitting next to Mallory.
Frank would lose 48 happiness units by sitting next to Alice.
Frank would gain 91 happiness units by sitting next to Bob.
Frank would gain 8 happiness units by sitting next to Carol.
Frank would lose 66 happiness units by sitting next to David.
Frank would gain 97 happiness units by sitting next to Eric.
Frank would lose 9 happiness units by sitting next to George.
Frank would lose 92 happiness units by sitting next to Mallory.
George would lose 44 happiness units by sitting next to Alice.
George would lose 25 happiness units by sitting next to Bob.
George would gain 17 happiness units by sitting next to Carol.
George would gain 92 happiness units by sitting next to David.
George would lose 92 happiness units by sitting next to Eric.
George would gain 18 happiness units by sitting next to Frank.
George would gain 97 happiness units by sitting next to Mallory.
Mallory would gain 92 happiness units by sitting next to Alice.
Mallory would lose 96 happiness units by sitting next to Bob.
Mallory would lose 51 happiness units by sitting next to Carol.
Mallory would lose 81 happiness units by sitting next to David.
Mallory would gain 31 happiness units by sitting next to Eric.
Mallory would lose 73 happiness units by sitting next to Frank.
Mallory would lose 89 happiness units by sitting next to George."""
# %%
puzzle_input = puzzle_input.upper()
puzzle_input =  re.sub(" WOULD", ",", puzzle_input)
puzzle_input =  re.sub(" GAIN ", "+", puzzle_input)
puzzle_input =  re.sub(" LOSE ", "-", puzzle_input)
puzzle_input =  re.sub(" HAPPINESS UNITS BY SITTING NEXT TO ", ",", puzzle_input)
puzzle_input =  re.sub("\.", "", puzzle_input)

puzzle_output = {}
person_master = set()

for line in puzzle_input.split("\n"):
    name1, cost, name2 = line.split(",")
    puzzle_output[(name1, name2)] = int(cost)
    person_master.add(name1)
    person_master.add(name2)

for person in person_master:
    puzzle_output[('me', person)] = 0
    puzzle_output[(person, 'me')] = 0

person_master.add('me')

# %%
def brute_force_solution(puzzle_output, person_master):
    def get_cost(path):
        cost = 0
        for i, person in enumerate(path):
            if(i==0):
                before = path[-1]
                after = path[i+1]
            elif(i==len(path)-1):
                before = path[i-1]
                after = path[0]
            else:
                before = path[i-1]
                after = path[i+1]
            
            cost += (puzzle_output[(person, before)] + puzzle_output[(person, after)])
        return cost
    
    max_cost = -math.inf
    fixed_person = next(iter(person_master))
    others = person_master - {fixed_person}

    for path in itertools.permutations(others, r=len(others)):
        cost = get_cost((fixed_person,) + path)
        max_cost = max(cost, max_cost)
    return max_cost

print(brute_force_solution(puzzle_output, person_master))
# %%
def pyomo_solution(puzzle_output, person_master):
    # initialize model object
    model = pyo.ConcreteModel()
    # define index sets
    model.persons = pyo.Set(initialize=list(person_master))
    # define parameters
    model.happiness = pyo.Param(model.persons, model.persons, initialize=puzzle_output, default=0)
    # define decision variables
    model.x = pyo.Var(model.persons, model.persons, domain=pyo.Binary, initialize=0)
    model.order = pyo.Var(model.persons, domain=pyo.NonNegativeIntegers, initialize=0)
    # define objective function
    model.obj = pyo.Objective(expr=sum(model.happiness[i,j]*model.x[i,j] for i in model.persons for j in model.persons), sense=pyo.maximize)
    # define constraints   
    def no_self_seating_rule(model, i):
        return model.x[i,i] == 0
    
    def commutative_rule(model, i, j):
        return model.x[i,j] == model.x[j,i]
    
    def make_circle_rule(model, i):
        return sum(model.x[i,j] for j in model.persons) == 2

    model.no_self_seating = pyo.Constraint(model.persons, rule=no_self_seating_rule)
    model.commutative = pyo.Constraint(model.persons, model.persons, rule=commutative_rule)
    model.make_circle = pyo.Constraint(model.persons, rule=make_circle_rule)
    # load and apply solver
    solver = pyo.SolverFactory('glpk')
    solver.solve(model)
    
    # Create a graph
    G = nx.Graph()
    # Add nodes
    for person in person_master:
        G.add_node(person)
    # Add edges based on the solution
    for i in model.persons:
        for j in model.persons:
            if model.x[i, j].value == 1:
                G.add_edge(i, j)
    # Use spring layout
    spring_pos = nx.spring_layout(G)

    # Draw the graph using the spring layout positions
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos=spring_pos, with_labels=True, node_size=1800, node_color="lightblue", font_size=12, edge_color="gray")
    plt.title("Seating Arrangement", fontsize=14)
    plt.show()
    
    return model.obj()

print(pyomo_solution(puzzle_output, person_master))
# %%
