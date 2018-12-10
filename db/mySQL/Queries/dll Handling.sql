# These are Queries for insertion and handling specific dll table things


# DLL DB Creation ----------------------
# Create DLL Entry
#INSERT INTO dlltable (dll_name) VALUES ('myFirstDll.dll');
# Connect DLL Entry to malware
#INSERT INTO malware2dll (Hash, malware_dll_id) VALUES ('# http://VirusShare.com        #', '1')

# DLL DB Lookups ----------------------
# Lookup malware that has dll at position 1
# This is broken
# select a.*
# FROM malware a
# INNER JOIN malware2dll m2d
# on a.hash = m2d.hash
# where m2d.malware_dll_id = 1;

# Find DLL's on given hash
select dll_name from dlltable d 
INNER JOIN malware2dll m
on d.malware_dll_id=m.malware_dll_id 
where hash='bbeb594f4fc4d3ef1802e1b0a935214f';


# Find a DLL ID
# select malware_dll_id,dll_name from dlltable where dll_name = '%s';

# select count(malware_dll_id) from malware2dll;