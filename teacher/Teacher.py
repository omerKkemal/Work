from flask import Flask,request,render_template,Blueprint

Teachters = Blueprint('teacher', __name__,static_folder='static',static_url_path='/static',template_folder='templates')

@Teachters.route('/teacher')
def teacher():
    return "teacher page"
