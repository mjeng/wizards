# wizards
Ever not want to sit in between two people because you know they'll talk around you? Well this NP-Complete algorithm solver can (usually) solve a very exaggerated version of this problem - given a line of N people, and any number of requests from any of these N people to not be between two other people, this algorithm will output a sequence of those N people that, as best it can, satisfies those constraints.
There are a few different implementations/attempts to solve this NP-Complete problem. The first algorithm uses a randomizer combined with a function that eliminates as many possible orderings as possible, then reconstructs an ordering from remaining possible orderings.
The second algorithm uses a 3SAT solver called pycosat to solve the problem.
Both methods encode constraints into number representations (a class called Base) to save runtime and space.
