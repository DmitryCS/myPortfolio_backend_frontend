from flask import Flask, render_template, redirect, request
from sqlalchemy import create_engine

# использовать для логирования в файл
# open('error.log', 'w').close()
# import logging
#
# logging.basicConfig(filename='error.log', level=logging.DEBUG)

engine = create_engine('sqlite:///mydb.db', echo=True)

from sqlalchemy.ext.declarative import declarative_base
#from models import User

base = declarative_base()


#database
from sqlalchemy import Column, String, Integer, ForeignKey


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


from sqlalchemy.orm import relationship
class UserData(base):
    __tablename__ = 'usersData'
    id = Column(Integer, primary_key=True)
    #id_user = Column(Integer, ForeignKey("users.id"), nullable=False)
    id_user = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(120))
    surname = Column(String(120))
    photoRef = Column(String(120))
    user = relationship('User', backref='uData')

    def __repr__(self):
        return '<Name %s, Surname %s, PhotoRef %s>' % (self.name, self.surname, self.photoRef)
#database

base.metadata.create_all(engine)

from sqlalchemy.orm.session import sessionmaker
session = sessionmaker(bind=engine)()


def addUserByEmailPsw(email, psw):
    user_ivan = User(name=email, fullname=psw)
    session.add(user_ivan)
    session.commit()
    session.close()

def addUser(user):
    session.add(user)
    session.commit()
    session.close()

def deleteUser(user):
    session.query(User).filter(User.email == user.email).delete()
    session.commit()
    session.close()

def selectAll():
    s = session.execute("select * from users order by id desc")  # позволяет делать запросы напрямую
    return s


def getListOfUsers():
    data = map(str, selectAll())  # только компиляция запроса в базу данных
    res = []
    for x in data:
      res.append(x)
    session.close()
    return res


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

@app.route('/grid.html')
def grid():
    return render_template('grid.html')


@app.route('/login.html')
def login():
    return render_template('login.html')


@app.route('/profile.html')
def profile():
    # user = User(email='i',password_hash='o')
    # user.uData = [UserData(name="Jack", surname="Brown", photoRef="no")]
    # print(user)
    # session.add(user.uData)
    # session.commit()
    # s = session.execute("select * from usersData order by id desc")
    # data = map(str, s)  # только компиляция запроса в базу данных
    # res = []
    # for x in data:
    #   res.append(x)
    # session.close()
    # print('\n'.join(res))
    return render_template('profile.html')


@app.route('/logout.html')
def logout():
    return render_template('logout.html')

import time


@app.route('/register.html')
def register():
    #time.sleep(2)
    return render_template('register.html')


@app.route('/rules.html')
def rules():
    return render_template('rules.html')


@app.route('/checkUser.html', methods=['POST'])
def check_user():
    #time.sleep(10)
    #if request.method == 'POST':
    data = request.data.decode("utf-8")
    login_psw = data.split('&')
    new_user = User(email=login_psw[0], password_hash=login_psw[1])  # Create an instance of the User class
    flag = checkUser(new_user)
    session.close()
    if flag:
        app.logger.info('Пользователь вошел в систему')
        print('Пользователь вошел в систему')
        return 'ok'
    else:
        app.logger.info('Пользователь не вошел в систему / Данный пользователь не зарегистрирован')
        print('Пользователь не вошел в систему / Данный пользователь не зарегистрирован')
        return 'not ok'


@app.route('/newReg.html', methods=['POST'])
def post_data():
    print(321)
    #open("info.txt", 'w').write('\n'.join(getListOfUsers()))
    #time.sleep(10)
    #data = request.data.decode("utf-8")
    data = request.get_json()
    login_psw = [data['uname'], data['psw']] #data.split('&')
    new_user = User(email=login_psw[0], password_hash=login_psw[1])  # Create an instance of the User class

    if checkLogin(new_user):
        session.close()
        app.logger.info('Пользователь не зарегистрирован / Возможно данный логин уже существует')
        print('Пользователь не зарегистрирован / Возможно данный логин уже существует')
        return 'not ok'
    else:
        addUser(new_user)
        session.close()
        app.logger.info('Пользователь зарегистрирован')
        print('Пользователь зарегистрирован')
        return 'ok'

'''    print('bad')
    with open("info.txt", 'w') as f:
        #db.create_session(User)
        f.write(str(data))
        f.write(str(selectAll().first()))
        f.write("dsfsfdssss222")
    f.close()
    session.close()
    print('sads')
    return 'ok'
'''

'''
def getIdUser(email):
    q = session.query(User).filter_by(email=email).first()
    print(q['id'])
    return q['id']

def addUserData(dataUser):
    q = "insert into usersData()"
    session.execute("insert into usersData()")
    user_ivan = User(name=email, fullname=psw)
    session.add(user_ivan)
    session.commit()

@app.route('dataUser.html', methods=['POST'])
def post_dataUser():
    data = request.get_json()
    dataUser = [data['email'], data['uname'], data['surname'], data['photo']] #data.split('&')
    if checkLogin(data['email']):
        pass
    else:
        pass
    #new_user = User(email=dataUser[0], =login_psw[1])  # Create an instance of the User class

'''


def getIdUser(email):
    q = "select id from users where email = '{}';".format(email)
    s = session.execute(q)
    print(s)
    idt = s.first().id
    session.close()
    return idt


@app.route('/changeData.html', methods=['POST'])
def updateData():
    data = request.get_json()
    login_psw = [data['email'], data['uname'], data['psw']]
    id = getIdUser(login_psw[0])
    print(login_psw[1])
    q = "update users set email='{}', password_hash='{}' where id = {};".format(str(login_psw[1]), login_psw[2], id)
    session.execute(q)
    session.commit()
    session.close()
    app.logger.info('Данные пользователя обновлены')
    print('Данные пользователя обновлены')
    return "200 ok"


@app.route('/1233')
def we():
    return '31233213'


if __name__ == '__main__':
    app.run(Debug=True)
