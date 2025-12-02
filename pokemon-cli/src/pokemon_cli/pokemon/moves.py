"""
This module contains code for describing moves.
"""

from enum import StrEnum, auto
from pathlib import Path
from typing import Optional, Self

from pydantic import BaseModel, Field, TypeAdapter

from .. import path
from .types import Type

_MOVEDEX_PATH = path.APPDATA / "moves.json"


class Category(StrEnum):
    """Categories of moves."""

    PHYSICAL = auto()
    SPECIAL = auto()
    STATUS = auto()


class Target(StrEnum):
    """Target of moves."""

    SELECTED = auto()
    SELF = auto()


class Move(BaseModel):
    """
    A move which can be used by a Pokemon.

    Attributes:
        name (str):
            The name of the move.
        type\\_ (Type):
            The type of the move.
        category (Category):
            The category of the move.
        description (str):#
            A description of the move.
        max_pp (int):
            The maximum number of times the move can be used.
        power (int):
            The base damage of the move.
        accuracy (Optional[int]):
            The accuracy of the move, between 0 and 100.
            A move with no accuracy is guaranteed to hit.
        target (Target):
            The target of the move.
        priority (int):
            The priority of the move.
        healing (int):
            The amount of healing the move does.
        drain (int):
            The amount of health drained by the move.
        flinch_chance (float):
            The chance of the move causing a flinch.
        crit_rate (int):
            The likelihood of a critical hit.
            0 is the base chance, while 1 is an increased likelihood.
        effect_chance (float):
            The chance of a secondary effect occurring.
        stat_chance (float)
             The chance of a stat change.
        ailment (Optional[str]):
            An ailment which the move can cause.
        ailment_chance (int):
            The chance of the move causing an ailment.
        max_hits (Optional[int]):
            The maximum number of hits for multihit moves.
        min_hits (Optional[int]):
            The minimum number of hits for multihit moves.
        max_turns (Optional[int]):
            The maximum number of turns for multiturn moves.
        min_turns (Optional[int]):
            The minimum number of turns for multiturn moves.
    """

    name: str
    type_: Type = Field(alias="type")
    category: Category
    description: str
    max_pp: int = Field(gt=0)
    power: int = Field(gt=0)
    accuracy: Optional[int] = Field(gt=0, le=100)
    target: Target = Target.SELECTED
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
