# TrojanTriage
This project is built to organize a collection of malware in order to gain knowledge from commonalities between certain pieces of malware.


The front end utilizes Django & Django ORM operations on the mySQL database
The data stored in the mySQL database is pulled from multiple major antivirus databases as well as local research.
The log malware scan log files are processed with python.


The Trojan Triage process consists of 3 main parts.
-------
The mySQL database provides storage for the malware information. [make tables](https://github.com/chris-ault/TrojanTriage/tree/master/db/mySQL/TableBuildingScripts/Database_Creation_Automation)

The Django interface provides a front end for viewing and sorting the malware samples.[database views interface](https://github.com/chris-ault/TrojanTriage/tree/master/FrontEnd/Django_Guis/Database_Views_Interface)

The VMAutomation portion providing malware information collection.[python scripts](https://github.com/chris-ault/TrojanTriage/tree/master/VMautomation)

[Django interface for displaying databases](https://github.com/chris-ault/TrojanTriage/tree/master/FrontEnd/Django_Guis/Database_Views_Interface)
<a href="https://github.com/chris-ault/TrojanTriage/tree/master/FrontEnd/Django_Guis/Database_Views_Interface">![Image of Django database page](https://github.com/chris-ault/TrojanTriage/blob/master/FrontEnd/Django_Guis/Database_Views_Interface/typePage.png)</a>
------------
[Django interface for Cuckoo uploads](https://github.com/chris-ault/TrojanTriage/tree/master/FrontEnd/Django_Guis/Cuckoo_JSON_fileUpload_Interface)
<a href="https://github.com/chris-ault/TrojanTriage/tree/master/FrontEnd/Django_Guis/Cuckoo_JSON_fileUpload_Interface">![Image of Django backend result](https://github.com/chris-ault/TrojanTriage/blob/master/FrontEnd/Django_Guis/Cuckoo_JSON_fileUpload_Interface/cuckoo_parsed_result.PNG)</a>

![Image of Flask GUI](https://github.com/chris-ault/TrojanTriage/blob/master/flask.JPG)
------------
![Image of SQL Results](https://github.com/chris-ault/TrojanTriage/blob/master/sql.JPG)

This database is for educational purposes only.
