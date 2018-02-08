import os
import argparse
from random import shuffle
from output_validator import processInput
P = False
NUM_EXECUTIONS = 10
# input_global = ''
# output_global = ''
"""
======================================================================
  Complete the following function.
======================================================================
"""

class Base:
    base = 10
    def __init__(self, base10num):
        """
        Assuming d1 < d2 < d3 is our constraint
        """
        self.rep_num = base10num
        self.d1, self.d2, self.d3 = Base.convert_to_base(self.rep_num)

    @classmethod
    def convert_to_base(cls, num):
        """
        Assumes 3 digits needed
        """
        d1 = num % cls.base
        d2 = num // cls.base % cls.base
        d3 = num // (cls.base**2) % cls.base
        return d1, d2, d3

    @classmethod
    def convert_from_base(cls, d1, d2, d3):
        return d1 + cls.base * d2 + cls.base**2 * d3

    def __repr__(self):
        # return ""
        return "w" + str(self.d1) + " < w" + str(self.d2) + " < w" + str(self.d3)

class Wizard:

    # comparison_array =

    def __init__(self, name, num):
        self.name = name
        self.num = num

    def __lt__(self, other):
        return Wizard.comparison_array[self.num][other.num] == -1

    def __eq__(self, other):
        return False # there should be no equal-aged wizards

    def __gt__(self, other):
        return Wizard.comparison_array[self.num][other.num] == 1

    def __repr__(self):
        return self.name



def eliminate_set(possible_constraints, n1, n2):
    """
    n1 should be < n2, so we will eliminate the sets:
        n2 < n1 < #
        n2 < # < n1
        # < n2 < n1
    """
    num_wizards = Base.base
    for i in range(num_wizards):
        possible_constraints[Base.convert_from_base(n2, n1, i)] = None
        possible_constraints[Base.convert_from_base(n2, i, n1)] = None
        possible_constraints[Base.convert_from_base(i, n2, n1)] = None

def arbitrarily_filter(possible_constraints, rand=True):
    if rand:
        shuffle(possible_constraints)
    for c in possible_constraints:
        if c is not None:
            eliminate_set(possible_constraints, c.d1, c.d2)
            eliminate_set(possible_constraints, c.d2, c.d3)

def construct_order(remaining_constraints, num_wizards, num_to_wizard):
    comparison_array = [[None] * num_wizards] * num_wizards
    for c in remaining_constraints:
        comparison_array[c.d1][c.d2] = -1
        comparison_array[c.d2][c.d3] = -1
        comparison_array[c.d2][c.d1] = 1
        comparison_array[c.d3][c.d2] = 1
    Wizard.comparison_array = comparison_array
    return [w.name for w in sorted([Wizard(num_to_wizard[i], i) for i in range(num_wizards)])]

def adjust_failed_constraints(order): # mutative

    print("#################################################") if P else None

    MAX_LOOPS = 10000
    # MAX_LOOPS = 10000
    num_loops = 0
    def swap(i1, i2):
        nonlocal order
        j = order.index(i1)
        k = order.index(i2)
        order[j], order[k] = order[k], order[j]
    # order = order[:]

    # SETUP LAYER 1
    input_file = input_global
    # input_file = 'input' + str(num_wizards) + '.in'
    output_file = 'temp.txt'
    write_output(output_file, order)

    # SETUP LAYER 2
    foo = processInput(input_file, output_file)
    constraints_satisfied = foo[0]
    total_constraints = foo[1]
    failed = foo[2]
    i = 0

    # EXECUTE SWAPPING WITHIN FAILED CONSTRAINTS
    while constraints_satisfied < total_constraints:

        print("START\n") if P else None
        if i >= len(failed):
            break
        print("# satisfied: {0}\ni: {1}\nfailed: {2}\n".format(constraints_satisfied, i, failed[i])) if P else None

        # SETUP
        # if num_loops > MAX_LOOPS:
        #     break
        prev_constr_satisfied = constraints_satisfied
        prev_failed = failed
        what_failed = failed[i]
        swap0 = what_failed[0]
        swap1 = what_failed[1]
        swap2 = what_failed[2]

        # SWAP 1
        print('    order1:', order) if P else None
        swap(swap0, swap2)
        print('new order1:', order) if P else None
        write_output(output_file, order)
        foo = processInput(input_file, output_file)
        constraints_satisfied = foo[0]
        failed = foo[2]

        print("\n# satisfied: {0}\ni: {1}\nfailed: {2}\n".format(constraints_satisfied, i, failed[i])) if P else None

        # UNSWAP & SWAP 2 only if necessary
        if prev_constr_satisfied >= constraints_satisfied:
            swap(swap0, swap2)
            print('    order2:', order) if P else None
            swap(swap1, swap2)
            print('new order2:', order) if P else None
            write_output(output_file, order)
            foo = processInput(input_file, output_file)
            constraints_satisfied = foo[0]
            failed = foo[2]

            print("\n# satisfied: {0}\ni: {1}\nfailed: {2}\n".format(constraints_satisfied, i, failed[i])) if P else None

            # if both swaps don't work then move onto next set of constraints
            if prev_constr_satisfied >= constraints_satisfied:
                print('    order3:', order) if P else None
                swap(swap1, swap2)
                print('new order3:', order) if P else None
                failed = prev_failed
                i += 1

                if i < len(failed):
                    print("\n# satisfied: {0}\ni: {1}\nfailed: {2}\n".format(constraints_satisfied, i, failed[i])) if P else None
                constraints_satisfied = prev_constr_satisfied

            else:
                i = 0
        else:
            i = 0

        num_loops += 1

        print("\nSTOP\n\n") if P else None

    print("CONSTRAINTS SATISFIED:", constraints_satisfied)
    return constraints_satisfied


