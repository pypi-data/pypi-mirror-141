from enum import Enum


class AccountType(str, Enum):
    CC = "CC"
    CD = "CD"
    CG = "CG"
    CI = "CI"
    PG = "PG"
    PP = "PP"