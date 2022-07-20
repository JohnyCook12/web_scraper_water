""" Compare water level data from list of rivers url with limits for floating """
""" email sending may be blocked by firewall """

import requests
import smtplib
from bs4 import BeautifulSoup
import credentials


urls = ["https://hydro.chmi.cz/hpps/hpps_prfdyn.php?seq=37829235", "https://hydro.chmi.cz/hpps/hpps_prfdyn.php?seq=37816755"]
names = ["horni botic", "dolni botic"]
limits = [37, 75]
passable_rivers = []


def current_level(url):
    """ scrape water level from url"""
    page = requests.get(url)
    doc = BeautifulSoup(page.content, 'html.parser')
    wanted_table = doc.find_all(text="Datum a čas")[0].parent.parent.parent
    first_tablerow = wanted_table.find_all("tr")[1]
    water_level = first_tablerow.find_all("td")[1].string
    return(water_level)


def send_email(data):
    """ send email """
    sender_email = credentials.s_login
    sender_pass = credentials.s_password
    receiver_email = "john.yy@seznam.cz"

    message = f'hey, those rivers are passable now: {data[0]}'
    print('trying to connect')

    try:
        # smtp_server = smtplib.SMTP_SSL('smtp.seznam.cz', 465)
        server = smtplib.SMTP('smtp.seznam.cz', 465, None, 20)
        server.starttls()
        server.login(sender_email, sender_pass)
        server.sendmail(sender_email, receiver_email, message)
        server.quit
        print("Successfully sent email")


    except Exception as ex:
        print("Something went wrong….", ex)


for url,limit,name in zip(urls,limits, names):
    water_level = current_level(url)

    print(name, ": ", water_level,"cm")
    print("limit=", limit)
    passable = True if (int(water_level) >= limit) else False
    print("sjizdny=", passable)
    print("")

    # if passable:
    passable_rivers.append(name)

print("passable rivers", passable_rivers)
send_email(passable_rivers)


