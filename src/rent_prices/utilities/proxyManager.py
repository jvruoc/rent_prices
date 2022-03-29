"""
    Investigación sobre rotación de proxies.

    Se prueba la lista free-proxy-list, pero solo daba un proxy
    en funcionamiento y una prueba posterior indicaba que también
    ese proxy fallama.

    Leído en varios artículos, casi todos los proxies libres 
    suelen estar caídos o bloqueados.
"""

class ProxiManager:
    pass



def search_proxy():
    import requests
    from bs4 import BeautifulSoup

    s = requests.Session()
    url = "http://free-proxy-list.net"
    #url = "https://spys.one/en/free-proxy-list/"

    # get page
    page = s.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    #get the list of ip's
    list = soup.select('textarea')[0].contents[0]

    #split the list of ip's
    list = list.splitlines()[3:]

    proxy_list = []
    for ip in list:
        try:
            proxy = {
                'http':f'http://{ip}',
                'https':f'http://{ip}'}
            proxy = s.get('https://api.ipify.org', proxies=proxy, timeout = 1)
        except Exception as e:
            pass
            print(f'{ip} - failed')
        else:
            if proxy.content != '68.110.86.107':
                print(f'{ip} - works')
                print(f'68.110.86.107 -> {ip} -> {str(proxy.content)}')
                proxy_list.append(ip)

    print(proxy_list)


if __name__ == "__main__":
    search_proxy()
