from dataclasses import dataclass


months = [
    'janeiro',
    'fevereiro',
    'março',
    'abril',
    'maio',
    'junho',
    'julho',
    'agosto',
    'setembro',
    'outubro',
    'novembro',
    'dezembro'
]

@dataclass
class GeneratePDFDocumentDTO:
    cnpj: str
    month: str
    year: int

    def __init__(self, cnpj: str, month: str, year: int):
        self.cnpj = cnpj
        self.month = self.get_month_name(month)
        self.year = year
    
    def get_month_name(self, month: str) -> str:
        if(month.isdigit()):
            if(1 <= int(month) <= 12):
                return months[int(month) - 1]
            raise IndexError('Informe um mês válido')
            
        if(not month in months):
            raise IndexError('Informe um mês válido')
        return month
