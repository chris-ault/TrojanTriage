#
# This script runs inside the VM automating the malware extraction process on any zip files
# Then after the malware is unzipped a defender scan is run on the resulting folder.
# The defender results are stored in the shared folder causing a refresh.
#
# Defender scan log C:\Users\user\AppData\Local\Temp\MpCmdRun.log
#
# Scan Option A:
#   MpCmdRun.exe  -scan -ScanType 3 -file C:\\Users\\user\\Desktop\\output
# Scan Option B:
#   powershell -command Start-MpScan -ScanPath C:\\Users\\user\\Desktop\\scanme -ScanType CustomScan -ThrottleLimit 70
# Store Results(append) :
#   powershell -command Get-MpThreatDetection >> \\\\Vboxsvr\\sharedrive2\\result.txt

import sys
import os.path
import time
import subprocess
import glob

# Input Malware
inputdir = "\\\\Vboxsvr\\sharedrive2\\input"
# Output Results.txt
outdir = "\\\\Vboxsvr\\sharedrive2\\"
# Windows Defender Prefix location
defdir = "C:\\Program Files\\Windows Defender"
# first command offers no throttle limit however disable remediation is good... This is far too slow, seems to be a 30% limit
# in combination with realtime protection disabled
scanCmd = "MpCmdRun.exe -Scan -ScanType 3 -DisableRemediation -File C:\\Users\\user\\Desktop\\scanme"
# scanCmd = "powershell -command Start-MpScan -ScanPath C:\\Users\\user\\Desktop\\scanme -ScanType CustomScan -ThrottleLimit 70"
# Save Results to txt file
storeResultsCmd = "powershell -command Get-MpThreat >> \\\\Vboxsvr\\sharedrive2\\resultpause.txt"
# This is brokenErase any old results
# This command is broken Clean MpThreat before getting results
cleanResultsCmd = "powershell -command Remove-MpThreat"

# First we must verify log is clean
output = (subprocess.Popen("powershell -command Get-MpThreat",stdout=subprocess.PIPE))
outResult = output.communicate()[0].rstrip()
if len(outResult) > 0:
    print "MpThreat Has results already, Fix it"
    raw_input()
    exit()
print "Logs must be clean"
os.chdir(inputdir)
for inputfile in glob.glob("*.zip"):
    # Clean old results before next possible file
    print str(os.system(cleanResultsCmd))
    file = inputfile
    print str(file)
    # file = "virusshare.rar"
    # file = "VirusShare_ELF_20140617.zip"
    command = "7z e -pinfected F:\\input\\" + \
        file + " -oC:\\Users\\user\\Desktop\\scanme\\"
    print command
    #print "File Ready to extract, wait and check Get-MpThreat"
    #raw_input()
    p = subprocess.Popen(command, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    # The following returns to stdin "A\r\n" to Always replace files while unzipping
    out, err = p.communicate()
    print out
    #
    # 7Zip returns "Everything is Ok"
    #
    if "Everything is Ok" in str(out):
        print "Files unzipped good"
        os.chdir(defdir)
        print "Attempt start scan now... "
        print scanCmd
        # scanCmd Returns 1 for failed scan, 2 for good scan, 0 for empty scan
        scanResults = str(os.system(scanCmd))
        time.sleep(5)
        #
        # Scan couldn't finish or didn't start due to defender issue
        #
        if scanResults == '1':
            print "scan FAILED, store results"
            print storeResultsCmd
            os.system(storeResultsCmd)
            os.system("move \\\\Vboxsvr\\sharedrive2\\resultpause.txt \\\\Vboxsvr\\sharedrive2\\%s.txt" %
                      file.split('.zip')[0])
        #
        # Scan was good lets Save results.
        #
        if scanResults == '2':
            print "scan Completed, Storing Results"
            print storeResultsCmd            
            os.system(storeResultsCmd)
            print "scan returned: " + str(scanResults)
            os.system("move \\\\Vboxsvr\\sharedrive2\\resultpause.txt \\\\Vboxsvr\\sharedrive2\\%s.txt" %
                      file.split('.zip')[0])
        #
        # Scan had no results, Make a Log anyways
        #
        if scanResults == '0':
            print "Scan Returned Empty :(, Store results"
            print storeResultsCmd
            os.system(storeResultsCmd)
            os.system("move \\\\Vboxsvr\\sharedrive2\\resultpause.txt \\\\Vboxsvr\\sharedrive2\\%s.txt" %
                      file.split('.zip')[0])
    #
    # Cleanup for next zip regardless of scan return
    #
    os.system("del /F /Q C:\\Users\\user\\Desktop\\scanme")
