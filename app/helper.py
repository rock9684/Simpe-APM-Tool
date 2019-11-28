from imutils.object_detection import non_max_suppression
from app import db

# query last 30 minutes data
def grab_metrics(metric_name, machine_id):