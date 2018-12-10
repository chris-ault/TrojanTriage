from virustotal import vt
vt = vt()
vt.getfile('306d6b8c1576071788517893f80602bc')
x = vt.out('json')
print x.dum
