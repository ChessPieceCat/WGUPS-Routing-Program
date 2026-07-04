
from logistics.routing import buildRoute
from models.status import Status
from collections import namedtuple

from simulation.event_log import logEvent
#initializes queues as a namedtuple for storing special notes
Queues = namedtuple('Queues', ['truckLocked', 'grouped', 'remaining'])
#sorts packages to be loaded onto trucks. Those with assigned trucks are loaded first followed by grouped packages. Remaining packages are appended after the others are exhausted
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
	#sorts remaining packages by deadline to avoid late deliveries
	remaining.sort(key=lambda package: package["deadline"])
	return Queues(truckLocked, grouped, remaining)
#checks if packages are eligible according to their delay status and current time
def isEligible(package, currentTime):
	if (package["status"] == Status.AT_HUB
			and package["availableTime"] <= currentTime
			and (package["addressHold"] == False or currentTime >= package["addressCorrectionTime"])):
		return True
	else:
		return False
#finds members of a group of packages according to their group ID
def findGroupMembers(groupID, table):
	members = []
	for bucket in table.table:
		for package in bucket:
			if package["groupPackages"] == groupID:
				members.append(package)
	return members
#loads individual trucks using sorted package data. Each section contains checks to ensure packages are eligible for loading and won't exceed the capacity
def loadTruck(truck, queues, currentTime, table, eventLog):
	currentLoad = 0
	assignedGroups = set()
	#first loads packages that are assigned to the called truck, updates the table and event log, and increments the current load
	for package in queues.truckLocked:
		if package["assignedTruckID"] == truck.truckID and currentLoad < truck.capacity and isEligible(package, currentTime):
			truck.packages.append(package)
			table.update(package["packageID"], Status.LOADED, None)
			logEvent(eventLog, package["packageID"], Status.LOADED, currentTime, truck.truckID)
			currentLoad += 1
	#next, loads packages that are grouped together so long as this will not exceed the capacity. Updates each package in the group in the table and event log before adding the load
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
	#finally, loads and updates remaining packages and increments the load for each
	for package in queues.remaining:
		if currentLoad < truck.capacity and isEligible(package, currentTime):
			truck.packages.append(package)
			table.update(package["packageID"], Status.LOADED, None)
			currentLoad += 1
#initial loading of all three trucks and assigning of drivers. This first calls priorityQueues to sort the packages
def loadAllTrucks(trucks, drivers, table, distanceTable, eventLog):
	queues = priorityQueues(table)
	currentTime = 8.0
	drivers[0].assignedTruck = trucks[0]
	drivers[1].assignedTruck = trucks[1]

	for truck in trucks:
		loadTruck(truck, queues, currentTime, table, eventLog)
		buildRoute(truck, distanceTable)
	return queues