import unittest
import contextlib
from io import StringIO
import pathlib
import os

from parameterized import parameterized

from source.rover import Rover
from source.main import main


class MainTest(unittest.TestCase):
    def test_incorrect_path(self):
        with self.assertRaises(SystemExit):
            working_dir = pathlib.Path().absolute()
            test_file = os.path.join(working_dir, "fake_gfg.txt")

            temp_stdout = StringIO()
            with contextlib.redirect_stdout(temp_stdout):
                main([test_file])
            output = temp_stdout.getvalue().splitlines()
            self.assertEqual(
                output[0], "The path specified does not exist or " "is not a file"
            )

    def test_correct_output(self):
        working_dir = pathlib.Path().absolute()
        test_file = os.path.join(working_dir, "input.txt")
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            main([test_file])
        output = temp_stdout.getvalue().splitlines()
        self.assertEqual(output[0], "1 3 N")
        self.assertEqual(output[1], "5 1 E")


class RoverTest(unittest.TestCase):
    @parameterized.expand([("N", "W"), ("W", "S"), ("S", "E"), ("E", "N")])
    def test_turn_left(self, heading, expected_heading):
        rover = Rover(heading, (0, 0), (5, 5))
        rover = rover.rotate_left()
        self.assertEqual(rover.heading, expected_heading)

    @parameterized.expand([("N", "E"), ("E", "S"), ("S", "W"), ("W", "N")])
    def test_turn_right(self, heading, expected_heading):
        rover = Rover(heading, (0, 0), (5, 5))
        rover = rover.rotate_right()
        self.assertEqual(rover.heading, expected_heading)

    @parameterized.expand([("N", (3, 4)), ("E", (4, 3)), ("S", (3, 2)), ("W", (2, 3))])
    def test_move_forward(self, heading, expected_position):
        rover = Rover(heading, (3, 3), (5, 5))
        rover = rover.move()
        self.assertEqual(rover.position, expected_position)

    @parameterized.expand([("N", (0, 5)), ("E", (5, 3)), ("S", (3, 0)), ("W", (0, 5))])
    def test_move_out_of_bounds(self, heading, position):
        with self.assertRaises(ValueError):
            rover = Rover(heading, position, (5, 5))
            rover.go("M")
            x = 0

    @parameterized.expand(
        [
            ("L", "W", (0, 0)),
            ("R", "E", (0, 0)),
            ("M", "N", (0, 1)),
        ]
    )
    def test_do_commands(self, command, expected_heading, expected_position):
        rover = Rover("N", (0, 0), (5, 5))
        rover = rover.do_command(command)
        self.assertEqual(rover.position, expected_position)
        self.assertEqual(rover.heading, expected_heading)

    @parameterized.expand(["P", "Q", "T", "S"])
    def test_invalid_commands(self, invalid_command):
        with self.assertRaises(KeyError):
            rover = Rover("N", (0, 0), (5, 5))
            rover.do_command(invalid_command)

    @parameterized.expand(
        [
            ("N", (1, 2), ["L", "M", "L", "M", "L", "M", "L", "M", "M"], (1, 3), "N"),
            (
                "E",
                (3, 3),
                ["M", "M", "R", "M", "M", "R", "M", "R", "R", "M"],
                (5, 1),
                "E",
            ),
        ]
    )
    def test_go_with_instructions(
        self, heading, position, instruction, expected_position, expected_heading
    ):
        rover = Rover(heading, position, (5, 5))
        rover = rover.go(instruction)
        self.assertEqual(rover.position, expected_position)
        self.assertEqual(rover.heading, expected_heading)
