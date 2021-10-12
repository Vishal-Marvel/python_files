import bs4
import requests
import socket
import smtplib
import datetime, time
from bs4 import BeautifulSoup
import pywhatkit


l = ['JKTYRE.BO', 'ASHOKLEY.BO', 'ICICIBANK.BO', 'LT.BO', 'ITDCEM.BO', 'MANGALAM.BO', 'INDOSOLAR.BO', 'MARKSANS.BO', 'TANLA.BO', 'THANGAMAYL.BO', 'VEDL.BO']
l.sort()
com = []
price = []
urls = []
def pracePrice():
    for i in l:
        link = 'https://finance.yahoo.com/quote/{}?p={}'.format(i,i)
        urls.append(link)
        r = requests.get(link)
        soup = bs4.BeautifulSoup(r.text, "lxml")
        price.append(soup.find('div', {'class':'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text)
        com.append(soup.find('h1', {'class':'D(ib) Fz(18px)'}).text.split('(')[0])


def send_mail(to_mail, message):
    now = datetime.datetime.now().strftime('%I:%M')
    subject = "This is the automated stock details at {} designed by Vishal".format(now)
    message = "Subject:" + subject + "\n\n" + message
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login('autostock2021@gmail.com', 'autostock@123')
        server.sendmail('autostock2021@gmail.com', to_mail, message)
        server.quit()
    except socket.gaierror:
        pass

def main():
    
    pracePrice()
    message = '\n\n'
    for index, i in enumerate(l):
        message += com[index] + '\t-->\t' + str(price[index]) + '\t-->\t' + urls[index] + '\n\n'
    # print(message)
    send_mail('vishal.pvn.edu@gmail.com', message)
    # h = int(datetime.datetime.now().strftime('%H'))
    # m = int(datetime.datetime.now().strftime('%M')) + 1
    # pywhatkit.sendwhatmsg('+919791077398', message, h, m)
    # send_mail('narayanan.pvn@gmail.com', message)
    # send_mail('usha.pvn@gmail.com', message)
    

if __name__ == '__main__':
    main()
    now = int(datetime.datetime.now().strftime('%H'))
    while now < 9:
        pass
    while 9 <= now < 16:
        main()
        time.sleep(1800)



