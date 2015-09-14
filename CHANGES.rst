Space Changelog
===============

:version: 1.0
:date: 2015-09-14
:summary: The basic goal of this release is to reach a relatively stable state
          with respect to the game model code, save file format, a basic yet
          more or less complete command line interface and the way that the
          various pieces are glued together.

- include electricity in str representation of planets
- fix bug in planet.build so buildings upgrade properly (it was adding multiple
  level 1 instances instead of upgrading the existing instance)
- include interpreter state in save file: now saves current_object setting
- added model query mixin to keep this type of code in one place, and
  accompanying unit tests
- document command line interface in README
- move logic for changing engine state from the front end into the engine
- remove the gamestate model object, not necessary
- commands: extract common command code into a base class and unit test
- fix Trello link in README
- Remove ditz content and move back to Trello for planning/issue tracking
- add/unittest user command
- add/unittest build command
- add/unittest list command
- add/unittest cd command
- add/unittest debug command

----

:version: 0.2
:date: 2015-05-29

- bugfix: state methods should call getstate/setstate dunder methods recursively
- bugfix: test that getstate only returns primitive objects
- bugfix: factory methods or better constructors for restoring state
- bugfix: planet: add buildings and research to state
- bugfix: planet: convert buildings dict into a list
- add json/yaml engine so save state can be human readable
- command for accessing game internals via the interpreter
- command line option for using PDB to investigate failures
- use generator comprehensions where possible

----

:version: 0.1
:date: 2015-05-06

- bugfix: building: add sun callback to solar power plant state
- bugfix: building: comparison tests make wrong assumption about value
- bugfix: lib.util needs to be abolished
- bugfix: remove show methods from object models
- run pep8/pyflakes on all files as part of tests
- common tests for model objects
- Coord model missing tests
- Resources missing tests
- Building missing tests
- System missing tests
- User missing tests
- Planet missing tests
- Galaxy missing tests
- lib.error missing tests
- UI module missing tests
- Interpreter module missing tests
- space main script missing tests
- resources: missing trade_value calculation tests
- replace 3rd party mock with unittest.mock
- use nosetests for running tests
- Gamestate missing tests
- format_object missing tests
- Engine missing tests
