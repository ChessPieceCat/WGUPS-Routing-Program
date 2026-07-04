
from logistics.routing import buildRoute, getDistance
from logistics.truck_management import loadAllTrucks, loadTruck
from models.status import Status
from simulation.event_log import logEvent
#updates packages that are/were delayed according to the time they will arrive at the hub
def updateArrivals(table, currentTime, eventLog=None):
    for bucket in table.table:
        for package in bucket:
            if package["status"] == Status.DELAYED and package["availableTime"] <= currentTime:
                table.update(package["packageID"], Status.AT_HUB, None)
                if eventLog is not None:
                    logEvent(eventLog, package["packageID"], Status.AT_HUB, currentTime, None)
#maintains a record of undelivered packages
def undeliveredPackages(table):
    for bucket in table.table:
        for package in bucket:
            if package["status"] != Status.DELIVERED:
                return True
    return False
#selects the next trip by checking driver and truck availability. Differentiates between the drivers assigned truck and the third "spare" truck that either can use
def selectNextTrip(trucks, drivers, currentTime):
    for driver in drivers:
        if driver.availableTime <= currentTime:
            assignedTruck = driver.assignedTruck

            if (assignedTruck.packages
                    and not assignedTruck.isActive):
                return assignedTruck, driver

            spareTruck = trucks[2]
            if (spareTruck.packages
                    and not spareTruck.isActive):
                return spareTruck, driver
    return None
#marks truck as active (on route)
def markTruckActive(truck):
    truck.isActive = True
#marks truck as returned to the hub and sets its location
def markTruckReturn(truck):
    truck.currentLocation = "4001 South 700 East,  Salt Lake City, UT 84107"
    truck.isActive = False
# logs packages with an on route status along with their time and their truck ID. This updates the table with this information as well as the event log
def markPackagesOnRoute(truck, table, currentTime, eventLog):
    for package in truck.packages:
        table.update(package["packageID"], Status.ON_ROUTE, currentTime)
        logEvent(eventLog,
                package["packageID"],
                Status.ON_ROUTE,
                currentTime,
                truck.truckID)
#marks drivers as returned and sets their available time
def markDriverReturn(driver, time):
    driver.availableTime = time
#simulates delivery by calling the functions above. This continues so long as there are undelivered packages and repeatedly calls the trip builder as well as the truck loader.
def simulateDelivery(trucks, drivers, table, distanceTable):
    #initiates the day and event log. Pending returns represents trucks and drivers that are on the road along with their return time
    currentTime = 8.0
    eventLog = {}
    pendingReturns = []
    mileageLog = []
    #calls to update and log the delayed packages
    updateArrivals(table, currentTime, eventLog)
    #calls loadAllTrucks to load the three trucks at the start of the day
    queues = loadAllTrucks(trucks, drivers, table, distanceTable, eventLog)
    #continues while packages are undelivered while repeatedly calling the trip builder and updating arrivals. madeProgress exists to prevent infinite looping
    while undeliveredPackages(table):
        updateArrivals(table, currentTime, eventLog)
        madeProgress = False
        trip = selectNextTrip(trucks, drivers, currentTime)
        #sets madeProgress to true after trip is selected and marks the truck and packages as on route using earlier functions.
        while trip:
            madeProgress = True
            truck, driver = trip
            markTruckActive(truck)
            markPackagesOnRoute(truck, table, currentTime, eventLog)
            #calls runTrip to log the trip and get the end time for pending returns. Also moves currentTime forward to the trip end time
            tripEndTime, eventLog = runTrip(truck, driver, table, currentTime, eventLog, distanceTable, mileageLog)
            currentTime = tripEndTime
            pendingReturns.append({"returnTime": tripEndTime, "Truck": truck, "Driver": driver})
            #selects the next trip
            trip = selectNextTrip(trucks, drivers, currentTime)
        #sorts trucks in pending returns to ensure trucks are loaded and sent out in waiting order. This prevents later trucks from being sent out first
        if pendingReturns:
            #sorts by next return, stores the earliest truck, and removes it from pending returns
            pendingReturns.sort(key=lambda r: r["returnTime"])
            nextReturn = pendingReturns.pop(0)
            #moves time forward to the time of the next returning truck/driver
            currentTime = nextReturn["returnTime"]
            #calls update again to refresh delayed packages
            updateArrivals(table, currentTime, eventLog)
            #marks truck and driver as returned and empties the route and packages loaded before loading again and building a new route
            markTruckReturn(nextReturn["Truck"])
            markDriverReturn(nextReturn["Driver"], currentTime)
            nextReturn["Truck"].packages = []
            nextReturn["Truck"].route = []
            loadTruck(nextReturn["Truck"], queues, currentTime, table, eventLog)
            buildRoute(nextReturn["Truck"], distanceTable)
            madeProgress = True
        #if time passes without a truck and driver combo becoming available, time is advanced and delayed packages are refreshed once more
        if not madeProgress:
            currentTime += 1
            updateArrivals(table, currentTime, eventLog)
    #returns an event log of all updates within the simulation
    return eventLog, mileageLog
#runs the route for the called truck
def runTrip(truck, driver, table, currentTime, eventLog, distanceTable, mileageLog):
    #gets distance to calculate travel time and mileage and adds to current time and truck mileage accordingly
    for stop in truck.route:
        distance = getDistance(truck.currentLocation, stop, distanceTable)
        travelTime = distance / 18
        currentTime += travelTime
        truck.currentLocation = stop
        truck.mileage += distance
        #logs mileage according to the time
        mileageLog.append({"time": currentTime, "distance": distance, "truckID": truck.truckID})
        #updates each package to delivered at the current time in the hash table and event log when the associated address is reached
        for package in truck.packages:
            if package["address"] == stop:
                table.update(package["packageID"], Status.DELIVERED, currentTime)

                logEvent(eventLog,
                        package["packageID"],
                        Status.DELIVERED,
                        currentTime,
                        truck.truckID)
    return currentTime, eventLog

def getMileageAtTime(queryTime, mileageLog):
    return sum(entry["distance"] for entry in mileageLog if entry["time"] <= queryTime)