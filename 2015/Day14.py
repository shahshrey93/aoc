# learnings:
# - possible to extract multiple groups from a single regex match with ()

# %%
import re
# %%
puzzle_input = \
"""Vixen can fly 19 km/s for 7 seconds, but then must rest for 124 seconds.
Rudolph can fly 3 km/s for 15 seconds, but then must rest for 28 seconds.
Donner can fly 19 km/s for 9 seconds, but then must rest for 164 seconds.
Blitzen can fly 19 km/s for 9 seconds, but then must rest for 158 seconds.
Comet can fly 13 km/s for 7 seconds, but then must rest for 82 seconds.
Cupid can fly 25 km/s for 6 seconds, but then must rest for 145 seconds.
Dasher can fly 14 km/s for 3 seconds, but then must rest for 38 seconds.
Dancer can fly 3 km/s for 16 seconds, but then must rest for 37 seconds.
Prancer can fly 25 km/s for 6 seconds, but then must rest for 143 seconds."""
# %%
pattern = re.compile('^([a-zA-Z]+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.')

input_dict = {name: {'speed': int(speed), 'runtime': int(runtime), 'resttime': int(resttime)}
              for name, speed, runtime, resttime in (pattern.match(line).groups() 
              for line in puzzle_input.splitlines())}

# %%
seconds = 2503

def distance_travelled(speed, runtime, resttime, seconds):
    cycle_time = runtime + resttime
    cycles = seconds // cycle_time
    remainder = seconds % cycle_time
    return speed * (cycles * runtime + min(remainder, runtime))

max_distance = max(distance_travelled(values['speed'], values['runtime'], values['resttime'], seconds) 
                   for values in input_dict.values())

print(max_distance)
# %%

output_dict = {'current distance':{name:0 for name in input_dict}, 
               'current score':{name:0 for name in input_dict}}

for t in range(seconds):
    
    for name, values in input_dict.items():
        output_dict['current distance'][name] = distance_travelled(values['speed'], values['runtime'], values['resttime'], t+1)
    
    max_curr_dist = max(output_dict['current distance'].values())
    
    for name, values in output_dict['current distance'].items():
        if values>=max_curr_dist:
            output_dict['current score'][name] += 1
        else:
            pass
        
print(output_dict['current score'])
# %%