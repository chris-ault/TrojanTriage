# -*- coding: utf-8 -*-
#
# -Parse Cuckoo Report JSON file directly after uploading
# -Create DLL Database of malware Sample
# -Parse Packer Signature of sample
# -Send Parsed Results to Database

######
# Handles: Will not crash if non json file is supplied by user
#
# Errors: If multiple JSON files are run one after the other
# the CuckooData Class Appends onto the old local variables
######

# Upload handling
import os
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
# Parsing and Database Handling
import json
from myproject.myapp.models import Document, Malware, Dlltable, Malware2Dll
from myproject.myapp.forms import DocumentForm
from django.conf import settings

from pprint import pprint

def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            #fname = newdoc.name
            newdoc.save()
            newdoc = request.FILES['docfile']
            # Redirect to the document list after POST
            print "\n\n\n######################################"
            print "File has uploaded, Parse file now"
            myData = CuckooData()
            myData.parseFile(newdoc.name) # Access bare Name attribute of the document uploaded
            del myData
            return HttpResponseRedirect(reverse('list'))
    else:
        form = DocumentForm()  # A empty, unbound form
        dllis = "user32.dll"
        n = Dlltable.objects.filter(dll_name=dllis)  # Lookup on dll
        # print n.query
        dllid = n.get().malware_dll_id                          # Return the ID
        # print "The dll " + dllis + " Has id #" + str(dllid)
        #print n.get(malware_dll_id)
        for E in n:
            pass # print E.malware_dll_id
        # print [e.malware_dll_id for e in Dlltable.objects.filter(dll_name="user32.dll")]

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render(
        request,
        'list.html',
        {'documents': documents, 'form': form}
    )

class CuckooData:
    packer = ""
    fileType = ""
    dlls = []
    md5 = ""

    def parseFile(self, filename):
        # myData = CuckooData()
        media_dir = settings.BASE_DIR + '\\media\\documents\\'
        try:
            with open(os.path.join(media_dir, filename)) as f:
                data = json.load(f)
            self.packer = data["static"]["peid_signatures"][0]
            self.fileType = data["target"]["file"]["type"]
            self.md5 = data["target"]["file"]["md5"]
            for n in data["static"]["pe_imports"]:
                self.dlls.append(n["dll"])
            dbInsert(self)
        except (ValueError, IOError) as e:
            y = e.args  # y contains error name
            print (y)

def dbInsert(object):
    print "Dlls: " + str(object.dlls)
    print "Type: " + str(object.fileType)
    print "Packer: " + str(object.packer)
    print "MD5: " + str(object.md5)
    print "######################################\n\n\n"
    x = Malware(hash=object.md5, filetype=object.fileType)
    x.save()
    # For every DLL in the object
    for n in object.dlls:
        o = Dlltable.objects.filter(dll_name=n)  # Lookup on dll
        # print o.query
        # Check if DLL exists in DB
        try:
            dllid = o.get().malware_dll_id
        # Otherwise we need to make a new dll
        except ObjectDoesNotExist:
            print "Don't have " + str(n) + ", make it"
            a = Dlltable(dll_name=n)
            a.save()
            dllid = o.get().malware_dll_id
        # print "DLL Exists @ ID: " + str(dllid) + " For hash " + str(object.md5)
        # Query for pre-existing row
        b = Malware2Dll.objects.filter(hash=str(object.md5), malware_dll_id=dllid)
        # If no results in query, save it
        if not b.all():
                # print "saving"
                c = Malware2Dll(hash=str(object.md5), malware_dll_id=dllid)
                c.save()
    print "Done"

