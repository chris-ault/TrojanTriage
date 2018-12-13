
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


# TODO
# Currently this adds directly to DB with no flat file inbetween
# DB Loss results in parsing needing to be done again
# Less DB Commit = More Speed!
import mysql.connector
import hashlib
import pefile
import glob


mydb = mysql.connector.connect(
    host="localhost",
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
    # This commit should not be removed, lookupAndInsert will depend on the above Insert to exist before returning to main
    mydb.commit()
    print "dll made return to lookupInsert"
    lookupAndInsert(hash, dllName)


# BUF_SIZE is totally arbitrary, change for your app!
BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

md5 = hashlib.md5()
# Iterate over all files in this DIR
for file in glob.glob('*'):
    with open(file, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)
    print(md5.hexdigest())
    # Check if PE Parsable
    try:
        pe = pefile.PE(file)
        for entry in pe.DIRECTORY_ENTRY_IMPORT:
            # Check if already exists or can insert
            try:
                lookupAndInsert(str(md5.hexdigest()), str(entry.dll.decode('utf-8')))
            except mysql.connector.Error as err:
                pass
        # Consider placing Db Commit here
        # And Removing from DEF
    except (pefile.PEFormatError, AttributeError):
        pass
print "done"
