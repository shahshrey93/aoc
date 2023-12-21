# learnings:
# - unsolved, didn't get how to read input properly

# %%
import io
# %%
puzzle_input = open("Day08.txt", "r").readlines()
# %%
char_cnt = 0
string_literal_cnt = 0

for line in puzzle_input:
    char_cnt += len(line[:-1])
    string_literal_cnt += len(eval(line))

print(char_cnt - string_literal_cnt)
# %%