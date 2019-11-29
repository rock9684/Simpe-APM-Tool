from flask import Flask,session
from flask_bcrypt import Bcrypt

webapp= Flask(__name__)

webapp.config['SECRET_KEY'] = "c7e22c3ba94bd20390e19e9954796d8b"

bcrypt = Bcrypt(webapp)
AWS_ACCESS_KEY = 'AKIAIJK4UQ7KTGQZY4OQ'
AWS_SECRET_KEY = '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'

from app import route
