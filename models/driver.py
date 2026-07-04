#driver class
class Driver:
	def __init__(self, driverID):
		self.driverID = driverID
		self.assignedTruck = None
		self.availableTime = 8.0