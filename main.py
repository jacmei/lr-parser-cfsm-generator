from Production import *
from ProductionState import *
from State import *

productions = []

def create_state(production_states, num):
    s = State(num, production_states, [])
    progresses = []
    ps_index = 0
    for ps in s._bases:
        if ps._production._RHS[ps._progress] not in progresses:
            progresses.append(ps._production._RHS[ps._progress])
            ps_index += 1
    ps_index += 1
    first = 0
    last = 0
    for prog in progresses:
        for prod in productions:
            if prod._LHS == prog:
                s._closures.append(ProductionState(prod, 0))
                last += 1
    
    for i in range(first, last + 1):
        for prod in productions:
            if prod._LHS == s._closures[i]._production[s._closures[i]._progress] and prod._LHS not in progresses:
                progresses.append(prod._LHS)
    first = last
    for i in range(ps_index, len(progresses)):

def generate():
    file_to_parse = "id_list_grammar.txt" #input("Input filename: ")
    try: 
        with open(file_to_parse) as f:
            for line in f:
                line = line.strip()
                p = line.split(" ")
                p.pop(1)
                productions.append(Production(p[0], p[1:]))
        initial_basis = [ProductionState(productions[0], 0)]
        states = []
        state_count = -1
        initial_state = create_state(initial_basis, 0)
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()

    