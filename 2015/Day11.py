# learnings:
# - converting recursion to iterative approach to be more memory-efficient

# %%
puzzle_input = \
"""cqjxxyzz"""
# %%
def incrementing_password(old_password):
    if old_password[-1]!='z':
        updated_char = chr(ord(old_password[-1]) + 1)
        return old_password[:-1] + updated_char
    else:
        return incrementing_password(old_password[:-1]) + 'a'
    
# def incrementing_password(old_password):
#     new_password = list(old_password)
#     i = len(new_password) - 1
#     while(i>=0):
#         if new_password[i]=="z":
#             new_password[i] == "a"
#             i -= 1
#         else:
#             new_password[i] = chr(ord(new_password[i]) + 1)
#             break
#     return ''.join(new_password)
    
def password_requirements(old_password):
    confusing_chars = any(char in old_password for char in {'i','o','l'})
    
    if confusing_chars:
        return False
    else:
        double_appear = set()
        three_seq = False
        
        for i in range(1, len(old_password)-1):  
            if(old_password[i-1]==old_password[i]):
                double_appear.add(old_password[i])
            elif(old_password[i]==old_password[i+1]):
                double_appear.add(old_password[i])
            else:
                pass

            if(ord(old_password[i])==1+ord(old_password[i-1])) and (ord(old_password[i+1])==1+ord(old_password[i])):
                three_seq = True
            else:
                pass

        if len(double_appear)>=2 and three_seq:
            return True
        else:   
            return False
# %%

input = puzzle_input

while not(password_requirements(incrementing_password(input))):
    input = incrementing_password(input)

print(incrementing_password(input))

# %%