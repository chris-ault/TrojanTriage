#
# This script runs inside the VM automating the malware extraction process
# The after the malware is unzipped a defender scan is run on the resulting folder.
# The defender results are stored in the shared folder causing a refresh.
#
# Defender scan log C:\Users\user\AppData\Local\Temp\MpCmdRun.log
#
import sys
import os.path
import time
import subprocess

inputdir = "\\\\Vboxsvr\\sharedrive2"
outdir = "\\\\Vboxsvr\\sharedrive2\\"
defdir = "C:\\Program Files\\Windows Defender"
# Old command offers no throttle limit
# OLD scanCmd = "MpCmdRun.exe -scan -ScanType 3 -DisableRemediation -hide -file C:\\Users\\user\\Desktop\\scanme"
scanCmd = "powershell -command Start-MpScan -ScanPath C:\\Users\\user\\Desktop\\scanme -ScanType CustomScan -ThrottleLimit 80"
storeResultsCmd = "powershell -command Get-MpThreat >> \\\\Vboxsvr\\sharedrive2\\resultpause.txt"


file = "virusshare.rar"
command = "7z e -pinfected " + file + " -oC:\\Users\\user\\Desktop\\scanme"


os.chdir(inputdir)
while not os.path.lexists(file):
    time.sleep(1)
if os.path.isfile(file):
    print "I spy a little file"
    print "unzip"
    p = subprocess.Popen(command, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    # The following returns to stdin "A\r\n" to Always replace files while unzipping
    out, err = p.communicate('A\r\n')
print out
if "Everything is Ok" in str(out):
    print "Everything is okay"
    os.chdir(defdir)
    # Scan :
    #   MpCmdRun.exe  -scan -ScanType 3 -file C:\\Users\\user\\Desktop\\output
    # Store Results(append) :
    #   powershell -command Get-MpThreatDetection >> \\\\Vboxsvr\\sharedrive2\\result.txt
    scanResults = str(os.system(scanCmd))
    os.system(storeResultsCmd)
    # This scan had better return 2 or we have issues and no malware
    print "scan returned: " + str(scanResults)
    os.system("move \\\\Vboxsvr\\sharedrive2\\resultpause.txt \\\\Vboxsvr\\sharedrive2\\result.txt")
