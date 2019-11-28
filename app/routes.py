from app import webapp, db
from app.helper import generate_presigned_url
from flask import render_template, request, session, redirect, url_for, jsonify, flash
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from datetime import datetime, timedelta
import os, signal
import time
import csv

@webapp.route('/', methods=['GET', 'POST'])
@webapp.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@webapp.route('/worker_view/<instance_id>', methods=['GET'])
def worker_view(instance_id):
	# set time range to be past 30 min
	# set period to 1 min
    start_time = datetime.utcnow() - timedelta(seconds = 30 * 60)
    end_time = datetime.utcnow()
    period = 60

    cpu_stats = aws_client.get_cpu_utilization(
    	instance_id = instance_id, 
    	start_time = start_time,
    	end_time = end_time,
    	period = period
    )

    http_stats = aws_client.get_http_request_rate(
    	instance_id = instance_id, 
    	start_time = start_time,
    	end_time = end_time,
    	period = period,
    	unit = 'Count'
    )

    return render_template('worker_view.html', instance_id = instance_id, cpu_stats = cpu_stats, http_stats = http_stats)

@webapp.route('/error', methods=['GET'])
def error():
	render_template('error.html')



















