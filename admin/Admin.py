# =========================================================================== #
# Author: Omer Kemal                                                          #
# Website: https://www.johndoe.com                                            #
# Social Media:                                                               #
#   - Facebook: https://www.facebook.com/johndoe                              #
#   - Telegram: https://t.me/johndoe                                          #
#   - Twitter: @JohnDoe                                                       #
#   - GitHub: https://github.com/johndoe                                      #
# =========================================================================== #

from flask import request, render_template, Blueprint, url_for, redirect, session
from sqlalchemy.orm import sessionmaker
import os

from utility._templates_filters import getlist
from utility.data_processor import read_from_json,allowed_file
from database.modle import Student, Teacher, CreatAssessment, Assessment, Sections, thought, Parent, Subjects, Resource
from database.manage_db import var, engine


Admin = Blueprint(
    var.ADMIN, __name__,
    static_folder=var.STATIC_FOLDE,
    static_url_path=var.STATIC_FOLDE_PATH,
    template_folder=var.TEMPLATE_FOLDER
)
Session = sessionmaker(bind=engine)
_session = Session()

Admin.add_app_template_filter(getlist, 'getList')

# student info (done!!!!)
@Admin.route('/admin/panal', methods=['GET'])
def admin():
    if "username" in session:
        if session["role"] == "admin":
            return render_template('admin_panal.html')
        else:
            return redirect(url_for('event.unautrized'))
    else:
        return redirect(url_for('Login.login'))


# add student(done!!!)
@Admin.route('/admin/panal/add_students', methods=['GET', 'POST'])
def add_students():
    try:
        if 'username' in session:
            data, _data = read_from_json()
            gender = data.Permanent.Gender
            grades = data.Permanent.grade
            sections = data.Permanent.section
            if session['role'] == 'admin':
                if request.method == 'POST':
                    fname = request.form['fname']
                    mname = request.form['mname']
                    lname = request.form['lname']
                    Grade = request.form['grade']
                    _gender = request.form["gender"]
                    _Section = request.form['section']
                    ID = var.ID()
                    exist = _session.query(Sections).filter(
                        Sections.section == _Section.upper(),
                        Sections.grade == Grade
                    ).first()

                    reg = Student(
                        ID, fname, mname, lname, _gender,
                        ID+fname, _Section.upper(), Grade
                    )
                    print(reg)
                    try:
                        if not exist:
                            section = Sections(var.ID(), _Section.upper(), Grade)
                            _session.add(section)
                            _session.commit()
                            print('section was added')

                        _session.add(reg)
                        _session.commit()
                        print('student was added')
                        message = 'meassage'
                        return redirect(url_for('event.successful'))
                    except Exception as e:
                        _session.rollback()
                        var.log(f"Error occurred: {e}")
                        return redirect(url_for('event.internal_server_error'))
                else:
                    return render_template(
                        'add_students.html',
                        sections=sections, gender=gender,grades=grades
                    )
            else:
                return redirect(url_for('event.unautrized'))
        else:
            return redirect(url_for('Login.login'))
    except Exception as e:
        var.log(f"Error occurred: {e}")
        return redirect(url_for('event.internal_server_error'))
    finally:
        _session.close()


# add student()
@Admin.route('/admin/panal/add_student/<grade>/<section>', methods=['GET', 'POST'])
def add_student(grade=None, section=None):
    try:
        if 'username' in session:
            if session['role'] == 'admin':
                data, _data = read_from_json()
                gender = data.Permanent.Gender
                if request.method == 'POST':
                    if grade and section:
                        fname = request.form['fname']
                        mname = request.form['mname']
                        lname = request.form['lname']
                        _gender = request.form["gender"]
                        ID = var.ID()
                        data, _data = read_from_json()
                        gender = data.Permanent.Gender
                        reg = Student(
                            ID,  fname, mname,
                            lname, _gender,ID+fname, section.upper(), grade
                        )
                        print(reg)
                        try:
                            _session.add(reg)
                            _session.commit()
                            print('student was added')
                            _session.close()
                            return redirect(url_for('event.successful'))
                        except Exception as e:
                            var.log(f"Error occurred: {e}")
                            return redirect(url_for('event.internal_server_error'))
                    else:
                        return redirect(url_for('event.error'))
                else:
                    data, _data = read_from_json()
                    gender = data.Permanent.Gender
                    return render_template('add_student.html', gender=gender, grade=grade, section=section)
            else:
                return redirect(url_for('event.unautrized'))
        else:
            return redirect(url_for('Login.login'))
    except Exception as e:
        var.log(f"Error occurred: {e}")
        return redirect(url_for('event.internal_server_error'))
    finally:
        _session.close()


