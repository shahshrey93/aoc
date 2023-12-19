# learnings:
# - use .startswith() to check if a string starts with a given substring

# %%
import hashlib
# %%
puzzle_input = \
"""ckczppom"""
# %%
i=0
hash_value = hashlib.md5(f"{puzzle_input}{i}".encode()).hexdigest()

while not(hash_value.startswith("00000")):
    i += 1
    hash_value = hashlib.md5(f"{puzzle_input}{i}".encode()).hexdigest()
# %%
print(i)