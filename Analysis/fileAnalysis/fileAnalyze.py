#!/usr/bin/python

# Runs File Command and dissassembly finding entry point on passed argument file
# Usage: python fileAnalyze.py questionableFileToTest.exe
# Result: Appends file type, hash[sha1], entry point, bytes to output file [fileTypes.txt]
#
# OS: Windows
# Requires: GnuWin32 file.exe 
#
# ERROR NEEDS CATCH FOR SPACES IN FILENAME
#
import os
import sys              # https://stackoverflow.com/questions/6591931/getting-file-size-in-python
import hashlib
import pefile           # https://github.com/erocarrera/pefile/blob/wiki/UsageExamples.md#introduction
import subprocess
from capstone import *  # https://stackoverflow.com/questions/36959122/capstone-disassemble-from-binary-file-in-python


fileCmd = """C:\\Program Files (x86)\\GnuWin32\\bin\\file.exe"""
output = "fileTypes.txt"
# Learning ASM
# https://stackoverflow.com/questions/34564542/understanding-these-assembly-instructions
# DeptOfDef PE File Github
# https://github.com/deptofdefense/SalSA/wiki/PE-File-Format
# Capstone Tut
# https://www.capstone-engine.org/lang_python.html

# BUF_SIZE is totally arbitrary, change for your app! Used for hash calculation
BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
location = sys.argv[1]


print "file is : " + location
# print "size is : " + str(convert_bytes(os.path.getsize(location)))

def add2db(hash, attribList):
    #print "Updating Database for element MD5:"+hash+"\nentry point, firstInstruction, bytes, SHA1"
    g.write(str(attribList) + '\n')
    print attribList
    #for x in attribList:
    #    print x.ljust(20)


atribs=[]
md5 = hashlib.md5()
sha1 = hashlib.sha1()

g= open(output,"a+")
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
    print("ERROR: %s" % e)
    pass
attribs.append(str(os.path.getsize(location)))
attribs.append(sha1.hexdigest())

output = subprocess.check_output([fileCmd,'-b', location])
mime = subprocess.check_output([fileCmd,'-bi', location])
attribs.append(output.strip() + "," + mime.strip() + "," + md5.hexdigest() + "," +  sha1.hexdigest())



add2db(md5.hexdigest(),attribs)
#print "\nEND"
g.close()
