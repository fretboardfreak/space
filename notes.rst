Design Notes
============

Database Schema
===============

The galaxy is represented by the database as a whole. *Items in italics are
future expansions to the game model.*

table SYSTEMS {
    - id : int
    - size : int
    - sun_brightness : int
    - coord : COORDS.id
    - last_update : datetime
}

table COORDS {
    - id : int
    - sector_x : int
    - sector_y : int
    - system_x : int
    - system_y : int
}

table PLANETS {
    - id : int
    - name : str
    - orbit : int
    - system : SYSTEMS.id
    - emperor : USERS.id
    - resources : RESOURCES.id
    - buildings : BUILDINGS.id
    - last_update : datetime
    - *type : str*
}

table USERS {
    - id : int
    - name : str
    - home_planet : PLANETS.id
    - last_update : datetime
}

table BUILDINGS {
    - id : int
    - type : str
    - level : int
    - under_construction : bool
    - *production_output : percentage*
}

table RESOURCES {
    - id : int
    - ore : int
    - metal : int
    - thorium : int
    - hydrocarbon : int
    - deuterium : int
}
