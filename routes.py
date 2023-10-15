import os
import sqlite3
import matplotlib.pyplot as plt
from flask import render_template, request, session ,jsonify
import matplotlib.dates as mdates
import config
import database

app = config.connex_app
topic = 'ESP_Easy'

path_app = os.path.split(os.path.realpath(__file__))[0]


@config.mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Connected successfully')
        config.mqtt.subscribe(topic + '/#') # subscribe topic
    else:
        print('Bad connection. Code:', rc)


@app.route('/')
@app.route('/index')
def index():
    datchiki = database.read_all_Name_topic()
    return render_template('index.html', title='Умный дом', username='user', datchiki = datchiki)

@app.route('/status_topic')
def status_topic():
    id=request.args.get("id")
    print(id)
    rezult_ts,rezult = database.read_Status_topic(topic + '/28_8b_cf')
    rezult_ts1,rezult1 = database.read_Status_topic(topic + '/28_b5_41')
    months = mdates.MonthLocator()
    days = mdates.DayLocator()
    timeFmt = mdates.DateFormatter('%Y-%m')

#print(data)
    #plt.plot(['2023-05-15 09:08:27', '2023-05-15 09:12:45', '2023-05-15 09:15:15', '2023-05-15 09:15:32'],[Decimal('29.99'), Decimal('39.99'), Decimal('39.99'), Decimal('27.56')])
    fig, ax = plt.subplots()
    plt.plot(rezult_ts,rezult)
    plt.plot(rezult_ts1,rezult1)

    plt.xlabel('X label')
    plt.ylabel('Y label')
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(timeFmt)
    ax.xaxis.set_minor_locator(days)

    plt.savefig(os.path.join(config.basedir, 'static', 'images', 'plot.png'))
    rows = database.read_all_Status_topic()
    return render_template('status_topic.html', title='Умный дом', username='user', status_topic = rows)

@config.mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
          topic=message.topic,
          payload=message.payload.decode()
    )

    payload = message.payload.decode('utf-8')
    sqlite_connection  = sqlite3.connect(path_app + '\\database.db')
    sql = 'INSERT INTO status_topic (topic, value) VALUES (?, ?)'
    cursor = sqlite_connection.cursor()
    cursor.execute(sql, (message.topic, payload))
    sqlite_connection.commit()
    cursor.close()
    print('Received message on topic: {topic} with payload: {payload}'.format(**data))


def main():

    config.mqtt.subscribe(topic + '/#')
    app.run(host='127.0.0.1', port=8085, use_reloader=False, debug=True)



if __name__ == '__main__':
    main()