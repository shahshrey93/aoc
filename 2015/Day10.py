# learnings:
# - 

# %%
puzzle_input = \
"""1321131112"""
# %%
def look_and_say(input_string):
    input_string = str(input_string) + '0'
    output = ''
    cnt = 1

    if len(input_string)==1:
        output = '1'+input_string
    else:
        for i in range(len(input_string)-1):
            if input_string[i+1]==input_string[i]:
                cnt += 1
            else:
                output += str(cnt) + str(input_string[i])
                cnt = 1
    return output
# %%
i = puzzle_input

for _ in range(50):
    i = look_and_say(i)

print(len(i))
# %%