from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field

from pokemon_helpers import Pokemon, PokemonCardPrinter

load_dotenv()


# --- 1 Structured Output ---
model = init_chat_model("google_genai:gemini-3.1-flash-lite-preview")

structured_model = model.with_structured_output(Pokemon)
response = structured_model.invoke("Pokemon with the most evolutions")

PokemonCardPrinter.print_card(response)


# --- 2 Nested Structure
class PokeDex(BaseModel):
    pokemon: list[Pokemon] = Field(
        description="A list of Pokemon entries in the Pokedex."
    )


print("~~~ Structured Response ~~~")
structured_pokedex_model = model.with_structured_output(PokeDex)

response = structured_pokedex_model.invoke(
    "Return the first 3 starter Pokemon from Generation 1. "
)

print(" ----- POKEDEX ( Nested Structure ) -----")

for pokemon in response.pokemon:
    PokemonCardPrinter.print_card(pokemon)

print("----- ~ -----")
