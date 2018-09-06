
import mysql.connector
from flask import Flask, request
from variables import query, sort
app = Flask(__name__, static_url_path="", static_folder="static")


mydb = mysql.connector.connect(
    host="localhost",
    user="user",
    passwd="password",
    database="malwareDB"
)

columnOptions = 'HASH', 'type', 'Location', 'subType','threatID','Date','Schemaversion','Rollupstatus','OS','severity'
baseurl = '/'

# Fill this query with user input for columns, extra unsafe
def getQuery(input, sort):
    myresult = ''
    if input:
        mycursor = mydb.cursor()
        strquery = ", ".join(input)
        mycursor.execute("SELECT %s FROM element order by %s desc LIMIT 13" % (strquery, sort))
        myresult = mycursor.fetchall()
        return myresult
    else:
        input = ['HASH', 'type', 'Location']
        mycursor = mydb.cursor()
        strquery = ", ".join(input)
        mycursor.execute("SELECT %s FROM element order by type" % strquery)
        myresult = mycursor.fetchall()
        return myresult


def displayPage(myresults, baseurl):
    # List of Checkbox names for column selection

    # Stuff at the top of the page
    headers = "<table width:auto; padding: 20px; margin: 0px;>\n<thead><tr><th>Column to remove</th>"
    if 'sort' in request.url_root:
        print "this is sort"
    for z in range(len(query)):
        headers += "<th><a href=\""+ baseurl + "sort/"+ str(z) + "\">%s</a></th>"
    headers += "</tr></thead>\n<tbody align =\"center\">\n<tr><td>"
    gap = "</td><td>"
    end = "</td></tr></tbody></table>"

    # Build check boxes for user input on columns requested
    checkbox = "<input type=\"checkbox\" name=\"%s\" unchecked> %s"
    boxes = []
    for x in columnOptions:
        boxes.append(checkbox % (2 * (x,)))
    body = []
    num = 0
    if len(myresults) < 4:
        for x in xrange (0, 15-len(myresults)):
                myresults.append([],[])

    for index, x in enumerate(myresults):
        if index == 15:
            break
        if num < len(columnOptions):
            # Print check boxes and elements
            # iterate over check box and elements
            body.append("<tr><td width=\"100\">" + boxes[num - 1])  # element + gap
            for y in range(len(x)):
                body.append(gap + str(x[y]))
            num = num + 1
            body.append("</td></tr>")
            box = True
            reset = True
        elif box:
            # Print submit button and elements
            body.append("<tr><td>" + "<input type=\"submit\" value=\"Remove\">") 
            for w in range(len(query)):
                body.append(gap + str(x[w]))
            body.append("</td></tr>\n")
            box = False
        elif reset:
            # Print Reset and elements
            body.append("</td></tr>\n<tr><td>" + " <a href=\"/reset/\">Reset</a>") 
            for w in range(len(query)):
                body.append(gap + str(x[w]))
            body.append("</td></tr>\n")
            reset = False
        else:
            # Print non controls and just elements
            body.append("<tr><td>" + " ")
            for v in range(len(query)):
                body.append(gap + str(x[v]))
            body.append("</td></tr>\n")  # element + gap
    out = ''.join(body)
    print "Query lookup is:" + str(query)
    print headers % tuple(query)
    page = headers % tuple(query) + "<form method = \"post\">" + out + "</form><center>" + end + str(len(myresults)) + " Pieces of fun"
    return page


# https://stackoverflow.com/questions/31859903/get-the-value-of-a-checkbox-in-flask
@app.route("/", methods=['GET', 'POST'])
def index():
    global baseurl
    baseurl = request.base_url
    if request.method == 'POST':
        for possible in columnOptions:
            if request.form.get(possible):
                query.remove(possible)
        #print(request.form.getlist('Location'))
    return displayPage(getQuery(query,1),baseurl)

@app.route("/reset/", methods=['GET', 'POST'])
def index2():
    global query
    query = 'HASH', 'type', 'Location', 'subType','threatID','Date','Schemaversion','Rollupstatus','OS','severity'
    if request.method == 'POST':
        for possible in columnOptions:
            print "Item to remove is:" + possible
            if request.form.get(possible):
                query.remove(possible)
    return displayPage(getQuery(query,1),baseurl)


@app.route("/sort/<sorton>", methods=['GET', 'POST'])
def sort0(sorton):
    global query
    if not query:
            query = 'HASH', 'type', 'Location', 'subType','threatID','Date','Schemaversion','Rollupstatus','OS','severity'
    if request.method == 'POST':
        for possible in columnOptions:
            if request.form.get(possible):
                query.remove(possible)
    global sort
    sort = query[int(sorton)]
    print sort
    return displayPage(getQuery(query,sort),baseurl)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=81)
