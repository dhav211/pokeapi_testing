import pytest
import requests

def test_check_content_type_is_json(working_pokemon_names):
  r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{working_pokemon_names}")
  assert "application/json" in r.headers["Content-Type"]

def test_crosspoint_consistency(working_pokemon):
  for t in working_pokemon.get("types"):
    r = requests.get(t.get("type").get("url"))
    pokemon = r.json()["pokemon"]

    assert len([p for p in pokemon if working_pokemon["name"] == p["pokemon"]["name"]]) == 1