## Scrapping service to download documents on site:  
https://www8.receita.fazenda.gov.br/SimplesNacional/Aplicacoes/ATSPO/pgmei.app

## Install
Clone this repository, change the directory to ```~/das_emitter_scapper``` and run:
```
pip install -r requirements.txt
```
and then run:
```
python app.py
```

## Endpoints
| **HTTP Method** |    **/**    |                                 JSON                                 |             Response             |
|:---------------:|:-----------:|:--------------------------------------------------------------------:|----------------------------------|
|       POST      |   /pdf      |     {"cnpj": "46823637000189", "month": "janeiro", "year": 2024}     |         application/pdf          |
