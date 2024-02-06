[![](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/release/python-31013/)
# DAS Emitter Scrapper
Scrapping service to download documents on site:  
https://www8.receita.fazenda.gov.br/SimplesNacional/Aplicacoes/ATSPO/pgmei.app

## Features
* hCaptcha bypass
* PDF automatic download

## Install
Clone this repository, change the directory to ```~/das_emitter_scrapper``` and run:
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
