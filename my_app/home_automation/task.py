from home_automation import celery, db
from .models import Emitters, Sensors, Datas, Types, SensorsRepos, DatasRepos, EmittersRepos
from .sensor import Sensor
from .data import Data
from datetime import datetime

# instanciation of repos globaly
emittersRepos = EmittersRepos()
sensorsRepos = SensorsRepos()
datasRepos = DatasRepos()


@celery.task(name='send_request')
def send_request():
	""" Function to request data to each emitters an store datas in the data table """
	for emitter_entity in emittersRepos.get_all():
		# instanciate an emitter object from emitter table
		emitter = emitter_entity.toDomain() 
		# get all sensors entities related to emitter 
		sensors = sensorsRepos.get_by_emitter(emitter.id)
		# test if request is responding an store the received data in datas
		# datas are received as a list of n float regarding number of sensors 
		try:
			datas = emitter.request()
		except:
			
			print(f"emitter {emitter.location} failed to request data")
		else:
			
			print(f"emitter {emitter.location} succeeded to request data")
			for i, sensor_entity in enumerate(sensors):
				# instanciate an sensor object from sensor entity
				# we have to add sensors in the same order ass data are comming from the emitter
				# so if arduino send temp, humidity. We nedd to add first temp and then hum in the GUI
				sensor = sensor_entity.toDomain()
				# first data received is associated with the first sensor
				sensor.value = datas[i]
				# we instantiate a data object with the sensor id and time as str from years to seconds
				data = Data(sensor.id, sensor.value, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
				# we instanciate a data entity from the data object
				data_entity = data.toEntities()
				db.session.add(data_entity)
				db.session.commit()

	 	
	return('done !')