# https://www.quora.com/How-do-I-write-multiple-select-queries-in-a-single-query-in-MySQL
SELECT 
    t1.hashCount, t2.unpackedHashesCount, t3.AVScannedAndParsed, t4.HashesParsed4dlls, t5.DLLsTotal
FROM
    (SELECT FORMAT(COUNT(HASH), 0) 
    AS hashCount
    FROM element
    WHERE NOT (HASH IS NULL)) AS t1,
    
    (SELECT FORMAT(COUNT(unpackedMD5), 0)
    AS unpackedHashesCount
    FROM element
    WHERE NOT (unpackedMD5 IS NULL)) AS t2,
    
    (SELECT FORMAT(COUNT(Location), 0) 
    AS AVScannedAndParsed
    FROM element
    WHERE NOT (Location IS NULL)) AS t3,
    
    (SELECT FORMAT(COUNT(Hash), 0) 
    AS HashesParsed4dlls
    FROM malware2dll) AS t4,
    
	(SELECT FORMAT(COUNT(dll_name), 0) 
    AS DLLSTotal
    FROM dlltable) AS t5;			