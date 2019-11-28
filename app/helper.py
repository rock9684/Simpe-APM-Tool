from imutils.object_detection import non_max_suppression
from app import db
from operator import itemgetter

# query last 30 minutes data
def grab_metrics(metric_name, machine_id):
	cur = db.cursor()
	cur.execute(
		"SELECT `metric_value`, `timestamp` FROM metrics WHERE machineid = '%s' and metric_name = '%s' \
		and timestamp < (now() - interval 30 minute);" % (machine_id, metric_name))

	result = cur.fetchall()
	cur.close()

	result = sorted(result, key=itemgetter(1))

	return result