# 导入flask
from flask import Flask;
from controller.user import user;
from controller.article import article;
from flask import session;
from flask import request;
import os;

app = Flask(__name__)

# 启用session
app.config["SECRET_KEY"] = os.urandom(24); # 生成一个随机的24位字节, 作为session的密钥
app.register_blueprint(user)
app.register_blueprint(article) 

@app.route("/login")
def login():
    session['isLogin'] = True
    return "<p>登录成功</p>"

@app.route("/update_user")
def update_user():
    return "<p>更新用户成功</p>"

# 全局拦截器
@app.before_request
def before():
    # 获取用户的url
    url = request.path;
    print(url);

    # 白名单
    pass_paths = [
        '/',
        '/login',
        '/reg'
    ];

    # 定义一个可通过的后缀名
    suffix = url.endswith("png") or url.endswith("jpg") or url.endswith("css") or url.endswith("js")

    if url in pass_paths or suffix:
        pass
    # if url == '/login':
    #     # return "<p>登录成功11</p>"
    #     pass
    else:
        if_login = session.get('isLogin')
        if  if_login != True:
            return "<p>请登录3</p>"
    
if __name__ == '__main__':
    app.run(debug=True)