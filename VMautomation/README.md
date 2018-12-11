VMAutomation
==================================

The goal with VMAutomation is to be able to parse through passworded ZIP malware archives in an automated fashion and return results back to the host machine.  

Usage (Python 2.0)
------------------
First ensure you have a Windows Host machine or Ubuntu 16+ with Python 2.15 installed.  The supported VM desktop virtualization options are VMware Workstation or Virtualbox, more can be easily added through changing the outer python script.  The Guest must be newer than Windows 7 SP1 and needs Python 2.15 installed along with 7zip for decompression via commandline.  

The overview of how VMAutomation works is as follows:

Outer host has a folder of numerous passworded zip files that it then provides Inner Guest with single passworded zip archive (here referred to as archive1.zip) through a shared folder.  The Guest runs a python script to decompress and initiates a scan of the decompressed archive1.zip.  The Guest then returns the scan results to the host with the name archive1.txt in the shared folder.  When the host finds archive1.txt it hard shuts off the VM and transfers archive1.zip back to its original folder.  The host then takes archive2.zip and puts it into the shared folder and reboots the VM and the process continues until all *.zip files have been processed and only *.txt files of results remain in the shared folder.

Usage Host (VMware, Ubuntu):
TODO

Usage Host (VirtualBox, Windows):
	
	Setup SharedFolder Full access to folder called MalwareInput
	In outerPython change 'OutDir' to match the location of MalwareInput
	The directory containing all ZIP Archives should be updated as 'MalDir'
		The host will take from 'MalDir' one at a time moving into shared folder 'OutDir'.
	Update 'directory' variable to match the location of the sharedfolder
		The host will request back resulting txt file from 'directory' location.


Usage Guest(Windows 10):
	
	Install Python 2.15 default directories.
	Copy innerPython.py to startup folder located at Run cmd > shell:startup
	Run innerpython.py using cmd > python innerPython.py
	Take snapshot with Host while innerPython is running.
