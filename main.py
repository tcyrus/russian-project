import os
from flask import Flask,session,request,render_template,redirect,url_for
from flask.ext.login import LoginManager,current_user,login_required,login_user,logout_user,UserMixin
from flask.ext.sqlalchemy import SQLAlchemy

tmpl_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)),'templates')

app=Flask(__name__,template_folder=tmpl_dir)
app.config.from_pyfile("config.py")
db=SQLAlchemy(app)
login_manager=LoginManager()
login_manager.init_app(app)

# User class
class DbUser(object):
    """Wraps User object for Flask-Login"""
    def __init__(self, user):
        self._user=user
    def get_id(self):
        return unicode(self._user.id)
    def is_active(self):
        return self._user.enabled
    def is_anonymous(self):
        return False
    def is_authenticated(self):
        return True

@login_manager.user_loader
def load_user(user_id):
    user=User.query.get(user_id)
    if user:
        return DbUser(user)
    else:
        return None

@app.route('/',methods=['GET','POST'])
def home():
  return render_template('index.html',login=current_user.is_authenticated())

@app.route('/login',methods=['GET','POST'])
def login():
  error=None
  if request.method=='POST':
      username=request.form['username']
      password=request.form['password']
      if authenticate(app.config['AUTH_SERVER'],username,password):
        user=User.query.filter_by(username=username).first()
        if user:
          if login_user(DbUser(user)):
            # do stuff
            flash("You have logged in")
            return redirect(url_for("dashboard"))
      error="Login failed"
  else:
    return render_template("login.html",error=error)

@app.route("/settings")
@login_required
def settings():
    pass

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have logged out')
    return redirect(url_for("home"))

@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    """
    Dashboard
    """
    return render_template("dashboard.html")

if __name__=='__main__':
    app.run()
