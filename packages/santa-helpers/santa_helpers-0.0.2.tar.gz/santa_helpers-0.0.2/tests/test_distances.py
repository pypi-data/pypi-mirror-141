import pytest

from santa_helpers.distances import manhattan


@pytest.mark.parametrize(
    'p1,p2,expected',
    (
        ((0, 0), (0, 0), 0),
        ((1, 1), (1, 1), 0),
        ((3, 2), (0, 0), 5),
        ((-3, -2), (0, 0), 5),
    )
)
def test_manhattan(p1, p2, expected):
    assert manhattan(p1, p2) == expected
