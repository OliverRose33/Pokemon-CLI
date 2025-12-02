"""
This module implements elemental types for Pokemon.
"""

import json
from enum import Enum, StrEnum, auto

from .. import path

_TYPECHART_FILEPATH = path.APPDATA / "type_chart.json"


class Type(StrEnum):
    """Enum of Pokemon elemental types."""

    NORMAL = auto()
    FIRE = auto()
    WATER = auto()
    GRASS = auto()
    ELECTRIC = auto()
    ICE = auto()
    FIGHTING = auto()
    POISON = auto()
    GROUND = auto()
    FLYING = auto()
    PSYCHIC = auto()
    BUG = auto()
    ROCK = auto()
    GHOST = auto()
    DRAGON = auto()
    DARK = auto()
    STEEL = auto()
    FAIRY = auto()


class Effectiveness(Enum):
    """Multipliers for effectiveness of elemental types."""

    NO_EFFECT = 0
    NOT_VERY_EFFECTIVE = 0.5
    NORMAL = 1
    SUPER_EFFECTIVE = 2
    QUADRUPLE_EFFECTIVE = 4

    def __rmul__(self, other: float) -> float:
        return self.value * other


def _load_type_chart() -> dict[Type, dict[Type, Effectiveness]]:
    """Loads the type chart from json, and converts strings to custom types."""
    with open(_TYPECHART_FILEPATH) as file:
        raw_dict: dict[Type, dict[Type, Effectiveness]] = json.load(file)
        type_chart: dict[Type, dict[Type, Effectiveness]] = {}
        for attacker, matchups in raw_dict.items():
            matchup_dict = {
                defender: Effectiveness(effectiveness)
                for defender, effectiveness in matchups.items()
            }
            type_chart[Type(attacker)] = matchup_dict
    return type_chart


_TYPE_CHART = _load_type_chart()


def _evaluate_matchup(attacker: Type, defender: Type) -> Effectiveness:
    """
    Evaluate the type matchup between two Pokemon types.

    Args:
        attacker (Type): The type of the attacking move.
        defender (Type): The type of the defending Pokemon.

    Returns:
        Effectiveness: The effectiveness of the move.
    """
    return _TYPE_CHART[attacker].get(defender, Effectiveness.NORMAL)


def get_effectiveness(attacker: Type, defender: list[Type]) -> Effectiveness:
    """
    Evaluate the type matchup between two Pokemon types.

    Args:
        attacker (Type): The type of the attacking move.
        defender (list[Type]): The types of the defending Pokemon.

    Returns:
        effectiveness (Effectiveness): The effectiveness of the move.
    """
    effectiveness = 1
    for type_ in defender:
        effectiveness *= _evaluate_matchup(attacker, type_)
    return Effectiveness(effectiveness)
