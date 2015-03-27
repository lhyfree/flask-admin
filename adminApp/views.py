__author__ = 'hongyaoli'

from redis import Redis
from flask import Flask,url_for,request,render_template,redirect,url_for,flash,session,escape
from flask.ext.admin import Admin,BaseView,expose
from flask.ext.admin.contrib.fileadmin import FileAdmin
from flask.ext.admin.contrib import rediscli
from flask.ext.admin.contrib.peewee import ModelView
from models import User,UserInfo,Post


def logged():
    if  "logged_in" in session:
        return True
    else:
        return False

def login_required(func):
    def _loginRequiredInner(*args, **kw):
        if "logged_in" in session:
            return func(*args, **kw)
        else:
            return redirect(url_for('login'))
    return _loginRequiredInner

# Flask views
#@app.route('/')
def index():
    return render_template('index.html')

#@app.route('/h')
@login_required
def hello_world():
    return 'Hello World!'

#@app.route('/login',methods=['GET','POST'])
def login():
    error = ''
    print request,session
    if request.method == 'POST':
        if request.form['username']=='admin' and request.form['password']=='123456':
            session['username'] = 'admin'
            session['logged_in'] = 1
            flash('You were successfully logged in')
            url_next=request.args.get('next')
            if url_next:
                return redirect(url_next)
            else:
                return redirect(url_for('index'))
        else:
            error = 'Invalid username/password'
    else:
        if logged():
            return redirect(url_for('index'))
    return render_template('login.html',error=error)

#@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('You were logged out')
    return redirect(url_for('login'))


class MyAuthBaseView(BaseView):
    def is_accessible(self):
        return logged()

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('login', next=request.url))


class MyView(MyAuthBaseView):
    @expose('/')
    def index(self):
        return self.render('admin/myview.html')


class MyFileAdmin(FileAdmin,MyAuthBaseView):
    pass


class MyRedisCli(rediscli.RedisCli,MyAuthBaseView):
    pass


class MyBaseModelView(ModelView):
    def is_accessible(self):
        return logged()

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('login', next=request.url))


class UserAdmin(MyBaseModelView):
    inline_models = (UserInfo,)


class PostAdmin(MyBaseModelView):
    # Visible columns in the list view
    column_exclude_list = ['text']
    # List of columns that can be sorted. For 'user' column, use User.email as
    # a column.
    column_sortable_list = ('title', ('user', User.email), 'date')
    # Full text search
    column_searchable_list = ('title', User.username)
    # Column filters
    column_filters = ('title',
                      'date',
                      User.username)
    form_ajax_refs = {
        'user': {
            'fields': (User.username, 'email')
        }
    }
