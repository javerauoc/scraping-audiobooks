
import re


import pandas as pd
import requests
#import csv
#import argparse
#from datetime import datetime
#from datetime import timedelta
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import  URLError
from urllib.parse import urlparse
#from urllib.error import  HTTPError

#from urllib.robotparser import RobotFileParser
from datetime   import datetime
from time import sleep
from lxml import html



def limpiar_url(url):
    url_limpia = re.sub(r'^[^/]*', '', url)
    patron = r'(^\/[^?]+\/[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}\/)'
    coincidencia = re.search(patron, url_limpia)

    if coincidencia:
        return coincidencia.group(1)
    else:
        base = url_limpia.split('?')[0]
        return base if base.endswith('/') else base + '/'

class Throttle:

    """Add a delay between downloads to the same domain
    """
    def __init__(self, delay):
        # amount of delay between downloads for each domain
        self.delay = delay
        # timestamp of when a domain was last accessed
        self.domains = {}
    def wait(self, url):
        domain = urlparse(url).netloc
        last_accessed = self.domains.get(domain)
        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.now() -
                        last_accessed).seconds
            if sleep_secs > 0:
                # domain has been accessed recently
                # so need to sleep
                sleep(sleep_secs)
        # update the last accessed time
        self.domains[domain] = datetime.now()

def salvar_to_csv(pd_vehicles,csv_file):

    pd_vehicles.to_csv(csv_file,sep=';')




    ## Anem a buscar les dades !!


def visualitzar_llista_vehicles(l_lista):

    for i,e  in enumerate(l_lista):
        print ("Vehicle {} -> Dades: {}".format(i,e))



def flatter(lst):
    ret = []
    for elem in lst:
        if isinstance(elem, list):
            ret.extend(flatter(elem))
        else:
            ret.append(elem)
    return ret
