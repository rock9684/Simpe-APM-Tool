from imutils.object_detection import non_max_suppression
from operator import itemgetter


USERNAME = 'ece1779_project'
PASSWORD = 'ece1779_project_pass'
HOSTNAME = 'ece1779-db.cr7yempg1jxm.us-east-1.rds.amazonaws.com'
DATABASE = 'ece1779_project'

db = mysql.connector.connect(
    user=USERNAME,
    password=PASSWORD,
    host=HOSTNAME,
    database=DATABASE)

# query last 30 minutes data
def grab_metrics(metric_name, machine_id):
	cur = db.cursor()
	cur.execute(
		"SELECT `timestamp`, `metric_value` FROM metrics WHERE machineid = '%s' and metric_name = '%s' \
		and timestamp < (now() - interval 30 minute);" % (machine_id, metric_name))

	result = cur.fetchall()
	cur.close()

	result = sorted(result, key=itemgetter(1))

	return result