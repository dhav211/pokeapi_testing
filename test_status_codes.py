import pytest
import requests

@pytest.mark.parametrize("working_pokemon", ["ditto", "pikachu", "appletun", "torkoal"])
def test_ok_status(working_pokemon):
  r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{working_pokemon}")
  assert r.status_code == 200

def test_not_real_pokemon_status():
  r = requests.get("https://pokeapi.co/api/v2/pokemon/dibbo")
  assert r.status_code == 404

@pytest.mark.parametrize("case_sensitive_pokemon", ["Pikachu", "PiKacHU", "PIKACHU"])
def test_case_insensitivity(case_insensitive_pokemon):
  r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{case_insensitive_pokemon}")
  assert r.status_code == 200

@pytest.mark.parametrize("edge_case", ["0", "-32", "9999999999999999999999"])
def test_get_404_from_edges(edge_case):
  r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{edge_case}")

  assert r.status_code == 404

def test_get_nested_species_url(pikachu):
  r = requests.get(pikachu["species"]["url"])

  assert r.status_code == 200