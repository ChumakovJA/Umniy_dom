from sqlalchemy.orm import sessionmaker

from config import db
from models import Name_topic, Status_topic
from datetime import datetime



def read_all_Name_topic():
    name_topic = Name_topic.query.all()
    return name_topic

def read_all_Status_topic():
    status_topic = db.session.query(Status_topic,Name_topic).filter(Name_topic.topic==Status_topic.topic and Name_topic.tip == 0).order_by(Status_topic.ts.desc()).all()
    return status_topic

def read_Status_topic(topic):
    status_topic = Status_topic.query.filter(Status_topic.topic == topic)
    rezult = []
    rezult_ts = []
    for top in status_topic:
        rezult.append(top.value)
        rezult_ts.append(str(top.ts))

    return rezult_ts,rezult


def insert_status_topic(topic,value):
    db.session.add(Status_topic(topic=topic, value=value, ts=datetime.now()))
    db.session.commit()