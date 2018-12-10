"""
This script adds and removes SQL entry via web interface 
Add item:
localhost/add/(item to add)
    returns a lookup of that items ID number
Remove item:
localhost/remove/(id to remove)
    returns success or failure of removal

"""
import mysql.connector
import re
import sys
import signal
from flask import Flask
app = Flask(__name__)


def signal_handler(signal, frame):
    print("Okay I'll close")
    sys.exit(0)


signal.signal(signal.SIGTERM, signal_handler)


mydb = mysql.connector.connect(
    host="localhost",
    user="user",
    passwd="password",
    database="mydatabase"
)

mycursor = mydb.cursor()
sql = "SELECT * FROM customers WHERE address LIKE '%Lane%'"
mycursor.execute(sql)
myresult = mycursor.fetchall()
output = " ".join(str(x) for x in myresult)
print (re.findall(r"'(.*?)'", output, re.DOTALL))


@app.route("/")
def hello():
    sql = "SELECT * FROM customers"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    final = ''
    for x in myresult:
        final = final, x, '</br>'
        outfinal = map(str, final)
    print outfinal
    return str(final)


@app.route('/add/<entry>')
def add(entry):
    print "entry is: " + entry
    sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
    val = (entry, "hello world")
    mycursor.execute(sql, val)
    mydb.commit()
    sql = "SELECT * FROM customers"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    print "Table currently"
    for x in myresult:
        print(x)
    mycursor.execute("SELECT id FROM customers WHERE name='" + entry + "'")
    myresult = mycursor.fetchall()
    output = entry, " is at ID #: ", myresult
    outstr = map(str, output)
    print outstr
    return str(outstr)


@app.route('/remove/<entry>')
def remove(entry):
    entry = str(entry)
    print "entry to remove is: " + entry
    if entry.isdigit():
        sql = "DELETE FROM customers WHERE id = ('%s')"
        mycursor.execute(sql % entry)
        mydb.commit()
        removeTrue = mycursor.rowcount
        foo = removeTrue, " record id:", entry, " removed.\n"
        bar = map(str, foo)
        print(''.join(bar))
        sql = "SELECT * FROM customers"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        print "Table currently"
        for x in myresult:
            print(x)
        if removeTrue == 1:
            return entry + " removed successfully"
        else:
            return "not a id that can be removed"
    else:
        return "not a valid number"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
