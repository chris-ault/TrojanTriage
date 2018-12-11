Database_Views_Interface
==================================

The goal with Database_Views_interface is to display a mySQL database of multiple tables with information about malware with Django.
![Type Page](https://github.com/chris-ault/TrojanTriage/blob/master/FrontEnd/Django_Guis/Database_Views_Interface/typePage.png)

Usage (Django 1.9)
------------------
First ensure you have installed the following:

Django==1.11.16
mysqlclient==1.3.13
(optional)
(mysql-connector==2.1.6)
(certifi==2018.8.24)
(pipenv==2018.7.1)
(pytz==2018.7)
(pywin32==223)
(virtualenv==16.0.0)
(virtualenv-clone==0.3.0)
(virtualenvwrapper-win==1.2.5)

Then:

	git clone https://github.com/chris-ault/TrojanTriage/tree/master/FrontEnd/Django_Guis/Database_Views_Interface
	cd Database_Views_Interface
	python manage.py migrate
	python manage.py runserver localhost:8001
