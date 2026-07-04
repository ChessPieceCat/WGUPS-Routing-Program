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

FUNCTION loadTruck(Truck, queues, currentTime, table)

	currentLoad = 0
	assignedGroups = set()

	FOR each package IN queues.truckLocked
			IF package.assignedTruckID == Truck.truckID
			AND currentLoad < Truck.capacity
			AND isEligible(package, currentTime)
				ADD package TO Truck.packages
				table.update(package.packageID, STATUS.LOADED, NULL)
				currentLoad++
			END IF
	END FOR

	FOR each package IN queues.grouped

			IF package.groupPackages NOT IN assignedGroups
			AND isEligible(package, currentTime)
				groupList = all packages sharing package.groupPackages
				groupSize = SIZE(groupList)
				IF currentLoad + groupSize <= Truck.capacity
					FOR each p IN groupList
						ADD p TO Truck.packages
						table.update(p.packageID, STATUS.LOADED, NULL)
					END FOR
					 ADD groupList[0].groupPackages TO assignedGroups
					currentLoad += groupSize
				END IF
		END IF
	END FOR

	FOR each package in queues.remaining
			IF currentLoad < Truck.capacity
			AND isEligible(package, currentTime)
			ADD package TO Truck.packages
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

	FOR each Truck IN trucks
		loadTruck(
			Truck,
			queues,
			currentTime,
			table
		)

		buildRoute(Truck, distanceTable)
	END FOR
	RETURN queues
END FUNCTION'''
from logistics.routing import buildRoute
from models.status import Status
from collections import namedtuple

from simulation.event_log import logEvent

Queues = namedtuple('Queues', ['truckLocked', 'grouped', 'remaining'])

def priorityQueues(table):
	truckLocked = []
	grouped = []
	remaining = []

	for bucket in table.table:
		for package in bucket:
			if package["assignedTruckID"] is not None:
				truckLocked.append(package)
			elif package["groupPackages"] is not None:
				grouped.append(package)
			else:
				remaining.append(package)

	remaining.sort(key=lambda package: package["deadline"])
	return Queues(truckLocked, grouped, remaining)

def isEligible(package, currentTime):
	if (package["status"] == Status.AT_HUB
			and package["availableTime"] <= currentTime
			and (package["addressHold"] == False or currentTime >= package["addressCorrectionTime"])):
		return True
	else:
		return False

def findGroupMembers(groupID, table):
	members = []
	for bucket in table.table:
		for package in bucket:
			if package["groupPackages"] == groupID:
				members.append(package)
	return members

def loadTruck(truck, queues, currentTime, table, eventLog):
	currentLoad = 0
	assignedGroups = set()

	for package in queues.truckLocked:
		if package["assignedTruckID"] == truck.truckID and currentLoad < truck.capacity and isEligible(package, currentTime):
			truck.packages.append(package)
			table.update(package["packageID"], Status.LOADED, None)
			logEvent(eventLog, package["packageID"], Status.LOADED, currentTime, truck.truckID)
			currentLoad += 1

	for package in queues.grouped:
		if package["groupPackages"] not in assignedGroups and isEligible(package, currentTime):
			groupList = findGroupMembers(package["groupPackages"], table)
			groupSize = len(groupList)
			if currentLoad + groupSize <= truck.capacity:
				for p in groupList:
					truck.packages.append(p)
					table.update(p["packageID"], Status.LOADED, None)
				assignedGroups.add(package["groupPackages"])
				currentLoad += groupSize

	for package in queues.remaining:
		if currentLoad < truck.capacity and isEligible(package, currentTime):
			truck.packages.append(package)
			table.update(package["packageID"], Status.LOADED, None)
			currentLoad += 1

def loadAllTrucks(trucks, drivers, table, distanceTable, eventLog):
	queues = priorityQueues(table)
	currentTime = 8.0
	drivers[0].assignedTruck = trucks[0]
	drivers[1].assignedTruck = trucks[1]

	for truck in trucks:
		loadTruck(truck, queues, currentTime, table, eventLog)
		buildRoute(truck, distanceTable)
	return queues

def getTotalMileage(trucks):
	return sum(truck.mileage for truck in trucks)