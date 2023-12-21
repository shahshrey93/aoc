# learnings:
# - 

# %%
import hashlib
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
    location_master.add(loc1)
    location_master.add(loc2)

# find closest 2 points
distance = min(distance_matrix.values())
loc1, loc2 = min(distance_matrix, key=distance_matrix.get)

# remove visited points from location master
location_master.discard(loc1)
location_master.discard(loc2)

while(len(location_master)>0):
    del distance_matrix[(loc1, loc2)]
    distance_matrix_subset = {(l1,l2):distance_matrix.get((l1,l2)) for l1,l2 in distance_matrix if any(c in {loc1, loc2} for c in {l1,l2})}
    distance += min(distance_matrix_subset.values())
    loc1, loc2 = min(distance_matrix_subset, key=distance_matrix_subset.get)
    location_master.discard(loc1)
    location_master.discard(loc2)

print(distance)
# %%