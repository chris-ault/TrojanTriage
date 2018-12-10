
import mysql.connector
import sys
#
## Takes (1) arg of file name of hash list file, new line separated comments ok
#
mydb = mysql.connector.connect(
    host="localhost",
    user="user",
    passwd="password",
    database="malwareDB"
)
mycursor = mydb.cursor()
fileinput = sys.argv[1]

num_lines = sum(1 for line in open(fileinput))
print "Number of total lines " + str(num_lines)
raw_input()
cur = 0
with open(fileinput) as fp:
    for line in fp:
        cur += float(1)
        line = line.partition('#')[0]
        line = line.rstrip()
        # Insert into element 'HASH' value 'line.replace('\n', '')'
        fhash = line.replace('\n', '')
        if fhash:
            print "Store:" + fhash
            sql = "INSERT INTO element (HASH) VALUES (%s)"
            val = (fhash)
            try:
                mycursor.execute(sql, (val,))
                mydb.commit()
            except mysql.connector.Error as err:
                            print err.msg
                            #print fhash + " Already exists"
                            #raw_input()
            print str(cur) + "/" + str(num_lines) + " " + str(cur/num_lines*100) + "% complete"
    fp.close()
