from dataclasses import dataclass


@dataclass
class GeneratePDFDocumentDTO:
    cnpj: str
    month: str
    year: int