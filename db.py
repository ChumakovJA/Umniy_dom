import decimal
import os
import sqlite3


from models import Name_topic,Status_topic
#from routes import path_app
path_app = os.path.split(os.path.realpath(__file__))[0]

def db_connect():
    sqlite_connection  = sqlite3.connect(path_app + '\\database.db')
    return sqlite_connection


def insert_db(topic,value):
    sqlite_connection  = sqlite3.connect(path_app + '\\database.db')
    cur = sqlite_connection.cursor()
    try:
        cur.execute("INSERT INTO status_topic (topic, value) VALUES ('"+topic+"', "+value+")")
        sqlite_connection.commit()
        cur.close()
        #print("insert db ")
    except sqlite3.Error as e:
        print(f"Error: {e}")


def select_name_topic_db():
    name_topic_l = []
    sqlite_connection  = sqlite3.connect(path_app + '\\database.db')
    cur = sqlite_connection.cursor()
    try:
        cur.execute("""select nt.topic, nt.name, nt.tip, st.VALUE,st.ts from name_topic nt 
        left join status_topic st on nt.topic= st.topic 
        where (st.ts,nt.topic) in (select max(ts), topic from status_topic group by topic) 
        group by nt.topic, nt.tip, nt.name, st.VALUE
        UNION
        select nt.topic, nt.name, nt.tip, st.VALUE,st.ts from name_topic nt
        left join status_topic st on nt.topic= st.topic
        where st.value is null""")
        rows = cur.fetchall()
        for row in rows :
            name_topic_l.append(Name_topic(row[0],row[1],row[2],row[3],row[4]))
        cur.close()
    except sqlite3.Error as e:
        print(f"Error: {e}")

    return name_topic_l

def update_db(topic,value):
    sqlite_connection  = sqlite3.connect('c:\\rb_projects\\Git1\\Umniy_dom\\database.db')
    cur = sqlite_connection.cursor()
    try:
        cur.execute("UPDATE status_topic SET topic=" +(topic,decimal.Decimal(value))+ " where topic='" +topic + "'")
        sqlite_connection.commit()
        cur.close()
    except sqlite3.Error as e:
        print(f"Error: {e}")

def select_status_topic_db(name_topic):
    status_topic_l = []
    sqlite_connection  = sqlite3.connect(path_app + '\\database.db')
    cur = sqlite_connection.cursor()
    print(name_topic)
    try:
        cur.execute("select topic, value, ts from status_topic where topic='"+name_topic+"' order by ts DESC")
        rows = cur.fetchall()
        for row in rows :
            status_topic_l.append(Status_topic(row[0],row[1],row[2]))
        cur.close()
    except sqlite3.Error as e:
        print(f"Error: {e}")

    return status_topic_l
