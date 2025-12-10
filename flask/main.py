# 导入flask
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>H22ello, World! eee</p>"
    
if __name__ == '__main__':
    app.run(debug=True)
