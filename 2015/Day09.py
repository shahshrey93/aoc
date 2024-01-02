# learnings:
# - use list comprehensions to make the code more pythonic and readable
# - replace the recursive in the greedy solution with iterative approach
# - python has a default recursion limit (usually 1000 calls deep), which is a safeguard against infinite recursion leading to stack overflow. Iterative solutions don't have this limitation.
# - each recursive call requires space on the call stack to store function arguments, local variables, and return addresses.
# - iterative solutions usually have less overhead since they avoid the costs associated with allocating memory, pushing/popping stack frames
# - mostly iterative approach uses a fixed amount of memory for loop variables
# %%
from utils import measure_runtime, measure_memory
import math
import itertools
# %%
puzzle_input = \
"""Faerun to Norrath = 129
Faerun to Tristram = 58
Faerun to AlphaCentauri = 13
Faerun to Arbre = 24
Faerun to Snowdin = 60
Faerun to Tambi = 71
Faerun to Straylight = 67
Norrath to Tristram = 142
Norrath to AlphaCentauri = 15
Norrath to Arbre = 135
Norrath to Snowdin = 75
Norrath to Tambi = 82
Norrath to Straylight = 54
Tristram to AlphaCentauri = 118
Tristram to Arbre = 122
Tristram to Snowdin = 103
Tristram to Tambi = 49
Tristram to Straylight = 97
AlphaCentauri to Arbre = 116
AlphaCentauri to Snowdin = 12
AlphaCentauri to Tambi = 18
AlphaCentauri to Straylight = 91
Arbre to Snowdin = 129
Arbre to Tambi = 53
Arbre to Straylight = 40
Snowdin to Tambi = 15
Snowdin to Straylight = 99
Tambi to Straylight = 70"""
# %%
distance_matrix = {}
location_master = set()

for line in puzzle_input.split("\n"):
    loc1, loc2 = line.split(" to ")
    loc2, distance = loc2.split(" = ")
    distance_matrix[(loc1, loc2)] = int(distance)
    distance_matrix[(loc2, loc1)] = int(distance)
    location_master.add(loc1)
    location_master.add(loc2)

# %%
def brute_force_solution(distance_matrix, location_master):
    
    def get_path_distance(path):
        return sum(distance_matrix.get((path[i], path[i+1]), math.inf) for i in range(len(path) - 1))
    
    distance = math.inf

    for path in itertools.permutations(location_master, len(location_master)):
        distance = min(distance, get_path_distance(path))

    return distance

print(measure_runtime(brute_force_solution, repeat=10, number=10)(distance_matrix, location_master))
measure_memory(brute_force_solution)(distance_matrix, location_master)
# %%
def greedy_solution(distance_matrix, location_master):
    # pick 2 locations closest to each other
    loc1, loc2 = min(distance_matrix, key=distance_matrix.get)
    distance = min(distance_matrix.values())
    path = [loc1, loc2]
    
    while(len(path)<len(location_master)):
        # subset the distance_matrix with first or last location in the path
        first = path[0]
        last = path[-1]
        distance_matrix_subset = {k:distance_matrix.get(k) 
                                  for k in distance_matrix 
                                  if any(c in {first, last} for c in k)}
        
        # remove paths between visited locations
        for c1,c2 in itertools.permutations(path, 2):
            distance_matrix_subset.pop((c1, c2), None)

        # pick the closest location to the path
        (loc1, loc2), min_distance = min(distance_matrix_subset.items(), key=lambda x: x[1])
        distance += min_distance

        # if the closest location is the first or last location in the path, append/prepend it
        if (loc1 == first):
            path.insert(0, loc2)
        elif (loc2 == last):
            path.append(loc1)
        elif (loc2 == first):
            path.insert(0, loc1)
        elif (loc1 == last):
            path.append(loc2)
        else:
            raise Exception("Something went wrong")

    return distance
    
print(measure_runtime(greedy_solution, repeat=10, number=10)(distance_matrix, location_master))
measure_memory(greedy_solution)(distance_matrix, location_master)