
# dll Linking Process
# Seek for dll entry
# select malware_dll_id,dll_name from dlltable where dll_name = '%s';
# If Exists dll_id
# Use ID while inserting
# INSERT INTO malware2dll (Hash, malware_dll_id) VALUES (hash, dll_id)
# else
# Create DLL entry
# INSERT INTO dlltable (dll_name) VALUES ('myFirstDll.dll');
# Repeat above process
####################################################################
#
# To empty TRUNCATE TABLE tablename;`
import mysql.connector
import hashlib
import pefile
import glob


mydb = mysql.connector.connect(
    #host="localhost",
    host="10.37.92.133",
    user="user",
    passwd="password",
    database="malwareDB"
)
mycursor = mydb.cursor()


def lookupAndInsert(hash, dllName):
    print "Seeking " + dllName + " ID"
    dllID = 0
    n = mycursor.execute("""select malware_dll_id from dlltable where dll_name = '%s'""" % (dllName))
    c = mycursor.fetchall()

    for i in c:
        if i[0]:
            dllID = i[0]
    if dllID:
        print "dll exists, using ID: " + str(dllID) + " to add to mal2dll table"
        mycursor.execute("""INSERT INTO malware2dll (Hash, malware_dll_id) VALUES ('%s', '%s')""" % (hash, dllID))
        mydb.commit()
    else:
        print "no dll"
        createNewDll(hash, dllName)


# This takes hash so it can return to lookupAndInsert the thing it was passed
# ovbiously a better way to do this but
def createNewDll(hash, dllName):
    print "make this new dll"
    mycursor.execute("""INSERT INTO dlltable (dll_name) VALUES ('%s')""" % (dllName))
    mydb.commit()
    print "dll made return to lookupInsert"
    lookupAndInsert(hash, dllName)


# BUF_SIZE is totally arbitrary, change for your app!       
BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

md5 = hashlib.md5()
for file in glob.glob('*'):
    with open(file, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)
    print(md5.hexdigest())
    try:
        pe = pefile.PE(file)
        for entry in pe.DIRECTORY_ENTRY_IMPORT:
            try:
                lookupAndInsert(str(md5.hexdigest()), str(entry.dll.decode('utf-8')))
            except mysql.connector.Error as err:
                pass
    except (pefile.PEFormatError, AttributeError):
        pass
print "By God I Think We Might Have Done It"
