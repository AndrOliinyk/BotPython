#   in  PowerShell:
#   pip install requests

#   https://requests.readthedocs.io/en/latest/

#   pypi.org

#В телеграме: ищем пользователя   BotFather  (для создания собственных ТГ-ботов)
#команда /newbot   -  создаем нового бота на Телеграме
#например, имя BeDevTodayBot    ИЛИ    myNewBotAndrOl...    Имя для всех:  myNewBotAndrOl_bot  (***_bot)
#получаем токен (код) для управления этим ботом
#Use this token to access the HTTP API:
#5497389613:AAGZq3lNckp9qHjIlPC32jKaedMVlNAKUkI    !!!!!!!!!!!!!!!!!!!!!!
#Keep your token secure and store it safely, it can be used by anyone to control your bot.
# https://api.telegram.org/bot5497389613:AAGZq3lNckp9qHjIlPC32jKaedMVlNAKUkI/getMe
# https://api.telegram.org/bot5497389613:AAGZq3lNckp9qHjIlPC32jKaedMVlNAKUkI/getUpdates
# https://api.telegram.org/bot5497389613:AAGZq3lNckp9qHjIlPC32jKaedMVlNAKUkI/sendMessage?chat_id=1894340634&text=55501BotText


import requests
import time

ROOT_URL="https://api.telegram.org/bot" 
TOKEN = "5497389613:AAGZq3lNckp9qHjIlPC32jKaedMVlNAKUkI"
last_update_id = 0

def get_updates(root_url, token):
	url=f"{root_url}{token}/getUpdates"
	res = requests.get(url)
	return res.json()


def sendMessage(root_url, token, chat_id, text):
	url=f"{root_url}{token}/sendMessage" 
	r=requests.post(url, data={'chat_id':chat_id,"text":text})


updates = get_updates(ROOT_URL, TOKEN)
result = updates["result"]
last_update_id = result[-1]["update_id"]


while True:
	updates = get_updates(ROOT_URL, TOKEN)
	messages = updates["result"]
	for message in messages:
		if message["update_id"] > last_update_id:
			chat_id=message["message"]["chat"]["id"]
			last_message_text=message["message"]["text"]
			last_update_id = message["update_id"]
			sendMessage(ROOT_URL, TOKEN, chat_id, last_message_text)
			# print (chat_id, last_message_text)
			




'''
last_message=update["result"][-1]
last_message_id=last_message["message"]["message_id"]


a=0
while True:
	time.sleep(1)
	a=a+1
	print(a)
	Updates=get_bot_Updates(token)
	last_message_new=Updates["data"]["result"][-1]
	last_message_id_new=last_message_new["message"]["message_id"]

	print(last_message_id_new, last_message_id)

	if last_message_id_new>last_message_id:
		chat_id_new=last_message_new["message"]["chat"]["id"]
		last_message_text_new=last_message_new["message"]["text"]
		sendMessage(token, chat_id_new, last_message_text_new)
	#	url=f"{root_url}{token}/sendMessage" 
	#	r=requests.post(url, data={'chat_id':chat_id_new,"text":last_message_text_new})
		last_message_id=last_message_id_new


'''

# Upd=get_bot_Updates(token)
# if Upd["error"] == None:
# 	print(Upd["data"])

# updates=Upd["data"]
# if len(updates["result"])>0:
# 	last_message=updates["result"][-1]     #последнее сообщение в нашем боте
# 	last_message_text=last_message["message"]["text"]    #текст в последнем сообщении
# 	chat_id=last_message["message"]["chat"]["id"]        #id чата в нашем боте, где было последнее сообщение
# 	print(last_message_text)
# else:
# 	print("no messages")

# #отсылаем сообщение нашему боту, текст которого дублирует текст последнего сообщения в нашем боте
# url=f"{root_url}{token}/sendMessage"  
# r=requests.post(url, data={'chat_id':chat_id,"text":last_message_text})

# #то же самое с помощью get-запроса. НО лучше так НЕ делать, т.к. в строке адреса некоторые комбинации символов будут преобразовываться, поэтому текст, например "789_+++апв", будет передаваться как "789_   апв"
# urlget=f"{url}?chat_id={chat_id}&text={last_message_text}" 
# r=requests.get(urlget)





# print(resp.status_code)
# print(resp.headers)
# print(resp.encoding)

# print(resp.text)      #Тело ответа (responce body) в текстовом формате
# print(resp.json())    #Тело ответа в формате json



#print(res.text)


# a = res.json()
# print(a[0])


# qw = requests.get('https://api.telegram.org/bot5497389613:AAGZq3lNckp9qHjIlPC32jKaedMVlNAKUkI/getUpdates')
# qw.json()
# print(qw.json())
#print(qw.json()['description'])


