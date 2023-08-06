from enum import Enum


class WarrantyType(str, Enum):
    FIDUCIARY = "fiduciary"
    PLEDGE = "pledge"