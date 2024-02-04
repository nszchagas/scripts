import requests
import sys
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from typing import List


class BaseBody():
    actual_page: int
    file_id: int

    def __init__(self, idx: int):
        self.actual_page = 1
        self.file_id = idx


class Proxy():
    # http: str
    https: str

    def __init__(self, ip: int, port: int):
        self.https = f'http://{ip}:{port}'
        # self.https = self.http.replace('http', 'https')


def get_proxies() -> List[Proxy]:
    proxies: List[Proxy] = []
    # URL of the webpage with proxy information
    url = 'https://www.sslproxies.org/'

    # Send an HTTP GET request to the webpage
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the table containing proxy information
        proxy_table = soup.find('table')

        if proxy_table:
            # Iterate through the rows of the table
            for row in proxy_table.find_all('tr')[1:]:  # Skip the header row
                columns = row.find_all('td')
                if len(columns) >= 2:
                    # Extract IP address and port
                    ip = columns[0].get_text()
                    port = columns[1].get_text()
                    https = columns[-2].get_text().lower() == 'yes'
                    proxies.append(Proxy(ip, port))

        else:
            print("Proxy table not found on the webpage.")
    else:
        print("Failed to fetch the webpage. Status code:", response.status_code)

    return proxies


base_url: str = 'https://asdocs.net/1r5s1'
viewer = f'{base_url}~pdfviewer'
file_id: int = 12332149

last_page: int = 221
proxies = get_proxies()
body: BaseBody = BaseBody(file_id)

s: HTMLSession = HTMLSession()
for t in proxies:
    try:
        r = requests.post(viewer, data=body.__dict__,
                          timeout=1, proxies=t.__dict__)
        soup = BeautifulSoup(r.content, 'html.parser')
        with open('a.html', 'wb') as page:
            page.write(r.content)

        for a in soup.findAll('img'):
            print(a)

        sys.exit(0)
    except requests.exceptions.ProxyError:
        pass

    except Exception as e:
        print(e)
        pass


# data = body.__dict__
