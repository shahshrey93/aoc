# learnings:
# - greedy search did not work

# %%
import re
import math
# %%
puzzle_input1 = \
"""Al => ThF
Al => ThRnFAr
B => BCa
B => TiB
B => TiRnFAr
Ca => CaCa
Ca => PB
Ca => PRnFAr
Ca => SiRnFYFAr
Ca => SiRnMgAr
Ca => SiTh
F => CaF
F => PMg
F => SiAl
H => CRnAlAr
H => CRnFYFYFAr
H => CRnFYMgAr
H => CRnMgYFAr
H => HCa
H => NRnFYFAr
H => NRnMgAr
H => NTh
H => OB
H => ORnFAr
Mg => BF
Mg => TiMg
N => CRnFAr
N => HSi
O => CRnFYFAr
O => CRnMgAr
O => HP
O => NRnFAr
O => OTi
P => CaP
P => PTi
P => SiRnFAr
Si => CaSi
Th => ThCa
Ti => BP
Ti => TiTi
e => HF
e => NAl
e => OMg"""

puzzle_input2 = \
'''CRnSiRnCaPTiMgYCaPTiRnFArSiThFArCaSiThSiThPBCaCaSiRnSiRnTiTiMgArPBCaPMgYPTiRnFArFArCaSiRnBPMgArPRnCaPTiRnFArCaSiThCaCaFArPBCaCaPTiTiRnFArCaSiRnSiAlYSiThRnFArArCaSiRnBFArCaCaSiRnSiThCaCaCaFYCaPTiBCaSiThCaSiThPMgArSiRnCaPBFYCaCaFArCaCaCaCaSiThCaSiRnPRnFArPBSiThPRnFArSiRnMgArCaFYFArCaSiRnSiAlArTiTiTiTiTiTiTiRnPMgArPTiTiTiBSiRnSiAlArTiTiRnPMgArCaFYBPBPTiRnSiRnMgArSiThCaFArCaSiThFArPRnFArCaSiRnTiBSiThSiRnSiAlYCaFArPRnFArSiThCaFArCaCaSiThCaCaCaSiRnPRnCaFArFYPMgArCaPBCaPBSiRnFYPBCaFArCaSiAl
'''
# %%
replacements = [tuple(line.split(" => ")) for line in puzzle_input1.splitlines()]
# %%
distinct_word = set()

for word, replace in replacements:
    pattern = re.compile(f'{word}')
    for match in pattern.finditer(puzzle_input2):
        start, end = match.span()
        distinct_word.add(puzzle_input2[:start] + replace + puzzle_input2[end:])

print(len(distinct_word))
# %%
i = 0
current_moleculeset = set([puzzle_input2])

while 'e' not in current_moleculeset:
    parent_moleculeset = set()

    for molecule in current_moleculeset:
        for replace, word in replacements:
            pattern = re.compile(f'{word}')
            for match in pattern.finditer(molecule):
                start, end = match.span()
                parent_moleculeset.add(molecule[:start] + replace + molecule[end:])
    
    # parent_moleculeset = list(parent_moleculeset)
    # parent_moleculeset.sort(key=lambda x: len(x))
    # parent_moleculeset = set(parent_moleculeset[:100])
    current_moleculeset = parent_moleculeset.copy()
    i+=1
    print(i, len(current_moleculeset))

print(i-1)
# %%