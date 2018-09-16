#
# This script runs inside the VM automating the malware extraction process
# The after the malware is unzipped a defender scan is run on the resulting folder.
# The defender results are stored in the shared folder causing a refresh.
#
import subprocess
import os.path
import time

inputdir = "\\\\Vboxsvr\\sharedrive2"
outdir = "\\\\Vboxsvr\\sharedrive2\\"
file = "virusshare.rar"
command = "7z e -p123456 " + file + " -oC:\\Users\\user\\Desktop\\output"


os.chdir(inputdir)
while not os.path.lexists(file):
    time.sleep(1)
if os.path.isfile(file):
    print "I spy a little file"
    print "unzip"
    p = subprocess.Popen(command, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    out, err = p.communicate('A\r\n')
print out
if "Everything is Ok" in str(out):
    print "Everything is okay"
    os.chdir(outdir)
    output = outdir + "result.txt"
    file = open(output, 'w+')
