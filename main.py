""" Compare water level data from list of rivers url with limits for floating """


import requests
import poplib
import smtplib
from bs4 import BeautifulSoup


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
    sender_email = "12john.yy@gmail.com"
    sender_pass = "Dsabtd12Ge"

    receiver_email = "john.yy@seznam.cz"

    message = f'hey, those rivers are passable now: {data[0]}'

    print('trying to connect')

    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(sender_email, sender_pass)
        smtp_server.sendmail(sender_email, receiver_email, message)

        smtp_server.close()

        print("Email sent successfully!")

    except Exception as ex:

        print("Something went wrong….", ex)

    # with poplib.POP3('pop.gmail.com', 995) as server:
    #     # Mailbox = poplib.POP3_SSL('pop.googlemail.com', '995')
    #     server.starttls()
    #     print('tls ok ')
    #     server.login(sender_email, sender_pass)
    #     print("login success")
    #     server.sendmail(sender_email,receiver_email,message)


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



