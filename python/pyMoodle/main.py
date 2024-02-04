import os
import re
from bs4 import BeautifulSoup
from requests import Session, Response


def get_soup(r: Response) -> BeautifulSoup:
    return BeautifulSoup(r.content, 'html.parser')


def get_course_id(course_name: str) -> int:
    c_id = 0
    # Select course
    for x in soup.find_all('a[href*="course/view"]'):
        print(x)
    return c_id


username = os.getenv('MOODLE_USER')
password = os.getenv('MOODLE_PASS')

base_url: str = 'https://aprender3.unb.br'
login_url: str = f'{base_url}/login/index.php'
courses_url: str = f'{base_url}/my/courses.php'
redes_url: str = f'{base_url}/course/view.php?id=20043'
s: Session = Session()

a = s.get(login_url)
soup = get_soup(a)
data = {
    'username': username,
    'password': password
}
for x in soup.find_all('input'):
    if x.get('value') and x.get('name'):
        data[x.get('name')] = x.get('value')

# Login
a = s.post(base_url, data=data)

a = s.get(redes_url)
soup = get_soup(a)
links = soup.find_all('a')

# with open('links_html.html', 'w', encoding='utf-8') as file:
#     file.write('\n'.join(links))

links_txt = [l.get('href') for l in links if l.get('href')]

with open('links.txt', 'w', encoding='utf-8') as file:
    file.write('\n'.join(links_txt))

for i, l in enumerate(links_txt):
    a = s.get(l)
    if 'pdf' in a.headers.get('Content-Type'):
        filename = f'./data/{l}.pdf'
        with open(filename, 'wb') as file:
            file.write(a.content)
