from pydantic import BaseModel

class Ability(BaseModel):
  is_hidden: bool
  slot: int
  ability: AbilityDetail

class AbilityDetail(BaseModel):
  name: str
  url: str