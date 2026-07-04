'''CLASS Truck
	truckID
	capacity = 16
	packages = []
	route = []
	currentLocation = "HUB"
	mileage = 0
END CLASS'''
class Truck:
	def __init__(self, truckID):
		self.truckID = truckID
		self.capacity = 16
		self.packages = []
		self.route = []
		self.currentLocation = "4001 South 700 East,  Salt Lake City, UT 84107"
		self.mileage = 0
		self.isActive = False