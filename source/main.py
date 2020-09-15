import argparse
import os
import sys
import itertools

from source.rover import Rover


def parse_plateau(plateau):
    c_plateau = tuple(map(int, plateau.split()))
    return c_plateau


def parse_position(position):
    position_split = position.split()
    x = int(position_split[0])
    y = int(position_split[1])
    heading = position_split[2]

    return (x, y), heading


def parse_instructions(instructions):
    return list(instructions.strip())


def main(args):
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("path", help="path of file")
    args = parser.parse_args(args)

    file = args.path
    if not os.path.isfile(file):
        print("The path specified does not exist or is not a file")
        sys.exit()

    with open(file, "r") as reader:
        plateau = parse_plateau(reader.readline())
        for line1, line2 in itertools.zip_longest(*[reader] * 2):
            position, heading = parse_position(line1)
            instructions = parse_instructions(line2)
            rover = Rover(heading=heading, position=position, plateau=plateau)
            rover = rover.go(instructions)
            print(f"{rover.position[0]} {rover.position[1]} {rover.heading}")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
