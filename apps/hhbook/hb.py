#!/usr/bin/env python3

from datetime import datetime
import sys
import pytz

class receipt:
    def __init__(self):
        self.date = datetime.now(pytz.timezone('Europe/Berlin'))
        self.store = 0
        self.article = ""


        pass


print(sys.version_info)
print(datetime.now())
