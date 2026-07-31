import pytest
import requests
from models.pokemon import Pokemon
from models.ability import Ability, AbilityDetail

def test_get_pikachu(pikachu):
  expected = Pokemon(
    id=25, 
    name="pikachu", 
    height=4, 
    weight=60,
    abilities=[
      Ability(
        ability=AbilityDetail(name="static", url="https://pokeapi.co/api/v2/ability/9/"),
        is_hidden= False,
        slot=1
      ),
      Ability(
        ability=AbilityDetail(name="lightning-rod", url="https://pokeapi.co/api/v2/ability/31/"),
        is_hidden= True,
        slot=3
      )
    ]
  )

  assert pikachu == expected

def test_get_pikachu_ability_names(pikachu, capsys):
  expected_abilities = ["lightning-rod", "static"]
  actual_abilities = [ability.ability.name for ability in pikachu.abilities]

  assert sorted(expected_abilities) == sorted(actual_abilities)
