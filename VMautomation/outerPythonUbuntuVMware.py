#
# This script runs outside the VM automating the boot, restore snapshot and shutdown process
# The shutdown of VM occurs when defender virus scan results are in the shared folder.
# After shutdown completes a new archive will be transferred to the share and the cycle loops.
#
import subprocess
import os.path
import getpass
import time
import glob

user = '/home/' + getpass.getuser()
vmdir = user + "/vmware/"
MalDir = user + "/malwareCollection" # Contains zip malware collection to parse
OutDir = user + "/malFolder"         # vm share folder (host)
vmxFile = "Win764/Windows 7 x64.vmx" # Win 7 SP1 does not have getMPThreat command
snapshot = "win7"
#vmcmd = "C:\\Program Files\\Oracle\\VirtualBox\\VBoxManage.exe"
vmcmd = "vmrun"
#  For loop Move a single file from directory into Share/input Directory
os.chdir(MalDir)
for singleZip in glob.glob("*.zip"):
    print "Working on " + str(singleZip)
    os.system("mv %s/%s %s" % (MalDir, singleZip, OutDir))
    #
    # Restore most recent snapshot
    #
    # result = (subprocess.Popen("""C:\Program Files\Oracle\VirtualBox\VBoxManage.exe snapshot win10 restorecurrent""", stdout=subprocess.PIPE).communicate()[0])
    os.chdir(vmdir)
    cmd = [ vmcmd, '-T', 'ws', 'revertToSnapshot', vmxFile, snapshot]
    result = (subprocess.Popen(cmd, stdout=subprocess.PIPE ).communicate()[0])
    if result:
        print result # vmrun returns nothing upon completion
        raw_input()
    print "good restore.. > booting"
    #
    # Boot VM
    #
    cmd = [vmcmd, 'start', vmxFile]
    result = (subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0])
    if result:
        print result # vmrun returns nothing upon completion
        raw_input()
    #
    # Set Shared Folder
    #
    cmd = [vmcmd, 'addSharedFolder', vmxFile, 'malware', OutDir]
    result = (subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0])
    print result
    print "booting, Waiting for result file"
    results = singleZip.split('.zip')[0] + str('.txt')
    print "File name I expect is: " + results
    os.chdir(OutDir)
    while not os.path.lexists(results):
        time.sleep(5)
    if os.path.isfile(results):
        print "File located, delay 60 seconds for it to finish copying, sleeping brb"
        time.sleep(60)
        print "shutdown"
        #
        # Shut down VM File found
        #
        os.chdir(vmdir)
        cmd = [vmcmd, 'stop',vmxFile, 'hard']
        result = (subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate())
        print result
        if not result[0]:
            print "Clean Kill"
        else:
            print "Couldn't shut down"
    else:
        raise ValueError("%s not a file" % results)
    # Move single file back where it came from
    print ("Removing old file back to Store")
    os.chdir(OutDir)
    os.system("mv %s %s" % ( singleZip, MalDir))
    print "Let the VM close up, sleeping brb"
    time.sleep(5)
print "Done"