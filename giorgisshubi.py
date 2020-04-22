import re
import pprint
import json

pp = pprint.PrettyPrinter(indent=4)


##############
# OPEN FILES #
##############

with open('static/definitions.json', 'r') as f:
    d = f.read()
    nouns = json.loads(d)

with open('static/roots.json', 'r') as g:
    r = g.read()
    roots = json.loads(r)

################
# USEFUL LISTS #
################

vowels = ['a', 'e', 'i', 'o', 'u']

cases = { 'a' : 'nom',
        'e' : 'nom',
        'i' : 'nom',
        'o' : 'nom',
        'u' : 'nom',
        'm' : 'erg',
        'ma' : 'erg',
        'is' : 'gen',
        's' : 'dat',
        'it' : 'inst',
        'ti' : 'inst', 
        't' : 'inst',
        'ad' : 'adv',
        'd' : 'adv'
        }

prepositions = { 'Si' } 

ani_alpha = {  'ა' : 'a' ,
                'ბ' : 'b' ,
                'გ' : 'g' ,
                'დ' : 'd' ,
                'ე' : 'e' ,
                'ვ' : 'v' ,
                'ზ' : 'z' ,
                'თ' : 'T' ,
                'ი' : 'i' ,
                'კ' : 'k' ,
                'ლ' : 'l' ,
                'მ' : 'm' ,
                'ნ' : 'n' ,
                'ო' : 'o' ,
                'პ' : 'p' ,
                'ჟ' : 'Z' ,
                'რ' : 'r' ,
                'ს' : 's' ,
                'ტ' : 't' ,
                'უ' : 'u' ,
                'ფ' : 'P' ,
                'ქ' : 'K' ,
                'ღ' : 'G' ,
                'ყ' : 'q' ,
                'შ' : 'S' ,
                'ჩ' : 'X' ,
                'ც' : 'C' ,
                'ძ' : 'j' ,
                'წ' : 'c' ,
                'ჭ' : 'x' ,
                'ხ' : 'H' ,
                'ჯ' : 'J' ,
                'ჰ' : 'h' ,
                }

alpha_ani = {}
for k,v in ani_alpha.items():
    alpha_ani[v] = k


#######################
# AVAILABLE FUNCTIONS #
# write_jason         #
# lgconvert           #
# glconvert           #
# noun_breaker        #
#######################


def write_json(filename, data):
    """
    Write to a human-readable json file
    """
    jstr = json.dumps(data, ensure_ascii=False, indent=4)
    with open(filename, 'w') as f:
        f.write(jstr)




def lgconvert(word):
    """
    Take a Latin string and return a Georgian string.
    """

    latin_check = re.search('[a-z]', word)
    # Make sure word is not already in Latin alphabet
    if latin_check:
        georgian = []
        for letter in word:
            if letter in alpha_ani:
                georgian.append(alpha_ani[letter])
            else:
                georgian.append(letter)

        return ''.join(georgian)

    else:
        return word




def glconvert(word):
    """
    Take a Georgian string and return a Latin string.
    """
    georgian_check = re.search('[აბგდევზთიკლმნოპჟრსტუფქღყშჩვძწჭხჯჰ]', word)
    # Make sure word is not already in Georgian alphabet
    if georgian_check:
        latin = []
        for letter in word:
            latin.append(ani_alpha[letter])

        return ''.join(latin)

    else:
        return word

def noun_breaker(word):
    _case = re.search('(ma|it|ti|is|ad|a|s|o|i|t|e|m|d)$', word)
    postposition = None
    result = {}

    if _case:
        case_ending = _case.group()
        root = word[:-len(case_ending)] 
         
        if root in roots:
            if case_ending in cases:
                case_type = cases[case_ending] 
                result['case_ending'] = lgconvert(case_ending)
                result['case_type'] = case_type
            for entry in roots[root]:
                result['groot'] = lgconvert(entry['root'])
                result['lroot'] = glconvert(entry['root'])
                result['definition'] = entry['definition'] 

            return result

        else:
            
            return "no_entry" 
    else:
        return "no_case"


#################
#x = noun_breaker("koxbroli")
#################




