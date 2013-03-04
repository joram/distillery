from distillery import app

def getActuatorValue(sensor_id, actuator_id):
	return -1

def setActutorValue(sensor_id, actuator_id, actuator_val):
	pass

@app.route("/still/<int:still_id>/actuator/<int:actuator_id>", methods=['GET', 'POST'])
def sensor(still_id,actuator_id):
	if request.method == "GET":
		actuator_val = getActuatorState(still_id, actuator_id)
		return "GET STILL:%s, ACTUATOR:%s" %(still_id,actuator_id)
	else:
		actuator_val = request.form['value']
		setActuatorValue(still_id, actuator_id, actuator_val)
		return "POST STILL:%s, ACTUATOR:%s" %(still_id,actuator_id)
