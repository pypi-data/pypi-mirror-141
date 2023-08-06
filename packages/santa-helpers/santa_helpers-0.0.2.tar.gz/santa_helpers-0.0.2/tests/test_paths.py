import pytest

from santa_helpers.paths import (
    get_direction,
    get_target_point,
    path_points,
)


@pytest.mark.parametrize(
    'ch,expected',
    (
        ('N', (0, 1)),
        ('S', (0, -1)),
        ('W', (-1, 0)),
        ('E', (1, 0)),
        ('U', (0, 1)),
        ('D', (0, -1)),
        ('L', (-1, 0)),
        ('R', (1, 0)),
    )
)
def test_get_direction(ch, expected):
    assert get_direction(ch) == expected


@pytest.mark.parametrize(
    'ch,exc',
    (
        ('X', KeyError),
        ('NE', KeyError),
        ('', KeyError),
    )
)
def test_get_direction_error(ch, exc):
    with pytest.raises(exc):
        assert get_direction(ch)


@pytest.mark.parametrize(
    'start,direction,target',
    (
        ((0, 0), 'L1', (-1, 0)),
        ((0, 0), 'L15', (-15, 0)),
        ((-15, 0), 'R15', (0, 0)),
        ((1, 1), 'U3', (1, 4)),
    )
)
def test_get_target_point(start, direction, target):
    assert get_target_point(start, direction) == target


@pytest.mark.parametrize(
    'start,direction,expected',
    (
        ((0, 0), 'L1', [(-1, 0)]),
        ((0, 0), 'L2', [(-1, 0), (-2, 0)]),
        ((0, 0), 'L3', [(-1, 0), (-2, 0), (-3, 0)]),
        ((3, 7), 'D2', [(3, 6), (3, 5)]),
    )
)
def test_path_points_generator(start, direction, expected):
    assert list(path_points(start, direction)) == expected
