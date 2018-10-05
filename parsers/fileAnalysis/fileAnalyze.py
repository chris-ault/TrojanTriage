#!/usr/bin/python

#
# ERROR HANDLING DONE, nEEDS CATCH FOR SPACES IN FILENAME
#
import os
import sys              # https://stackoverflow.com/questions/6591931/getting-file-size-in-python
import hashlib
import pefile           # https://github.com/erocarrera/pefile/blob/wiki/UsageExamples.md#introduction
import subprocess
from capstone import *  # https://stackoverflow.com/questions/36959122/capstone-disassemble-from-binary-file-in-python


fileCmd = "C:\\Users\\captn\\Documents\\CyberInternship\\Resources\\GnuWin32\\bin\\file.exe"

# Learning ASM
# https://stackoverflow.com/questions/34564542/understanding-these-assembly-instructions
#DeptOfDef PE File Github
# https://github.com/deptofdefense/SalSA/wiki/PE-File-Format
# Capstone Tut
# https://www.capstone-engine.org/lang_python.html
# BUF_SIZE is totally arbitrary, change for your app!
BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
location = sys.argv[1]
# https://stackoverflow.com/questions/2104080/how-to-check-file-size-in-python
def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0
print "file is : " + location
#print "size is : " + str(convert_bytes(os.path.getsize(location)))

def add2db(hash, attribList):
    #print "Updating Database for element MD5:"+hash+"\nentry point, firstInstruction, bytes, SHA1"
    g.write(attribList[4] + '\n')
    #for x in attribList:
    #    print x.ljust(20)


atribs=[]
md5 = hashlib.md5()
sha1 = hashlib.sha1()

g= open("fileTypes.txt","a+")
with open(location, 'rb') as f:
    while True:
        data = f.read(BUF_SIZE)
        if not data:
            break
        md5.update(data)
        sha1.update(data)
try:
    attribs = []
    pe = pefile.PE(location, fast_load=True)
    #print "Entry Point: " + hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint)
    attribs.append(hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint))
except pefile.PEFormatError as a:
    attribs.append("NULL")
    attribs.append("NULL")
    #print "Bad Entry Point"
file = open(location, 'rb')
CODE = file.read()
#print("MD5: {0}".format(md5.hexdigest()))
#print("SHA1: {0}".format(sha1.hexdigest()))
first = True
try:
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    for i in md.disasm(CODE, pe.OPTIONAL_HEADER.AddressOfEntryPoint):
        #print "0x%x:\t%s\t%s" % (i.address, i.mnemonic, i.op_str)
        if first:
            #print (hex(i.address))
            attribs.append(hex(i.address))
        first = False
except NameError as e:
    #print("ERROR: %s" % e)
    pass
attribs.append(str(os.path.getsize(location)))
attribs.append(sha1.hexdigest())

output = subprocess.check_output([fileCmd, location])
attribs.append(output.split(';')[1].strip())



add2db(md5.hexdigest(),attribs)
#print "\nEND"
g.close()
