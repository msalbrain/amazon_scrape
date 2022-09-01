from pymongo import MongoClient
from env import *

if not db_string:
    client = MongoClient()
elif db_string:
    client = MongoClient(db_string)

db = client["amazon"]
status_col = db["status"]
review_col = db["reviews"]


def reset_status():
    s = status_col.find_one({"_id": 1})
    if s:
        s.update({"active": 0})
        status_col.replace_one({"_id": 1}, s)


import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
# ch = logging.StreamHandler()
fh = logging.FileHandler(filename='./server.log')
formatter = logging.Formatter(
    "%(asctime)s - %(module)s - %(funcName)s - line:%(lineno)d - %(levelname)s - %(message)s"
)

# ch.setFormatter(formatter)
fh.setFormatter(formatter)
# logger.addHandler(ch) #Exporting logs to the screen
logger.addHandler(fh) #Exporting logs to a file


logger = logging.getLogger(__name__)