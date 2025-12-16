# 导入flask
from flask import Flask;
from controller.user import user;
from controller.article import article;
from flask import session;
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

@app.errorhandler(404)
def page_not_found(e):
    return "<p>页面不存在404</p>"

@app.errorhandler(500)
def internal_server_error(e):
    return "<p>服务器内部错误500</p>"

if __name__ == '__main__':
    app.run(debug=True)
