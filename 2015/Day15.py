# learnings:
# - using a dictionary of namedtuples or data classes instead of a dictionary of dictionaries. Makes the code more readable and maintainable.
# - use of exec for dynamic variable assignment is discouraged due to potential security risks and debugging difficulties
# - constraint programming (CP) in solving combinatorial problems works better than brute force
# - CP highly efficient in pruning the search space, avoids considering combinations that violate the constraints
# - CP algorithms use constraint propagation techniques, early detection of conflicts or infeasibility, allowing the algorithm to avoid unnecessary computations
# - CP backtracks intelligently, often pruning other related dead-ends that don't need to be explored 

# %%
import re
import itertools
from collections import namedtuple
from ortools.sat.python import cp_model
# %%
puzzle_input = \
"""Sprinkles: capacity 2, durability 0, flavor -2, texture 0, calories 3
Butterscotch: capacity 0, durability 5, flavor -3, texture 0, calories 3
Chocolate: capacity 0, durability 0, flavor 5, texture -1, calories 8
Candy: capacity 0, durability -1, flavor 0, texture 5, calories 8"""
# %%
Property = namedtuple('Property', ['capacity', 'durability', 'flavor', 'texture', 'calories'])
pattern = re.compile('^([A-Za-z]+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)')

input_dict = {ingredient: Property(*map(int, attributes))
              for ingredient, *attributes in (pattern.match(line).groups() 
              for line in puzzle_input.splitlines())}
# %%

def brute_force_solution(input_dict):
    max_score = 0
    max_recipe = None

    for recipe in itertools.product(range(101), repeat=len(input_dict)):
        if sum(recipe) == 100:

            properties = {prop:0 for prop in ['capacity', 'durability', 'flavor', 'texture','calories']}

            for prop in properties:
                properties[prop] = sum(getattr(input_dict[ing], prop) * amount for ing, amount in zip(input_dict, recipe))
            
            # if properties['calories']==500:
            total_score = max(properties['capacity'],0) * max(properties['durability'],0) * max(properties['flavor'],0) * max(properties['texture'],0)
            
            if total_score>max_score:
                max_score = total_score
                max_recipe = recipe
            else:
                continue
        else:
            continue

    return max_score, max_recipe

print(brute_force_solution(input_dict))
# %%
# Create the model
model = cp_model.CpModel()

# Input data
amounts, caps, durs, flavs, texts, cals = [], [], [], [], [], []

for name, props in input_dict.items():
    amounts.append(model.NewIntVar(0, 100, f'amount_{name}'))
    caps.append(props.capacity)
    durs.append(props.durability)
    flavs.append(props.flavor)
    texts.append(props.texture)
    cals.append(props.calories)

# Define recipe properties
cap_sum = model.NewIntVar(0, max(max(caps), sum(caps)) * 100, 'cap_sum')
dur_sum = model.NewIntVar(0, max(max(durs), sum(durs)) * 100, 'dur_sum')
flav_sum = model.NewIntVar(0, max(max(flavs), sum(flavs)) * 100, 'flav_sum')
text_sum = model.NewIntVar(0, max(max(texts), sum(texts)) * 100, 'text_sum')

model.Add(sum(caps[i] * amounts[i] for i in range(len(amounts))) == cap_sum)
model.Add(sum(durs[i] * amounts[i] for i in range(len(amounts))) == dur_sum)
model.Add(sum(flavs[i] * amounts[i] for i in range(len(amounts))) == flav_sum)
model.Add(sum(texts[i] * amounts[i] for i in range(len(amounts))) == text_sum)

# Constraint - recipe amount 100
model.Add(sum(amounts) == 100)

# Constraint - recipe properties>0
model.Add(cap_sum > 0)
model.Add(dur_sum > 0)
model.Add(flav_sum > 0)
model.Add(text_sum > 0)

# Creating a new variable for the score
max_product_value = \
    max(max(caps), sum(caps)) * \
        max(max(durs), sum(durs)) * \
            max(max(flavs), sum(flavs)) * \
                max(max(texts), sum(texts)) * \
                    10**8
score = model.NewIntVar(0, max_product_value, 'score')

# Define the multiplication equality for the score
model.AddMultiplicationEquality(score, [cap_sum, dur_sum, flav_sum, text_sum])

# Objective: Maximize the score
model.Maximize(score)

# Solver
solver = cp_model.CpSolver()
status = solver.Solve(model)

# Output
if status == cp_model.OPTIMAL:
    print(f"Score: {solver.Value(score)}")
    print("Amounts:", [solver.Value(a) for a in amounts])
    print(f"Totals: {solver.Value(cap_sum)}, {solver.Value(dur_sum)}, {solver.Value(flav_sum)}, {solver.Value(text_sum)}")
else:
    print("No optimal solution found.")
# %%