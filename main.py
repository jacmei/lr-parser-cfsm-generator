from Production import *
from ProductionState import *
from State import *
import sys, os, copy, traceback

def stringify_state(s):
    line_separator = "-----------------------------"
    output = "STATE : " + str(s._value) + "\n" + line_separator + "\n"
    if len(s._conflicts) == 0:
        output += "NO CONFLICTS\n"
    else:
        for conflict in s._conflicts:
            output += conflict + "\n"
    output += "-----------------------------\n"
    for production_states in s._bases:
        output += production_states._production._LHS + " : "
        for i in range(len(production_states._production._RHS)):
            if i == production_states._progress:
                output += ". "
            output += production_states._production._RHS[i] + " "
        if production_states._progress == len(production_states._production._RHS):
            output += ". "
        if production_states._action == "R":
            output += "| R(" + str(len(production_states._production._RHS)) + ")"
        elif production_states._action == "S/R":
            output += "| on " + production_states._production._RHS[production_states._progress] + ", S/R(" + str(len(production_states._production._RHS)) + ")"
        elif production_states._action == "S":
            output += "| on " + production_states._production._RHS[production_states._progress] + ", S and goto " + str(production_states._goto)
        output += "\n"
    output += "-----------------------------\n"
    if len(s._closures) == 0:
        output += "NO CLOSURE\n"
    else:
        for production_states in s._closures:
            output += production_states._production._LHS + " : "
            for i in range(len(production_states._production._RHS)):
                if i == production_states._progress:
                    output += ". "
                output += production_states._production._RHS[i] + " "
            if production_states._progress == len(production_states._production._RHS):
                output += ". "
            if production_states._action == "R":
                output += "| R(" + str(len(production_states._production._RHS)) + ")"
            elif production_states._action == "S/R":
                output += "| on " + production_states._production._RHS[production_states._progress] + ", S/R(" + str(len(production_states._production._RHS)) + ")"
            elif production_states._action == "S":
                output += "| on " + production_states._production._RHS[production_states._progress] + ", S and goto " + str(production_states._goto)
            output += "\n"
    output += "-----------------------------\n\n"
    return output

def generate_states(production_master_list, initial_basis, outfile):
    state_value = 0
    current_states_list = [State(state_value, initial_basis, [])]
    states_master_list = [State(state_value, initial_basis, [])]
    while len(current_states_list) > 0:
        s = current_states_list[0]
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
            for i in range(first, last):
                if s._closures[i]._progress != len(s._closures[i]._production._RHS):
                    prog_in_closure = s._closures[i]._production._RHS[s._closures[i]._progress]
                    if prog_in_closure not in unique_progresses_list:
                        unique_progresses_list.append(prog_in_closure)
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
                production_state._action = "S"
            elif production_state._progress == len(production_state._production._RHS) - 1:
                prog_in_basis = production_state._production._RHS[production_state._progress]
                if unique_progress_dictionary[prog_in_basis] > 1:
                    production_state._action = "S"
                elif unique_progress_dictionary[prog_in_basis] == 1:
                    production_state._action = "S/R"
            elif production_state._progress == len(production_state._production._RHS):
                production_state._action = "R"
                prev_prog_in_basis = production_state._production._RHS[production_state._progress - 1]
                other_basis_index = 0
                for other_production_state in s._bases:
                    if basis_index != other_basis_index:
                        if other_production_state._progress > 0:
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
                production_state._action = "S"
            elif production_state._progress == len(production_state._production._RHS) - 1:
                prog_in_closure = production_state._production._RHS[production_state._progress]
                if unique_progress_dictionary[prog_in_closure] > 1:
                    production_state._action = "S"
                elif unique_progress_dictionary[prog_in_closure] == 1:
                    production_state._action = "S/R"
            elif production_state._progress == len(production_state._production._RHS):
                production_state._action = "R"
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
            future_basis_list = []
            basis_list = []
            to_increment = False
            for production_state in s._bases:
                if production_state._progress != len(production_state._production._RHS):
                    if progress == production_state._production._RHS[production_state._progress] and production_state._action == "S":
                        future_basis_list.append(ProductionState(production_state._production, production_state._progress + 1))
                        basis_list.append(production_state)
                        production_state._goto = new_state_value
                        to_increment = True
            for production_state in s._closures:
                if production_state._progress != len(production_state._production._RHS):
                    if progress == production_state._production._RHS[production_state._progress] and production_state._action == "S":
                        future_basis_list.append(ProductionState(production_state._production, production_state._progress + 1))
                        basis_list.append(production_state)
                        production_state._goto = new_state_value
                        to_increment = True
            future_state = State(new_state_value, future_basis_list, [])
            #print(future_state)
            #print()
            #for x in states_master_list:
            #    print(x)
            #print()
            for existing_state in states_master_list:
                if future_state == existing_state:
                    for production_state in basis_list:
                        production_state._goto = existing_state._value
                    to_increment = False
            if to_increment:
                new_state_value += 1

        print(stringify_state(s), file = outfile)
        for i in range(state_value + 1, new_state_value):
            new_basis = []
            for production_state in s._bases:
                if production_state._goto == i:
                    new_basis.append(ProductionState(production_state._production, production_state._progress + 1))
            for production_state in s._closures:
                if production_state._goto == i:
                    new_basis.append(ProductionState(production_state._production, production_state._progress + 1))
            new_state = State(i, new_basis, [])
            states_master_list.append(new_state)
            current_states_list.append(copy.deepcopy(new_state))
            
        current_states_list.pop(0)
        state_value = new_state_value - 1
        #for x in states_master_list:
        #    print(x)
        
def main():
    file_to_parse = input("Input filename: ")
    try:
        production_master_list = []
        outfile = open("outfile.txt", "w")
        with open(file_to_parse) as f:
            for line in f:
                line = line.strip()
                p = line.split(" ")
                p.pop(1)
                production_master_list.append(Production(p[0], p[1:]))
        initial_basis = [ProductionState(production_master_list[0], 0)]
        generate_states(production_master_list, initial_basis, outfile)
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        exc_info = sys.exc_info()
        traceback.print_exception(*exc_info)
        print(e)

if __name__ == '__main__':
    main()

    