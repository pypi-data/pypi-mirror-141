from typing import Tuple

RELATIVE_DIRECTIONS = {
    'U': (0, 1),
    'D': (0, -1),
    'L': (-1, 0),
    'R': (1, 0),
}

GEOGRAPHICAL_DIRECTIONS = {
    'N': (0, 1),
    'S': (0, -1),
    'W': (-1, 0),
    'E': (1, 0),
}


def get_direction(ch: str) -> Tuple[int, int]:
    """Coordinates point for direction

    Args:
        ch: str - direction as a single letter UDLR or NEWS

    Returns:
        tuple (x, y) - direction coordinates.
        E.g.:
            N -> (0, 1)  # north
            S -> (0, -1)  # south
            L -> (-1, 0)  # left

    Raises KeyError:
        if direction char not in allowed directions.
    """
    try:
        return (
            RELATIVE_DIRECTIONS.get(ch, None) or
            GEOGRAPHICAL_DIRECTIONS[ch]
        )
    except KeyError:
        raise KeyError(
            f'No such direction {ch}. Available directions: NSWE and UDLR'
        )


def get_target_point(start: Tuple[int, int], steps: str) -> Tuple[int, int]:
    """Coordinates of target point based on start point and steps.

    Args:
        start: tuple (x, y) - coordinates of the starting point.
        steps: string e.g U15 - contains direction (U D L R or N E S W)
            and number of steps.

    Directions - two direction systems are possible:
        Relative orientations:
            U - Up -> (0, 1)
            D - Down -> (0, -1)
            L - Left -> (-1, 0)
            R - Right -> (1, 0)

        Geographical directions:
            N - North -> (0, 1)
            E - East -> (1, 0)
            S - South -> (0, -1)
            W - West -> (-1, 0)

    Returns:
        tuple (x, y) - coordinates of the target point.
    """
    x, y = start
    ch, n = steps[0], int(steps[1:])
    dx, dy = get_direction(ch)
    return x + n * dx, y + n * dy


def path_points(start, steps):
    """Generate coordinates of each path point based on start point and steps.

    Args:
        start: tuple (x, y) - coordinates of the starting point.
        steps: string e.g U15 - contains direction (UDLR or NESW)
            and number of steps.

    Directions - two direction systems are possible:
        Relative orientations:
            U - Up -> (0, 1)
            D - Down -> (0, -1)
            L - Left -> (-1, 0)
            R - Right -> (1, 0)

        Geographical directions:
            N - North -> (0, 1)
            E - East -> (1, 0)
            S - South -> (0, -1)
            W - West -> (-1, 0)

    Yields:
        tuple (x, y) - point.
    """
    x, y = start
    ch, n = steps[0], int(steps[1:])
    dx, dy = get_direction(ch)
    tx, ty = x + n * dx, y + n * dy

    while not (x == tx and y == ty):
        x += dx
        y += dy
        yield x, y
