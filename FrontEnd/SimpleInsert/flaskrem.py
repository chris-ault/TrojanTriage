"""
This script deletes row from table using flask server and url structure
ex: localhost:80/remove/5
the row removed would be of id '5'

"""

import mysql.connector
import re
import sys
from flask import Flask
app = Flask(__name__)

mydb = mysql.connector.connect(
    host="localhost",
    user="user",
    passwd="password",
    database="mydatabase"
)
mycursor = mydb.cursor()


@app.route("/")
def hello():
    return "hello there"


@app.route('/remove/<entry>')
def remove(entry):
    print "entry to remove is: " + entry
    sql = "DELETE FROM customers WHERE id = ('%s')"
    mycursor.execute(sql % entry)
    mydb.commit()
    foo = mycursor.rowcount, " record id:", entry, " removed.\n"
    bar = map(str, foo)
    print(''.join(bar))
    sql = "SELECT * FROM customers"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    print "Table currently"
    for x in myresult:
        print(x)
    return entry + " removed successfully"




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)