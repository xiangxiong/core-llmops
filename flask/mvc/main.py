# 导入flask
from flask import Flask
from controller.user import user
from controller.article import article

app = Flask(__name__)
app.register_blueprint(user)
app.register_blueprint(article) 
    
if __name__ == '__main__':
    app.run(debug=True)