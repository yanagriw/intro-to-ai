# Planning Domain Definition Language
Domain definition for the following transportation problem using Planning Domain Definition Language [PDDL](https://en.wikipedia.org/wiki/Planning_Domain_Definition_Language).  
The domain definition file contains the following commands with arguments in the given order:
* *load(box car place)*: Load a box into a car, both located the given place.
* *unload(box car place)*: Unload a box from a car located a place.
* *move(car place_origin place_destination)*: Move a car from the original place to the destination.

# Transportation problem
A logistic company needs to create a plan for transporting goods packed in boxes by cars located in various places.
The initial and the goal positions are given in problem definition files. The capacity of every car is one box and boxes can be transported only by car.
