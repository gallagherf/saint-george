import re
import pprint
import json

pp = pprint.PrettyPrinter(indent=4)

"""
Strictly for messing around with the contents of dictionaries.
"""

def write_json(filename, data):
    """
    Write to a human-readable json file
    """
    jstr = json.dumps(data, ensure_ascii=False, indent=4)
    with open(filename, 'w') as f:
        f.write(jstr)

def load_data():
    with open('static/definitions.json', 'r') as f:
        d = f.read()
        definitions = json.loads(d)

    with open('static/roots.json', 'r') as g:
        r = g.read()
        roots = json.loads(r)

    return definitions, roots

def get_max(dictionary):
    # Return the highest integer in a definitions
    # dictionary 
    numbers = [int(k) for k in dictionary.keys()]

    return max(numbers)

definitions, roots = load_data()

start = get_max(definitions) + 1


with open('static/dictionary.json', 'r') as h:
    n = h.read()
    nouns = json.loads(n)


#write_json('static/OLD_definitions.json', definitions)
#write_json('static/OLD_roots.json', roots)
#write_json('static/OLD_dictionary.json', nouns)


print(len(nouns))
for noun in nouns:
    for entry in nouns[noun]:
        if entry['root'] in roots:
            if entry['category'] == 'n':
                nouns[noun].remove(entry)

counter = 0

print(len(nouns))

#write_json('static/dictionary.json', nouns)

