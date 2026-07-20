from pydantic import BaseModel, Field


class Pokemon(BaseModel):
    name: str = Field(description="Pokemon name")
    primary_type: str = Field(
        description="The primary type of the Pokemon",
        examples=["grass", "fire", "water", "normal", "electric"],
    )
    evolutions: str = Field(description="All evolution forms")


class PokemonCardPrinter:
    @staticmethod
    def print_card(pokemon: Pokemon) -> None:
        print("-----------")
        print(f"Name: {pokemon.name}")
        print(f"Type: {pokemon.primary_type}")
        print(f"Evolutions: {pokemon.evolutions}")
        print("-----------")