def analyze(word):
    """
    Take a word and break it up
    """
    
    latin_check = re.search('[a-z]', word)

    if not latin_check:
        word = glconvert(word)

    marks = {}
    prefixes = []
    suffixes = []

    # Check for preverb
    _preverb = re.search('^(carmo|gadmo|Semo|Xamo|gada|camo|gamo|amo|ca|Xa|Se|ga|da|mo|mi|a)', word)
    if _preverb:
        preverb = _preverb.group()
        word = word[len(preverb):]
        prefixes.append(preverb)
        marks['preverb'] = preverb
    else:
        marks['preverb'] = ''

    # Check for agreeing prefix
    _agrpref = re.search('^(gv|g|v|m)', word)
    if _agrpref:
        agrpref = _agrpref.group()
        word = word[len(agrpref):]
        prefixes.append(agrpref)
        marks['agrpref'] = agrpref
    else:
        marks['agrpref'] = ''

    # Check for version
    _version = re.search('^(a|i|u|e)', word)
    if _version:
        version = _version.group()
        word = word[len(version):]
        prefixes.append(version)
        marks['version'] = version
    else:
        marks['version'] = ''

    # H Marker
    _hseries = re.search('^(h|s|m)', word)
    if _hseries:
        hseries = _hseries.group()
        word = word[len(hseries):]
        prefixes.append(hseries)
        marks['hseries'] = hseries
    else:
        marks['hseries'] = ''

    # Plural T
    _pluralt = re.search('(T)$', word)
    if _pluralt:
        pluralt = _pluralt.group()
        word = word[:-len(pluralt)]
        suffixes.append('T')
        marks['pluralt'] = 'T'
    else:
        marks['pluralt'] = ''

    # Agreeing endings 
    _agr = re.search('(qvnen|qavi|nen|Har|var|an|en|e|i|a|s|n)$', word)
    if _agr:
        agr = _agr.group()
        word = word[:-len(agr)]
        suffixes.append(agr)
        marks['agrsuf'] = agr
    else:
        marks['agrsuf'] = ''

    # Sm check
    """
    Not sure what this is. Stem marker I think.
    """
    _sm = re.search('(i|e|o)$', word)
    if _sm:
        sm = _sm.group()
        word = word[:-len(sm)]
        suffixes.append(sm)
        marks['sm'] = sm
    else:
        marks['sm'] = ''

    # od-check
    _od = re.search('(od)$', word)
    if _od:
        od = _od.group()
        word = word[:-len(od)]
        suffixes.append(od)
        marks['od'] = od
    else:
        marks['od'] = ''

    # Stem formant check
    _sf = re.search('(av|am|ev|eb|em|ob)$', word)
    if _sf:
        sf = _sf.group()
        word = word[:-len(sf)]
        suffixes.append(sf)
        marks['sf'] = sf
    else:
        marks['sf'] = ''

    # Doniani check
    _doniani = re.search('(d)$', word)
    if _doniani:
        doniani = _doniani.group()
        word = word[:-1]
        suffixes.append(doniani)
        marks['doniani'] = 'd'
    else:
        marks['doniani'] = ''

    # Participle check
    _participle = re.search('(ul|el)$', word)
    if _participle:
        participle = _participle.group()
        word = word[:-2]
        suffixes.append(participle)
        marks['participle'] = participle
    else:
        marks['participle'] = ''
   
    root = word
    marks['root'] = root

    return marks


def finalize(word, roots):
    # Check for mistakes in the analysis against entries in the dictionary

    marks = analyze(word)

    # Check to make sure that the (o)d wasn't misanalyzed as doniani
    if marks['sf'] == '' and marks['od'] == '':
        if marks['doniani'] == 'd':
            if marks['root'] not in roots:
                _sf = re.search('(av|am|ev|eb|em|ob)$', marks['root'])
                if _sf:
                    sf = _sf.group()
                    marks['root'] = marks['root'][:-len(sf)]
                    marks['sf'] = sf
                    marks['doniani'] = ''
                    marks['od'] = 'd'

    # Agrsuf recheck, makes sure that the agreeing suffix
    # isn't mislabeled as a stem marker
    if marks['agrsuf'] == '' and marks['sm'] != '':
        marks['agrsuf'] = marks['sm']
        marks['sm'] = ''

    # Check to make sure that doniani wasn't
    # a false positive 
    if marks['doniani'] != '':
        root = marks['root'] + marks['doniani']
        if root in roots:
            marks['root'] = root 
            marks['doniani'] = ''
  
    # Check to make sure that hseries wasn't a false
    # positive
    if marks['hseries'] != '':
        root = marks['hseries'] + marks['root']
        if root in roots:
            marks['root'] = root
            marks['hseries'] = ''

    # Check to make sure that hseries and doniani weren't false positives
    if marks['hseries'] + marks['root'] + marks['doniani'] in roots:
        root = marks['hseries'] + marks['root'] + marks['doniani']
        if root in roots:
            marks['root'] = root
            marks['hseries'] = ''
            marks['doniani'] = '' 


    # Check to make sure that doniani wasn't a false negative
    if marks['doniani'] == '':
        if marks['root'] not in roots:
            if marks['root'][-1] == 'd':
                marks['doniani'] = 'd'
                marks['root'] = marks['root'][:-1]

    return marks 





def recompile(marks):
    # Take a marks dictionary and reassemble a word from it

    word = marks['preverb'] + marks['agrpref'] + marks['version'] + marks['hseries'] + marks['root']
    word = word + marks['doniani'] + marks['od'] + marks['sf'] + marks['sm'] + marks['agrsuf']
    
    return word

def compare(goal, target_list):
    # GOAL is an analyzed word from the wild. TARGET_LIST is an entry
    # in the roots dictionary which contains multiple possible instances
    # of that particular root. The function compares the GOAL dictionary
    # to each entry, finds the maximum number of matches and returns a list
    # of those entries which have the maximum number of matches

    deviant = 0
    current_comp = 0
    current_champs = []

    for target in target_list:
        comp = 0
        for k in goal:
            try:
                if goal[k] == target[k]:  
                    comp += 1
            except:
                pass
        if comp == current_comp:
            current_champs.append(target)

        if comp > current_comp:
            current_comp = comp
            current_champs = [target]

    return current_champs


