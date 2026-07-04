#truck class to separate individual trucks with their packages, routes, locations, and mileage. Also contains a boolean to track whether they are on route or not
class Truck:
	def __init__(self, truckID):
		self.truckID = truckID
		self.capacity = 16
		self.packages = []
		self.route = []
		self.currentLocation = "4001 South 700 East,  Salt Lake City, UT 84107"
		self.mileage = 0
		self.isActive = False