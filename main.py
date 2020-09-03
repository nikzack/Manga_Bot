import telebot
from bs4 import BeautifulSoup as BS
import requests

token = '1123880191:AAFeXitxFGL_ViTBpusV1ogjqnTJeO4qgKk'

markup = telebot.types.InlineKeyboardMarkup()
itembtna = telebot.types.InlineKeyboardButton('next>>', callback_data="next")
markup.row(itembtna)

bot = telebot.TeleBot(token)
part = 0
msg = []

def uppdate():
	url = "https://ranobelib.me/violet-evergarden-novel"
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}

	r = requests.get(url, headers=headers)

	soup = BS(r.text, "html.parser")

	chp_lst = soup.find('div', {'class': 'chapters-list'})

	links = chp_lst.find_all('div', {'class': 'chapter-item__name'})

	msg = []

	for link in links:
		msg.append(link.find('a').get('title') + "\n" + link.find('a').get('href'))

	msg.reverse()
	return msg

@bot.message_handler(commands=['update', 'start'])
def update(message):
	global msg
	global part
	msg = uppdate()
	try:
		bot.send_message(message.chat.id, msg[part], reply_markup=markup)
		part +=1
	except:
		bot.send_message(message.chat.id, "Сорян, ещё не перевели.")

@bot.callback_query_handler(func=lambda call: True)
def CallBack(call):
	global part
	if call.data == "next":
		try:
			bot.send_message(call.message.chat.id, msg[part], reply_markup=markup)
			part += 1
		except:
			bot.send_message(call.message.chat.id, "Сорян, ещё не перевели.")

bot.polling()