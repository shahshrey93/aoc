# learnings:
# - None; yet to get feedback from chatGPT
# - solve this with linear and constraint programming both and check speed

# %%
import re
import pyomo.environ as pyo
from ortools.sat.python import cp_model
# %%
puzzle_input = \
"""Hit Points: 104
Damage: 8
Armor: 1"""
# %%
pattern = re.compile(r'(\w+): (\d+)')
boss_stats = dict(re.findall(pattern, puzzle_input))
# %%