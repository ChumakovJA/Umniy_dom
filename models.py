from config import db




class Name_topic(db.Model):
    topic = db.Column(db.String(100), primary_key=True)
    tip = db.Column(db.Integer)
    name = db.Column(db.Text)

    def __repr__(self):
        return f'<Post "{self.topic}">'


class Status_topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(100))
    value = db.Column(db.DECIMAL(10,2))
    ts = db.Column(db.TIMESTAMP)

    def __repr__(self):
        return self.topic + " " + str(self.value)
