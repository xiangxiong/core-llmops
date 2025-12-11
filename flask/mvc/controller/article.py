from flask import Blueprint

article = Blueprint('article', __name__);

@article.route("/article/add")
def add_article():
    return "<p>添加文章成功</p>"

@article.route("/article/update")
def update_article():
    return "<p>更新文章成功</p>"