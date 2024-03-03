# learnings:
# - constraint programming is useful for combinatorial problems
# - there is a dynamic programming solution on reddit, but I didn't get it

# %%
import pandas as pd
from ortools.sat.python import cp_model
# %%
puzzle_input = \
"""11
30
47
31
32
36
3
1
5
3
32
36
15
11
46
26
28
1
19
3"""
# %%
puzzle_input = tuple(int(val) for val in puzzle_input.splitlines())
target = 150
# %%
model = cp_model.CpModel()

in_vars = model.NewBoolVarSeries('in', pd.Index(range(len(puzzle_input))))

model.Add(cp_model.LinearExpr.WeightedSum(in_vars, puzzle_input) == 150)

# Enumerate and Display all solutions
solver = cp_model.CpSolver()
solver.parameters.enumerate_all_solutions = True

class AllSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, input_coeff, in_vars):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._input_coeff = input_coeff
        self._in_vars = in_vars
        self._solution_count = 0
        self._all_solutions = set()

    def on_solution_callback(self):
        self._solution_count += 1
        result = [self._input_coeff[i] for i in range(len(self._input_coeff)) if self.Value(self._in_vars[i])>0]
        self._all_solutions.add(tuple(result))
        print(result)

    def solution_count(self):
        return self._solution_count
    
    def all_solutions(self):
        return self._all_solutions

solution_printer = AllSolutionPrinter(puzzle_input, in_vars)
status = solver.Solve(model, solution_printer)

# Statistics.
print("\nStatistics")
print(f"  status   : {solver.StatusName(status)}")
print(f"  conflicts: {solver.NumConflicts()}")
print(f"  branches : {solver.NumBranches()}")
print(f"  wall time: {solver.WallTime()} s")
print(f"  sol found: {solution_printer.solution_count()}")

print(min([len(sol) for sol in solution_printer.all_solutions()]))
# %%