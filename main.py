import telebot
import requests
import time, sched
from tinydb import TinyDB, Query
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

#token 1969047481:AAHRZrAdsl6DEg7yXVkZktvBifHcon6J57M

scheduler = sched.scheduler(time.time, time.sleep)

bot = telebot.TeleBot("1969047481:AAHRZrAdsl6DEg7yXVkZktvBifHcon6J57M", parse_mode=None)

rates_response = requests.get("https://api.exchangerate.host/latest?base=USD")
history_resonse = requests.get("https://api.exchangerate.host/fluctuation?base=USD&start_date=2021-09-17&end_date=2021-09-24&symbols=USD,CAD&format=csv")
exchanhe_response = requests.get("https://api.exchangerate.host/convert?from=USD&to=CAD&amount=10")

x = []
y = []

for i in range (7):
	df = pd.read_csv(f"https://api.exchangerate.host/fluctuation?base=USD&start_date=2021-09-17&end_date=2021-09-{17+i}&symbols=USD,CAD&format=csv")
	y.append(df['end_rate'][0])
	x.append(17+i)

new_y = []

for i in y:
	i = i.replace(',','.')
	new_y.append(float(i))

plt.title('Exchange Rate Chart from 17Sep to 23Sep')
plt.xlabel('Day')
plt.ylabel('CAD for 1 USD')
plt.plot( x, new_y, color = 'b', linestyle = 'dashed')
plt.savefig('foo.png')
img = open('foo.png', 'rb')
plt.show()
data_r = rates_response.json()
data_ex = exchanhe_response.json()
rates = data_r['rates']
db = TinyDB('db.json')
User = Query()
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
db.insert(data_r['rates'])
db.insert({'time_stamp':current_time})
lst_resp = ""
ex_result = "$"+ str(data_ex['result'])
for key, value in rates.items():
	lst_resp += f"{key} : {round(value,2)}\n"



@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(commands=['help'])
def send_welcome(message):
	bot.reply_to(message, "-to view all available rate use: /list or /lst \n"
						  "-to exchange 10 USD to CAD use: /exchange10USDtoCAD \n"
						  "-to view chart use: /historyUSDtoCAD")


@bot.message_handler(commands=['list', 'lst'])
def send_welcome(message):
	bot.reply_to(message, lst_resp)

@bot.message_handler(commands=["exchange10USDtoCAD"])
def send_welcome(message):
	bot.reply_to(message, ex_result)


@bot.message_handler(commands=["historyUSDtoCAD"])
def send_photo(message):
	bot.send_chat_action(message.chat.id, 'upload_photo')
	img = open('foo.png', 'rb')
	bot.send_photo(message.chat.id, img, reply_to_message_id=message.message_id)
	img.close()

@bot.message_handler(func=lambda m: True)
def echo_all(message):
	bot.reply_to(message, "I don't understand you :( \nUse /help to get all available commands :)")

bot.polling()