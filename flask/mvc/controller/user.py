from flask import Blueprint

user = Blueprint('user', __name__)
@user.route("/user/add")
def add_user():
    return "<p>添加用户成功</p>"
        
@user.route("/user/update")
def update_user():
    return "<p>更新用户成功</p>"