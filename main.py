""" Compare water level data from list of rivers url with limits for floating """


import requests
from bs4 import BeautifulSoup


urls = ["https://hydro.chmi.cz/hpps/hpps_prfdyn.php?seq=37829235", "https://hydro.chmi.cz/hpps/hpps_prfdyn.php?seq=37816755"]
limits = [37, 75]

for url,limit in zip(urls,limits):
    page = requests.get(url)
    doc = BeautifulSoup(page.content, 'html.parser')

    wanted_table = doc.find_all(text="Datum a čas")[0].parent.parent.parent
    first_tablerow = wanted_table.find_all("tr")[1]
    water_level = first_tablerow.find_all("td")[1].string

    print(water_level)
    print(limit)
    if int(water_level) >= limit:
        print("reka je sjizdna")

