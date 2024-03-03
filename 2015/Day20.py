# learnings:
# - no need to initialize a list to the size of puzzle_input/10. 
# - it was a theoretical upper bound, but in practice, the required size could be smaller
# - hence used a dictionary instead of a list

# %%

# %%
puzzle_input = 34000000
# %%
# Part 1
houses = {}

for elf in range(1, puzzle_input//10):
    for house in range(elf, puzzle_input//10, elf):
        houses[house] = houses.get(house, 0) + elf * 10

min_house = min(house for house, presents in houses.items() if presents >= puzzle_input)
print(min_house)
# %%
# Part 2
houses = {}

for elf in range(1, puzzle_input//10):
    for house in range(elf, elf*50 + 1, elf):
        houses[house] = houses.get(house, 0) + elf * 11

min_house = min(house for house, presents in houses.items() if presents >= puzzle_input)
print(min_house)
# %%