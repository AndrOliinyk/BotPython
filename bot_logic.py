"""
Данные, которые у нас имеются в начале работы:
1. Список пользователей нашего бота
"""
users = [{
		   "user_id":777,
		   "username": "Freg",
		   "user_level":2
		  },
		  {
		  	"user_id":383,
		  	"username": "Oleg",
		 	"user_level":1},
		  {
		  	"user_id":918,
		  	"username": "Anna",
		  	"user_level":3
		  }]

# 2. Набор предложений
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

	,
	{"text": "Sent111 If you want to make enemies, try to change something.", 
	"level": 1},
	{"text": "Sent222 If you want to make enemies, try to change something.", 
	"level": 1},
	{"text": "Sent333 If you want to make enemies, try to change something.", 
	"level": 1}
]

# 3. Сообщение с сервера, где указано от юзера с каким ID прилетел запрос и какое слово он ищет
req_from_server = {"user_id":383, "text":"change"}

""" 
Здесь ваш код. 
Используйте наработки предущей практической и последних занятий, чтоб завернуть его в функции

На выходе мы должны получить словарь вида
{user_id: 123, text: "blah-blah-blah \n ... \n anothe blah-blah-blah"}, 
где:
text - это одна большая строка, в которой содержаться английские предложения (либо сообщение, что результат не найден)
user_id - это id юзера, от которого нам прилетело сообщение, и на который мы же отправляем ответ
"""

# Результирующее сообщение должно готовиться функций типа prepare_message (название можете выбрать сами)
#message = prepare_message(some-input-arguments)

###!!!### функция поиска предложений в списке sentences, соответствующих уровню пользователя user["level"] 
# и содержащих слово message["text"]

def prepare_message(DBsentences=None, request=None):
	#получаем уровень пользователя user_lvl по его user_id
	for user in users:
		if user["user_id"]==request.get("user_id"):
			user_lvl=user["user_level"]
	#print(user_lvl)

	result_message = []
	for sentence in DBsentences:
		sentence_lvl = sentence.get("level")
		if user_lvl == sentence_lvl:
			if request.get("text") in sentence.get("text"):
				result_message.append(sentence["text"])
 			#print(sentence["text"])
	return {"user_id":request.get("user_id"), "text":result_message}


message = prepare_message(DBsentences=sentences, request=req_from_server)
print(message)



# Завершаем вот здесь
def send_message(message):
	msgTxt=message.get("text")
	# Вместо принта, а будущем ,у нас будет логика отправки сообщения на сервера Телеграм
	result_message=""
	if not msgTxt:
		result_message = "None result"
	if len(msgTxt) == 1:
		result_message = msgTxt[0]
	if len(msgTxt) > 1:
		for x in msgTxt:
			result_message += x + "\n...\n"
	print(result_message)

send_message(message)
