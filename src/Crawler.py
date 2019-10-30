import requests
from bs4 import BeautifulSoup

r = requests.get('https://www.cse.ust.hk/ug/comp1991/')

if r.status_code == requests.codes.ok:
    soup = BeautifulSoup(r.text, 'html.parser')

print(soup.get_text())
