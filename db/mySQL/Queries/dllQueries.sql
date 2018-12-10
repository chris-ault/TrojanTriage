# These are queries for understanding results from the database

# This picks out unique category malwares but is incomplete
#select distinct CategoryID, count(*), dlltable malware2dll from element where not (CategoryID is NULL) group by CategoryID order by count(*) desc;

#select malware_dll_id, count(*) as count 
#from malware2dll 
#GROUP BY malware_dll_id 
#order by count desc;

# Counts DLLS per hash
#select hash,count(malware_dll_id) from malware2dll group by hash order by count(malware_dll_id) desc;

# Count hashes per dll
select malware_dll_id,count(hash) from malware2dll
group by malware_dll_id 
order by count(hash) desc;

# Count samples per specified DLL
#select count(*) from malware2dll where malware_dll_id = '9';

# Find all samples that have dll and defender results (type)
select * from element a
INNER JOIN malware2dll m on a.hash=m.Hash
where not (a.type is null);

# Show DLL Name along with count of samples per DLL
# "Top 10 Most commonly used DLL's by malware"
select t.dll_name, count(*) from malware2dll d
INNER JOIN dlltable t on t.malware_dll_id=d.malware_dll_id
group by t.dll_name
order by count(*) desc
limit 10;

# Number of linked DLL's to Hashes
select Count(hash) from malware2dll;