import requests, datetime, random

from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_KEY = "4JM1MX763JGK93SD"
STOCK_URL = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TSLA&apikey=4JM1MX763JGK93SD"
NEWS_URL = "https://newsapi.org/v2/everything?q=tesla&apiKey=5505c5f68d0f4b8fad97d5fe9e8d308c"
account_sid = #SID
auth_token = #TOKEN

print(NEWS_URL)

response = requests.get(STOCK_URL)
response.raise_for_status()
stock_data = response.json()

price_at_close = "4. close"
price_change = False
perc_change = 0
titles_list = []
desc_list = []
link_list = []


#Check for price change, taking into consideration weekend when stock market is closed
def check_for_price_change():
    global price_change
    global perc_change
    if datetime.datetime.today().weekday() == 0:  # is Monday - check friday-thursday
        yesterday = datetime.datetime.today() - datetime.timedelta(days=3)
        before_yesterday = yesterday - datetime.timedelta(days=1)

        yesterday = str(yesterday).split(" ")
        before_yesterday = str(before_yesterday).split(" ")

        yesterday_date = yesterday[0]
        before_yesterday_date = before_yesterday[0]

        print(stock_data["Time Series (Daily)"][yesterday_date][price_at_close])
        print(stock_data["Time Series (Daily)"][before_yesterday_date][price_at_close])

        if float(stock_data["Time Series (Daily)"][yesterday_date][price_at_close]) - \
                float(stock_data["Time Series (Daily)"][before_yesterday_date][price_at_close]) >= (
                5 * float(stock_data["Time Series (Daily)"][yesterday_date][price_at_close])) / 100 or \
                float(stock_data["Time Series (Daily)"][yesterday_date][price_at_close]) - \
                float(stock_data["Time Series (Daily)"][before_yesterday_date][price_at_close]) <= -(
                5 * float(stock_data["Time Series (Daily)"][yesterday_date][price_at_close])) / 100:
            print("mai mare naspa")
            price_change = True
            perc_change = (float(stock_data["Time Series (Daily)"][yesterday_date][price_at_close]) -
                           float(stock_data["Time Series (Daily)"][before_yesterday_date][price_at_close])) / float(
                stock_data["Time Series (Daily)"][yesterday_date][price_at_close]) * 100
            print(perc_change)
        else:
            print("nu inca")

    if datetime.datetime.today().weekday() == 1:  # is Tuesday - check monday-friday
        yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
        before_yesterday = yesterday - datetime.timedelta(days=3)

        yesterday = str(yesterday).split(" ")
        before_yesterday = str(before_yesterday).split(" ")

        yesterday_date = yesterday[0]
        before_yesterday_date = before_yesterday[0]

        print(stock_data["Time Series (Daily)"][yesterday_date][price_at_close])
        print(stock_data["Time Series (Daily)"][before_yesterday_date][price_at_close])

        if float(stock_data["Time Series (Daily)"][yesterday_date][price_at_close]) - \
                float(stock_data["Time Series (Daily)"][before_yesterday_date][price_at_close]) >= (
                5 * float(stock_data["Time Series (Daily)"][yesterday_date][price_at_close])) / 100 or \
                float(stock_data["Time Series (Daily)"][yesterday_date][price_at_close]) - \
                float(stock_data["Time Series (Daily)"][before_yesterday_date][price_at_close]) <= -(
                5 * float(stock_data["Time Series (Daily)"][yesterday_date][price_at_close])) / 100:
            print("mai mare naspa")
            price_change = True
            perc_change = (float(stock_data["Time Series (Daily)"][yesterday_date][price_at_close]) -
                           float(stock_data["Time Series (Daily)"][before_yesterday_date][price_at_close])) / float(
                stock_data["Time Series (Daily)"][yesterday_date][price_at_close]) * 100
            print(round(perc_change, 2))
        else:
            print("nu inca")

    else:
        yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
        before_yesterday = yesterday - datetime.timedelta(days=1)

        yesterday = str(yesterday).split(" ")
        before_yesterday = str(before_yesterday).split(" ")

        yesterday_date = yesterday[0]
        before_yesterday_date = before_yesterday[0]

        print(stock_data["Time Series (Daily)"][yesterday_date][price_at_close])
        print(stock_data["Time Series (Daily)"][before_yesterday_date][price_at_close])

        if float(stock_data["Time Series (Daily)"][yesterday_date][price_at_close]) - \
                float(stock_data["Time Series (Daily)"][before_yesterday_date][price_at_close]) >= (
                5 * float(stock_data["Time Series (Daily)"][yesterday_date][price_at_close])) / 100 or \
                float(stock_data["Time Series (Daily)"][yesterday_date][price_at_close]) - \
                float(stock_data["Time Series (Daily)"][before_yesterday_date][price_at_close]) <= -(
                5 * float(stock_data["Time Series (Daily)"][yesterday_date][price_at_close])) / 100:

            price_change = True
            perc_change = (float(stock_data["Time Series (Daily)"][yesterday_date][price_at_close]) -
                           float(stock_data["Time Series (Daily)"][before_yesterday_date][price_at_close])) / float(
                stock_data["Time Series (Daily)"][yesterday_date][price_at_close]) * 100
        else:
            pass



check_for_price_change()

#Get news pieces of company
def get_news(company_name):
    global titles_list
    news_url = f"https://newsapi.org/v2/everything?q={company_name}&apiKey=5505c5f68d0f4b8fad97d5fe9e8d308c"
    news_response = requests.get(news_url)
    news_response.raise_for_status()
    news_data = news_response.json()
    for i in range(0, 3):
        titles_list.append(news_data["articles"][i]["title"])
        desc_list.append(news_data["articles"][i]["description"])
        link_list.append(news_data["articles"][i]["url"])
    print(titles_list)


#Send sms with info about price change
if price_change:
    print("Check news")
    get_news("tesla")
    client = Client(account_sid, auth_token)
    message = client.messages.create(body=f'{STOCK}: 🔺{round(perc_change,2)}\nHeadline: {titles_list[0]}\nBrief: {desc_list[0]}. To read more, visit: {link_list[0]}', from_='+19894496479', to="+40722648462")



