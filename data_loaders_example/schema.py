import strawberry
import typing
from typing import List, Union
from strawberry.dataloader import DataLoader
import asyncio

@strawberry.type
class Planet:
    name: str = strawberry.field(description="The name of the planet")
    neighbours: typing.List[str] = strawberry.field(description="The neighbours of the planet")

planets_database = {
        1: Planet(
            name='Mercury',
            neighbours=['Venus'],
        ),
        2: Planet(
            name='Venus',
            neighbours=['Mercury','Earth'],
        ),
        3: Planet(
            name='Earth',
            neighbours=['Venus', 'Mars'],
        ),
        4: Planet(
            name='Mars',
            neighbours=['Earth', 'Jupiter'],
        ),
        5: Planet(
            name='Jupiter',
            neighbours=['Mars', 'Saturn'],
        ),
        6: Planet(
            name='Saturn',
            neighbours=['Jupiter', 'Uranus'],
        ),
        7: Planet(
            name='Uranus',
            neighbours=['Saturn', 'Neptune'],
        ),
        8: Planet(
            name='Neptune',
            neighbours=['Uranus'],
        )
}

async def load_planets(keys: List[int]) -> List[Union[Planet, ValueError]]:
    def lookup(key: int) -> Union[Planet, ValueError]:
       planet = planets_database.get(key)
       if planet:
           return planet
 
       return ValueError("not found")

    return [lookup(key) for key in keys]

loader = DataLoader(load_fn=load_planets)

@strawberry.type
class Query:
    @strawberry.field
    async def get_planet(self, id: int) -> Planet:
        return await loader.load(id)
    
    @strawberry.field
    async def get_planets(self, ids: typing.List[int]) -> typing.List[Planet]:
        return await loader.load_many(ids)
    
    @strawberry.field
    async def get_default_planet(self) -> Planet:
        return await loader.load(1)
    
    @strawberry.field
    async def get_default_planets(self) -> List[Planet]:
        [planet_a, planet_b] = await asyncio.gather(loader.load(1), loader.load(2))
        return [planet_a, planet_b]
    
    @strawberry.field
    async def get_many_planets(self) -> List[Planet]:
        [planet_a, planet_b, planet_c] = await loader.load_many([1, 2, 3])
        return [planet_a, planet_b, planet_c]

schema = strawberry.Schema(query=Query)
