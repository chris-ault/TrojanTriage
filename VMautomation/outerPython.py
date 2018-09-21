#
# This script runs outside the VM automating the boot, restore snapshot and shutdown process
# The shutdown of VM occurs when defender virus scan results are in the shared folder.
# After shutdown completes a new archive will be transferred to the share and the cycle loops.
#
import subprocess
import os.path
import time
import glob
MalDir = "C:\\Users\\captn2\\Documents\\CyberIntern\\VMs\\MalwareArchives\\Test\\"
OutDir = "C:\\Users\\captn2\\Documents\\CyberIntern\\VMs\\SHAREDRIVE\\input"


#  For loop Move a single file from directory into Share/input Directory
os.chdir(MalDir)
for singleZip in glob.glob("*.zip"):
    print "Working on " + str(singleZip)
    os.system("move %s%s %s" % (MalDir, singleZip, OutDir))
    #
    # Restore most recent snapshot
    #
    result = (subprocess.Popen("""C:\Program Files\Oracle\VirtualBox\VBoxManage.exe snapshot win10 restorecurrent""", stdout=subprocess.PIPE).communicate()[0])
    if "Restoring" in result:
        print "good restore.. > booting"
        #
        # Boot VM
        #
        result = (subprocess.Popen("""C:\\Program Files\\Oracle\\VirtualBox\\VBoxManage.exe startvm win10""", stdout=subprocess.PIPE).communicate()[0])
        if "started." in result:
            print "booted, Waiting for result file"
            directory = "C:\\Users\\captn2\\Documents\\CyberIntern\\VMs\\SHAREDRIVE\\"
            results = singleZip.split('.zip')[0] + str('.txt')
            os.chdir(directory)
            while not os.path.lexists(results):
                time.sleep(3)
            if os.path.isfile(results):
                print "I spy a little file, delay 60 seconds for it to finish copying, press enter to confirm copied"
                time.sleep(60)
                print "shutdown"
                #
                # Shut down VM File found
                #
                result = (subprocess.Popen("""C:\Program Files\Oracle\VirtualBox\VBoxManage.exe controlvm win10 poweroff hard""",
                                           stdout=subprocess.PIPE).communicate())
                print result
                if not result[0]:
                    print "Clean Kill"
                else:
                    print "Couldn't shut down"
            else:
                raise ValueError("%s not a file" % results)
        else:
            print "couldn't start"
    else:
        print "No Restore"
    # Move single file back where it came from
    print ("Removing old file back to Store")
    os.chdir(OutDir)
    os.system("move %s %s" % ( singleZip, MalDir))
    print "Let the VM close up"
    time.sleep(15)
print "Done"