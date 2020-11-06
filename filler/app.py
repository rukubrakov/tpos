import pymysql
from pymysql.cursors import DictCursor
import csv
import time
import sys
import logging
data=[]
reader = csv.DictReader(open("/var/filler/data.csv"), delimiter=',')
for line in reader:
    data.append((line["text"], int(line["number"])))
    
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
        
with conn.cursor() as cursor:
    query = 'INSERT INTO test (text,number) VALUES (%s,%s)'
    cursor.executemany(query, data)
    conn.commit()
with conn.cursor() as cursor:
    query = 'SELECT text,number FROM test'
    cursor.execute(query)
    i=0
    for row in cursor:
        if row["number"]!=data[i][1] or row["text"]!=data[i][0]:
            logging.error("Error: value mismatch %s %d : %s %d"%(data[i][0],data[i][1],row["text"],row["number"])) 
            connection.close()
            sys.exit(1)
        else:
            i+=1
            if i==len(data):
                break
conn.close()
logging.info("Success: database updated")
