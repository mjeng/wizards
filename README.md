# NP-Complete algorithm solver
Given a line of N people, and a list of requests from any of these N people to not be between two other people in the line, this algorithm will output a sequence of those N people that, most of the time, satisfies those constraints.
There are a few different implementations/attempts to solve this NP-Complete problem. The first algorithm uses a randomizer combined with a function that eliminates as many possible orderings as possible, then reconstructs an ordering from remaining possible orderings.
The second algorithm uses a 3SAT solver called pycosat to solve the problem.
Both methods encode constraints into number representations (a class called Base) to save runtime and space.
The best solution tried so far, though not implemented here, is simulated annealing.
