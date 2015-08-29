Space
=====

:author: Curtis Sand
:date: 2015

Concept:
    A game where each player strives to manage a growing empire of planets and
    to conquer all other empires.

The project was started as a side project after a number of years of thinking
about the concept. The concept may not be especially new but some of the design
ideas were chosen due to frustrations found in similar games.

Command Line Interface
----------------------

:added: v1.0 dev

*Under Construction*

The user is the ruler of an empire of planets. He/She needs to be able to
manage the development of each planet while also performing exploratory and
military type space activities too.

To minimize the amount of typing most commands will use a "currently focused
object" concept. Each planet and ship squadron will be a focus-able object. To
leverage a familiar command concept the linux ``cd`` and ``ls`` commands will
be used in a similar manner.

*Command List:*

:debug: access to debugging tools and game internals

:quit: save and exit the game

    - aliases: EOF (C-D), exit, q

:ls [OBJECT]: list focus-able entitites like planets or squadrons

    - aliases: list, show, sh

    - With no arguments, print details of focussed object.
      With object identifier argument, print details of identefied object.
      With "-a|--available", print a list of objects that could be focussed on
      using the "cd" commmand.

:cd OBJECT: change focussed object

    - aliases: focus

:user: access to the user's profile and statistics

:build: direct construction activities

*Planned Future Commands:*

:shipyard: direct shipyard activities

:research: direct research activities

Development
-----------

The main repository is hosted on Github while a public mirror is maintained at
Bitbucket.

- https://github.com/fretboardfreak/space
- https://bitbucket.org/fret/space

The code is predominantly written in python 3 and the python PEP8
recommendation is followed to help ensure clean readable style.

For planning and issue tracking I am trying out the `PyDitz`_ project, which is
a python fork of the original Ditz project.

Note:

    For installing pyditz I've cloned the mercurial repository and have been
    using 0.9 in-development version.  To do this I cloned the repo, installed
    the pre-requisites (now included in Space's ``dev-requirements.txt`` file),
    and installed ditz with "python setup.py install".  At the time of this
    writing you can also get pyditz by installing version 0.8 from `PyPi`_.

.. _PyDitz: https://bitbucket.org/zondo/pyditz
.. _PyPI: https://pypi.python.org

Note:

    Releases v0.1 and v0.2 were created before the project migrated to ditz.
    As such the content in the ``CHANGES`` change-log file and export content
    from pyditz may appear different than later releases.

Versioning
^^^^^^^^^^

Early development will use numbers less than 1.0. Above 1.0 the whole number or
major version will be incremented for save file incompatible changes and the
decimal number or minor version will be incremented when something new happens.

The definition of "when something new happens" is intentionally left ambiguous
until there is a better idea of what the minor number changes actually mean.

The version number will be monotonically increasing and the format used will be
the same as interpreted by ``ls -v`` or by distutils' ``LooseVersion`` class.

Coding Style
^^^^^^^^^^^^

In general I try to follow PEP 8. A good rule of thumb is to ensure your changes
pass all tests performed by the ``pep8`` and ``pyflakes`` tools. They can be
installed using ``pip install -r dev-requirements.txt`` from the top level
directory of this repository.

Some non-obvious conventions that I also like to use are:

- ``repr`` strings should have the format "classname(details)" where the details
  is the repr representation of the relevant data contained in the class.

- ``repr`` strings do not contain newlines.

- ``str`` strings should be a multiline block of text - including a user facing
  classname if it makes sense.

- Anything that needs to be saved between sessions needs to implement
  ``__getstate__`` and ``__setstate__``. Although not explicitly required for
  pickle, enforcing the implementation now might make switching to a SQL
  database more straight forward later. The object states should be a tuple of
  primitive types.

Tests
^^^^^

Test code lives under the ``tests/`` directory in the top level of the
repository. The packages listed in the dev-requirements.txt file are required
for the tests to work correctly.

In general tests should try to use actual code where possible to ensure changes
meet interface expectations that dependent code might have.
