=============
santa-helpers
=============


.. image:: https://img.shields.io/pypi/v/santa_helpers.svg
        :target: https://pypi.python.org/pypi/santa_helpers

.. image:: https://img.shields.io/travis/lenarother/santa_helpers.svg
        :target: https://travis-ci.com/lenarother/santa_helpers

.. image:: https://readthedocs.org/projects/santa-helpers/badge/?version=latest
        :target: https://santa-helpers.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/lenarother/santa_helpers/shield.svg
     :target: https://pyup.io/repos/github/lenarother/santa_helpers/
     :alt: Updates



Helpers for Advent of Codee


* Free software: MIT license
* Documentation: https://santa-helpers.readthedocs.io.


Features
--------

* Calculate manhattan distance

    .. code-block:: python

        >>> distances.manhattan((-3, 1), (0, 0))

        4

* Generate neighbors

    .. code-block:: python

        >>> list(neighbors.neighbors((1, 1)))

        [(1, 0), (0, 1), (2, 1), (1, 2)]

        >>> list(neighbors.neighbors((1, 1), 8))

        [
            (0, 0),
            (1, 0),
            (2, 0),
            (0, 1),
            (2, 1),
            (0, 2),
            (1, 2),
            (2, 2)
        ]

        >>> list(neighbors.neighbors((1, 1), p_min=(1, 1)))

        [(2, 1), (1, 2)]

* Generate points in path

    .. code-block:: python

        >>> list(paths.path_points((0, 0), 'R2'))

        [(1, 0), (2, 0)]


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
