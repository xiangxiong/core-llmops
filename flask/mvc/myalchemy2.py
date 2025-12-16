from sqlalchemy import Table
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Column
from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

engine = create_engine('postgresql://postgres:postgres@localhost:5432/test')

# 连接数据库
session = sessionmaker(engine)
# 保证线程安全
db_session = scoped_session(session)
# 获取基类
Base = declarative_base()

# # sqlalchemy 是支持使用代码进行表结构创建的.
# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     username = Column(String(50), unique=True)
#     password = Column(String(50))

# User.metadata.create_all(engine)

class User(Base):
    __table__ = Table("users",Base.metadata,autoload_with=engine)

@app.route('/login',methods=['post'])
def login():
    request_data = request.get_json();
    username = request_data['username']
    password = request_data['password']

    result = db_session.query(User).filter_by(username=username,password=password).first();
    if result:
        return "登录成功"
    else:
        return "登录失败"

@app.route('/register',methods=['post'])
def register():
    request_data = request.get_json();
    username = request_data['username'];
    password = request_data['password'];

    insertData ={
        "id":2,
        "username":username,
        "password":password
    };
    
    user = User(**insertData);
    db_session.add(user);
    db_session.commit();
    return "注册成功"

@app.route('/updateUser',methods=['post'])
def updateUser():
    request_data = request.get_json();
    username = request_data['username'];
    password = request_data['password'];
    id = request_data['id'];

    updateData ={
        "id":id,
        "username":username,
        "password":password
    };

    row = db_session.query(User).filter_by(id=id).first();
    row.username = username
    row.password = password
    db_session.commit();
    return "更新成功"



    






# 创建一个引擎，目的是连接到我们的数据库上


def index():
    return "<p>Hello, World!</p>"

if __name__ == '__main__':
    app.run(debug=True, port=5002)