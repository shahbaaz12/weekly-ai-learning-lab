# Structured Outputs

## Objective

Learn how to ask a model for data that follows a fixed Pydantic schema instead of an unstructured text response.

## What this project builds

`_1_pydantic_output.py` requests Pokemon data in two forms:

1. A single validated `Pokemon` object.
2. A nested `PokeDex` object containing a list of `Pokemon` entries.

The reusable `Pokemon` schema and `PokemonCardPrinter` helper live in `pokemon_helpers.py`.

## Run

Run these commands from this folder:

```powershell
uv sync
uv run python _1_pydantic_output.py
```

## Key idea

`model.with_structured_output(Pokemon)` asks the model to return data matching the `Pokemon` schema. Pydantic validates the returned data and lets the program access fields with attributes such as `pokemon.name`.

This project uses Gemini and requires `GOOGLE_API_KEY` in the repository-root `.env` file.
