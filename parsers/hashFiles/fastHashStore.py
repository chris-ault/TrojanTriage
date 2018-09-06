# https://stackoverflow.com/questions/6591931/getting-file-size-in-python
import sys
from os import walk
import mysql.connector
import time
from datetime import datetime, timedelta
# this must be run like so mysql -u user -p mydatabase --local-infile=1
mydb = mysql.connector.connect(
    host="localhost",
    user="user",
    passwd="password",
    database="malwaredb",
    connect_timeout=1000
)

mycursor = mydb.cursor()

mypath = '.'
f = []
for (dirpath, dirnames, filenames) in walk(mypath):
    f.extend(filenames)
    break
f.remove(sys.argv[0])
f.remove('element.ibd')
# f.remove('storeWalk.py')

# Adjust List for request
targetList = f[(f.index(sys.argv[1])):(f.index(sys.argv[2]) + 1)]
print "Files to add: " + str(targetList)

# Calculate lines and store file line array
linecount = 0
linearray = []
for x in targetList:
    num_lines = sum(1 for line in open(x))
    linearray.append(num_lines)
    linecount = linecount + num_lines
    print str(num_lines) + " lines in file " + x
print "Total lines to process = " + str(linecount)
sql = " LOAD DATA INFILE %s IGNORE INTO TABLE element FIELDS TERMINATED BY '\n' (HASH);"
badList = []
for x in targetList:
    speed = 0.00
    print "\nWorking on " + x + " at " + str(datetime.now().time().replace(microsecond=0))
    print "This file etc " +str(float(linearray[targetList.index(x)]) / (600.00*60)) + " minutes"
    a = time.clock()
    target = x
    try:
        mycursor.execute(sql, (target,))
        mydb.commit()
    except mysql.connector.Error as err:
        print err.msg
        badList.append(target)
    b = time.clock()
    seconds = b - a
    # speed = float(lines / fl(seconds
    speed = float(linearray[targetList.index(x) - 1]) / float(seconds)
    print "Took: " + str(seconds) + " sec @ speed " + str(float(speed)) + " lines / sec"
    remainder = sum(linearray[targetList.index(x)+1:])
    minutes = float(remainder) / (float(speed) * 60.0)
    hours = float(minutes) * 60.0
    # if hours < 1 print minutes display
    if hours < 1.00:
        print "ETC " + str(minutes) + " Minutes"
    else:
        print "ETC " + str(hours) + " Hours"
        hours_from_now = datetime.now() + timedelta(hours=hours)
        print (format(hours_from_now, '%H:%M:%S'))
print "Incomplete files: " + str(badList)
