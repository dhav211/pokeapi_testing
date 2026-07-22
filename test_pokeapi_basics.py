import pytest
import requests

@pytest.fixture()
def pikachu():
  """Get pikachu from the api and convert into a json"""
  r = requests.get("https://pokeapi.co/api/v2/pokemon/pikachu")
  return r.json()

def test_ok_status():
  r = requests.get("https://pokeapi.co/api/v2/pokemon/ditto")
  assert r.status_code == 200

def test_not_real_pokemon_status():
  r = requests.get("https://pokeapi.co/api/v2/pokemon/dibbo")
  assert r.status_code == 404
  """
  Fetch a Pokémon and check the response has the expected keys (name, id, height, weight, types, abilities, stats) 
  and that they're the right types (e.g. id is an int, name is a string, types is a list). 
  This is where you'd learn about JSON schema validation.
  """
def test_get_pikachu(pikachu):
  assert pikachu["name"] == "pikachu"