
from models.status import Status

#defines a class hashTable as an array of lists
class HashTable:
	def __init__(self, tableSize=101):
		self.tableSize = tableSize
		self.table = [[] for i in range(tableSize)]

	def hash(self, key):
		return key % self.tableSize
	#insert function with required fields as well as extra for the special notes section
	def insert(self, packageID, address, deadline, city, zipCode, weight, availableTime, assignedTruckID, groupPackages, addressCorrectionTime, correctAddress, addressHold):
		index = self.hash(packageID)
		initialStatus = Status.DELAYED if availableTime > 8.0 else Status.AT_HUB

		record = {
			"packageID": packageID,
			"address": address,
			"deadline": deadline,
			"city": city,
			"zip": zipCode,
			"weight": weight,
			"availableTime": availableTime,
			"assignedTruckID": assignedTruckID,
			"groupPackages": groupPackages,
			"addressCorrectionTime": addressCorrectionTime,
			"correctAddress": correctAddress,
			"addressHold": addressHold,
			"status": initialStatus,
			"deliveryTime": None
		}
		self.table[index].append(record)
	#search function that takes packageID as input
	def search(self, packageID):
		index = self.hash(packageID)

		for record in self.table[index]:
			if record["packageID"] == packageID:
				return record
		return None
	#update function to modify status and delivery time for each package
	def update(self, packageID, status, deliveryTime):
		record = self.search(packageID)

		if record is not None:
			record["status"] = status
			record["deliveryTime"] = deliveryTime