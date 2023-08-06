from enum import Enum

class DocumentType(str, Enum):
    CPF = "CPF"
    CNPJ = "CNPJ"