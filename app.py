# =========================================================================== #
# Author: Omer Kemal                                                          #
# Website: https://www.johndoe.com                                            #
# Social Media:                                                               #
#   - Facebook: https://www.facebook.com/johndoe                              #
#   - Telegram: https://t.me/johndoe                                          #
#   - Twitter: @JohnDoe                                                       #
#   - GitHub: https://github.com/johndoe                                      #
# =========================================================================== #

from flask import Flask

from admin.Admin import Admin
from login.login import Login
from student.Student import Student
from teacher.Teacher import Teachters
from public.public import public
from event.event import event
from database.manage_db import var


app = Flask(__name__)
var.setting_var()

app.jinja_env.globals['enumerate'] = enumerate
app.secret_key = var.SECRAT_KEY

app.register_blueprint(public)
app.register_blueprint(event)
app.register_blueprint(Teachters)
app.register_blueprint(Admin)
app.register_blueprint(Student)
app.register_blueprint(Login)


if __name__ == '__main__':
    app.run(debug=True)
