'''CLASS truck
	truckID
	capacity = 16
	packages = []
	route = []
	currentLocation = "HUB"
	mileage = 0
END CLASS'''
class truck:
	def __init__(self, truckID):
		self.truckID = truckID
		self.capacity = 16
		self.packages = []
		self.route = []
		self.currentLocation = "HUB"
		self.mileage = 0