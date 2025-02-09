import smtplib
from email.message import EmailMessage
from sqlalchemy.orm import sessionmaker
from types import SimpleNamespace
import json
#import openpyxl

from utility.setting import Setting
from utility._templates_filters import getlist
from database.modle import avrage,rank,Assessment,Student,CreatAssessment
from database.manage_db import engine

Session = sessionmaker(bind=engine)
_session = Session()

var = Setting()
var.setting_var()

# Define the path to the JSON file
json_file = var.DB_DIR + '/' + var.JSON_FILE_NAME

def sendEmail(subject,body,to):
    msg = EmailMessage()
    msg.add_alternative(body,subtype=var.EMAIL_TYPE)
    msg['Subject'] = subject
    msg['To'] = to
    msg['From'] = var.EMAIL

    with smtplib.SMTP(var.SMTP_LINK,var.SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(var.EMAIL,var.EMAIL_PASSWORD)

        smtp.send_message(msg)

def read_from_json():
    """
    Reads data from the `memory.json` file and returns it as two formats:
    - A `SimpleNamespace` object for easier attribute-based access.
    - A raw Python dictionary (from JSON).

    Returns:
        tuple: A tuple containing two items:
            1. `data` (SimpleNamespace): The JSON data converted into an object.
            2. `_data` (dict): The original dictionary representing the raw data from the JSON file.
    """
    with open(json_file, 'r') as file:
        _data = json.load(file)  # Read the raw data as a Python dictionary
    # Convert the raw data into a SimpleNamespace object for easier attribute access
    data = json.loads(json.dumps(_data), object_hook=lambda d: SimpleNamespace(**d))
    return data, _data

def write_into_json(new_data, memory, location=None):
    """
    Writes new data into the `memory.json` file. The data is inserted into a specified
    memory section and location within the JSON structure. If the location already exists,
    it either appends to the list or updates the dictionary. If the section doesn't exist,
    it is created.

    Args:
        new_data (dict): The new data to be written to the JSON file.
        memory (str): The section of the JSON structure where the data should be added.
        location (str, optional): The specific location within the section to insert the data.

    Returns:
        bool: `True` if the data was successfully written, `False` if there was an issue.
    """
    # Load the current data from the JSON file
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Check if the section exists and if the location is valid
    if memory in data and location:
        # If the location is a list, append the new data
        if isinstance(data[memory][location], list):
            data[memory][location].append(new_data)
        # If the location is a dictionary, update the existing data
        elif isinstance(data[memory][location], dict):
            data[memory][location].update(new_data)
        else:
            print(f"Cannot append data to {memory}: Not a list or dictionary.")
            return False
    else:
        # If the section doesn't exist, initialize it
        # If the section is 'Temporary', store the data as a list, otherwise as a direct object
        data[memory][location] = [new_data] if memory == 'Temporary' else new_data

    # Write the updated data back into the JSON file
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)

    return True

def delete_from_json(memory, key):
    """
    Deletes a key-value pair from a specific section of the `memory.json` file.

    Args:
        memory (str): The section of the JSON structure where the key-value pair is stored.
        key (str): The key to be deleted from the specified section.

    Returns:
        bool: `True` if the deletion was successful, `False` if the key was not found.
    """
    # Read the current data from the JSON file
    data = read_from_json()[1]

    # Check if the section and key exist, then delete the key-value pair
    if memory in data and key in data[memory]:
        del data[memory][key]
        return True
    else:
        return False

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in var.ALLOWED_EXTENSIONS


def student_registor_using_excel():
    ...


def export_strudent_grade(grade,section):
    ...


def login_input_filter():
    ...



def cheack_for_rank(grade,section,teacher_id):
    
    try:
        exit = _session.query(Assessment).filter_by(
            section=section,
            grade=grade
        ).all()
        if len(exit) != 0:
            Students = _session.query(Student).filter_by(
                section=section,
                grade=grade
            ).all()

            totalNumerStudent = len(Students)*len(
                _session.query(CreatAssessment).filter_by(ID=teacher_id).all()
            )

            validStudent = len(exit)

            byPercent = (100*validStudent)/totalNumerStudent

            if byPercent != 100:
                return False

            return True

        return False
    except Exception as e:
        var.log(f"cheack_for_rank --> error {e}")
        return False
    finally:
        _session.close()

def avrage(section,grade,teacher_id):
    if cheack_for_rank(grade,section,teacher_id):
        ...
        student = _session.query(Assessment).filter_by(
            section=section,
            grade=grade
        ).all()
        students = getlist(student)

        for student_assessment in students:
            ...
        
    return 'It is not complite yet'


def rank(grade,section,teacher_id):
    if cheack_for_rank():
        ...
    return 'It is not complite yet'

