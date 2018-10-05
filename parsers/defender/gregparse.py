defenderfile = "sample.txt"
fin = open(defenderfile, 'r')

num_entries = 0


class defenderEntry(object):
    categoryID = 0
    threatID = 0


entries = {}

a = defenderEntry()

for line in fin:
    # Line stripped has nothing to offer
    if not len(line.strip()):
        # End of entry encountered
        num_entries = num_entries + 1
        entries[num_entries] = a
        a = defenderEntry()
    else:
        value = ''
        # parts = line.split(':', 1)
        parts = [line[:19].strip(), line[19:].strip()]
        # The front part is empty
        if not len(parts[0]):
            # This is part of a multi-line value
            a.resources = a.resources + parts[1]
        # The front part is not empty
        else:
            value = parts[1].strip()
            if 'CategoryID' in parts[0]:
                a.categoryID = int(value)
            if 'DidThreatExecute' in parts[0]:
                a.didthreatexecute = eval(value)
            if 'IsActive' in parts[0]:
                a.isActive = eval(value)
            if 'Resources' in parts[0]:
                a.resources = value
                print a.resources
            if 'RollupStatus' in parts[0]:
                a.rollupStatus = int(value)
            if 'SchemaVersion' in parts[0]:
                a.schemaVersion = value
            if 'SeverityID' in parts[0]:
                a.severityID = int(value)
            if 'ThreatID' in parts[0]:
                a.threatID = int(value)
            if 'ThreatName' in parts[0]:
                a.threatName = value
            if 'TypeID' in parts[0]:
                a.typeID = int(value)


entriesReady = {}
b = defenderEntry()
index = 0
bad_items = []
# Iterate over num_entries to clean and fill hashes
# From the list of entries grab a 'item'
for item in entries.keys():
    # print entries[item].threatID

    # Iterate over each resource
    # From the resources in that entry make a list of locations
    threatGroup = entries[item].resources.strip('{').strip('}').strip('...').split(',')
    for subItems in threatGroup:
                                # Make the new dictionary item have this location
        location = subItems
        # from that list of locations find the hash
                                # Make the new dictionary item have this hash
        item_hash = str(location.split('VirusShare_', -1)
                        [-1]).split('-', -1)[0]
        if not (len(item_hash) == 32):
            bad_items.append(location)
            # entries.pop(item) // I do not want to pop the entire item but just the bad location from it
            print "Unhandled location"    # 
            threatGroup.remove(location)  # Remove item from temp list
            raw_input()
        else:
            # Hash looks good let's make a list for submitting to database
            # break apart defender threatName into sub pieces
            tempName = entries[item].threatName[1].split('/')
            tempOS = str(entries[item].threatName).split('/')[0].split(':')[1]
            tempType = str(entries[item].threatName[0]).split('/')[0].split(':')[0]
            # Store b dictionary for sql entry
            b.location = location
            b.hash = item_hash
            b.catID = entries[item].categoryID
            b.rollUp = entries[item].rollupStatus
            b.schema = entries[item].schemaVersion
            b.severity = entries[item].severityID
            b.threat = entries[item].threatID
            b.typeID = entries[item].typeID
            b.streetName = tempName
            b.OS = tempOS
            b.category = tempType

            # a.hash = item_hash
            print "to db-> " + b.location
            print "hash-> " + a.hash
        # First iteration has completed lets increment and set things
        index = index + 1
        entriesReady[index] = b
        b = defenderEntry()
        entries[item].resources = threatGroup  # Add temp list into resources
print "ERR Weird name or hash Not added to db-> " + str(bad_items)

for item in entries.keys():
    print entries[item].resources
    raw_input()
