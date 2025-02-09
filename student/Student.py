from flask import Flask,request,render_template,Blueprint

Student = Blueprint('student', __name__,static_folder='static',static_url_path='/static',template_folder='templates')

@Student.route('/student')
def index():
    return "Student page"
