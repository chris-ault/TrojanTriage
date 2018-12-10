
SELECT @@innodb_buffer_pool_size/1024/1024; 

# BIG InnoDB 4GB
# SET GLOBAL innodb_buffer_pool_size=4000000000; # or .75  SET GLOBAL innodb_buffer_pool_size=3000000000;
# Small InnoDB 512MB
SET GLOBAL innodb_buffer_pool_size=536870912;

SELECT @@innodb_buffer_pool_size/1024/1024; 
