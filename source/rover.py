from dataclasses import dataclass, replace
from functools import reduce

compass = ["N", "E", "S", "W"]
vectors = [[0, 1], [1, 0], [0, -1], [-1, 0]]


@dataclass()
class Rover:
    """
    Mars rover class
    """

    heading: str
    position: (int, int)
    plateau: (int, int)

    def go(self, instructions):
        return reduce(
            lambda rover, instruction: rover.do_command(instruction), instructions, self
        )

    def do_command(self, instruction):
        """Execute single letter command:

        L/R - turn 90 degrees left/right
        M   - move one grid square in the current heading.
        """
        try:
            commands = {
                "L": lambda: self.rotate_left(),
                "R": lambda: self.rotate_right(),
                "M": lambda: self.move(),
            }
            return commands[instruction].__call__()
        except KeyError:
            raise KeyError(f"Unrecognized command '{instruction}'")

    def rotate_right(self):
        """ rotate rover 90 degees clockwise """
        current = compass.index(self.heading)
        return replace(self, heading=compass[(current + 1) % 4])

    def rotate_left(self):
        """ rotate rover 90 degees counter clockwise """
        reversed_compass = compass[::-1]
        current = reversed_compass.index(self.heading)
        return replace(self, heading=reversed_compass[(current + 1) % 4])

    def move(self):
        """ moves the rover 1 grid square along current heading."""
        vector = vectors[compass.index(self.heading)]
        x = self.position[0] + vector[0]
        y = self.position[1] + vector[1]
        self._check_move(x, self.plateau[0])
        self._check_move(y, self.plateau[1])
        return replace(self, position=(x, y))

    def _check_move(self, point, plateau):
        if point < 0 or point > plateau:
            raise ValueError("Rover cannot move out of bounds of plateau")
