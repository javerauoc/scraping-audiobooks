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
