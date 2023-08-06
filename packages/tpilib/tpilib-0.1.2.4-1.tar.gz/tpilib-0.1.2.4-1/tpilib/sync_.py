import requests
import json
import datetime


class SettingsClass:
	def __init__(self, token = None, apiTag = "tgn"):
		self.apiSelection = {
			"tgn":"https://edu-tpi.donstu.ru/api/",
			"rnd":"https://edu.donstu.ru/api/"
		}
		self.url_api = self.apiSelection[apiTag]  
		self.headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 YaBrowser/21.3.3.234 Yowser/2.5 Safari/537.36",
			"Content-Type": "application/json; charset=utf-8"
		}
		if token is not None:
			self.headers["authorization"] = "Bearer {}".format(token)

# Получаем токен от аккаунта и наслаждаемся
class User(SettingsClass):


	"""
	METHODS_URL = {

		/GET/
		Все сообщения: https://edu-tpi.donstu.ru/api/Mail/InboxMail
		Непрочитанные сообщения: https://edu-tpi.donstu.ru/api/Mail/CheckMail
		Конкретное сообщение: https://edu-tpi.donstu.ru/api/Mail/InboxMail?&id={id}
		Просмотр студентов в группе: https://edu-tpi.donstu.ru/api/Mail/Find/Students?groupID={groupID}
		Поиск студента по ФИО: https://edu-tpi.donstu.ru/api/Mail/Find/Students?fio={fio}
		Поиск преподователя по ФИО: https://edu-tpi.donstu.ru/api/Mail/Find/Prepods?fio={fio}
		Список всех групп в {N-N} учебном году: https://edu-tpi.donstu.ru/api/groups?year={N1}-{N2}
		Информация об аккаунте: https://edu-tpi.donstu.ru/api/tokenauth
		Информация о студенте: https://edu-tpi.donstu.ru/api/UserInfo/Student?studentID=-{studentID}
		Возвращает максимульный/минимальный/текущий день расписания группы GROUP: https://edu-tpi.donstu.ru/api/GetRaspDates?idGroup=GROUP 
		Возвращает расписание группы GROUP с DATE: https://edu-tpi.donstu.ru/api/Rasp?idGroup=GROUP&sdate=DATE
		Возвращает задолженности студента: https://edu-tpi.donstu.ru/api/StudentsDebts/list?studentID={studentID}
		Возвращает ленту пользователя: https://edu-tpi.donstu.ru/api/Feed?userID={userID}&startDate=null
[admin]	Возвращает достижения всех пользователей: https://edu-tpi.donstu.ru/api/Portfolio/Verifier/ListWorks?year={year}&sem=-1&finished={veref}&type={typeVeref}
[admin] Возвращает все файлы приклеплённые к работе: https://edu-tpi.donstu.ru/api/Portfolio/FilesList?workID={workID}

		/POST/
		Авторизация: https://edu-tpi.donstu.ru/Account/Login.aspx
		Отправить сообщение на почту: https://edu-tpi.donstu.ru/api/Mail/InboxMail
[admin]	Создание чата: https://edu-tpi.donstu.ru/api/Chats/Chat


	}
	"""

	def checking_unread_messages(self):
		return requests.get(f"{self.url_api}Mail/CheckMail", headers=self.headers).json()

	def checking_all_mail(self, page: int = 1):
		return requests.get(f"{self.url_api}Mail/InboxMail?page=1&pageEl=15&unreadMessages=false&searchQuery=", headers=self.headers).json()

	def read_mail_message(self, messageID):
		for msg in self.checking_all_mail()['data']['messages']:
			if msg['messageID'] == messageID:
				return requests.get(f"{self.url_api}Mail/InboxMail?id={msg['id']}", headers=self.headers).json()['data']['messages'][0]

	def find_stundent(self, fio):
		return requests.get(f"{self.url_api}Mail/Find/Students?fio={fio}", headers=self.headers).json()

	def find_teacher(self, fio):
		return requests.get(f"{self.url_api}Mail/Find/Prepods?fio={fio}", headers=self.headers).json()

	def all_groups_year(self, year: int = datetime.datetime.now().year):
		return requests.get(f"{self.url_api}groups?year={year}-{year+1}").json()

	def send_message(self, statusID, from_user, title_message, text_message, type_message: int = 1):

		if statusID == 0:
			usertoID = self.find_stundent(fio=from_user)['data']['arrStud']
		elif statusID == 1:
			usertoID = self.find_teacher(fio=from_user)['data']['arrPrep']
		elif statusID == 2:
			pass

		print(usertoID)
		data = {
			"markdownMessage": text_message,
			"htmlMessage": "",
			"message": "",
			"theme": title_message,
			"userToID": usertoID,
			"typeID": type_message,
		}
		req = requests.post(f"{self.url_api}Mail/InboxMail", data=json.dumps(data), headers=self.headers)

	def infoAccount(self):
		return requests.get(f"{self.url_api}tokenauth", headers=self.headers).json()

	def infoUser(self, userID):
		return requests.get(f"{self.url_api}UserInfo/user?userID={userID}", headers=self.headers).json()

	def infoStudent(self, studentID):
		return requests.get(f"{self.url_api}UserInfo/Student?studentID={studentID}", headers=self.headers).json()

	def feed(self, userID):
		return requests.get(f"{self.url_api}Feed?userID={userID}&startDate=null", headers=self.headers).json()

	def studentMark(self, studentID):
		return requests.get(f"{self.url_api}EducationalActivity/StudentAvgMark?studentI={studentID}", headers=self.headers).json()

	def statisticsMarks(self, studentID):
		return requests.get(f"{self.url_api}EducationalActivity/StatisticsMarksCount?studentID={studentID}", headers=self.headers).json()

	def listStudentsDebts(self, studentID):
		return requests.get(f"{self.url_api}StudentsDebts/list?studentID={studentID}", headers=self.headers).json()

	def journalList(self):
		return requests.get(f"{self.url_api}Journals/JournalList", headers=self.headers).json()

	def createChat(self, nameChat):
		data = {
			"channel": False,
			"chatUsers": [],
			"description": "",
			"name": nameChat,
		}

		res = requests.post(f"{self.url_api}Chats/Chat", data=json.dumps(data), headers=self.headers)
		return res.text

	def listWorks(self, typeVeref):
		# https://edu-tpi.donstu.ru/api/Portfolio/Verifier/ListWorks?year={year}&sem=-1&finished={veref}&type={typeVeref}
		return requests.get(f"{self.url_api}Portfolio/Verifier/ListWorks?finished=false&type={typeVeref}", headers=self.headers).json()

	def filesList(self, workID):
		return requests.get(f"{self.url_api}Portfolio/FilesList?workID={workID}", headers=self.headers).json()
	# https://edu-tpi.donstu.ru/api/Portfolio/FilesList?workID=9020

