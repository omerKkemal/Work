# =========================================================================== #
# Author: Omer Kemal                                                          #
# Website: https://www.johndoe.com                                            #
# Social Media:                                                               #
#   - Facebook: https://www.facebook.com/johndoe                              #
#   - Telegram: https://t.me/johndoe                                          #
#   - Twitter: @JohnDoe                                                       #
#   - GitHub: https://github.com/johndoe                                      #
# =========================================================================== #

from sqlalchemy import ForeignKey, String, Integer, Column, Float
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class base_db(Base):
    ...
