class Sensor:
	def __init__(self, id, emitter_id, data_type):
		self.id = id
		self.emitter_id = emitter_id
		self.data_type = data_type
		self.value = None