class Rasp(SettingsClass):

	def infoRasp(self, groupID, sdate = datetime.datetime.now().strftime("%Y-%m-%d")):
		return requests.get(f"{self.url_api}Rasp?idGroup={groupID}&sdate={sdate}", headers=self.headers).json()

	def GroupsRasp(self):
		return requests.get(f"{self.url_api}raspGrouplist", headers=self.headers).json()

	def AudRasp(self, audCode, sdate = datetime.datetime.now().strftime("%Y-%m-%d")):
		return requests.get(f"{self.url_api}Rasp?idAudLine={audCode}&sdate={sdate}",headers=self.headers).json()

	def AudsRasp(self):
		return requests.get(f"{self.url_api}raspAudlist", headers=self.headers).json()

	def infoRaspTeacher(self, teacherID, sdate = datetime.datetime.now().strftime("%Y-%m-%d") ):
		return requests.get(f"{self.url_api}Rasp?idTeacher={teacherID}&sdate={sdate}", headers=self.headers).json()

	def TeachersRasp(self):
		return requests.get(f"{self.url_api}raspTeacherlist", headers=self.headers).json()

# https://edu-tpi.donstu.ru/api/UserInfo/user?userID=1172
class Account:

	def __init__(self, email, password = None):
		self.email = email
		self.password = password
		self.auth_url = 'https://edu-tpi.donstu.ru/Account/Login.aspx'
		self.data = {
			"__VIEWSTATE": "/wEPDwULLTE5Njc0MjQ0ODAPZBYCZg9kFgICAw9kFggCAQ88KwAKAgAPFgIeDl8hVXNlVmlld1N0YXRlZ2QGD2QQFgFmFgE8KwAMAQAWBh4EVGV4dAUO0JPQu9Cw0LLQvdCw0Y8eC05hdmlnYXRlVXJsBQ5+L0RlZmF1bHQuYXNweB4OUnVudGltZUNyZWF0ZWRnZGQCCw8WAh4JaW5uZXJodG1sBTrQrdC70LXQutGC0YDQvtC90L3QvtC1INC/0L7RgNGC0YTQvtC70LjQviDRgdGC0YPQtNC10L3RgtCwZAINDzwrAAkCAA8WAh8AZ2QGD2QQFgFmFgE8KwALAQAWCh8BZR4ETmFtZQUCZ2gfAmUeBlRhcmdldGUfA2dkZAIRDzwrAAQBAA8WAh4FVmFsdWUFHTIwMjEgwqkgQ29weXJpZ2h0IGJ5IE1NSVMgTGFiZGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgMFD2N0bDAwJEFTUHhNZW51MQURY3RsMDAkQVNQeE5hdkJhcjEFKmN0bDAwJE1haW5Db250ZW50JHVjTG9naW5Gb3JtUGFnZSRidG5Mb2dpbj6AgDxOZVnZwij5bL/VFy59O/phPxVn2KrrW7LSWHWF", "ctl00$MainContent$ucLoginFormPage$btnLogin": "(unable to decode value)",

			"ctl00$MainContent$ucLoginFormPage$tbUserName$State": "{&quot;rawValue&quot;:&quot;"+self.email+"&quot;,&quot;validationState&quot;:&quot;&quot;}",
			"ctl00$MainContent$ucLoginFormPage$tbPassword$State": "{&quot;rawValue&quot;:&quot;"+self.password+"&quot;,&quot;validationState&quot;:&quot;&quot;}",
			"ctl00$MainContent$ucLoginFormPage$tbUserName": self.email,
			"ctl00$MainContent$ucLoginFormPage$tbPassword": self.password, 
		}

	def auth(self):
		s = requests.Session()
		req = s.post(self.auth_url, data=self.data)
		try:
			if s.cookies.items()[2][1]: 
				authToken = s.cookies.items()[2][1]
				s.cookies.clear()
				return authToken
			else: return False
		except IndexError as e:
			return False