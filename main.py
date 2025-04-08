
import time
import re



import requests
from bs4 import BeautifulSoup
from urllib.error import  URLError
from lxml import html

from robots import verificar_acceso_url
from robots import leer_robot
from proxy import escollir_proxy_atzar

from config import config


import pandas as pd
from lxml import html

from bs4 import BeautifulSoup
from random import randrange
from selenium import  webdriver

from scraper import datos_vehiculo
from scraper import download_page

from util import visualitzar_llista_vehicles
from util import salvar_to_csv
from util import flatter

from robots import verificar_acceso_url

from config import config

from proxy import descarregar_llista_proxies
from proxy import get_proxies_actius
from proxy import escollir_proxy_atzar

from robots import leer_robot

def ver_columnas_libro(d_libro):
    for k in d_libro.keys():
        print ("Columna: {}".format(i))


def visualizar_libros(l_libros,pasada=0):

    for i, libro in enumerate(l_libros, 1):
        print(f"---- PASADA {pasada}:")
        print(f"Libro {i}:")
        print(f"Título: {libro['titulo']}")
        print(f"Autor(es): {', '.join(libro['autor'])}")
        print(f"Descargas: {libro['descargas']}")
        print(f"URL: {libro['url']}")
        print("-" * 50)




def parsear_libro(respuesta):
    import json

    # Suponiendo que la respuesta está almacenada en una variable llamada response_text
    data = json.loads(respuesta)

    # Extraer los hits (libros)
    libros = []
    for hit in data['response']['body']['hits']['hits']:
        campos = hit['fields']
        libro = {
            'identifier': campos.get('identifier'),
            'titulo': campos.get('title'),
            'descripcion': campos.get('description'),
            'autor': campos.get('creator', []),
            'fecha_publicacion': campos.get('date'),
            'idioma': campos.get('language', []),
            'descargas': campos.get('downloads'),
            'tamano': campos.get('item_size'),
            'temas': campos.get('subject', []),
            'formato': campos.get('mediatype'),
            'url': f"https://archive.org/details/{campos.get('identifier')}"
        }
        libros.append(libro)

    # Imprimir resultados


    return libros

def descargar_datos_libro_ampliado(d_libro,proxy=None,num_reintents=0):


    id=d_libro['identifier']
    url="https://archive.org/details/"+str(id)

    page = download_page(url=url, user_agent="wsp", num_reintents=2, proxy=proxy, robots_txt=config['robots_archive'])
    bs = BeautifulSoup(page, 'html5lib')

    pattern = re.compile(r'M4B', re.IGNORECASE)

    # Encontrar todos los elementos 'a' que coincidan
    m4b_links = []
    for a_tag in bs.find_all('a', href=True):
        if a_tag.find(string=pattern) and 'nofollow' in a_tag.get('rel', []):
            m4b_links.append({
                'url': a_tag['href'],
                'text': a_tag.get_text(strip=True)
            })

    # Imprimir resultados
    if len(m4b_links) == 0:
        m4b_links="NO DEFINIT"

    #print ("Libro: {} -> Enlaces {}".format(id,m4b_links))


    review_span = bs.find('span', {
        'class': 'item-stats-summary__count',
        'itemprop': 'userInteractionCount'
    })

    # 5. Extraer y formatear el número
    reviews_number=None

    if review_span:
        reviews = review_span.text.strip()
        # Eliminar comas y convertir a número
        reviews_number = int(reviews.replace(',', ''))
        #print(f'Número de reviews: {reviews_number}')
    else:
        reviews_number="NO DEFINIT"
        #print("Elemento no encontrado")

    favorite_container = bs.find('p', class_='favorite-count')
    favorite_count_span = favorite_container.find('span', class_='item-stats-summary__count')

    favorite_count = None

    # Extraer y convertir el número
    if favorite_count_span:
        favorite_count = int(favorite_count_span.get_text(strip=True))
        #print(f'Favoritos: {favorite_count}')
    else:
        print('No se encontró el contador de favoritos')
        #favorite_count="NO DEFINIT"

    date_span = bs.find('span', {'itemprop': 'datePublished'})
    fecha=None
    if date_span:
        # Obtener el texto y eliminar espacios en blanco
        fecha = date_span.get_text(strip=True)
        #print(f'Fecha publicada: {fecha}')  # 2021-11-09
    else:
        fecha="NO DEFINIT"
        #print("No se encontró la fecha de publicación")

    keywords_container = bs.find('dd', {'itemprop': 'keywords'})
    topics=None
    if keywords_container:
        # Extraer todos los textos de los enlaces
        keywords = [a.get_text(strip=True) for a in keywords_container.find_all('a')]

        # Unir con comas y espacio
        topics = ", ".join(keywords)
        #print(topics)
    else:
        topics="NO DEFINIT"
        #print("No se encontraron palabras clave")

    idioma = None
    idioma = bs.select_one('dl.metadata-definition dt:-soup-contains("Language") + dd a').text.strip()
    if idioma is None:
        idioma="NO DEFINIT"



    return idioma,topics,fecha,favorite_count,reviews_number,m4b_links


