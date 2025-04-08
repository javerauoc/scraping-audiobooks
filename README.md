# Màster en Ciència de Dades - UOC
# Tipologia de ciencia de dades
# PRÀCTICA 1: Com podem capturar les dades de la web? 

# scraping-audiobooks:  _Scrapping de d'audiobooks de archive.org_
## Authors:
- Concepción Gàlvez
- Juan Antonio Vera


ScrappingAudiobooks és el resultat de la PRÀCTICA de l'assignatura _Tipologia i cicle de vida de les dades (any 2025)_ del Màster de Ciència de Dades de la Universtati Oberta de Catalunua (UOC)



## Features

- Realitza l'scrapping d'audiollibres  del web Archive (_https://www.archive.org_) recopilant les sevees característiques.
- Unifica en un sol dataset els enllaços de descàrrega dels arxius d'àudio..
- L'scraping és anònim (es fan servir un conjunt de proxies diferents en cada descàrrega d'informació).
- L'scraping s'adapta als temps de resposta dels llocs web
- Respectuòs amb directrius robots.txt dels llocs web.
- Gestiona problema scroll_infinit amb crides a endpont AJAX.
- Generació arxiu CSV amb les principals característiques dels llibres.

## Getting started
1. Ubicar-se a la carpeta a on es vol instal·lar el programari. Per exemple:

   $ cd /home/<usuari>/

2. Crear entorn virtual

   $ python -m venv scraping-audiobooks

3. Activar entorn virutal
 
   $ source scraping-audiobooks/bin/activate

4. Clonar repositori 

   $ git clone https://github.com/javerauoc/scraping-audiobooks.git

5. Instal·lar requeriments

   $ cd scraping ; pip install -r requeriments.txt

6. Executar aplicació

   $ python main .py
