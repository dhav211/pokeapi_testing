import pytest
import requests


def test_ok_status(working_pokemon_names):
  r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{working_pokemon_names}")
  assert r.status_code == 200

def test_api_requests_reasonable_speed(working_pokemon_names):
  r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{working_pokemon_names}")
  assert r.elapsed.seconds < 2.0

def test_not_real_pokemon_status():
  r = requests.get("https://pokeapi.co/api/v2/pokemon/dibbo")
  assert r.status_code == 404

@pytest.mark.parametrize("case_insensitive_pokemon", ["Pikachu", "PiKacHU", "PIKACHU"])
def test_case_insensitivity(case_insensitive_pokemon):
  r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{case_insensitive_pokemon}")
  assert r.status_code == 200

@pytest.mark.parametrize("edge_case", ["0", "-32", "9999999999999999999999", "p"])
def test_get_404_from_edges(edge_case):
  r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{edge_case}")
  assert r.status_code == 404

@pytest.mark.parametrize("sql_injection", ["' OR '1'='1", "1; DROP TABLE pokemon;--", "' UNION SELECT NULL--", "admin'--"])
def test_get_400_on_sql_injection(sql_injection):
  r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{sql_injection}")
  assert r.status_code == 400

def test_get_414_from_string_too_long():
  r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{"".join(["a" for i in range(0, 10000)])}")
  assert r.status_code == 414

def test_get_nested_species_url(working_pokemon_names):
  pokemon = requests.get(f"https://pokeapi.co/api/v2/pokemon/{working_pokemon_names}").json()
  inner_request = requests.get(pokemon["species"]["url"])
  assert inner_request.status_code == 200

@pytest.mark.parametrize("special_character", ["⚡", "%20", "!?", "%00"])
def test_get_404_from_special_characters(special_character):
  r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{special_character}")
  assert r.status_code == 400
