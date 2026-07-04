'''CREATE hash table as array of lists
SET tableSize = 101

FUNCTION hash(key)
	RETURN key MOD tableSize
END FUNCTION

FUNCTION insert(packageID, address, deadline, city, zip, weight, availableTime, assignedTruckID, 			  groupPackages, addressCorrectionTime, correctAddress, addressHold)
	index = hash(packageID)

	create record = {
		packageID: packageID,
		address: address,
		deadline: deadline,
		city: city,
		zip: zip,
		weight: weight,
		availableTime: availableTime,
		assignedTruckID: assignedTruckID,
		groupPackages: groupPackages,
		addressCorrectionTime: addressCorrectionTime,
		correctAddress: correctAddress,
	 addressHold: addressHold,
		status: STATUS.AT_HUB,
		deliveryTime: NULL
	}

	APPEND record TO table[index]
END FUNCTION

FUNCTION search(packageID)
	index = hash(packageID)

	FOR each record IN table[index]
		IF record.packageID == packageID
			RETURN record
		END IF
	END FOR
	RETURN null
END FUNCTION

FUNCTION update(packageID, status, deliveryTime)
	record = search(packageID)

	IF record is not null
		record.status = status
		record.deliveryTime = deliveryTime
	END IF
END FUNCTION'''
from models.status import Status


class HashTable:
	def __init__(self, tableSize=101):
		self.tableSize = tableSize
		self.table = [[] for i in range(tableSize)]

	def hash(self, key):
		return key % self.tableSize

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

	def search(self, packageID):
		index = self.hash(packageID)

		for record in self.table[index]:
			if record["packageID"] == packageID:
				return record
		return None

	def update(self, packageID, status, deliveryTime):
		record = self.search(packageID)

		if record is not None:
			record["status"] = status
			record["deliveryTime"] = deliveryTime