@Admin.route('/admin/panal/section_info')
def info():
    try:
        if 'username' in session:
            if session['role'] == 'admin':
                sections = _session.query(Sections).all()
                print(sections)
                return render_template('info_section.html', sections=sections)
            else:
                return redirect(url_for('event.unautrized'))
        else:
            return redirect(url_for('Login.login'))
    except Exception as e:
        var.log(f"Error occurred: {e}")
        return redirect(url_for('event.internal_server_error'))
    finally:
        _session.close()


@Admin.route('/admin/panal/get_students/<grade>/<section>')
def get_students(grade=False, section=None):
    try:
        if 'username' in session:
            if session['role'] == 'admin':
                if grade and section:
                    students = _session.query(Student).filter_by(grade=grade, section=section).all()
                    return render_template(
                        'get_students.html', students=students, grade=grade, section=section
                        )
                else:
                    return 'No grade provided'
            else:
                return redirect(url_for('event.unauthorized'))
        else:
            return redirect(url_for('Login.login', message=var.NONE_LOGIN_MESSAGE))
    except Exception as e:
        var.log(f"Error occurred: {e}")
        return redirect(url_for('event.internal_server_error'))
    finally:
        _session.close()

# update basic info(name and gender)
@Admin.route('/admin/panal/update_student_Basic/<ID>', methods=['GET', 'POST'])
def update_student_Basic(ID):
    try:
        if 'username' in session:
            _student = _session.query(Student).filter_by(ID=ID).all()
            student = getlist(_student)
            data, _data = read_from_json()
            sections = data.Permanent.section
            grades = data.Permanent.grade
            gender = data.Permanent.Gender
            if session['role'] == 'admin':
                if request.method == 'GET':
                    return render_template('basic_update.html', student=student,gender=gender,grades=grades,sections=sections)
                elif request.method == 'POST':
                    student_fname = request.form['fname']
                    student_mname = request.form['mname']
                    student_lname = request.form['lname']
                    student_gender = request.form["gender"]

                    _session.query(Student).filter_by(ID=ID).update({
                        'fname': student_fname,
                        'mname': student_mname,
                        'lname': student_lname,
                        'gender': student_gender
                    })
                    _session.commit()
                    _session.close()
                    print(student)
                    return redirect(url_for('event.successful'))
            else:
                return redirect('event.unauthorized')
        else:
            return redirect(url_for('login.Login'))
    except Exception as e:
        var.log(f"Error occurred: {e}")
        return redirect(url_for('event.internal_server_error'))
    finally:
        _session.close()


# reset password
@Admin.route('/admin/panal/reset_password/<role>/<ID>')
def reset_password(role,ID):
    try:
        if 'username' in session:
            if session['role'] == 'admin':
                if role == 'teacher':
                    endpoint = "info"
                    teacher = getlist(_session.query(Teacher).filter_by(ID=ID).all())
                    new_password = teacher[0][0] + teacher[0][1]
                    _session.query(Teacher).filter_by(ID=ID).update({
                        'password': new_password
                    })
                elif role == "student":
                    endpoint = "options"
                    student = getlist(_session.query(Student).filter_by(ID=ID).all())
                    new_password = student[0][0] + student[0][1]
                    _session.query(Student).filter_by(ID=ID).update({
                        'password': new_password
                    })
                elif role == 'parent':
                    parent = getlist(_session.query(Parent).filter_by(ID=ID).all())
                    new_password = parent[0][0] + parent[0][1]
                    _session.query(Parent).filter_by(ID=ID).update({
                        'password': new_password
                    })
                
                _session.commit()
                return redirect(url_for(f"admin.update_{endpoint}",ID=ID))
            else:
                return redirect('event.unauthorized')
        else:
            return redirect(url_for('login.Login'))
    except Exception as e:
        var.log(f"Error at reset occurred: {e}")
        return redirect(url_for('event.internal_server_error'))
    finally:
        _session.close()
# update advance(section , grade and change password)
@Admin.route('/admin/panal/update_options/<ID>')
def update_options(ID):
    try:
        if 'username' in session:
            if session['role'] == 'admin':
                _student = _session.query(Student).filter_by(ID=ID).all()
                student = getlist(_student)
            
                return render_template('update_options.html', student=student)
            else:
                return redirect('event.unauthorized')
        else:
            return redirect(url_for('login.Login'))
    except Exception as e:
        var.log(f"Error occurred: {e}")
        return redirect(url_for('event.internal_server_error'))
    finally:
        _session.close()


