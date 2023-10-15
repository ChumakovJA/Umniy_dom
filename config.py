import os
import pathlib

import configparser
import connexion
from flask_mqtt import Mqtt
from flask_sqlalchemy import SQLAlchemy

basedir = pathlib.Path(__file__).parent.resolve()
connex_app = connexion.App(__name__, specification_dir=basedir)
print(basedir)
config = configparser.ConfigParser()
config.read(basedir / 'config.ini')


app = connex_app.app
app.config['SECRET'] = 'my secret key'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = config.get('mqqt_server','MQTT_BROKER_URL')
app.config['MQTT_BROKER_PORT'] = config.getint('mqqt_server','MQTT_BROKER_PORT')
if config.get('mqqt_server','MQTT_USERNAME') != "":
    app.config['MQTT_USERNAME'] = config.get('mqqt_server','MQTT_USERNAME')
if config.get('mqqt_server','MQTT_PASSWORD') != "":
    app.config['MQTT_PASSWORD'] = config.get('mqqt_server','MQTT_PASSWORD')

app.config['MQTT_KEEPALIVE'] = config.getint('mqqt_server','MQTT_KEEPALIVE')
app.config['MQTT_TLS_ENABLED'] = config.getboolean('mqqt_server','MQTT_TLS_ENABLED')

app.config['SQLALCHEMY_DATABASE_URI'] =  f"sqlite:///{basedir / 'database.db'}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
mqtt = Mqtt(app)