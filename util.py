
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

def salvar_to_csv(pd_llibres,csv_file):

    pd_llibres.to_csv(csv_file,sep=';')

