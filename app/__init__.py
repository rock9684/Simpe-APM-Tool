from flask import Flask
from config import Config
import mysql.connector
import boto3
import csv

# create flask instance
webapp = Flask(__name__)
# configure the instance using variables defined in config.py
webapp.config.from_object(Config)

# configure and connect to database
db = mysql.connector.connect(
    user=webapp.config['USERNAME'],
    password=webapp.config['PASSWORD'],
    host=webapp.config['HOSTNAME'],
    database=webapp.config['DATABASE'])

from app import routes