# teacher
@Admin.route('/admin/panal/add_teacher',methods=['POST', 'GET'])
def add_teacher():
    try:
        if 'username' in session:
            if session['role'] == 'admin':
                if request.method == 'POST':
                    fname = request.form["fname"]
                    mname = request.form["mname"]
                    lname = request.form["lname"]
                    gender = request.form["gender"]
                    try:
                        teacher = Teacher(
                            var.ID(), fname, mname,
                            lname,gender,var.ID() + fname
                        )
                        _session.add(teacher)
                        _session.commit()
                        return redirect(url_for('event.successful'))
                    except Exception as e:
                        print(e)
                        _session.rollback()
                        return redirect(url_for('event.internal_server_error'))
                elif request.method == "GET":
                    data, _data = read_from_json()
                    gender = data.Permanent.Gender
                    return render_template(
                        'add_techer.html',gender=gender
                    )
            else:
                return redirect('event.unauthorized')
        else:
            return redirect(url_for('Login.login'))
    except Exception as e:
        var.log(f"Error occurred: {e}")
        return redirect(url_for('event.internal_server_error'))
    finally:
        _session.close()

@Admin.route("/admin/panal/get_teachers")
def get_teacher():
    try:
        if "username" in session:
            if session["role"] == "admin":
                teachers = _session.query(Teacher).all()
                return render_template("get_teacher.html", teachers=teachers)
            else:
                return redirect(url_for('event.unauthorized'))
        else:
            return redirect(url_for('Login.login'))
    except Exception as e:
        var.log(f"Error occurred: {e}")
        return redirect(url_for('event.internal_server_error'))
    finally:
        _session.close()


@Admin.route("/admin/panal/update/<ID>")
def update_info(ID):
    try:
        if 'username' in session:
            if session['role'] == 'admin':
                teacher = _session.query(Teacher).filter_by(ID=ID).all()
                teacher = getlist(teacher)
            
                return render_template('update_info.html', teacher=teacher)
            else:
                return redirect('event.unauthorized')
        else:
            return redirect(url_for('login.Login'))
    except Exception as e:
        var.log(f"Error occurred: {e}")
        return redirect(url_for('event.internal_server_error'))
    finally:
        _session.close()

@Admin.route('/admin/panal/add_subject_to_teacher/<ID>',methods=['POST','GET'])
def add_subject_to_teacher(ID=None):
    try:
        if 'username' in session:
            if session['role'] == 'admin':
                if request.method == 'POST':
                    if ID:
                        subject = request.form['subject']
                        grade = request.form['grade']
                        sections = request.form.getlist('sections')
                        for section in sections:
                            try:
                                _thought = thought(
                                    var.ID(),subject,ID,grade, section, var.ACCSESS[1]
                                )
                                _session.add(_thought)
                            except Exception as e:
                                _session.rollback()
                                var.log(f"Error occurred at routte(/admin/panal/add_subject_to_teacher/): {e}")
                        _session.commit()
                        return redirect(url_for('event.successful'))
                    else:
                        return redirect(url_for('event.error'))
                else:
                    data = read_from_json()[0]
                    teacher = _session.query(Teacher).filter_by(ID=ID).all()
                    subjects = getlist(_session.query(Subjects).all())
                    grades = data.Permanent.grade
                    sections = data.Permanent.section
                    return render_template(
                        'add_subject_to_teacher.html', teacher=getlist(teacher),
                        sections=sections,grades=grades,subjects=subjects
                    )
            else:
                return redirect(url_for('event.unauthorized'))
        else:
            return redirect(url_for('Login.login'))
    except Exception as e:
        var.log(f"Error occurred: {e}")
        return redirect(url_for('event.internal_server_error'))


