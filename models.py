#from app import db
'''
from sqlalchemy import Column, String, Integer
from app import base

class User(base):
    __tablename__ = 'users'
    # id = db.Column(db.Integer, primary_key=True)
    # username = db.Column(db.String(64), index=True, unique=True)
    email = Column(String(120),primary_key=True)
    # email = db.Column(db.String(120), index=True, unique=True)
    password_hash = Column(String(128))

    def __repr__(self):
        return '<Email %r>' % self.email
'''
'''
    def __init__(self, em, psw):
        self.email = em
        self.password_hash = psw

    def get(self):
        return str(self.email) + " " + str(self.password_hash)
'''