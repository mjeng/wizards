import argparse
import pycosat

"""
======================================================================
  Complete the following function.
======================================================================
"""

class Wizard:

    # comparison_array =

    def __init__(self, name, num):
        self.name = name
        self.num = num

    def __lt__(self, other):
        return Wizard.comparison_array[self.num][other.num]

    def __eq__(self, other):
        return False # there should be no equal-aged wizards

    def __gt__(self, other):
        return not Wizard.comparison_array[self.num][other.num]

    def __repr__(self):
        return self.name


def solve(num_wizards, num_constraints, wizards, constraints):
    """
    Write your algorithm here.
    Input:
        num_wizards: Number of wizards
        num_constraints: Number of constraints
        wizards: An array of wizard names, in no particular order
        constraints: A 2D-array of constraints,
                     where constraints[0] may take the form ['A', 'B', 'C']i

    Output:
        An array of wizard names in the ordering your algorithm returns
    """
    wizard_to_num = {}
    num_to_wizard = {}
    for i in range(len(wizards)):
        wizard_to_num[wizards[i]] = i
        num_to_wizard[i] = wizards[i]


    def convert_from_triple(w1, w2, w3):
        return w1 + w2 * num_wizards + w3 * num_wizards**2
    def convert_to_triple(num):
        return [num % num_wizards, (num // num_wizards) % num_wizards, ((num // num_wizards) // num_wizards) % num_wizards]

    #initialize cnf array
    cnf = []
    #read in constraints by line
    for constraint in constraints:
        #match each of 3 wizards to numbers, (temp: 1,2,3
        # ws = []
        # for w in constraint:
        #     ws.append(wizards.index(w))

        ws = [wizard_to_num[w] for w in constraint]

        #initialize pairs 1,3 and 2,3
    # convert = PairToIndex(ws[0], ws[2], num_wizards)
        #convert2 = PairToIndex(ws[2], ws[3], num_wizards)
        #add both pair's PairToIndex to cnf format
        cond1 = convert_from_triple(ws[0], ws[1], ws[2])
        cond2 = convert_from_triple(ws[0], ws[2], ws[1])
        cond3 = convert_from_triple(ws[1], ws[0], ws[2])
        cond4 = convert_from_triple(ws[1], ws[2], ws[0])
        cond5 = convert_from_triple(ws[2], ws[0], ws[1])
        cond6 = convert_from_triple(ws[2], ws[1], ws[0])
        cnf.append([cond1, cond3, cond5, cond6])
        cnf.append([-cond1, -cond3])
        cnf.append([-cond1, -cond5])
        cnf.append([-cond1, -cond6])
        cnf.append([-cond3, -cond5])
        cnf.append([-cond3, -cond6])
        cnf.append([-cond5, -cond6])
        cnf.append([-cond2])
        cnf.append([-cond4])

    #sol = pycosat cnf
    solution = pycosat.solve(cnf)
    print(solution)

    ###############################################
    # converting

    # solution = [n - 1 if n > 0 else n + 1 for n in solution]
    comparison_array = [[None] * num_wizards] * num_wizards
    for num in solution:
        if num > 0:
            triple = convert_to_triple(num)
            comparison_array[triple[0]][triple[1]] = True
            comparison_array[triple[0]][triple[2]] = True
            comparison_array[triple[1]][triple[2]] = True
            comparison_array[triple[1]][triple[0]] = False
            comparison_array[triple[2]][triple[0]] = False
            comparison_array[triple[2]][triple[1]] = False
        # else:
        #     triple = convert_to_triple(-num)
        #     comparison_array[triple[0]][triple[1]] = False
        #     comparison_array[triple[0]][triple[2]] = False
        #     comparison_array[triple[1]][triple[2]] = False
        #     comparison_array[triple[1]][triple[0]] = True
        #     comparison_array[triple[2]][triple[0]] = True
        #     comparison_array[triple[2]][triple[1]] = True
    # for num in solution:
    #     if num > 0:
    #         pair = convert_to_pair(num)
    #         comparison_array[pair[0]][pair[1]] = True
    #         comparison_array[pair[1]][pair[0]] = False
    #     else:
    #         pair = convert_to_pair(-num)
    #         comparison_array[pair[0]][pair[1]] = False
    #         comparison_array[pair[1]][pair[0]] = True
    Wizard.comparison_array = comparison_array

    return [w.name for w in sorted([Wizard(num_to_wizard[i], i) for i in range(num_wizards)])]
    #iterate thru sol
        #make into boolean 2d array table thing size [num_wizards][num_wizards], row x col, (row < col)
    #convert to names
    # return []

"""
======================================================================
   No need to change any code below this line
======================================================================
"""

def read_input(filename):
    with open(filename) as f:
        num_wizards = int(f.readline())
        num_constraints = int(f.readline())
        constraints = []
        wizards = set()
        for _ in range(num_constraints):
            c = f.readline().split()
            constraints.append(c)
            for w in c:
                wizards.add(w)

    wizards = list(wizards)
    return num_wizards, num_constraints, wizards, constraints

def write_output(filename, solution):
    with open(filename, "w") as f:
        for wizard in solution:
            f.write("{0} ".format(wizard))

if __name__=="__main__":
    parser = argparse.ArgumentParser(description = "Constraint Solver.")
    parser.add_argument("input_file", type=str, help = "___.in")
    parser.add_argument("output_file", type=str, help = "___.out")
    args = parser.parse_args()

    num_wizards, num_constraints, wizards, constraints = read_input(args.input_file)
    solution = solve(num_wizards, num_constraints, wizards, constraints)
    write_output(args.output_file, solution)
