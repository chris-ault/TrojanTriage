# Log file located at :  C:\ProgramData\AVG\Antivirus\chest

import xmltodict
with open('index.xml') as fd:
    doc = xmltodict.parse(fd.read())
    x = 0
    for x in range(len(doc['aswObject']['ChestEntry'])):
        print doc['aswObject']['ChestEntry'][x].get('ChestId'), doc['aswObject']['ChestEntry'][x].get('Virus')
        print doc['aswObject']['ChestEntry'][x].get('OrigFileName').split('_')[1] +'\n'

