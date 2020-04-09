from .models import Datas

class Data:
	def __init__(self, sensor_id, value, time):
		self.sensor_id = sensor_id
		self.value = value
		self.time = time

	def toEntities(self):
		return Datas(sensor_id = self.sensor_id, value = self.value, time=self.time)