import requests

def sendtelegrammsg(msg):
    base = 'https://api.telegram.org/bot7334081801:AAFYpGcHtxyqllOYYigyyO2EHGYBGPIN6ss/'
    chatid = '-4238563016'
    url = base + 'sendMessage?chat_id=' + chatid + '&text=' + msg
    requests.get(url)

