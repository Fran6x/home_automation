
from flask import Flask, render_template, request, redirect, jsonify
from home_automation import flask_app, db
from .models import Emitters, Sensors, Datas, Types, SensorsRepos, DatasRepos, EmittersRepos 
import time



# instanciation of repos globaly
emittersRepos = EmittersRepos()
sensorsRepos = SensorsRepos()
datasRepos = DatasRepos()


# project home page which is monitor page
@flask_app.route("/")
def index():
	
	templateData = {
	 'emittersRepos': emittersRepos,
	 'sensorsRepos' : sensorsRepos,
	 'datasRepos' : datasRepos,
	}
	
	return render_template('monitor.html', **templateData)

@flask_app.route("/emitters")
def emitter():
	emitters = emittersRepos.get_all()
	types = Types.query.all()
	templateData = {
		'emitters':emitters,
		'types' : types,

	}
	return render_template('emitters.html', **templateData)

@flask_app.route("/sensors")
def sensor():
	emitters = emittersRepos.get_all()
	types = Types.query.all()
	templateData = {
		'emitters':emitters,
		'types' : types,

	}
	return render_template('sensors.html', **templateData)
	


@flask_app.route("/add_emitter", methods= ['POST'] )
def add_emitter():
	""" adding an emitter in the DB  """

	# storing the data from the html form.
	# reslust is a dict with the location and the address
	result=request.form
	emitter = Emitters(location=result['location'], address=int(result['address']))

	# try to add to db, as location has to be unique, ORM will raise an exception.
	# in case of error we print a danger alert on the page
	# in case of succes we print a succes alert on the page  
	try:
		db.session.add(emitter)
		db.session.commit()
	except:
		templateData={
			'error': 'error'
		}
		return render_template('emitters.html', **templateData)
	else:
		templateData={
			'error': 'ok'
		}
		return render_template('emitters.html', **templateData)



@flask_app.route("/add_sensor", methods= ['POST'])
def add_sensor():
	""" function to add a sensor to an emitter """

	# storing the data from the html form.
	# result is a dict with the emitter location and the type
	result = request.form
	# get the emitter entity with location = result['emitter']
	emitter = emittersRepos.get_by_location(result['emitter'])
	type = result['type']
	# instanciate a sensor object with the received datas
	sensor = Sensors(sensor_type = type, emitter_id=emitter.id)
	# adding it to the DB
	db.session.add(sensor)
	db.session.commit()
	
	return redirect("/sensors")

@flask_app.route("/delete", methods= ['POST'])
def delete():
	""" function to delete an emeter and all the sensors/datas related to it """

	# get the emiter id from the html select form
	result = request.form.get('select')
	# deleting the emitter and all the sensors and datas related to it
	emittersRepos.cascade_delete(result)
	
	return redirect("/")

@flask_app.route("/refresh")
def sendData():
	""" send the data to the client via asynchone javascript request to refresh permanently 
	the datas on the client screen """
	datas = emittersRepos.get_all_last_datas() 
	response = { "datas": datas,
				}

	return jsonify(response)
