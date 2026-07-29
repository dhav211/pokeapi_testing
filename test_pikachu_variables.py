import pytest
import requests

def test_get_pikachu(pikachu):
  actual = {
    "name": pikachu["name"],
    "id": pikachu["id"],
    "height": pikachu["height"],
    "weight": pikachu["weight"],
  }

  expected = {
    "name": "pikachu",
    "id": 25,
    "height": 4,
    "weight": 60
  }

  assert actual == expected

def test_get_pikachu_ability_names(pikachu):
  expected_abilities = ["lightning-rod", "static"]
  actual_abilities = [ability["ability"]["name"] for ability in pikachu["abilities"]]

  assert sorted(expected_abilities) == sorted(actual_abilities)

def test_get_pikachu_data_types(pikachu):
  assert isinstance(pikachu["name"], str)
  assert isinstance(pikachu["base_experience"], int)
  assert isinstance(pikachu["abilities"], list)
