from dataclasses import dataclass
from enum import Enum
from typing import Union, NamedTuple, List
from flask import Flask, request
from error import InvalidType, InvalidName

# SpaceCowboy models a cowboy in our super amazing system
@dataclass
class SpaceCowboy:
    name: str
    lassoLength: int

# SpaceAnimal models a single animal in our amazing system
@dataclass
class SpaceAnimal:
    # SpaceAnimalType is an enum of all possible space animals we may encounter
    class SpaceAnimalType(Enum):
        PIG = "pig"
        COW = "cow"
        FLYING_BURGER = "flying_burger"

    type: SpaceAnimalType

# SpaceEntity models an entity in the super amazing (ROUND UPPER 100) system
@dataclass
class SpaceEntity:
    class Location(NamedTuple):
        x: int
        y: int

    metadata: Union[SpaceCowboy, SpaceAnimal]
    location: Location

# ==== HTTP Endpoint Stubs ====
app = Flask(__name__)
space_database: List[SpaceEntity] = []

# the POST /entity endpoint adds an entity to your global space database
@app.route('/entity', methods=['POST'])
def create_entity():
    entities = request.get_json()['entities']
    for entity in entities:
        metadata = entity['metadata']
        coordinate = entity['location']
        if entity['type'] == 'space_cowboy':
            data = SpaceCowboy(metadata['name'], metadata['lassoLength'])
        elif entity['type'] == 'space_animal':
            data = SpaceAnimal(metadata['type'])
        else:
            raise InvalidType
        location = SpaceEntity.Location(coordinate['x'], coordinate['y'])
        space_database.append(SpaceEntity(data, location))
    return {}

# lasooable returns all the space animals a space cowboy can lasso given their name
@app.route('/lassoable', methods=['GET'])
def lassoable():
    name = request.get_json()['cowboy_name']


# DO NOT TOUCH ME, thanks :D
if __name__ == '__main__':
    app.run(debug=True, port=8080)