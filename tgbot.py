"""
Задача:
Соеденить два скрипта, которые уже есть. 
Нужно прикрутить скрипт, ищущий предложения на английском, которые содержат слово, 
введенное юзером и подбирают предложение на английском, где содержится это слово, 
и которое подохдит юзеру по уровню. 


Что уже имеем: 
1. Простой эхо-бот для Телеги, который пулит последние сообщения, через ТелеграмБотАПИ и шлет 
	в ответ копию того, что юзер ему написал.
2. Скрипт, который принимает слово и юзера (дикт, где указан юзернейм и уровень английского) 
   и возыращает строчку, которая содержит одно или несколько предложений, либо сообщение о том,
   	что ничего не найдено.


Соответвенно, нужно сделать так, чтоб бот в телеге читал сообщение от юзера, 
и, если это слово на английском, возвращал сообщение с результатом.


Для практической мы используем очень примитивный флоу, 
без большинства нужных проверок, т.к. на них можно сильно застрять. Они остануться на домашки.

Норимальный флоу должен быть такой:
- Принимаем сообщение.
- Смотрим на ID юзера и проверяем, есть у нас такой или нет. 
- Если нет, тосоздаем нового, забиваем туда ID и шлем юзеру в ответ сообщение:
  "Выбери свой уровень английского"
- Принимаем его и записыаем к юзеру.
- Теперь можем обратывать его сообщения - слова на английском.
- На каждон из этих сообщений делаем такие проверки:
	 - если сообщение не начинаеися со / (служебные команды), 
	 - не число, 
	 - не кирилица 
	то это просто слово на английском, и мы его кидаем в функцию, 
	которая выдает предложения с этим словом и отправляемю юзеру ответ.


Для практической сделаем более примитивный.
- Юзера захардкодим в виде словаря {"username": str, "level"; int}
- Будем исходить из того, что мы всегда шлем только корректные сообщения: 
  одно словo на английском.
- Поэтому, все что нужно, это прокидывать слово из телеграм-сообщения в скрипт, 
 получать результат и отсылать обратно.

- еще было бы неплохо добавить логирование, пока просто принтами.
"""

import requests

#token = "5497389613:AAGZq3lNckp9qHjIlPC32jKaedMVlNAKUkI"		#t.me/myNewBotAnfrOl_bot
#token = "5522426557:AAFKXBHE3VeSmiRYVI3jyuo0tHMMdz_Hl18"		#t.me/myNewBotAnfrOl02_bot
token = "5757316929:AAFvoxzakJC1GK0diW_tetDb04gzrmFRK40"		#t.me/myNewBotAnfrOl03_bot
root_url = "https://api.telegram.org/bot" 

ok_codes = 200, 201, 202, 203, 204
ok_levels = "1", "2", "3", "4", "5"


import json
import time

# Информацию о пользователях и их уровнях английского храним в файле users.txt
# Инфу о текущем user'е (отправившем сообщение в ТГ) берем из сообщения в ТГ (параметр "id"). 
# Если такого пользователя нет, добавляем информацию о нем в файл users.txt
# user = {"username" : "Egor",
# 		  "level" : 1} 


sentences = [
	{"text": "When my time comes \n Forget the wrong that I’ve done.", 
	"level": 1},
	{"text": "In a hole in the ground there lived a hobbit.", 
	"level": 2},
	{"text": "The sky the port was the color of television, tuned to a dead channel.", 
	"level": 1},
	{"text": "I love the smell of napalm in the morning.", 
	"level": 0},
	{"text": "The man in black fled across the desert, and the gunslinger followed.", 
	"level": 0},
	{"text": "The Consul watched as Kassad raised the death wand.", 
	"level": 1},
	{"text": "If you want to make enemies, try to change something.", 
	"level": 2},
	{"text": "We're not gonna take it. \n Oh no, we ain't gonna take it \nWe're not gonna take it anymore", 
	"level": 1},
	{"text":"I learned very early the difference between knowing the name of something and knowing something.", 
	"level": 2}
]



def fill_matched_sentences(message, user, sentences)->list:
	matched_sentences = []
	for sentence in sentences:
		user_lvl = user.get("level")
		sentences_lvl = sentence.get("level")
		sentences_txt = sentence.get("text")
		if  sentences_lvl == user_lvl:
#			if message in sentences_txt:
			if message.lower() in sentences_txt.lower():       #преобразовываем к нижнему регистру - для правильной проверки всех слов без учета регистра
				matched_sentences.append(sentences_txt)
	return matched_sentences


def create_result_message(matched_sentences:list) -> str:
	result_message = ""
	if not matched_sentences:
	    result_message = "Sorry, not found sentences for your request"
	if len(matched_sentences) == 1:
	    result_message = matched_sentences[0]
	if len(matched_sentences) > 1:
			for x in matched_sentences:
				result_message += x + "\n...\n"
	return result_message

def send_message(token, chat_id, message):
	url = f"{root_url}{token}/sendMessage"
	res = requests.post(url, data={'chat_id': chat_id, "text": message})
	if res.status_code in ok_codes:
		return True
	else:
		print(f"Request failed with status_code {res.status_code}")
		return False

def get_updates(token):
	url = f"{root_url}{token}/getUpdates"
	res = requests.get(url)
	if res.status_code in ok_codes:
		updates = res.json()
		return updates

