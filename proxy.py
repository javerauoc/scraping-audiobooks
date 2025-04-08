
import requests
from random import choice
from config import config


## REF: https://www.youtube.com/watch?v=Y_3BTOMGGa4

def extraer_ip_puerto(cadena):
    print ("cadena proxy leida: {}".format(cadena))
    partes = cadena.split(':')
    proxy=':'.join(partes[:2])

    return proxy

def escollir_proxy_atzar (l_proxies_funcionant):
    proxy = choice(l_proxies_funcionant)
    print ("PROXY ESCOLLIT: {}".format(proxy))

    return {'http':proxy }

def descarregar_llista_proxies():

    url=config['url_llista_proxies']
    r = requests.get(url)
    l_proxies=[]
    for line in r.text.splitlines():
        l_proxies.append(extraer_ip_puerto(line))

    print("Retornant llista de proxies disponibles de url: {}\n {}".format(url,l_proxies))

    return l_proxies

def get_random_proxy(l_proxies):
    return {"http": choice(l_proxies) }

def get_proxies_actius(l_proxies=None):
    l_proxies_ok = []
    for i,proxy in enumerate(l_proxies):
        http_proxy={'http':proxy}
        try:
            r = requests.get("https://www.google.com",proxies=http_proxy,timeout=1)
            if r.status_code==200:
                print ("Estat proxy {}: OK".format(proxy))
                l_proxies_ok.append(proxy)
        except:
            pass
    print ("Retornem llista proxies disponibles verificats: {}".format(l_proxies_ok))
    return l_proxies_ok



