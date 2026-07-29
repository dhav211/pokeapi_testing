import pytest
import requests

@pytest.fixture(scope="session")
def pikachu():
  """Get pikachu from the api and convert into a json"""
  r = requests.get("https://pokeapi.co/api/v2/pokemon/pikachu")
  return r.json()

@pytest.fixture(scope="session", params=["ditto", "pikachu", "appletun", "torkoal"])
def working_pokemon_names(request):
  return request.param

@pytest.fixture(scope="session")
def working_pokemon(working_pokemon_names):
  return requests.get(f"https://pokeapi.co/api/v2/pokemon/{working_pokemon_names}").json()