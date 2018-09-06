import mysql.connector
import re
#from mysql.connector import errorcode
#from mysql.connector.errors import Error
#
#
# TODO:
# Enumerate Severity and type id
# https://docs.microsoft.com/en-us/previous-versions/windows/desktop/defender/msft-mpthreat
#

# File to import from
defenderOutput = "mbamResult2.txt"
print "Starting Mbam processing of: " + defenderOutput + '\n'
# mydb = mysql.connector.connect(
#     host="localhost",
#     user="user",
#     passwd="password",
#     database="malwareDB"
# )
# mycursor = mydb.cursor()

#catID = []
#types = ["Known Bad", "Behavior", "Unknown", "Known Good", "NRI"]
#severities = ["Unknown","Low","Moderate","High","Severe"]
entry = 0
fileHashes = []
fileLocations = []
with open(defenderOutput) as fp:
    # print "Element #:" + str(entry)
    inFiles = False
    for line in fp:
        Type = ''
        subType = ''
        StreetName = ''
        location = ''
        # Find where files start
        if str(line).startswith("File:"):
            inFiles = True
            x = line.split(" ")[1].strip()
            print "Found " + str(x) + " number of files"
        if inFiles:
            newLine = line.split(', ')
            print newLine
            if len(newLine) > 4:
                newLine = newLine.split(',')
                print newLine[0]
                Type = newLine[0].split('.')[0]
                #updatePackage = newLine[-1].split(',')[1].strip()
                print "Type" + Type + "\n\t" + location + '\n'
            if newLine[0].startswith("Physical"):
                # inFiles = False
                print "Done"
                break
        if str(line).startswith("File:") & !inFIles:
            inFiles = True
            x = line.split(" ")[1].strip()
            print "Found " + str(x) + " number of files"
        
fp.close()
