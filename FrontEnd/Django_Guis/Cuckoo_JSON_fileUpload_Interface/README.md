Cuckoo_Json_fileUpload_Interface
==================================

The goal with Cuckoo_JSON_fileUpload_Interface is to provide a web page for Cuckoo file analysis submissions to be parsed and submitted to the databse with Python and Django.
![Upload Results](https://github.com/chris-ault/TrojanTriage/blob/master/FrontEnd/Django_Guis/Cuckoo_JSON_fileUpload_Interface/cuckoo_parsed_result.PNG)

Usage (Django 1.9)
------------------
First ensure you have installed the following:

	Django==1.11.15
	mysqlclient==1.3.13
	pytz==2018.5

Then:

    $ git clone https://github.com/chris-ault/TrojanTriage/tree/master/FrontEnd/Django_Guis/Parrot_JSON_fileUpload_Interface
	$ cd Parrot_JSON_fileUpload_Interface
	$ cd myproject
	$ python manage.py migrate
	$ python manage.py runserver localhost:8000
	Open a browser point to localhost:8000/type/

This long query to load this initial page will take between 20-60 seconds as it is counting all the malware samples and sorting them.  You will be presented with a sorted list of malware types and counts of identefied infected malware samples in the database.

Selecting a 'Type' name such as Trojan will take you to http://localhost:8000/type/details/Trojan/severity/.  Here you will see all samples of infected malware that have been parsed with the type titled 'Trojan'. Selecting "DLLs" will take you to the analysis of that specific sample showing detailed information on which DLL filenames that sample requested.  From the 'Virus Type' page select a hash of a sample to be taken to virustotal to see online scan results of that specific sample.  Choosing 'Street Name' will direct you to Microsofts description of that paticular malware type.