def main ():

    ## Obtenir llista de proxies
    l_proxies = descarregar_llista_proxies()
    ## Verifiquem els que funcionen
    l_proxies_funcionant = get_proxies_actius(l_proxies)

    if len(l_proxies_funcionant) > 0:
        ## Escollim un a l'atzar
        proxy = escollir_proxy_atzar(l_proxies_funcionant)
    else:
        proxy = None

    ## url identificada como endpoint de llamadas AJAX
    ## ens retorna un JSON amb la llista de audiobooks

    url = "https://archive.org/details/librivoxaudio?and%5B%5D=mediatype%3A%22audio%22&and%5B%5D=year%3A%222021%22"

    items_per_page=10
    page_actual=1
    cont = 0
    l_libros_total=[]
    ## camps d'informació dels llibres

    libros_keys = [
        'identifier',
        'titulo',
        'descripcion',
        'autor',
        'fecha_publicacion',
        'idioma',
        'descargas',
        'tamano',
        'temas',
        'formato',
        'url',
        'topics',
        'data',
        'num_favoritos',
        'num_revisions',
        'm4b_links'
    ]
    l_columns = list(libros_keys)
    ## datafram a on gardarem els llibres
    df_audiobooks = pd.DataFrame(columns=l_columns)
    total_libros=4000
    total_libros = 40
    n_pasades = int(total_libros / items_per_page)
    item_per_page=10

    n_libros=0

    for i in range(n_pasades):

        url = "https://archive.org/services/search/beta/page_production/?user_query=&page_type=collection_details&page_target"+\
           "=librivoxaudio&hits_per_page="+str(items_per_page)+"&page="+str(page_actual)+"&filter_map=%7B%22mediatype%22%3A%7B%22audio%22%3A%22inc%22%7D%2C%22year%22%3A%7B%222021%22%3A%22"+ \
           "inc%22%7D%7D&aggregations=false&uid=R%3Ad3fc420cc282d5fc9a45-S%3Aba291ebceb35c5739d30-P%3A1-K%3Ah-T%3A1744104285124&"+ \
           "client_url=https%3A%2F%2Farchive.org%2Fdetails%2Flibrivoxaudio%3Fand%255B%255D%3Dmediatype%253A%2522audio%2522%26and%255B%255D%3Dyear%253A%25222021%2522"
        print (url)
        proxy=escollir_proxy_atzar(l_proxies_funcionant)
        page = download_page(url=url, user_agent="wsp", num_reintents=2, proxy=proxy, robots_txt=config['robots_archive'])
        cont +=1
        page_actual +=1

        l_libros_pagina=parsear_libro(page)
        d_libro={}


        for libro in l_libros_pagina:
            idioma, topics, data, num_favoritos, num_revisions, m4b_links = descargar_datos_libro_ampliado (libro, proxy, 2 )
            libro['topics'] = topics
            libro['data'] = data
            libro['num_favoritos'] = num_favoritos
            libro['num_revisions'] = num_revisions
            libro['m4b_links'] = m4b_links

            new_row_df = pd.DataFrame([libro])
            n_libros+=1
            print("Libro {} -> {}".format(n_libros,libro))


            #print ("columnas de df_audioboosk: {}".format(df_audiobooks.columns))
            #print ("columnas de df_newroo: {}".format(new_row_df.columns))
            df_audiobooks = pd.concat([df_audiobooks, new_row_df], ignore_index=True)


    ## Ara ja tenim el dataframe amb tots els vehicles.
    ## El podem escriure a l'arxiu sortida_vehicles_autohero.csv

    arxiu_dataset=config['arxiu_sortida_dataset']
    salvar_to_csv(df_audiobooks, arxiu_dataset)

if __name__=="__main__":
    main()