@Admin.route('/admin/panal/remove_subject_from_teacher/<ID>',methods=['POST','GET'])
def remove_subject_from_teacher(ID):
    try:
        if 'username' in session:
            if session['role'] == 'admin':
                if request.method == 'GET':
                    subject_and_gerad = getlist(_session.query(thought).filter_by(teacher_id=ID))
                    by_section = {}
                    sub_id = []
                    sub = ''
                    for i, subject in enumerate(subject_and_gerad):
                        sub_id.append(subject[1])
                         # If it's the first subject, initialize the dictionary with this sub_id
                        if i == 0:
                            print(sub_id)
                            sub = getlist(_session.query(Subjects).filter_by(ID=sub_id[0]).all())[0][1]
                            by_section[sub] = [[subject[0],subject[3], subject[4]]]
                        else:
                            print(sub_id)
                            # If the current sub_id matches the previous one, append to the existing list
                            if sub_id[0] == subject[1]:
                                by_section[sub].append([subject[0],subject[3], subject[4]])
                            else:
                                # If the sub_id changes, initialize a new entry for the new sub_id
                                sub_id[0] = subject[1]
                                sub = getlist(_session.query(Subjects).filter_by(ID=subject[1]).all())[0][1]
                                by_section[sub] = [[subject[0],subject[3], subject[4]]]
                    return render_template('remove_subject_from_teacher.html', by_section=by_section,access=var.ACCSESS,ID=ID)
                
                elif request.method == "POST":
                    thoughts = getlist(_session.query(thought).filter_by(teacher_id=ID).all())
                    accsess = var.ACCSESS
                    old_sub = []
                    for i,_thought in enumerate(thoughts):
                        sub = _thought[0]
                        print("id--",sub)
                        try:
                            if i == 0:
                                old_sub.append(sub)
                            else:
                                if sub != old_sub[0]:
                                    old_sub[0] = sub
                            
                            print(sub)
                            acc = request.form[f'{sub}']

                            print(acc)

                            _session.query(thought).filter_by(teacher_id=ID,ID=acc.split('-')[0]).update({
                                'access_level': acc.split('-')[1]
                            })
                        except Exception as e:
                            print(e)
                    _session.commit()
                    return redirect(url_for('event.successful'))
            
            else:
                return redirect('event.unauthorized')
        else:
             return redirect(url_for('login.Login'))
    except Exception as e:
        var.log(f"Error occurred: {e}")
        return redirect(url_for('event.internal_server_error'))
    finally:
        _session.close()

@Admin.route('/admin/panal/edit_teacher_info/<ID>',methods=['POST','GET'])
def edit_teacher_basic_info(ID=None):
    if 'username' in session:
        if session['role'] == 'admin':
            teacher = getlist(_session.query(Teacher).filter_by(ID=ID).all())
            data, _data = read_from_json()
            gender = data.Permanent.Gender
            if request.method == "GET":
                return render_template('edit_teacher_info.html', gender=gender,teacher=teacher)
            elif request.method == "POST":
                teacher_fname = request.form['fname']
                teacher_mname = request.form['mname']
                teacher_lname = request.form['lname']
                teacher_gender = request.form['gender']
                try:
                    _session.query(Teacher).filter_by(ID=ID).update({
                        'fname': teacher_fname,
                        'mname': teacher_mname,
                        'lname': teacher_lname,
                        'gender': teacher_gender
                    })
                    _session.commit()
                    return render_template('edit_teacher_info.html', gender=gender,teacher=teacher)
                except Exception as e:
                    _session.rollback()
                    print(e)
                    return 'error'

        else:
            return redirect(url_for('event.unauthorized'))
    else:
        return redirect(url_for('Login.login'))


# resource

@Admin.route('/resource_option')
def resource_option():
    if 'username' in session:
        if session['role'] == "admin":
            return render_template('resource_option.html')
    else:
        ...


@Admin.route("/add_resource",methods=['POST','GET'])
def add_resourc():
    try:
        if "username" in session:
            role = session['role']
            if request.method == "POST":
                file_property = request.files['files']
                description = request.form['description']
                resource_type = request.form['resource_type']
                userID = session['userID']
                sections_id = request.form['section']
                if session['role'] == "admin":
                    if allowed_file(filename=file_property.filename):
                        if resource_type == var.RESOURCE_TYPE[1] or resource_type == var.RESOURCE_TYPE[0]:
                            file_property.save(
                                os.path.join(
                                    var.WORK_SHEET_PATH,
                                    file_property.filename
                                )
                            )
                            PATH = var.WORK_SHEET_LINK_PATH

                        elif resource_type == var.RESOURCE_TYPE[2]:
                            file_property.save(
                                os.path.join(
                                    var.EXTRA_RESOURCE_PATH,
                                    file_property.filename
                                )
                            )
                            PATH = var.EXTRA_RESOURCE_LINK_PATH
                        valid = 1

                        resourcs = Resource(
                            var.ID(),sections_id,description,
                            file_property.filename,PATH,
                            "None",userID,resource_type,valid
                        )
                        _session.add(resourcs)
                        _session.commit()
                        return 'succsess'
                    return "not allowed"
                elif session['role'] == 'teacher':
                    valid = 0
                    resourcs = Resource(
                        var.ID(),sections_id,description,
                        file_property.filename,var.RESOURCE_FULL_PATH,
                        userID,"None",resource_type,valid
                    )
                    _session.add(resourcs)
                    _session.commit()
                    return 'succsess'
            else:
                sections = getlist(_session.query(Sections).all())
                return render_template("uplaod_resource.html",sections=sections,resource=var.RESOURCE_TYPE)
        else:
            return 'i am the problam'
    except Exception as e:
        var.log(e)
        return str(e)


