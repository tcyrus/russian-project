import os
from flask import Flask,session,request,render_template,redirect,url_for
from flask.ext.login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin, confirm_login, fresh_login_required)

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),'templates')

app = Flask(__name__,template_folder=tmpl_dir)
app.config.from_object(__name__)

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

app.config.from_envvar('MAIN_SETTINGS',silent=True)
login_manager=LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    return User.get(userid)

@app.route('/',methods=['GET','POST'])
def home():
  return render_template('index.html',login=current_user.is_authenticated())

@app.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        # login and validate the user...
        login_user(user)
        flash("Logged in successfully.")
        return redirect(url_for("dashboard"))
    return render_template("login.html",form=form)

@app.route("/settings")
@login_required
def settings():
    pass

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    """
    Dashboard
    """
    # ToDo

if __name__=='__main__':
    app.run()
