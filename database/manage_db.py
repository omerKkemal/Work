# =========================================================================== #
# Author: Omer Kemal                                                          #
# Website: https://www.johndoe.com                                            #
# Social Media:                                                               #
#   - Facebook: https://www.facebook.com/johndoe                              #
#   - Telegram: https://t.me/johndoe                                          #
#   - Twitter: @JohnDoe                                                       #
#   - GitHub: https://github.com/johndoe                                      #
# =========================================================================== #

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.modle import Base, Admin, Subjects
from utility.setting import Setting

# Initialize settings and set variables
var = Setting()
var.setting_var()


# Ensure the database directory exists
def create_db_dir():
    db_dir = var.DB_DIR
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
        return 'db directory has been created ^_^'
    else:
        return 'db directory already exist ^_^'


# Ensure the log directory exists
def create_log_dir():
    log_dir = var.LOG_DIR
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        return 'log directory has been created ^_^'
    else:
        return 'log directory already exist ^_^'


# Ensure the excel directory exists
def create_excel_dir():
    excel_dir = var.EXCEL_DIR
    if not os.path.exists(excel_dir):
        os.makedirs(excel_dir)
        return 'execl directory has been created ^_^'
    else:
        return 'execl directory already exist ^_^'


# Create the engine using the database URI from settings
def _create_engine():
    return create_engine(var.DB_URI)

engine = _create_engine()


# Create all tables defined in the models (if they don't exist yet)
def create_all_db_tables(_engine):
    Base.metadata.create_all(_engine)
    return 'database was created successfully along with the table'


def create_admin_account(_engine):
    # Create a session factory and a new session
    _session = sessionmaker(bind=_engine)
    session = _session()
    exist = session.query(Admin).filter(
        Admin.fullname == var.ADMIN_USER_NAME
    ).first()
    # cahking if the user already exsit
    if not exist:
        # Try to add the admin user, commit if successful, rollback on error
        try:
            admin = Admin(ID=var.ID(), fullname=var.ADMIN_USER_NAME, password=var.ADMIN_PASSWORD)
            session.add(admin)
            session.commit()
            print("Admin user added successfully.")
        except Exception as e:
            session.rollback()  # Rollback the transaction in case of error
            print(f"Error occurred while adding admin: {e}")
        finally:
            session.close()  # Always close the session to clean up resources
    else:
        print('user already exist.')


def default_subject(_engine):
    from utility.data_processor import read_from_json

    _session = sessionmaker(bind=_engine)
    session = _session()
    default_subjects = read_from_json()[1]['Permanent']['subjects']
    for key in default_subjects:
        try:
            subject = Subjects(var.ID(),key,var.SUBJECT_PRIVLAGE[0])
            session.add(subject)
        except Exception as e:
            session.rollback()
            return e
    session.commit()
    return 'Subjects was Added Successfully'