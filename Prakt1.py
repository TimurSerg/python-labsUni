# 1. Отримати курси евро за попередній тиждень, вивести на екран дату + курс
# 2. З отриманого словника побудувати графк зміни курсу за тиждень

import json

import requests

response_data = requests.get("https://bank.gov.ua/NBU_Exchange/exchange_site?start=20250321&end=20250326&valcode=eur&json")


print(response_data)
#print (response_data.content)

response_list = json.loads(response_data.content)

exchange_date = []
exchange_rate = []
for item in response_list:
    exchange_date.append(item['exchangedate'])
    exchange_rate.append(item['rate'])

    print(f"Дата: {item['exchangedate']}, Курс: {item['rate']}, Валюта: {item['enname']}")

### Part 2
#Matplotlib
import matplotlib.pyplot as plt
plt.plot(exchange_date,exchange_rate)
plt.show()