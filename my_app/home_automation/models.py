from . import db
from .emitter import Emitter
from .sensor import Sensor


class Emitters(db.Model):
	id = db.Column('id', db.Integer, primary_key=True)
	location = db.Column('location', db.String(), unique=True, nullable=False)
	pipe = db.Column('pipe', db.Integer, default=1)
	address = db.Column('address', db.Integer)
	 
	def get_number_of_sensors(self):
		sensorsRepos = SensorsRepos()
		return len(sensorsRepos.get_by_emitter(self.id))
	def toDomain(self):
		return Emitter(self.address, self.location, self.id, self.get_number_of_sensors())


class Sensors(db.Model):
	id = db.Column('id', db.Integer, primary_key=True)
	sensor_type = db.Column('sensor_type', db.String())
	emitter_id = db.Column('emitter_id', db.Integer)
	

	def toDomain(self):
		return Sensor(self.id, self.emitter_id, self.sensor_type)


class Datas(db.Model):
	id = db.Column('id', db.Integer, primary_key=True)
	sensor_id = db.Column('sensor_id', db.Integer)
	time = db.Column('time', db.String())
	value = db.Column('value', db.Float)



class Types(db.Model):
	id = db.Column('id', db.Integer, primary_key=True)
	type = db.Column('type', db.String())





class SensorsRepos:

	def get_all(self):
		return Sensors.query.all()

	def get_by_emitter(self, id):
		return Sensors.query.filter_by(emitter_id=id).all()

	def delete_all(self):
		db.session.delete(self)
		db.session.commit()
		
	def delete_by_emitter(self, id):
		Sensors.query.filter_by(emitter_id=id).delete()
		db.session.commit()

	def cascade_delete(self, id):
		sensors_to_del = self.get_by_emitter(id)
		datasRepos = DatasRepos()
		for sensor in sensors_to_del:
			datasRepos.delete_by_sensor(sensor.id)
		self.delete_by_emitter(id)



class DatasRepos:

	def get_all(self):
		return Datas.query.all()

	def get_by_sensor(self, id):
		return Datas.query.filter_by(sensor_id=id).all()

	def get_last(self, id):
		return Datas.query.filter_by(sensor_id=id).order_by(Datas.id.desc()).first()

	def delete_all(self):
		Datas.query.all().delete()
		db.session.commit()

	def delete_by_sensor(self, id):
		Datas.query.filter_by(sensor_id=id).delete()
		db.session.commit()


class EmittersRepos:

	def get_all(self):
		return Emitters.query.all()

	def get_by_id(self, id):
		return Emitters.query.filter_by(id=id).first()

	def get_by_location(self, location):
		return Emitters.query.filter_by(location=location).first()

	def delete_all(self):
		Emitters.query.all().delete()
		db.session.commit()

	def delete_by_id(self, id):
		Emitters.query.filter_by(id=id).delete()
		db.session.commit()

	def cascade_delete(self, id):
		emitter_to_del = self.get_by_id(id)
		sensorsRepos = SensorsRepos()
		sensorsRepos.cascade_delete(emitter_to_del.id)
		self.delete_by_id(id)


	def get_all_last_datas(self):
		""" return a dict of all the data and the last time recorded of the last data of the first 
		sensor of an emitter. It has to be a dict to be jsonified and sended to the client where 
		javascript will manage it"""

		sensorsRepos = SensorsRepos()
		datasRepos = DatasRepos()
		dictio = {}
		for emitter in self.get_all():
			last_time = ""
			dictio[emitter.id] = {1:{},2:""}
			

			for sensor in sensorsRepos.get_by_emitter(emitter.id):
				data = datasRepos.get_last(sensor.id)
				dictio[emitter.id][1][sensor.id] = {}

				if data is None:
					dictio[emitter.id][1][sensor.id] = 'no data yet'
				else:	
					dictio[emitter.id][1][sensor.id] = {"value": datasRepos.get_last(sensor.id).value,
										 			"time" : datasRepos.get_last(sensor.id).time}
					
					last_time = datasRepos.get_last(sensor.id).time

			dictio[emitter.id][2] = last_time

		return dictio
