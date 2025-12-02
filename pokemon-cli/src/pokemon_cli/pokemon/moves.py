"""
This module contains code for describing moves.
"""

from __future__ import annotations

from enum import StrEnum, auto
from pathlib import Path
from typing import Optional, Self

from pydantic import BaseModel, Field, TypeAdapter

from .. import path
from .types import Type

_MOVEDEX_PATH = path.APPDATA / "moves.json"


class Category(StrEnum):
    PHYSICAL = auto()
    SPECIAL = auto()
    STATUS = auto()


class Target(StrEnum):
    SELECTED = auto()
    SELF = auto()


class Move(BaseModel):
    name: str
    type_: Type = Field(alias="type")
    category: Category
    description: str
    max_pp: int = Field(gt=0)
    power: int = Field(gt=0)
    accuracy: Optional[int] = Field(gt=0, le=100)
    target: str = Target.SELECTED
    priority: int = 0
    drain: int = 0
    healing: int = 0
    flinch_chance: float = 0
    crit_rate: int = 0
    effect_chance: float = 0
    stat_chance: float = 0
    ailment: Optional[str] = None
    ailment_chance: int = 0
    max_hits: Optional[int] = None
    min_hits: Optional[int] = None
    max_turns: Optional[int] = None
    min_turns: Optional[int] = None

    @classmethod
    def load_json(cls, filepath: Path) -> Self:
        with open(filepath, "r") as file:
            return cls.model_validate_json(file.read())

    def __str__(self) -> str:
        return (
            f"{self.name} ({self.type_.title()}, {self.category.title()}) | "
            f"PP: {self.max_pp}, "
            f"Power: {self.power}, "
            f"Accuracy: {self.accuracy} | "
            f"{self.description}"
        )


class Movedex(object):
    """Class used to access moves."""

    _movedex: dict[str, Move] = {}

    def __init__(self) -> None:
        with open(_MOVEDEX_PATH) as file:
            moves = TypeAdapter(list[Move]).validate_json(file.read())
            self._movedex = {move.name.lower(): move for move in moves}

    def get_move(self, name: str) -> Move:
        try:
            move = self._movedex[name.lower()]
        except KeyError:
            msg = f"Move '{name}' not found in Movedex."
            raise KeyError(msg)
        return move.model_copy(deep=True)
