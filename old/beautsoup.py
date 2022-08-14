from bs4 import BeautifulSoup
from urllib.request import urlopen

url = "http://192.168.10.200/cellcnt.htm"
page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

print(soup.contents)

pass