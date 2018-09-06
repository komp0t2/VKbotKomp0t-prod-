import vk_requests
import time
import requests, json

api = vk_requests.create_api(app_id='6683177', login='89127578732', password='TTvip784569', scope=['offline', 'status', 'messages', 'docs', 'photos'], api_version='5.63')
if api:
	print('Сессия создана')
f = api.users.get()
print(f)
ts = ""
pts = ""
# def pts_update(new_pts):
# 	global pts
# 	pts = new_pts
def write_msg(user_id, s):
    api.messages.send(peer_id=user_id, message=s)

def update(): #Обновлние данных Long poll
	global ts, pts
	lps = api.messages.getLongPollServer(need_pts=1)
	key = lps['key']
	server = 'https://' + lps['server']
	ts = lps['ts']
	pts = lps['pts']
	params = {  # Стандартные параметры указанные в документации
	                'act': 'a_check',
	                'key': key,
	                'ts': ts,
	                'wait': 25,
	                'mode': 2,
	                'version': 2
	            }
update()
print(ts)
while True:
	r = api.messages.getLongPollHistory(ts = ts, pts = pts, ip_version = 5.84) #Получение данных о новых сообщениях
	if 'failed' in r :
		print(r)
		if r['failed'] == 1 :
			pts = r['new_pts']
		if r['failed'] in [2, 3]:
			update()
		r = api.messages.getLongPollHistory(ts = ts, pts = pts, ip_version = 5.84)
	if r['messages']['items']:	#Если получено собщение
		item = r['messages']['items']
		user_id = item[0]['user_id']
		body = item[0]['body']
		if (user_id != 388078504):
			if 'chat_id' in r['messages']['items'][0]: #Сообщение из чата
				print('message from chat')
			else: #Сообщение из лички
				if 'Как дела'.lower() in body.lower():
					write_msg(user_id, 'Отлично)), У тебя как?')
				elif 'привет'.lower() in body.lower():
					write_msg(user_id, 'Привет))')
				elif 'Что делаешь'.lower() in body.lower():
					write_msg(user_id, 'Пишу этого бота) Ты что делаешь?')
				elif 'Зайдешь'.lower() in body.lower():
					write_msg(user_id, 'Извини, я сейчас занят, пишу программный код')
				elif 'любишь меня'.lower() in body.lower():
					write_msg(user_id, 'Люблю тебя безумно^^')
				elif 'Зайдёшь'.lower() in body.lower():
					write_msg(user_id, 'Извини, я сейчас занят, пишу программный код')
				else: print
	pts = api.messages.getLongPollHistory(ts = ts, pts = pts, ip_version = 5.84)['new_pts']
	time.sleep(1)

                  