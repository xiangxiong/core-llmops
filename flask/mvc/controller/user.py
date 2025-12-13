from flask import Blueprint
from flask import request

user = Blueprint('user', __name__)

@user.before_request
def before():
    if request.path.startswith('/v'):
        pass
    else:
        return "<p>请登录</p>"
@user.route("/user/add")
def add_user():
    return "<p>添加用户成功</p>"
        
@user.route("/user/update")
def update_user():
    return "<p>更新用户成功</p>"

@user.route("/v/user/info")
def get_info():
    return "<p>获取用户信息成功</p>"
