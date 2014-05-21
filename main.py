import os
from flask import Flask,session,request,render_template,redirect,url_for

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('MAIN_SETTINGS',silent=True)

@app.route('/',methods=['GET','POST'])
def home():
  return render_template('site/index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    error=None
    if request.method=='POST':
        if request.form['username']!=app.config['USERNAME']:
            error='Invalid username'
        elif request.form['password']!=app.config['PASSWORD']:
            error='Invalid password'
        else:
            session['logged_in']=True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html',error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    flash('You were logged out')
    return redirect(url_for('home'))

@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    """
    Dashboard
    """
    # ToDo

if __name__=='__main__':
    app.run()
