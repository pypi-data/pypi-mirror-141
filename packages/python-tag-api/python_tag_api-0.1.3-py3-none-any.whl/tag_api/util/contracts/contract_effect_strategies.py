from enum import Enum


class EffectStrategy(str, Enum):
    OVERRAL = 'overall'
    SPECIFIC = 'specific'
    CUSTOM = 'custom'