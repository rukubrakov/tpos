import pymysql
from pymysql.cursors import DictCursor
from flask import Flask
import flask
import json
import time
import logging
app = Flask(__name__)

err=('<head><meta http-equiv="refresh" content="1;URL=http://0x0.st/K0" /></head>',404)

conn=None
while not conn:
    time.sleep(0.5)
    try:
        conn = pymysql.connect(
            host='db',
            user='user',
            password='test',
            db='test',
            cursorclass=DictCursor
        )
    except Exception as e:
        logging.warning("Failed to connect to the database %s" % str(e))



def querry_db():
    stuff=[]
    with conn.cursor() as cursor:
        query = 'SELECT text,number FROM test'
        cursor.execute(query)
        for row in cursor:
            stuff.append({'text':row['text'],'number':row['number']})
    return json.dumps(stuff)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if flask.request.method == 'GET':
        if path == '':
            return querry_db(),200
        elif path == 'health':
            return 'ok',200
        else:
            return err
    else:
        return err

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=4580)
