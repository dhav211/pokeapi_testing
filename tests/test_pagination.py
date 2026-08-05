from math import floor

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

def test_too_high_offset():
    r = requests.get("https://pokeapi.co/api/v2/pokemon?offset=9999999").json()
    assert len(r["results"]) == 0

@pytest.mark.parametrize("negative_offsets", [-2, -5, -10, -30, -50, -100, -1351])
def test_negative_limits(negative_offsets):
    """Negative offset will only work if the absolute value of the negative offset is at least one lower"""
    request_with_results = requests.get(f"https://pokeapi.co/api/v2/pokemon?offset={negative_offsets}&limit={abs(negative_offsets)-1}").json()
    request_without_results = requests.get(f"https://pokeapi.co/api/v2/pokemon?offset={negative_offsets}&limit={abs(negative_offsets)}").json()

    assert len(request_with_results["results"]) == abs(negative_offsets)-1
    assert len(request_without_results["results"]) == 0

@pytest.mark.parametrize("non_number", ["abc", "😀", "a5"])
def test_non_number_limits(non_number):
    r = requests.get(f"https://pokeapi.co/api/v2/pokemon?limit={non_number}")

    assert r.status_code == 200
    assert len(r.json()["results"]) == 20

@pytest.mark.parametrize("decimal", [1.5, 3.3, 9.6, 10.000000001, 9.999999999999999])
def test_decimal_limits(decimal):
    r = requests.get(f"https://pokeapi.co/api/v2/pokemon?limit={decimal}").json()
    assert len(r["results"]) == floor(decimal)

@pytest.mark.parametrize("number_letter", ["1a", "5a4", "14z55d22"])
def test_numbers_with_letters_limits(number_letter):
    extracted_number = []
    for c in number_letter:
        if c.isdigit():
            extracted_number.append(c)
        elif c.isalpha():
            break

    r = requests.get(f"https://pokeapi.co/api/v2/pokemon?limit={number_letter}").json()

    assert len(r["results"]) == int("".join(extracted_number))

def test_next_and_previous_urls():
    initial_url = "https://pokeapi.co/api/v2/pokemon?offset=40&limit=20"
    r = requests.get(initial_url).json()
    
    next_request = requests.get(r["next"])
    previous_request = requests.get(r["previous"])

    assert next_request.status_code == 200
    assert previous_request.status_code == 200
    assert next_request.json()["previous"] == previous_request.json()["next"]
    assert next_request.json()["previous"] == initial_url
    assert previous_request.json()["next"] == initial_url