def process_message(message:str)->str:
	""" обрабтывает входящее сообщение и выдает ответ, который будет отправлен юзеру
	"""
	#<CODE HERE>
	print(message)


	if message[0] == '/':
		message = 'This is command. Please enter a word'
		return message
	if message.isnumeric()==True:
		message = 'This is number. Please enter a word'
		return message

	if isinstance(message, str):
		matched_sentences = fill_matched_sentences(message, user, sentences)
		message = create_result_message(matched_sentences)
	 
	return message



#read info about users from txt file in JSON format
def openJSONfile(filename):
	with open(filename, 'r') as openfile:
		users_jsonFormat = json.load(openfile)
	users=users_jsonFormat["users_data"]
	return users

#rewrite file in JSON format (append info about NEW user)
def rewriteJSONfile(filename, newdata):
	with open(filename, 'r+') as openfile:
		users_jsonFormat = json.load(openfile)
		users_jsonFormat["users_data"].append(newdata)
		openfile.seek(0)
		json.dump(users_jsonFormat, openfile, indent = 4)


#===========Запуск программы===================#

#считываем информацию о пользователях из файла 
#(условно считаем их зарегистрированными, т.е. такими, которые уже пользовались ботом и о которых известна информация об их уровне английского) 
users=openJSONfile('users.txt')

#получаем обновления из ТГ-канала нашего бота
updates = get_updates(token)
#result = updates["result"]
last_update_id = updates["result"][-1]["update_id"]
user_id=updates["result"][-1]["message"]["from"]["id"]   #id пользователя, отправившего последнее сообщение
chat_id=updates["result"][-1]["message"]["chat"]["id"]
#last_message_id = updates["result"][-1]["message"]["message_id"]

#Первое сообщение пользователю:
username=updates["result"][-1]["message"]["from"]["first_name"]
first_message=f"Уважаемый {username}, Вы открыли ТГ-бот для изучения английского языка. Вы вводите слово, бот выдает Вам список предложений с этим словом на английском языке. Служебные команды бота:  /changelvl - изменить уровень;  /quit (или /stop)  - прекратить работу бота"
send_message(token, chat_id, first_message)
	

# список id всех пользователей, уже пользовавшихся ботом
userS_id=[]
for user in users:
	userS_id.append(user["user_id"])

if user_id in userS_id:
	print("OK")
	print(f"работа с пользователем {user_id}")
else:
	send_message(token, chat_id, "Вас нет в нашей базе. Скорее всего Вы пользуетесь ботом первый раз. Введите, пожалуйста, Ваш уровень английского (от 1 до 5) :")
	last_update_id_new = last_update_id
	while (last_update_id_new==last_update_id):
		updates = get_updates(token)
		last_update_id_new = updates["result"][-1]["update_id"]
	user_lvl=updates["result"][-1]["message"]["text"]
	newUser = {
            "user_id":user_id,
 		  	"username": updates["result"][-1]["message"]["from"]["first_name"],
 		  	"user_level":int(user_lvl)
			}
	rewriteJSONfile('users.txt', newUser)
	users.append(newUser)
	print(user_lvl)


user_lvl = 0
#получаем уровень пользователя user_lvl по его user_id
for user in users:
	if user["user_id"]==user_id:
		user_lvl=user["user_level"]


user = {"user_id" : user_id,
 		  "level" : user_lvl} 


#основной цикл обработки сообщений пользователя
last_message_id = 0

while True:
	updates = get_updates(token)
	last_message = updates["result"][-1]	
	message_id = last_message["message"]["message_id"]
	
	last_message_text = last_message["message"]["text"]
	chat_id = last_message["message"]["chat"]["id"]	
	
	time.sleep(1) #задержка на 1 сек. Служебный вариант. Потом можно удалить

	if message_id > last_message_id:

		#обработка команды /changelvl  - изменить уровень
		if  last_message_text == "/changelvl":
			send_message(token, chat_id, "Вы выбрали команду изменения уровня. Введите новое значение Вашего уровня (1-5):")
			last_message_id = message_id
			
			vas=0
			while message_id==last_message_id:
				updates = get_updates(token)
				last_message = updates["result"][-1]
				last_message_text = last_message["message"]["text"]
				chat_id = last_message["message"]["chat"]["id"]
				message_id = last_message["message"]["message_id"]
				if message_id > last_message_id:
					user_lvl=last_message_text
					if user_lvl in ok_levels:
						user["level"]= int(user_lvl)
						message_to_user = f"Ваш новый уровень: {user_lvl}" 
						send_message(token, chat_id, message_to_user)
						last_message_text="/changelvl"
					else:
						message_to_user = f"Вы НЕверное значение уровня. Введите новое значение Вашего уровня (ЧИСЛО от 1 до 5): {user_lvl}" 
						send_message(token, chat_id, message_to_user)
						last_message_id = message_id
		
	    #обработка команды /quit (синоним = /stop)  - завершить работу бота (на стороне сервера), но не выйти из него в Телеграме
		if  last_message_text in ("/quit", "/stop"):
			send_message(token, chat_id, f"Вы выбрали команду завершения работы бота {last_message_text}. Спасибо за пользование нашим ботом")
			quit()


		message_to_user = process_message(last_message_text)
		send_message(token, chat_id, message_to_user)
		last_message_id = message_id





