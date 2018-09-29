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
defenderOutput = "VirusShare_CryptoRansom_20160715.txt"
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
# types = ["Known Bad", "Behavior", "Unknown", "Known Good", "NRI"]
# severities = ["Unknown","Low","Moderate","High","Severe"]


def checkHash(hashToTest):
    if (len(hashToTest) == 32):
        return True
    else:
        print "Bad hash: " + str(hashToTest) + "has " + str(len(hashToTest))

inserts = 0
entry = 0
fileLocations = ''
fileLocGroup, badFiles, fileHashes = ([] for i in range(3))

with open(defenderOutput) as fp:
    # print "Element #:" + str(entry)
    for line in fp:
            parts = [line[:16].strip(), line[19:].strip()]
            # print parts[0:]
            # The front part is empty but the back has something
            if not len(parts[0]):
                fileLocations = fileLocations + parts[1]
            else:
                if parts[0].strip() == "CategoryID":
                    # Store Category ID
                    if int(parts[1]) > 47:
                        category = "undefined"
                    else:
                        category = catID[int(parts[1])]
                        # print category
                if parts[0].strip() == "Resources":
                    fileLocations = fileLocations + parts[1]
                if parts[0].strip() == "RollupStatus":
                    curRollup = parts[1].strip()
                    # print "Roll up " + parts[1].strip()
                if parts[0].strip() == "SchemaVersion":
                    curSchema = parts[1].strip()
                    # print "schema " + parts[1].strip()
                if parts[0].strip() == "SeverityID":
                    curSeverity = parts[1].strip()
                    # print 'Severity ' + parts[1].strip()
                if parts[0].strip() == "ThreatID":
                    curID = parts[1].strip()
                    # print "ThreatID " + parts[1].strip()
                if parts[0].strip() == "ThreatName":
                    # print "Threat name is " + parts[1].strip()
                    # Check to see if name is short
                    if ':' not in parts[1]:
                        threatName = parts[1].strip('!').split('_')
                        threatType = threatName[0]
                        threatSub = threatName[1]
                        OS = 'UNKNOWN'
                    else:
                        threatName = parts[1].split(':')
                        temp = threatName[1].split('/')
                        OS = temp[0].strip()
                        threatSub = temp[1].strip()
                        threatType = threatName[0].strip()

                    # Split multi line and check hashes
                    locationsGroup = fileLocations.split(',')
                    for single in locationsGroup:
                        # print single
                        containerCheck = 1
                        # Dangerous while loop
                        while len(single.rsplit('_', containerCheck)[1]) < 32:
                            containerCheck = containerCheck + 1
                            if containerCheck > 5:
                                break
                        testHash = single.rsplit('_', containerCheck)[1].split("-")[0].strip("}").strip("...")
                        if checkHash(testHash):
                            fileHashes.append(testHash)
                            fileLocGroup.append(single.strip('{').strip('}').strip("..."))
                        else:
                            badFiles.append(single)
                    entry = entry + 1
                    print "Element #:" + str(entry)
                    i = 0
                    for i in range(len(fileHashes)):
                        if checkHash(fileHashes[i]):
                            print "Vars: " + str((curSeverity, threatType, OS, category, curRollup, curSchema, curID))
                            print "hash:", fileHashes[i]
                            print "location:", fileLocGroup[i]
                            # raw_input()
                            sql = "UPDATE element SET severity=%s, type=%s, OS=%s, CategoryID=%s, Rollupstatus=%s, Schemaversion=%s, threatID=%s, Location=%s, subType=%s WHERE HASH=%s"
                            val = (curSeverity, threatType, OS, category, curRollup, curSchema, curID, fileLocGroup[i], threatSub, fileHashes[i])
                            try:
                                mycursor.execute(sql, val)
                                inserts = inserts + mycursor.rowcount
                            except mysql.connector.Error as err:
                                print err.msg
                                print fileHashes[i] + " Already exists"
                            #raw_input()
                        else:
                            print "Bad hash, not even trying " + str(fileHashes[i]) + "is " + str(len(fileHashes[i]))
                    # Reset everything 
                    fileLocations = ''
                    locationsGroup = []
                    del fileHashes[:]
                    del fileLocGroup[:]
print "Bad files not added " + str(badFiles)
print(inserts, " hash record inserted.")
mydb.commit()

fp.close()
