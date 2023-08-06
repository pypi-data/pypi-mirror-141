from enum import Enum


class EffectType(str, Enum):
    WARRANTY = "warranty"
    OWNERSHIP_ASSIGNMENT = "ownershipAssignment"
    PAWN = "pawn"
    ADVANCEMENT = "advancement"