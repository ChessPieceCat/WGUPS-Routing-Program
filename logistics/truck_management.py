'''FUNCTION priorityQueues(table)
	truckLocked = []
	grouped = []
	remaining = []

	FOR each bucket IN table
			FOR each package IN bucket

				IF package.assignedTruckID != NULL
					ADD package TO truckLocked

				ELSE IF package.groupPackages != NULL
					ADD package TO grouped

				ELSE
					ADD package TO remaining
				END IF
			END FOR
	END FOR

	SORT remaining BY deadline

	RETURN truckLocked, grouped, remaining

END FUNCTION

FUNCTION isEligible(package, currentTime)
		IF package.status == STATUS.AT_HUB
		AND package.availableTime <= currentTime
		AND (package.addressHold == FALSE OR currentTime >= 						           package.addressCorrectionTime)
			RETURN TRUE
		ELSE
			RETURN FALSE
		END IF
END FUNCTION

FUNCTION loadTruck(truck, queues, currentTime, table)

	currentLoad = 0
	assignedGroups = set()

	FOR each package IN queues.truckLocked
			IF package.assignedTruckID == truck.truckID
			AND currentLoad < truck.capacity
			AND isEligible(package, currentTime)
				ADD package TO truck.packages
				table.update(package.packageID, STATUS.LOADED, NULL)
				currentLoad++
			END IF
	END FOR

	FOR each package IN queues.grouped

			IF package.groupPackages NOT IN assignedGroups
			AND isEligible(package, currentTime)
				groupList = all packages sharing package.groupPackages
				groupSize = SIZE(groupList)
				IF currentLoad + groupSize <= truck.capacity
					FOR each p IN groupList
						ADD p TO truck.packages
						table.update(p.packageID, STATUS.LOADED, NULL)
					END FOR
					 ADD groupList[0].groupPackages TO assignedGroups
					currentLoad += groupSize
				END IF
		END IF
	END FOR

	FOR each package in queues.remaining
			IF currentLoad < truck.capacity
			AND isEligible(package, currentTime)
			ADD package TO truck.packages
				table.update(package.packageID, STATUS.LOADED, NULL)
				currentLoad++
			END IF
	END FOR

     END FUNCTION

     FUNCTION loadAllTrucks(trucks, drivers, table, distanceTable)
	queues = priorityQueues(table)
	currentTime = 8.0
	drivers[0].assignedTruck = trucks[0] //maybe move these two to main controller later
	drivers[1].assignedTruck = trucks[1]

	FOR each truck IN trucks
		loadTruck(
			truck,
			queues,
			currentTime,
			table
		)

		buildRoute(truck, distanceTable)
	END FOR
	RETURN queues
END FUNCTION'''
from ctypes.wintypes import SIZE
from data.hash_table import HashTable
from models.status import Status


def priorityQueues(table):
	truckLocked = []
	grouped = []
	remaining = []

	for truck in table:
		for package in truck:
			if package.assignedTruck is not None:
				truckLocked.append(package)
			elif package.groupPackages is not None:
				grouped.append(package)
			else:
				remaining.append(package)

	remaining.sort(key=lambda package: package["deadline"])
	return truckLocked, grouped, remaining

def isEligible(package, currentTime):
	if package.status == Status.AT_HUB & package.availableTime <= currentTime & (package.addressHold == False or currentTime >= package.addressCorrectionTime):
		return True
	else:
		return False

def loadTruck(truck, queues, currentTime, table):
	currentLoad = 0
	assignedGroups = set()

	for package in queues.truckLocked:
		if package.assignedTruckID == truck.truckID & currentLoad < truck.capacity & isEligible(package, currentTime):
			truck.packages.append(package)
			table.update(package.packageID, Status.LOADED, None)
			currentLoad += 1

	for package in queues.grouped:
		if package.groupPackages is not in assignedGroups & isEligible(package, currentTime):
			groupList = package.groupPackages
			groupSize = SIZE(groupList)
			if currentLoad + groupSize <= truck.capacity:
				for p in groupList:
					truck.packages.append(p)
					table.update(p.packageID, Status.LOADED, None)
					currentLoad += groupSize

	for package in queues.remaining:
		if currentLoad < truck.capacity & isEligible(package, currentTime):
			truck.packages.append(package)
			table.update(package.packageID, Status.LOADED, None)
			currentLoad += 1

def loadAllTrucks(trucks, drivers, table, distanceTable):
	queues = priorityQueues(table)
	currentTime = 8.0
	drivers[0].assignedTruck = trucks[0]
	drivers[1].assignedTruck = trucks[1]

	for truck in trucks:
		loadTruck(truck, queues, currentTime, distanceTable)
		buildRoute(truck, distanceTable)
	return queues