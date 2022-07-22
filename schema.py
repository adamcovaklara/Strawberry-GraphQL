import typing
from typing import Union
import strawberry
import random
import datetime

@strawberry.type
class Periodic:
    orbital_period: float

@strawberry.type
class NonPeriodic:
    inclination: float

@strawberry.type
class NoOrbit:
    perihelion_distance: float

@strawberry.type
class Lost:
    discovery_date: datetime.date
    
@strawberry.interface
class Passerby:
    name: str

@strawberry.type
class Moon(Passerby):
    orbital_period: str = strawberry.field(description="The orbital_period of the moon")
    diameter: int = strawberry.field(description="The diameter of the moon")
    name: str = strawberry.field(description="The name of the moon")

@strawberry.type
class Asteroid(Passerby):
    size: int = strawberry.field(description="The size of the asteroid")
    speed: str = strawberry.field(description="The shape of the asteroid")
    name: str = strawberry.field(description="The name of the asteroid")

@strawberry.type
class Planet:
    name: str = strawberry.field(description="The name of the planet")
    neighbours: typing.List[str] = strawberry.field(description="The neighbours of the planet")

all_planets = [
        Planet(
            name='Mercury',
            neighbours=['Venus'],
        ),
        Planet(
            name='Venus',
            neighbours=['Mercury','Earth'],
        ),
        Planet(
            name='Earth',
            neighbours=['Venus', 'Mars'],
        ),
        Planet(
            name='Mars',
            neighbours=['Earth', 'Jupiter'],
        ),
        Planet(
            name='Jupiter',
            neighbours=['Mars', 'Saturn'],
        ),
        Planet(
            name='Saturn',
            neighbours=['Jupiter', 'Uranus'],
        ),
        Planet(
            name='Uranus',
            neighbours=['Saturn', 'Neptune'],
        ),
        Planet(
            name='Neptune',
            neighbours=['Uranus'],
        )
    ]
    
def get_planets():
    return all_planets

def get_passerby() -> Passerby:
    list = [1, 2, 3, 4, 5, 6]
    if random.choice(list) % 2 != 0:
        return Moon(orbital_period=27, diameter=3475, name="The Moon")
    return Asteroid(size=1, speed=76193, name="7482 (1994 PC1)")

@strawberry.type
class Query:
    planets: typing.List[Planet] = strawberry.field(resolver=get_planets, description="Get the names of the planets")
    passerby: Passerby = strawberry.field(resolver=get_passerby, description="Get the passerby")
    comet: Union[Periodic, NonPeriodic, NoOrbit, Lost]
    
    @strawberry.field
    def comet(self) -> Union[Periodic, NonPeriodic, NoOrbit, Lost]:
        list = [1, 2, 3, 4]
        choice = random.choice(list)
        if choice == 1:
            return Periodic(orbital_period=5.44)
        elif choice == 2:
            return NonPeriodic(inclination=60.6784)
        elif choice == 3:
            return NoOrbit(perihelion_distance=0.007)
        elif choice == 4:
            return Lost(discovery_date=datetime.date(1770, 6, 14))
                
    @strawberry.field
    def first_planet(self) -> Planet:
        return all_planets[0]
    
    @strawberry.field
    def last_planet(self) -> Planet:
        return all_planets[-1]
    
    @strawberry.field
    def planet(self, name: str) -> Planet:
        for item in all_planets:
            if item.name == name:
                return item
        return ValueError("not found")

@strawberry.input
class PlanetInput:
    name: str
    neighbours: typing.List[str]
  
@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_planet(self, planet: PlanetInput) -> Planet:
        all_planets.append(planet)
        return planet
        
    @strawberry.mutation
    def delete_planet(self, planet: PlanetInput) -> typing.List[Planet]:
        all_planets.remove(planet)
        return all_planets
    
    @strawberry.mutation
    def edit_neighbours(self, planet: PlanetInput) -> typing.List[Planet]:
        for item in all_planets:
            if item.name == planet.name:
                item.neighbours=planet.neighbours
        return all_planets

schema = strawberry.Schema(query=Query, mutation=Mutation, types=[Moon, Asteroid])
