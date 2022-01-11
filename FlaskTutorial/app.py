from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/signin', methods=['GET'])
def signin_form():
    return render_template('form.html')

@app.route('/signin', methods=['POST'])
def signin():
    # 需要从request对象读取表单内容
    if request.form['username'] == 'admin' and request.form['password'] == 'password':
        a = 3
        b = a*2
        te = a*b
        print(te)
        return '<h3>Hello, admin!</h3>'
    return '<h3>Bad username or password.</h3>'

##########################################
if __name__ == '__main__':
    app.run()
