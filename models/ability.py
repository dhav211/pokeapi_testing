from pydantic import BaseModel


class AbilityDetail(BaseModel):
  name: str
  url: str

class Ability(BaseModel):
  is_hidden: bool
  slot: int
  ability: AbilityDetail
