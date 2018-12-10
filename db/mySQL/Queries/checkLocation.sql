# This query results in no rows assuming all files start with "file" or "container"
SELECT * 
FROM element
 where (location  REGEXP '^[ -B].*$' OR location  REGEXP '^[D-E].*$' OR location  REGEXP '^[G-Z].*$')