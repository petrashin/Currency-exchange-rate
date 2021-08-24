import requests
from bs4 import BeautifulSoup
import time
import datetime
import smtplib


class Currency:
	Dollar_to_Ruble = "https://www.google.ru/search?q=доллар+к+рублю&newwindow=1&source=hp&ei=2KnMYNOACo2mUMPUqWg&iflsig=AINFCbYAAAAAYMy36P5kG0sch35xPvEhwWroRN6wpgxN&oq=доллар+к+&gs_lcp=Cgdnd3Mtd2l6EAMYADIFCAAQsQMyBQgAELEDMgUIABCxAzIFCAAQsQMyCAgAELEDEMkDMgUIABCxAzICCAAyAggAMgIIADIICAAQsQMQgwE6CAgAEMcBEKMCOgsIABCxAxDHARCjAjoGCAAQChABOgwILhCxAxAKECoQkwI6AgguOgoIABDHARCjAhAKOgQIABAKOgsIABCxAxDHARCvAToFCC4QsQM6BQgAEJIDOgoIABCxAxBGEIICULQGWJ0fYNgmaAJwAHgAgAFNiAHVBZIBAjExmAEAoAEBqgEHZ3dzLXdperABAA&sclient=gws-wiz"
	Euro_to_Ruble = "https://www.google.ru/search?q=евро+к+рублю&newwindow=1&ei=irrMYNWMNZbX3AOVvbRw&oq=евро+к+рублю&gs_lcp=Cgdnd3Mtd2l6EAMyCggAELEDEEYQggIyAggAMggIABCxAxCDATICCAAyAggAMgIIADICCAAyAggAMgIIADICCAA6BAgAEEM6CgguELEDEIMBEEM6BQgAELEDOgoIABCxAxCDARBDOgkIABBDEEYQggI6DAgAELEDEEMQRhCCAjoFCAAQyQM6BQgAEJIDUJsyWM9CYL9EaABwAngBgAHfAYgB-QiSAQYxMS4xLjGYAQCgAQGqAQdnd3Mtd2l6wAEB&sclient=gws-wiz&ved=0ahUKEwjV-aXLvqHxAhWWK3cKHZUeDQ4Q4dUDCA4&uact=5"
	headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.41 Safari/537.36"}

	current_converted_price_of_dollar = 0
	current_converted_price_of_euro = 0
	difference = 0.01 #разница курса

	def __init__(self):
		self.current_converted_price_of_dollar = float(self.get_currency_price_of_dollar().replace(",", "."))
		self.current_converted_price_of_euro = float(self.get_currency_price_of_euro().replace(",", "."))

	def get_currency_price_of_dollar(self):
		full_page = requests.get(self.Dollar_to_Ruble, headers = self.headers)

		soup = BeautifulSoup(full_page.content, "html.parser")

		convert = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})

		return convert[0].text

	def get_currency_price_of_euro(self):
		full_page = requests.get(self.Euro_to_Ruble, headers = self.headers)

		soup = BeautifulSoup(full_page.content, "html.parser")

		convert = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})

		return convert[0].text

	def check_currency(self):
		currency_of_dollar = float(self.get_currency_price_of_dollar().replace(",", "."))
		currency_of_euro = float(self.get_currency_price_of_euro().replace(",", "."))

		if currency_of_dollar >= self.current_converted_price_of_dollar + self.difference:
			self.send_mail_about_dollar_growth()

		elif currency_of_dollar <= self.current_converted_price_of_dollar - self.difference:
			self.send_mail_about_dollar_fall()

		if currency_of_euro >= self.current_converted_price_of_euro + self.difference:
			self.send_mail_about_euro_growth()

		elif currency_of_euro <= self.current_converted_price_of_euro - self.difference:
			self.send_mail_about_euro_fall()

		now = datetime.datetime.now()
		print("В момент времени " + now.strftime("%d-%m-%Y %H:%M") + " " + "курс доллара равен: " + str(currency_of_dollar))
		print("В момент времени " + now.strftime("%d-%m-%Y %H:%M") + " " + "курс евро равен: " + str(currency_of_euro))
		print()

		time.sleep(3)

		self.check_currency()

	def send_mail_about_dollar_growth(self):
		server = smtplib.SMTP("smtp.gmail.com", 587)
		server.ehlo()
		server.starttls()
		server.ehlo()

		server.login("veryjek88282@gmail.com", "Nikita1234")

		subject = "Currency exchange rate"
		body = "Course"
		#body = "Курс доллара вырос больше, чем на 5 рублей"
		message = f'Subject: {subject}\n\n{body}'

		server.sendmail(
			"veryjek88282@gmail.com",
			"petrashin02@bk.ru",
			message
		)
		server.quit()

	def send_mail_about_dollar_fall(self):
		server = smtplib.SMTP("smtp.gmail.com", 587)
		server.ehlo()
		server.starttls()
		server.ehlo()

		server.login("veryjek88282@gmail.com", "Nikita1234")

		subject = "Currency exchange rate"
		body = "Course"
		#body = "Курс доллара упал больше, чем на 5 рублей"
		message = f'Subject: {subject}\n\n{body}'

		server.sendmail(
			"veryjek88282@gmail.com",
			"petrashin02@bk.ru",
			message
		)
		server.quit()

	def send_mail_about_euro_growth(self):
		server = smtplib.SMTP("smtp.gmail.com", 587)
		server.ehlo()
		server.starttls()
		server.ehlo()

		server.login("veryjek88282@gmail.com", "Nikita1234")

		subject = "Currency exchange rate"
		body = "Course"
		#body = "Курс евро вырос больше, чем на 5 рублей"
		message = f'Subject: {subject}\n\n{body}'

		server.sendmail(
			"veryjek88282@gmail.com",
			"petrashin02@bk.ru",
			message
		)
		server.quit()

	def send_mail_about_euro_fall(self):
		server = smtplib.SMTP("smtp.gmail.com", 587)
		server.ehlo()
		server.starttls()
		server.ehlo()

		server.login("veryjek88282@gmail.com", "Nikita1234")

		subject = "Currency exchange rate"
		body = "Course"
		#body = "Курс евро упал больше, чем на 5 рублей"
		message = f'Subject: {subject}\n\n{body}'

		server.sendmail(
			"veryjek88282@gmail.com",
			"petrashin02@bk.ru",
			message
		)
		server.quit()	

currency = Currency()
currency.check_currency()
