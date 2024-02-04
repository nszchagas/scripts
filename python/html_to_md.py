from glob import glob
import re
from bs4 import BeautifulSoup

tags = set()

for h in glob("*.html"):
    with open(h, 'r', encoding='utf-8') as html:
        s = BeautifulSoup(html.read().replace('\n', ' '), 'html.parser')
    with open(h.replace('.html', '.md'), 'w', encoding='utf-8') as md:
        for x in s.find_all(True):
            tags.add(x.name)

            if x.name == 'ul':
                txt = re.sub(r'<\/?span>|<\/?ul>', '', str(x))
                txt = txt.replace('<li>', '\n- ')
                txt = txt.replace('</li>', '\n')
                txt = re.sub(r'\ +', ' ', txt)
                md.write(txt)
            elif x.name == 'ol':
                txt = re.sub(r'<\/?span>|<\/?ol.*?>', '', str(x))
                txt = txt.replace('<li>', '\n1. ')
                txt = txt.replace('</li>', '\n')
                txt = re.sub(r'\ +', ' ', txt)
                md.write(txt)
            elif x.name == 'a':
                r = re.findall(r'<a.*href="(.*)">(.*)<\/a>', str(x))
                if len(r) > 0:
                    l, t = r[0]
                    md.write(f'[{t}]({l})')
                # md.write(f'[{x.get("innerHTML")}]({x.get("href")}) ')
            elif x.name == 'table':
                md.write(f'\n{x}\n')
            else:
                m = re.findall(r'h(\d)', x.name)
                if m:
                    md.write(f"\n{'#'*int(m[0])} {x.text.strip()}\n")


print(sorted(tags))

tags = ['a',
        'h1', 'h2', 'h3', 'h4', 'h5',
        'img',
        'li', 'ol', 'ul',
        'p', 'span',
        'table', 'td', 'tr']
