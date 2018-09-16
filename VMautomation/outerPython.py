import subprocess
import os.path
import time

directory = "C:\\Users\\captn2\\Documents\\CyberIntern\\VMs\\SHAREDRIVE\\"
file_path = "result.txt"

result = (subprocess.Popen("""C:\Program Files\Oracle\VirtualBox\VBoxManage.exe snapshot win10 restorecurrent""",
                           stdout=subprocess.PIPE).communicate()[0])
if "Restoring" in result:
    print "good restore.. > booting"
    result = (subprocess.Popen("""C:\Program Files\Oracle\VirtualBox\VBoxManage.exe startvm win10""",
                               stdout=subprocess.PIPE).communicate()[0])
    if "started." in result:
        print "booted"
        os.chdir(directory)
        while not os.path.lexists(file_path):
            time.sleep(1)
        if os.path.isfile(file_path):
            print "I spy a little file"
            print "shutdown"
            result = (subprocess.Popen("""C:\Program Files\Oracle\VirtualBox\VBoxManage.exe controlvm win10 poweroff hard""",
                                       stdout=subprocess.PIPE).communicate())
            print result
            if not result[0]:
                print "Clean Kill"
            else:
                print "Couldn't shut down"
        else:
            raise ValueError("%s not a file" % file_path)
    else:
        print "couldn't start"
else:
    print "No Restore"
