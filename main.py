from Production import *
from ProductionState import *
from State import *

def create_state(production_states, num):
    s = State()

def main():
    file_to_parse = "id_list_grammar.txt" #input("Input filename: ")
    try: 
        productions = []
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

    