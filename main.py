from Production import *
from ProductionState import *
from State import *

def generate_states(production_master_list, production_states, state_value):
    s = State(state_value, production_states, [])
    unique_progresses_list = []
    unique_progress_index = 0
    
    for production_state in s._bases:
        if production_state._progress != len(production_state._production._RHS):
            prog_in_basis = production_state._production._RHS[production_state._progress]
            if prog_in_basis not in unique_progresses_list:
                unique_progresses_list.append(prog_in_basis)
    
    first = 0
    last = 0
    for progress in unique_progresses_list:
        for production in production_master_list:
            if progress == production._LHS:
                s._closures.append(ProductionState(production, 0))
                last += 1
    unique_progress_index = len(unique_progresses_list)
    
    while (last > first):
        for i in range(first, last + 1):
            if s._closures[i]._progress != len(s._closures[i]._production._RHS):
                prog_in_closure = s._closures[i]._production._RHS[s._closures[i]._progress]
                if prog_in_closure not in unique_progresses_list:
                    unique_progresses_list.append(production._LHS)
        first = last
        for i in range(unique_progress_index, len(unique_progresses_list)):
            for production in production_master_list:
                if unique_progresses_list[i] == production._LHS:
                    s._closures.append(ProductionState(production, 0))
                    last += 1
        unique_progress_index = len(unique_progresses_list)
    
    unique_progress_dictionary = {}
    for progress in unique_progresses_list:
        unique_progress_dictionary.setdefault(progress, 0)
    for production_state in s._bases:
        if production_state._progress != len(production_state._production._RHS):
            prog_in_basis = production_state._production._RHS[production_state._progress]
            unique_progress_dictionary[prog_in_basis] += 1
    for production_state in s._closures:
        if production_state._progress != len(production_state._production._RHS):
            prog_in_closure = production_state._production._RHS[production_state._progress]
            unique_progress_dictionary[prog_in_closure] += 1
    basis_index = 0
    for production_state in s._bases:
        if production_state._progress < len(production_state._production._RHS) - 1:
            production_state.action = "S"
        elif production_state._progress == len(production_state._production._RHS) - 1:
            prog_in_basis = production_state._production._RHS[production_state._progress]
            if unique_progress_dictionary[prog_in_basis] > 1:
                production_state.action = "S"
            elif unique_progress_dictionary[prog_in_basis] == 0:
                production_state.action = "S/R"
        elif production_state._progress == len(production_state._production._RHS):
            production_state.action = "R"
            prev_prog_in_basis = production_state._production._RHS[production_state._progress - 1]
            other_basis_index = 0
            for other_production_state in s._bases:
                if basis_index != other_basis_index:
                    if other_production_state._progress - 1 > 0:
                        other_prev_prog_in_basis = other_production_state._production._RHS[other_production_state._progress - 1]
                        if prev_prog_in_basis == other_prev_prog_in_basis and other_production_state._progress != len(other_production_state._production._RHS):
                            s._conflicts.add("SHIFT/REDUCE")
                        elif prev_prog_in_basis == other_prev_prog_in_basis and other_production_state._progress == len(other_production_state._production._RHS):
                            s._conflicts.add("REDUCE/REDUCE")

                other_basis_index += 1
        basis_index += 1
    closure_index = 0
    for production_state in s._closures:
        if production_state._progress < len(production_state._production._RHS) - 1:
            production_state.action = "S"
        elif production_state._progress == len(production_state._production._RHS) - 1:
            prog_in_closure = production_state._production._RHS[production_state._progress]
            if unique_progress_dictionary[prog_in_closure] > 1:
                production_state.action = "S"
            elif unique_progress_dictionary[prog_in_closure] == 0:
                production_state.action = "S/R"
        elif production_state._progress == len(production_state._production._RHS):
            production_state.action = "R"
            prev_prog_in_closure = production_state._production._RHS[production_state._progress - 1]
            other_closure_index = 0
            for other_production_state in s._closures:
                if closure_index != other_closure_index:
                    if other_production_state._progress - 1 > 0:
                        other_prev_prog_in_closure = other_production_state._production._RHS[other_production_state._progress - 1]
                        if prev_prog_in_closure == other_prev_prog_in_closure and other_production_state._progress != len(other_production_state._production._RHS):
                            s._conflicts.add("SHIFT/REDUCE")
                        elif prev_prog_in_closure == other_prev_prog_in_closure and other_production_state._progress == len(other_production_state._production._RHS):
                            s._conflicts.add("REDUCE/REDUCE")

                other_closure_index += 1
        closure_index += 1
    new_state_value = state_value + 1
    for progress in unique_progresses_list:
        for production_state in s._bases:
            if production_state._progress != len(production_state._production._RHS):
                if progress == production_state._production._RHS[production_state._progress] and production_state._action == "S":
                    production_state._goto = new_state_value
        for production_state in s._closures:
            if production_state._progress != len(production_state._production._RHS):
                if progress == production_state._production._RHS[production_state._progress] and production_state._action == "S":
                    production_state._goto = new_state_value
        new_state_value += 1
    
def print_state(s):
    line_separator = "-----------------------------"
    output = "STATE : " + str(s._value) + "\n" + line_separator + "\n"
    if len(s._conflicts) == 0:
        output += "NO CONFLICTS\n"
    else:
        for conflict in s._conflicts:
            output += conflict + "\n"
    output += "-----------------------------\n"

def initialize():
    file_to_parse = "id_list_grammar.txt" #input("Input filename: ")
    try: 
        production_master_list = []
        with open(file_to_parse) as f:
            for line in f:
                line = line.strip()
                p = line.split(" ")
                p.pop(1)
                production_master_list.append(Production(p[0], p[1:]))
        initial_basis = [ProductionState(production_master_list[0], 0)]
        states = []
        state_count = -1
        initial_state = create_state(initial_basis, 0)
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()

    