def solve(num_wizards, num_constraints, wizards, constraints):
    """
    Write your algorithm here.
    Input:
        num_wizards: Number of wizards
        num_constraints: Number of constraints
        wizards: An array of wizard names, in no particular order
        constraints: A 2D-array of constraints,
                     where constraints[0] may take the form ['A', 'B', 'C']

    Output:
        An array of wizard names in the ordering your algorithm returns
    """
    Base.base = num_wizards

    # create constraints
    possible_constraints = [None] * (num_wizards**3)
    for i in range(len(possible_constraints)):
        d1, d2, d3 = Base.convert_to_base(i)
        if d1 != d2 and d1 != d3 and d2 != d3:
            possible_constraints[i] = Base(i)

    # eliminate constraints
    wizard_to_num = {}
    num_to_wizard = {}
    for i in range(len(wizards)):
        wizard_to_num[wizards[i]] = i
        num_to_wizard[i] = wizards[i]
    for c in constraints:
        w1 = wizard_to_num[c[0]]
        w2 = wizard_to_num[c[1]]
        w3 = wizard_to_num[c[2]]
        possible_constraints[Base.convert_from_base(w1, w3, w2)] = None
        possible_constraints[Base.convert_from_base(w2, w3, w1)] = None

    foo = [possible_constraints[:] for _ in range(NUM_EXECUTIONS)]
    for p_c in foo:
        arbitrarily_filter(p_c)
    arbitrarily_filter(possible_constraints, False)

    bar = [[elem for elem in p_c if elem is not None] for p_c in foo]
    remaining_constraints = [elem for elem in possible_constraints if elem is not None]

    foofoo = [construct_order(r_c, num_wizards, num_to_wizard) for r_c in bar]
    order = construct_order(remaining_constraints, num_wizards, num_to_wizard)
    foofoo.append(order)

##########################
    # foobar = [adjust_failed_constraints(o) for o in foofoo]

    try:
        foobar = [0] * len(foofoo)
        for i in range(len(foobar)):
            foobar[i] = adjust_failed_constraints(foofoo[i])
    except KeyboardInterrupt:
        if os.path.isfile(output_global):
            prev_satisfied = processInput(input_global, output_global)[0]
            if prev_satisfied > max(foobar):
                return
        result = foofoo[foobar.index(max(foobar))]
        print(result)
        return result

##########################
    if os.path.isfile(output_global):
        prev_satisfied = processInput(input_global, output_global)[0]
        if prev_satisfied > max(foobar):
            return


    result = foofoo[foobar.index(max(foobar))]
    print(result)
    return result

"""
======================================================================
   No need to change any code below this line
======================================================================
"""

def read_input(filename):
    with open(filename) as f:
        num_wizards = int(f.readline())
        # f.readline() # throw away answer line for personal tests
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
    #################
    global input_global
    input_global = args.input_file
    global output_global
    output_global = args.output_file
    #################
    num_wizards, num_constraints, wizards, constraints = read_input(args.input_file)
    solution = solve(num_wizards, num_constraints, wizards, constraints)
    if isinstance(solution, list):
        write_output(args.output_file, solution)
