import logging
import os
from flask import Flask

from adminApp.views import *



app = Flask(__name__)
app.config['SECRET_KEY'] = '123456790'
app.debug = True

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

app.add_url_rule('/','index', view_func=index)
app.add_url_rule('/hello',view_func=hello_world)
app.add_url_rule('/login',view_func=login,methods=['GET','POST'])
app.add_url_rule('/logout',view_func=logout)

admin = Admin(app,name='My App')
admin.add_view(UserAdmin(User))
admin.add_view(PostAdmin(Post))
admin.add_view(MyView(name='Hello 1', endpoint='test1', category='Test'))
admin.add_view(MyView(name='Hello 2', endpoint='test2', category='Test'))
admin.add_view(MyView(name='Hello 3', endpoint='test3', category='Test'))

admin.add_view(MyView(name='lhy', endpoint='lhy',))
static_path = os.path.join(os.path.dirname(__file__), 'static')
admin.add_view(MyFileAdmin(static_path, '/static/', name='Static Files'))

admin.add_view(MyRedisCli(Redis(host='172.18.21.34')))

if __name__ == '__main__':
    try:
        User.create_table()
        UserInfo.create_table()
        Post.create_table()
    except:
        pass
    app.run(host='0.0.0.0',port=8080)
    #app.run()