@Admin.route("/view_resource")
def view_resour():
    try:
        if "username" in session:
            role = session['role']
            all_resources = getlist(_session.query(Resource).all())
            return render_template('view_resources.html',all_resources=all_resources,role=role)
        else:
            return redirect(url_for('Login.login'))
    except Exception as e:
        var.log(e)
        return 'error'

# Delete

@Admin.route('/admin/panal/delete_student', methods=['POST'])
def delete_student():
    try:
        if 'username' in session:
            if session['role'] == 'admin':
                data = request.get_json()
                student = _session.query(Student).filter_by(ID=data['id']).first()

                if student is None:
                    return {'message': 'Student not found'}, 404  # Return error if student doesn't exist

                _session.delete(student)
                _session.commit()

                return {'message': 'Student deleted successfully'}, 200  # Return success message as JSON

            else:
                return {'message': 'Unauthorized access'}, 403  # Return unauthorized status if user is not admin
        else:
            return {'message': 'Not logged in'}, 401  # Return not authorized status if session doesn't exist

    except Exception as e:
        _session.rollback()  # Rollback if any error occurs
        var.log(f"Error occurred: {e}")
        return {'message': 'An error occurred while deleting student'}, 500  # Return general error response

    finally:
        _session.close()  # Ensure session is closed


@Admin.route('/admin/panal/delete_resource', methods=['POST'])
def delete_resource():
    try:
        if 'username' in session:
            if session['role'] == 'admin':
                data = request.get_json()
                resource = getlist(_session.query(Resource).filter_by(ID=data['id']).all())
                
                print('omer',resource)

                if resource is None:
                    return {'message': 'Resource not found'}, 404  # Return error if Teacher doesn't exist
                
                if 'work_sheet' in resource[0][4]:
                     path = os.path.join(var.WORK_SHEET_PATH,resource[0][3])
                else:
                    path = os.path.join(var.EXTRA_RESOURCE_PATH ,resource[0][3])
                if os.path.exists(path):
                    os.remove(path)
                    print('path',path)
                delete = _session.query(Resource).filter_by(ID=data['id']).first()
                _session.delete(delete)
                
                _session.commit()

                return {'message': 'Resource deleted successfully'}, 200  # Return success message as JSON

            else:
                return {'message': 'Unauthorized access'}, 403  # Return unauthorized status if user is not admin
        else:
            return {'message': 'Not logged in'}, 401  # Return not authorized status if session doesn't exist

    except Exception as e:
        _session.rollback()  # Rollback if any error occurs
        var.log(f"Error occurred: {e}")
        return {'message': 'An error occurred while deleting Resource'}, 500  # Return general error response

    finally:
        _session.close()  # Ensure session is closed


@Admin.route('/admin/panal/delete_teacher', methods=['POST'])
def delete_teacher():
    try:
        if 'username' in session:
            if session['role'] == 'admin':
                data = request.get_json()
                student = _session.query(Teacher).filter_by(ID=data['id']).first()

                if student is None:
                    return {'message': 'Teacher not found'}, 404  # Return error if Teacher doesn't exist

                _session.delete(student)
                _session.commit()

                return {'message': 'Teacher deleted successfully'}, 200  # Return success message as JSON

            else:
                return {'message': 'Unauthorized access'}, 403  # Return unauthorized status if user is not admin
        else:
            return {'message': 'Not logged in'}, 401  # Return not authorized status if session doesn't exist

    except Exception as e:
        _session.rollback()  # Rollback if any error occurs
        var.log(f"Error occurred: {e}")
        return {'message': 'An error occurred while deleting Teacher'}, 500  # Return general error response

    finally:
        _session.close()  # Ensure session is closed

