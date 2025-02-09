from flask import render_template, Blueprint, session, redirect, url_for

from utility.setting import Setting


var = Setting()
var.setting_var()

event = Blueprint(
    'event', __name__,
    static_folder=var.STATIC_FOLDE,
    static_url_path=var.STATIC_FOLDE_PATH,
    template_folder=var.TEMPLATE_FOLDER
)


@event.route('/unauthorized')
def unauthorized():
    if 'username' in session:
        var.log(f" [Unauthorized access] --> (505) By:ID={session['userID']} name={session['username']}")
        return render_template('unauthorized.html')
    else:
        return redirect(url_for('Login.login'))


@event.route('/error')
def error():
    if 'username' in session:
        var.log(f" [Error] --> (400) By:ID={session['userID']} name={session['username']}")
        return render_template('error.html')
    else:
        return redirect(url_for('Login.login'))


@event.route('/successful')
def successful():
    if 'username' in session:
        return render_template('error.html')
    else:
        return redirect(url_for('Login.login'))


@event.route('/internal_server_error')
def internal_server_error():
    if 'username' in session:
        var.log(f"internal_server_error --> (500) By:ID={session['userID']} name={session['username']}")
        return render_template("500.html")
    else:
        return redirect(url_for('Login.login'))
