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
defenderOutput = "test.txt"
print "Starting processing of :" + defenderOutput
mydb = mysql.connector.connect(
    host="localhost",
    user="user",
    passwd="password",
    database="malwareDB"
)
mycursor = mydb.cursor()
catID = ["invalid", "adware", "spyware",
         "passwordstealer", "trojandownloader",
         "worm", "backdoor",
         "remoteaccesstrojan",
         "trojan", "emailflooder",
         "KEYLOGGER", "DIALER", "MONITORINGSOFTWARE",
         "BROWSERMODIFIER", "COOKIE",
         "BROWSERPLUGIN", "AOLEXPLOIT",
         "NUKER", "SECURITYDISABLER"
         "JOKEPROGRAM", "HOSTILEACTIVEXCONTROL",
         "SOFTWAREBUNDLER", "STEALTHNOTIFIER",
         "SETTINGSMODIFIER", "TOOLBAR",
         "REMOTECONTROLSOFTWARE", "TROJANFTP",
         "POTENTIALUNWANTEDSOFTWARE", "ICQEXPLOIT",
         "TROJANTELNET", "FILESHARINGPROGRAM",
         "MALWARE_CREATION_TOOL", "REMOTE_CONTROL_SOFTWARE",
         "TOOL", "TROJAN_DENIALOFSERVICE",
         "TROJAN_DROPPER", "TROJAN_MASSMAILER",
         "TROJAN_MONITORINGSOFTWARE", "TROJAN_PROXYSERVER",
         "VIRUS", "KNOWN", "UNKNOWN", "SPP",
         "BEHAVIOR", "VULNERABILTIY", "POLICY"
         ]
#types = ["Known Bad", "Behavior", "Unknown", "Known Good", "NRI"]
#severities = ["Unknown","Low","Moderate","High","Severe"]
entry = 0
fileHashes = []
fileLocations = []
with open(defenderOutput) as fp:
    # print "Element #:" + str(entry)
    for line in fp:
        # This strips newlines between entries and catches /
        # white space before "  Resources"
        if re.match(r'[^\S\n\t]+', line.rstrip('/r/n')):
            print "Found other resources:"
            fileLocation = line.strip().strip(",").strip("...}")
            fileLocations.append(fileLocation)
            print fileLocations
            fileHashes.append(fileLocation.split('_', 2)[-1].split("-")[0].strip("}"))
            print fileHashes
            # print line.strip().strip('}')
        else:
            currentline = line.split(':', 1)
            if currentline[0].strip() == "CategoryID":
                # Store Category ID
                if int(currentline[1]) > 47:
                    category = "undefined"
                else:
                    category = catID[int(currentline[1])]
                    #print category
            if currentline[0].strip() == "Resources":
                fileLocation1 = currentline[1].strip().strip('{').strip(',').strip("}")
                fileLocations.append(fileLocation1)
                fileHashes.append(fileLocation1.split('_', 2)[-1].split("-")[0])
            if currentline[0].strip() == "RollupStatus":
                curRollup = currentline[1].strip()
                # print "Roll up " + currentline[1].strip()
            if currentline[0].strip() == "SchemaVersion":
                curSchema = currentline[1].strip()
                # print "schema " + currentline[1].strip()
            if currentline[0].strip() == "SeverityID":
                curSeverity = currentline[1].strip()
                # print 'Severity ' + currentline[1].strip()
            if currentline[0].strip() == "ThreatID":
                curID = currentline[1].strip()
                # print "ThreatID " + currentline[1].strip()
            if currentline[0].strip() == "ThreatName":
                # print "Threat name is " + currentline[1].strip()
                threatName = currentline[1].split(':')
                temp = threatName[1].split('/')
                OS = temp[0].strip()
                threatSub = temp[1].strip()
                threatType = threatName[0].strip()
                # print "Os:" + OS + " type:" + threatType + " subtype:" /
                #     + threatSub
                entry = entry + 1
                print "Element #:" + str(entry)                
                i = 0
                for i in range(len(fileHashes)):
                    print "Vars: " + str((curSeverity, threatType, OS, category, curRollup, curSchema, curID))
                    print ("hash:",fileHashes[i], "location:",fileLocations[i])
                    # raw_input()
                    sql = "INSERT INTO element (severity, type, OS, CategoryID, Rollupstatus, Schemaversion, threatID, HASH, Location, subType) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    val = (curSeverity, threatType, OS, category, curRollup, curSchema, curID, fileHashes[i], fileLocations[i], threatSub)
                    try:
                        mycursor.execute(sql, val)
                        mydb.commit()
                        print(mycursor.rowcount, " hash record inserted.")                        
                    except mysql.connector.Error as err:
                        print err.msg
                        print fileHashes[i] + " Already exists"
                        #raw_input()
                del fileHashes[:]
                del fileLocations[:]

fp.close()
