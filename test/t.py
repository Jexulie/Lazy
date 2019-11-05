

a = [
    {'n': 'a', 's': 1},
    {'n': 'b', 's': 1},
    {'n': 'c', 's': 1},
    {'n': 'd', 's': 1},
    {'n': 'e', 's': 1}, ## remove this
]

b = [
    'a',
    'b',
    'c',
    'd',
]

#! Works Tho
# a = [file for file in a if 'e' not in file['n']]
e = []

for file in a:
    if file['n'] in b:
        e.append(file)

print(e)
