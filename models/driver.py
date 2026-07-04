'''CLASS driver
	driverID
	assignedTruck = NULL
	availableTime = 8.0
END CLASS'''
class driver:
	def __init__(self, driverID):
		self.driverID = driverID
		self.assignedTruck = None
		self.availableTime = 8.0