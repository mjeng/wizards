import argparse
from random import shuffle
from random import randint
NUM_ORDERS = int(input("How many orders in order_array? "))
P = False
"""
======================================================================
  Complete the following function.
======================================================================
"""
class WizardOrder:
    constraints = None
    num_wizards = None

    def __init__(self, order):
        self.order = order
        self.find_num_constraints_satisfied()
        ####################################
        # TODO: may remove this line for runtime purposes
        assert set(self.order) == set([i for i in range(num_wizards)]), "WizardOrder instance has invalid self.order"
        ####################################

    def find_num_constraints_satisfied(self):
        ordering_map = {k: v for v, k in enumerate(self.order)}
        constraints_satisfied = 0
        for c in WizardOrder.constraints:
            wiz_a = ordering_map[c[0]]
            wiz_b = ordering_map[c[1]]
            wiz_mid = ordering_map[c[2]]
            if not ((wiz_a < wiz_mid < wiz_b) or (wiz_b < wiz_mid < wiz_a)):
                 constraints_satisfied += 1
        self.constraints_satisfied = constraints_satisfied
        return constraints_satisfied

    def __lt__(self, other):
        return self.constraints_satisfied > other.constraints_satisfied
    def __eq__(self, other):
        return self.constraints_satisfied == other.constraints_satisfied
    def __gt__(self, other):
        return self.constraints_satisfied < self.constraints_satisfied


def execute_optimization(order_array):

    def swap_random2(wizorder):
        order = wizorder.order[:]
        a = randint(0, len(order) - 1)
        b = randint(0, len(order) - 1)
        while b == a:                   # makes sure b != a
            b = randint(0, len(order) - 1)
        order[a], order[b] = order[b], order[a]
        return WizardOrder(order)

    def swap_random3(wizorder):
        order = wizorder.order[:]
        a = randint(0, len(order) - 1)
        b = randint(0, len(order) - 1)
        while b == a:                   # makes sure b != a
            b = randint(0, len(order) - 1)
        ############################
        c = randint(0, len(order) - 1)
        while c == b or c == a:
            c = randint(0, len(order) - 1)
        order[a], order[b], order[c] = order[c], order[a], order[b]
        #############################
        return WizardOrder(order)


    ###################################
    # TODO: adjust these accordingly
    MARGIN = 0
    MAX_NUM_LOOPS = float('inf')
    # WHEN_SWITCH_THREE = 2000000
    WHEN_SWITCH_THREE = 500
    ###################################
    announced = False
    num_loops = 0
    repeated = 0
    repeated_comparator = order_array[0].constraints_satisfied
    try:
        while order_array[0].constraints_satisfied < num_constraints - MARGIN and num_loops < MAX_NUM_LOOPS:
            order_array = order_array[:NUM_ORDERS//2]
            order_array.extend([swap_random2(wo) for wo in order_array]) if repeated < WHEN_SWITCH_THREE else order_array.extend([swap_random3(wo) for wo in order_array])
            if repeated >= WHEN_SWITCH_THREE and not announced:
                print('switched to three')
                announced = True
            if repeated < WHEN_SWITCH_THREE:
                announced = False
            assert len(order_array) == NUM_ORDERS, "order_array was not restored to NUM_ORDERS number of orderings"
            order_array = sorted(order_array)
            print([wo.constraints_satisfied for wo in order_array]) if P else None
            if num_loops % 50 == 0:
                print(order_array[0].constraints_satisfied, num_loops)
            num_loops += 1
            print("looped " + str(num_loops) + " times") if P else None

            if order_array[0].constraints_satisfied == repeated_comparator:
                repeated += 1
            else:
                repeated_comparator = order_array[0].constraints_satisfied
                repeated = 0
    except KeyboardInterrupt:
        print([wo.constraints_satisfied for wo in order_array])
        num = int(input("Number of orders to test: "))
        order_array = order_array[:num]
        for wo in order_array:
            for i in range(num_wizards):
                for j in range(i + 1, num_wizards):
                    old_constraints_satisfied = wo.constraints_satisfied
                    print("old: " + str(old_constraints_satisfied)) if P else None
                    wo.order[i], wo.order[j] = wo.order[j], wo.order[i]
                    if wo.find_num_constraints_satisfied() == num_constraints:
                        break
                    print("new: " + str(wo.constraints_satisfied)) if P else None
                    if wo.constraints_satisfied > old_constraints_satisfied and len(order_array) < 2 * num:
                        print("Beneficial but not perfect swap")
                        order_array.append(WizardOrder(wo.order[:]))
                    wo.order[i], wo.order[j] = wo.order[j], wo.order[i]
                    wo.find_num_constraints_satisfied()
        if order_array[0].constraints_satisfied != num_constraints:
            print("onto three swaps")
            for wo in order_array:
                for i in range(num_wizards):
                    for j in range(i + 1, num_wizards):
                        for k in range(j + 1, num_wizards):
                            old_constraints_satisfied = wo.constraints_satisfied
                            wo.order[i], wo.order[j], wo.order[k] = wo.order[k], wo.order[i], wo.order[j]
                            if wo.find_num_constraints_satisfied() == num_constraints:
                                break
                            if wo.constraints_satisfied > old_constraints_satisfied and len(order_array) < 3 * num:
                                print("Beneficial but not perfect swap")
                                order_array.append(WizardOrder(wo.order[:]))
                            wo.order[i], wo.order[j], wo.order[k] = wo.order[k], wo.order[i], wo.order[j]
                            if wo.find_num_constraints_satisfied() == num_constraints:
                                break
                            if wo.constraints_satisfied > old_constraints_satisfied and len(order_array) < 3 * num:
                                print("Beneficial but not perfect swap")
                                order_array.append(WizardOrder(wo.order[:]))
                            wo.order[i], wo.order[j], wo.order[k] = wo.order[k], wo.order[i], wo.order[j]
                            wo.find_num_constraints_satisfied()
        order_array = sorted(order_array)


    if num_loops == MAX_NUM_LOOPS:
        print("exited because passed MAX_NUM_LOOPS")

    return order_array[0]

# def eliminate_margin(wizorder):



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
    # SETUP
    wizard_to_num = {}
    num_to_wizard = {}
    for i in range(len(wizards)):
        wizard_to_num[wizards[i]] = i
        num_to_wizard[i] = wizards[i]
    renamed_constraints = [[wizard_to_num[w] for w in c] for c in constraints]
    WizardOrder.constraints = renamed_constraints
    WizardOrder.num_wizards = num_wizards

    order = [i for i in range(num_wizards)]
    order_array = []
    for _ in range(NUM_ORDERS):
        order_array.append(WizardOrder(order))
        shuffle(order)

    optimized_to_margin_WO = execute_optimization(order_array)

    print("constraints failed: " + str(num_constraints - optimized_to_margin_WO.constraints_satisfied))

    # target = optimized_to_margin_WO[0]
    # for i in range(num_wizards):
    #     for j in range(i + 1, num_wizards):

    return [num_to_wizard[num] for num in optimized_to_margin_WO.order]

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
