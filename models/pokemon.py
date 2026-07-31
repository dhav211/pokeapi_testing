from pydantic import BaseModel
from models.ability import Ability

class Pokemon(BaseModel):
  id: int
  name: str
  height: int
  weight: int
  abilities: list[Ability]