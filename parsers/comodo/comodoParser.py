# Choose Show 'Antivirus Events'
# Choose filter all time
# Choose export htm file avExport.htm
name = 'test.htm'
# Skip down to line 64
# a
# Look for <td>
# Date
# Location
# Name split @
# skip
# skip
# </tr> ends row
# </table> break out
# loop a

array = ['date', 'loc', 'type', 'streetName', 'action', 'status']

# Convert to ascii comodo outputs non ascii
def convertascii(input):
    fread = open(input, 'rb').read()
    mytext = fread.decode('utf-16')
    mytext = mytext.encode('ascii', 'ignore')
    fwrite = open(input.split('.')[0] + '.ascii', 'wb+')
    fwrite.write(mytext)


def submit2db(entries):
    print "Sending to db"
    for values in entries.items():
        print values

entries = {}
convertascii(name)
with open(name.split('.')[0] + '.ascii') as f:
    for i in xrange(63):
        f.next()
    ind = 0
    for line in f:
        # Date
        line = line.strip('\n')
        if line.startswith('<td>'):
            if line.__contains__('@'):
                entries = {array[ind]: line.split('@')[0].strip('<td>')}
                submit2db(entries)
                entries = {array[ind + 1]: line.split('@')[1]}
                ind = ind + 2
            else:
                entries = {array[ind]: line.strip('<td>')}
                #print entries
                ind = ind + 1
            submit2db(entries)
        if line.startswith('</tr>'):
            ind = 0
            print ' '
        if line.startswith('</table'):
            break
