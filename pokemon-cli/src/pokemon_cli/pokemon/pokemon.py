"""
This module contains
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Self

from pydantic import BaseModel, Field

from .. import path
from .types import Type

_POKEDEX_DIR = path.APPDATA / "pokedex"


@dataclass
class BaseStats(object):
    """Base stats of a Pokemon."""

    hp: int
    attack: int
    defense: int
    special_attack: int
    special_defense: int
    speed: int

    @property
    def total(self) -> int:
        return (
            self.hp
            + self.attack
            + self.defense
            + self.special_attack
            + self.special_defense
            + self.speed
        )

    def __str__(self) -> str:
        return (
            f"HP: {self.hp}, "
            f"Atk: {self.attack}, "
            f"Def: {self.defense}, "
            f"SpA: {self.special_attack}, "
            f"SpD: {self.special_defense}, "
            f"Spe: {self.speed} "
            f"(Total: {self.total})"
        )


class Pokemon(BaseModel):
    """A Pokemon."""

    pokedex_id: int
    name: str
    type_: list[Type] = Field(alias="type", min_length=1, max_length=2)
    level: int = 5
    base_stats: BaseStats

    @classmethod
    def load_json(cls, filepath: Path) -> Self:
        with open(filepath, "r") as file:
            return cls.model_validate_json(file.read())

    def __str__(self) -> str:
        return (
            f"{self.pokedex_id:0>4} {self.name} "
            f"({', '.join(self.type_).title()}) "
            f"| {self.base_stats}"
        )


class Pokedex(object):
    """Class used to access Pokemon."""

    _pokedex_id: dict[int, Pokemon] = {}
    _pokedex_name: dict[str, Pokemon] = {}

    def __init__(self) -> None:
        for file in _POKEDEX_DIR.iterdir():
            pokemon = Pokemon.load_json(file)
            self._pokedex_id[pokemon.pokedex_id] = pokemon
            self._pokedex_name[pokemon.name.lower()] = pokemon

    def get_pokemon(self, name_or_id: str | int) -> Pokemon:
        if isinstance(name_or_id, str):
            try:
                pokemon = self._pokedex_name[name_or_id.lower()]
            except KeyError:
                msg = f"Pokemon '{name_or_id}' not found in Pokedex."
                raise KeyError(msg)
        else:
            try:
                pokemon = self._pokedex_id[name_or_id]
            except KeyError:
                msg = f"Pokemon with ID '{name_or_id}' not found in Pokedex."
                raise KeyError(msg)
        return pokemon.model_copy(deep=True)
