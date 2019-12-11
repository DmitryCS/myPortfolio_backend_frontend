from flask import Flask, render_template, redirect, request
from sqlalchemy import create_engine

engine = create_engine('sqlite:///mydb.db', echo=True)

from sqlalchemy.ext.declarative import declarative_base
#from models import User

base = declarative_base()


#database
from sqlalchemy import Column, String, Integer

class User(base):
    __tablename__ = 'users'
    # id = db.Column(db.Integer, primary_key=True)
    # username = db.Column(db.String(64), index=True, unique=True)
    id = Column(Integer, primary_key=True)
    email = Column(String(120))
    # email = db.Column(db.String(120), index=True, unique=True)
    password_hash = Column(String(128))

    def __repr__(self):
        return '<Email %s, Password %s>' % (self.email, self.password_hash)
#database

base.metadata.create_all(engine)

from sqlalchemy.orm.session import sessionmaker
session = sessionmaker(bind=engine)()

def addUserByEmailPsw(email, psw):
    user_ivan = User(name=email, fullname=psw)
    session.add(user_ivan)
    session.commit()

def addUser(user):
    session.add(user)
    session.commit()

def selectAll():
    s = session.execute("select * from users order by id desc")  # позволяет делать запросы напрямую
    return s

def checkUser(user):
    q = session.query(User).filter_by(email=user.email, password_hash=user.password_hash).first()
    with open("info.txt", 'w') as f:
        # db.create_session(User)
        f.write(str(q))
    f.close()
    #query = "select * from users where email='{}' and password_hash='{}'".format(user.email, user.password_hash)
    #s = session.execute(query)  # позволяет делать запросы напрямую
    #return s.count() != 0
    return q != None

def checkLogin(user):
    q = session.query(User).filter_by(email=user.email).first()
    print(q)
    return q is not None
#from config import Config
#from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate

app = Flask(__name__)
#app.config.from_object(Config)
#db = SQLAlchemy(app)
#migrate = Migrate(app, db)
#db.create_all()


@app.route('/')
def hello_world():
    return render_template('main.html')

@app.route('/skills.html')
def skills():
    return render_template('skills.html')

@app.route('/ican.html')
def ican():
    return render_template('ican.html')

@app.route('/langs.html')
def langs():
    return render_template('langs.html')

@app.route('/exs.html')
def exs():
    data = map(str, selectAll())            #только компиляция запроса в базу данных
    with open("info.txt", 'w') as f:        #выполнение запроса в базу данных
        for x in data:
            f.write(x+'\n')
    session.close()
    f.close()
    return render_template('exs.html')

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/profile.html')
def profile():
    return render_template('profile.html')

@app.route('/logout.html')
def logout():
    return render_template('logout.html')

import time

@app.route('/register.html')
def register():
    time.sleep(2)
    return render_template('register.html')

@app.route('/rules.html')
def rules():
    return render_template('rules.html')

@app.route('/checkUser.html', methods=['POST'])
def check_user():
    #if request.method == 'POST':
    data = request.data.decode("utf-8")
    login_psw = data.split('&')
    new_user = User(email=login_psw[0], password_hash=login_psw[1])  # Create an instance of the User class
    flag = checkUser(new_user)
    session.close()
    if flag:
        return 'ok'
    else:
        return 'not ok'

@app.route('/newReg.html', methods=['POST'])
def post_data():
    print(321)
    print(request.data)
    print(request.get_json())

    #time.sleep(10)
    #return 'ss'
    data = request.data.decode("utf-8")
    print(request.get_json())
    login_psw = data.split('&')
    # try:
    new_user = User(email=login_psw[0], password_hash=login_psw[1])  # Create an instance of the User class

    if checkLogin(new_user):
        session.close()
        print('here2')
        return 'not ok'
    else:
        addUser(new_user)
        session.close()
        print('here')
        return 'ok'

    print('bad')
    with open("info.txt", 'w') as f:
        #db.create_session(User)
        f.write(str(data))
        f.write(str(selectAll().first()))
        f.write("dsfsfdssss222")
    f.close()
    session.close()
    print('sads')
    return 'ok'
    #return render_template('profile.html') #'200 okkkkkkkkkkk'

    # with open("info.txt", 'w') as f:
    #     f.write("dsfsfdssss1000")
    # f.close()
    # return 'asd'

@app.route('/1233')
def we():
    return '31233213'

if __name__ == '__main__':
    # with open("info.txt", 'w') as f:
    #     f.write("dd")
    # f.close()
    app.run(Debug=True)
