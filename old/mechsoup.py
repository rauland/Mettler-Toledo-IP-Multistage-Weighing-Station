import mechanicalsoup
browser = mechanicalsoup.Browser()

url = "http://192.168.10.200/cellcnt.htm"
page = browser.get(url)
browser.
html = page.soup

frame = html.select("frame")



print(frame)