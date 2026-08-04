import pytest
import requests

from models.pokemon import Pokemon


def test_default_pagination_behavior():
  r = requests.get("https://pokeapi.co/api/v2/pokemon/").json()
  assert r["count"] > 1100
  assert len(r["results"]) == 20
  assert r["previous"] is None
  assert r["next"] is not None

@pytest.mark.parametrize("limits", [1, 20, 1000])
def test_pagination_with_working_limits(limits):
    r = requests.get(f"https://pokeapi.co/api/v2/pokemon?limit={limits}").json()
    assert len(r["results"]) == limits

@pytest.mark.parametrize("limits", [-1, -50, -1351])
def test_pagination_with_negative_limits(limits):
    r = requests.get(f"https://pokeapi.co/api/v2/pokemon?limit={limits}").json()
    assert len(r["results"]) == r["count"] - abs(limits)

def test_for_no_limit_cap():
    r = requests.get("https://pokeapi.co/api/v2/pokemon?limit=9999").json()
    assert len(r["results"]) == r["count"]

def test_for_offset_correctness():
    page1 = requests.get("https://pokeapi.co/api/v2/pokemon?offset=0&limit=20").json()
    page2 = requests.get("https://pokeapi.co/api/v2/pokemon?offset=20&limit=20").json()

    last_pokemon_of_page1 = Pokemon.model_validate(requests.get(page1["results"][19]["url"]).json())
    first_pokemon_of_page2 = Pokemon.model_validate(requests.get(page2["results"][0]["url"]).json())

    assert first_pokemon_of_page2.id == last_pokemon_of_page1.id + 1

def test_last_page():
    r = requests.get("https://pokeapi.co/api/v2/pokemon").json()
    offset = r["count"] - 5
    limit = 20
    last_page = requests.get(f"https://pokeapi.co/api/v2/pokemon?offset={offset}&limit={limit}").json()
    
    assert len(last_page["results"]) < limit
    assert last_page["next"] is None