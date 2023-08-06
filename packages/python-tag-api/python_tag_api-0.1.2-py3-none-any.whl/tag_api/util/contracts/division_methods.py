from enum import Enum


class DivisionMethod(str, Enum):
    FIXED_AMOUNT = 'fixedAmount'
    PERCENTAGE = 'percentage'