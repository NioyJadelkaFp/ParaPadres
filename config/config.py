import os

class Config:
    SECRET_KEY = os.urandom(24)
    DB_CONFIG = {
        'host': "by8ekzvhusvvn2yqc71b-mysql.services.clever-cloud.com",
        'user': "uueyyhu8xg3oenlv",
        'password': "VFbwWo8TNmZQbg04Dd7i",
        'database': "by8ekzvhusvvn2yqc71b",
        'cursorclass': 'DictCursor'
    }