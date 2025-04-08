# Màster en Ciència de Dades - UOC
# Tipologia de ciencia de dades
# PRÀCTICA 1: Com podem capturar les dades de la web? 

# AutoHeroSrapper:  _Scrapping de vechiculos publicados en AutoHero_
## Authors:
- Concepción Gàlvez
- Juan Antonio Vera


AutoHeroScrapper és el resultat de la PRÀCTICA de l'assignatura _Tipologia i cicle de vida de les dades (any 2025)_ del Màster de Ciència de Dades de la Universtati Oberta de Catalunua (UOC)



## Features

- Realitza l'scrapping de vehices del web AutoHero (_https://www.autohero.com/search_) recopilant les característiques més important.
- Complementa la informació del vehicle incorporant l'etiqueta ambiental fent scraping del web de ls DGT.
- L'scraping és anònim (es fan servir un conjunt de proxies diferents en cada descàrrega d'informació).
- L'scraping s'adapta als temps de resposta dels llocs web
- Respectuòs amb directrius robots.txt dels llocs web.
- Fa servir Selenium per tractar _scroll infinit_.
- Generació arxiu CSV amb les principals característiques dels vehicles.

## Getting started
1. Ubicar-se a la carpeta a on es vol instal·lar el programari. Per exemple:

   $ cd /home/<usuari>/

2. Crear entorn virtual

   $ python -m venv autohero-venv

3. Activar entorn virutal
 
   $ source autohero-venv/bin/activate

4. Clonar repositori 

   $ git clone https://github.com/javerauoc/scraping.git

5. Instal·lar requeriments

   $ cd scraping ; pip install -r requeriments.txt

6. Executar aplicació

   $ python main .py
