#select malware_dll_id,count(hash) 
#from malware2dll 
#group by malware_dll_id 
#order by count(hash) 
#desc limit 10 ;


SELECT  a.dll_name, count(c.Hash)
FROM dlltable a 
    INNER JOIN malware2dll c
        ON a.malware_dll_id = c.malware_dll_id
			group by a.malware_dll_id
            order by count(c.hash) desc;