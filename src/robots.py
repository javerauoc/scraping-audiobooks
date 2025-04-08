import requests
from urllib.parse import urlparse


def leer_robot(url,proxy=None):
    from urllib.parse import urlparse

    dominio = urlparse(url).netloc
    robots_url = f'http://{dominio}/robots.txt'
    print ("Leyendo URL ROBOTS.TXT -> {}".format(robots_url))

    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)'
                                 'AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;'
                             'q=0.9,image/webp,*/*;q=0.8'}
        if proxy is not None:
            print("Download-page -> Download with proxy: {}".format(proxy))
            req = requests.get(url, headers=headers, proxies=proxy)
        else:
            req = requests.get(url, headers=headers)

        req.raise_for_status()  # Lanza un error si la respuesta no es exitosa
        # Leer el contenido del robots.txt
        robots_txt = req.text.splitlines()
    except requests.exceptions.RequestException as e:
        print(f"Error al acceder al archivo robots.txt: {e}")
        return None  # Si no se puede obtener robots.txt, se asume que no es accesible
    print ("devolviendo robots.txt: {}".format(robots_txt))

    return robots_txt


def verificar_acceso_url(url=None,robots_txt=None):


    print("Verificando acceso a {}: ".format(url),end='')
    if robots_txt is not None:
        user_agent = "*"
        for line in robots_txt:
            if line.lower().startswith('user-agent'):
                user_agent = line.split(":")[1].strip()  # Captura el user-agent actual
            if user_agent == "*":
                if "disallow" in line.lower() and urlparse(url).path in line.lower():
                    print ("url bloqueada: {}".format(url))
                    return False  # URL bloqueada
        print ("OK".format(url))
        return True  # Si no hay reglas que bloqueen la URL
    else:
        print("NO AUTORITZAT")
        return False

