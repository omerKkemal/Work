# =========================================================================== #
# Author: Omer Kemal                                                          #
# Website: https://www.johndoe.com                                            #
# Social Media:                                                               #
#   - Facebook: https://www.facebook.com/johndoe                              #
#   - Telegram: https://t.me/johndoe                                          #
#   - Twitter: @JohnDoe                                                       #
#   - GitHub: https://github.com/johndoe                                      #
# =========================================================================== #

from datetime import datetime
import random
import string
import filelock
import os


class Setting:
    """
    The Setting class is responsible for storing application settings and
    providing utility methods for generating random identifiers, logging events,
    and managing configuration paths and database details.
    """

    def setting_var(self):
        """
        This function initializes various application settings, including:
        - Secret key for the application
        - Event and log message constants
        - Paths for log files and database files
        - Database connection URI
        - Admin user credentials
        - User roles and access levels
        - Folder paths for static files and templates

        These settings can be used across the application for consistent configuration.
        """
        # app setting
        self.SECRAT_KEY = random.choices(
            string.ascii_uppercase + string.ascii_lowercase + string.digits, k=100
        )

        # event messages
        self.NONE_LOGIN_MESSAGE = "login first"

        # log dir path
        self.LOG_DIR = "data/log/"

        # excel dir
        self.EXCEL_DIR = "data/excel/"

        # email setting
        self.EMAIL_PASSWORD = 'your password'
        self.EMAIL = 'your email(gmail)'
        self.SMTP_LINK = 'smtp.gmail.com'
        self.SMTP_PORT = 587
        self.EMAIL_TYPE = "html"

        # database config
        self.LOG_FILE_NAME = "log.txt"
        self.DB_NAME = "student.db"
        self.DB_DIR = 'data/db'
        self.JSON_FILE_NAME = 'memory.json'
        self.DB_URI = f'sqlite:///{self.DB_DIR}/{self.DB_NAME}'

        self.RESOURCE_TYPE = ['assigment','work sheet','extra books']

        # Admin credentials
        self.ADMIN_USER_NAME = 'admin'
        self.ADMIN_PASSWORD = 'admin'

        # available roles in the system
        self.ROLES = ['admin', 'student', 'parent', 'teacher']

        # blueprint names for different areas of the application
        self.ADMIN = 'admin'
        self.STUDENT = 'student'
        self.TEACHER = 'teacher'
        self.EVENT = 'event'

        # folder paths for static and template resources
        self.STATIC_FOLDE = 'static'
        self.STATIC_FOLDE_PATH = '/static'
        self.TEMPLATE_FOLDER = 'templates'

        # resource config
        self.RESOURCE_PATH = f'{self.STATIC_FOLDE_PATH}/resources'
        self.WORK_SHEET_FOLDER = '/work_sheet'
        self.EXTRA_RESOURCE_LINK_PATH = f'{self.RESOURCE_PATH}/extra_resources'
        self.WORK_SHEET_LINK_PATH = f'{self.RESOURCE_PATH}/work_sheet'
        self.RESOURCE_FULL_PATH = 'C:\\Users\\hacker\\PycharmProjects\\Work\\static\\resources'
        self.EXTRA_RESOURCE_PATH = f'{self.RESOURCE_FULL_PATH}/extra_resources'
        self.WORK_SHEET_PATH = f'{self.RESOURCE_FULL_PATH}/work_sheet'

        # Access levels for teachers
        self.ACCSESS = ['ReadOnly', 'Read&Write', 'Forbidden']
        self.SUBJECT_PRIVLAGE = ['ReadOnly','Read&Write']


        self.ALLOWED_EXTENSIONS = {'txt', 'png', 'jpg', 'jpeg', 'gif','pdf','pp','doc','docx','xls','xlsx'}

    def ID(self,n=5):
        """
        Generates a random alphanumeric ID of length 5. This ID can be used
        for creating unique identifiers for entities in the system, such as users,
        events, or records.

        Returns:
            str: A randomly generated 5-character string consisting of uppercase letters,
                 lowercase letters, and digits.
        """
        RandomID = ''.join(
            random.choices(
                string.ascii_uppercase + string.ascii_lowercase + string.digits, k=n
            )
        )
        return RandomID

    def log(self, event):
        """
        Records an event in the application log file with a timestamp.
        The event is appended to a log file with a date and time when it occurred.

        A file lock is used to prevent simultaneous access to the log file, ensuring
        thread safety when logging events.

        Args:
            event (str): The event message that describes the action or occurrence.
        """
        # Use file lock to prevent concurrent access to the log file
        lock = filelock.FileLock('counter.lock')
        event_rec = datetime.now()  # Capture the current timestamp

        with lock:
            # Open the log file in append mode and write the event with timestamp
            with open(self.LOG_DIR + self.LOG_FILE_NAME, "a") as f:
                f.write(f"[  {str(event_rec)}  ] : {str(event)}\n")

