import re
import requests
from bs4 import BeautifulSoup
from urllib.error import  URLError
from lxml import html

from robots import verificar_acceso_url
from robots import leer_robot
from proxy import escollir_proxy_atzar

from config import config


def download_page(url=None, user_agent="wsp", num_reintents=2, proxy=None,robots_txt=None):

    print ("Descarregant url: {} proxy: {}".format(url,proxy))
    if verificar_acceso_url(url=url,robots_txt=robots_txt) is False:
        return None
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)'
                             'AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
               'Accept': 'text/html,application/xhtml+xml,application/xml;'
                         'q=0.9,image/webp,*/*;q=0.8'}
        if proxy is not None:
            req=requests.get(url,headers=headers,proxies=proxy)
        else:
            req = requests.get(url, headers=headers)

    except URLError as e:
        print ("Error al descarregar: {}".format(e.reason))
        req=None
        if num_reintents>0:
            if hasattr(e,'code') and e.code >=500 and e.code<600:
                print("Error descarregant -> Intents restants: {}".format(num_reintents))
                return download_page(url, user_agent="wsp", num_reintents=num_reintents - 1, proxy=proxy)
    return req.content

def datos_vehiculo(link,l_proxies=None,timeout=0,robots=None):

    print("")
    proxy = escollir_proxy_atzar(l_proxies)

    page = download_page(url=link, user_agent="wsp", num_reintents=2, proxy=proxy,robots_txt=robots)
    bs = BeautifulSoup(page, 'html5lib')
    patro_cerca = re.compile(r"^feature-section-item-")
    enlaces = bs.find_all('div', attrs={'data-qa-selector': patro_cerca})

    d_valores = {}
    i = 0
    for feature in enlaces:

        data_qa = feature.get('data-qa-selector', '')
        match = re.search(r'feature-section-item-(.+?)-body', data_qa)

        if match:
            clave = match.group(1)
            d_valores[clave] = feature.text  # Asignamos 7 como valor para cada clave

    #robots_dgt = leer_robot(url=config['url_robots_dgt'], proxy=proxy)

    etiqueta = recuperar_etiqueta_ambiental(matricula=d_valores['licensePlate'],user_agent="wsp", num_reintents=2,
                                            proxy=proxy,robots_dgt=config['robots_dgt'])

    d_valores['ambientalSticker-link']=etiqueta


    return d_valores


def recuperar_etiqueta_ambiental(matricula,user_agent="wsp", num_reintents=2, proxy=None,robots_dgt=None):

    print ("Inici descarrega ETIQUETA AMBIENTAL matricula: {}, proxy: {}".format(matricula,proxy))
    url=config['url_dgt_verificat'] + matricula.upper()

    if verificar_acceso_url(url=url,robots_txt=robots_dgt) is not True:
        return None
    try:

        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)'
                                 'AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;'
                             'q=0.9,image/webp,*/*;q=0.8'}
        if proxy is not None:
            req = requests.get(url, headers=headers, proxies=proxy)
        else:
            req = requests.get(url, headers=headers)
    except URLError as e:
        print("Error al descarregar: {}".format(e.reason))
        req = None
        if num_reintents > 0:
            if hasattr(e, 'code') and e.code >= 500 and e.code < 600:
                print("Error descarregant -> Intents restants: {}".format(num_reintents))
                return recuperar_etiqueta_ambiental(url, user_agent="wsp", num_reintents=num_reintents - 1, proxy=proxy)

    tree = html.fromstring(req.content)
    elements = tree.xpath('/html/body/main/div[1]/div[1]/div/div[2]/div/div/div/p/strong[2]')
    etiqueta =elements[0].text
    print ("ETIQUETA RECUPERADA!! -> Matricula: {} -> Etiqueta: {}".format(matricula,etiqueta))

    return etiqueta