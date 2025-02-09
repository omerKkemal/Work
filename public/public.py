# =========================================================================== #
# Author: Omer Kemal                                                          #
# Website: https://www.johndoe.com                                            #
# Social Media:                                                               #
#   - Facebook: https://www.facebook.com/johndoe                              #
#   - Telegram: https://t.me/johndoe                                          #
#   - Twitter: @JohnDoe                                                       #
#   - GitHub: https://github.com/johndoe                                      #
# =========================================================================== #

from flask import Blueprint, url_for, render_template

from database.manage_db import var

public = Blueprint(
    'public', __name__,
    static_folder=var.STATIC_FOLDE, static_url_path=var.STATIC_FOLDE_PATH, template_folder=var.TEMPLATE_FOLDER
)


@public.route('/')
def index():
    return render_template('index.html')

@public.route("/about")
def about():
    pass
