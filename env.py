import os

MONGO_DBNAME = os.environ.setdefault('MONGO_DBNAME', 'myfirstdb')
MONGO_URI = os.environ.setdefault('MONGO_URI', 'mongodb+srv://Sebson1990:ZJREXjhCSSPZOp66@cluster0.g4vuv.mongodb.net/myfirstdb?ssl=true&ssl_cert_reqs=CERT_NONE')
SECRET_KEY = os.environ.setdefault("SECRET_KEY", "this is a random secret key")