from datetime import datetime
from app import db

class Prints(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    printDate = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    sheets = db.Column(db.Integer)
    totalPrice = db.Column(db.Integer)
    state = db.Column(db.Integer)
    
    def __repr__(self):
        return '<Print sheets {}>'.format(self.sheets)

