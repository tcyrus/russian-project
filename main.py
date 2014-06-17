import os
from flask import Flask,session,request,render_template,redirect,url_for
from flask.ext.login import LoginManager,current_user,login_required,login_user,logout_user,UserMixin
from flask.ext.sqlalchemy import SQLAlchemy

tmpl_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)),'templates')

app=Flask(__name__,template_folder=tmpl_dir)
app.config.from_pyfile("config.py")
db=SQLAlchemy(app)

class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    q = db.Column(db.String(100))
    content = db.Column(db.String(1000))

    def __init__(self, q, content):
        self.content = content
        self.q = q

    def __repr__(self):
        return '<Response %s>' % self.content

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/flashcards/')
def flashcards():
    return render_template('flashcards.html')

@app.route('/letterrules/')
def letterrules():
    return render_template('letter_rules.html')
@app.route('/dashboard/')
def dashboard():
    """
    Dashboard
    """
    return render_template("dashboard.html")

@app.route('/questions/', methods=['GET','POST'])
def questions():
    if request.method == 'POST':
        form = request.form
        name = Response('name', form['name'])
        live = Response('live', form['live'])
        age = Response('age', form['age'])
        time = Response('time', form['time'])
        db.session.add(name)
        db.session.add(live)
        db.session.add(age)
        db.session.add(time)
        db.session.commit()
       
    return render_template("questions.html")

if __name__=='__main__':
    app.run(port=5555)
