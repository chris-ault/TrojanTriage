fileAnalyze.py
==================================

The goal with fileAnalyze.py is to append to a flat file: file type, MIME type information, Charset Information, calculated hash[sha1], hash[md5], entry point, first instruction point, bytes.

example result: 
	['0x3265', '0x3265L', '645729', '6fa92dd2ca691c11dfbfc0a239e34369897a7fab', 'PE32 executable for MS Windows (GUI) Intel 80386 32-bit,application/octet-stream; charset=binary,3abf1c149873e25d4e266225fbf37cbf,6fa92dd2ca691c11dfbfc0a239e34369897a7fab']

Usage (Python 2.0)
------------------
install pefile, capstone
	python -m pip install pefile
	python -m pip install capstone
install GNU File command using file-*-setup.exe to install DLL dependency files as well
	https://sourceforge.net/projects/gnuwin32/files/file/5.03/file-5.03-setup.exe/download
walk.py will take 1 argument that is the folder of binaries to test
run walk.py C:\folder to test\

Example:
	python E:\CyberIntern\Code\TrojanTriage\Analysis\fileAnalysis\walk.py E:\CyberIntern\Code\TrojanTriage\Analysis\fileAnalysis\fileCommandAnalysis\
In this example fileCommandAnalysis\ contains binaries to test

Resulting output file is located in fileAnalysis.py folder as fileTypes.txt