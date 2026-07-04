'''FUNCTION simulateDelivery(trucks, drivers, table, distanceTable)
    SET currentTime = 8.0
    SET eventLog = {}
    SET pendingReturns = []

    queues = loadAllTrucks(trucks, drivers, table, distanceTable)

    WHILE undeliveredPackages(table)
        trip = selectNextTrip(trucks, drivers, currentTime)

        WHILE trip != NULL
            driver = trip.driver
            truck = trip.truck
            markTruckActive(truck)
            markDriverActive(driver)
            markPackagesOnRoute(truck, table, currentTime, eventLog)

            tripEndTime, eventLog = runTrip(truck, driver, table, currentTime, eventLog, distanceTable)
            ADD(returnTime: tripEndTime, truck: truck, driver: driver) TO pendingReturns

            trip = selectNextTrip(trucks, drivers, currentTime)
        END WHILE
        IF pendingReturns.isEmpty == FALSE
            SORT pendingReturns BY returnTime // ascending
            nextReturn = pendingReturns[0]
            REMOVE nextReturn FROM pendingReturns

            currentTime = nextReturn.returnTime

            markTruckReturn(nextReturn.truck)
            markDriverReturn(nextReturn.driver, currentTime)
            nextReturn.truck.packages = []
            nextReturn.truck.route = []
            loadTruck(nextReturn.truck, queues, currentTime, table)
            buildRoute(nextReturn.truck, distanceTable)
        ELSE
            currentTime += 0.1
        END IF
    END WHILE
    RETURN eventLog
END FUNCTION

FUNCTION runTrip(truck, driver, table, currentTime, eventLog, distanceTable)
    FOR each stop IN truck.route
        distance = getDistance(truck.currentLocation, stop, distanceTable)
        travelTime = distance / 18 mph
        currentTime += travelTime
        truck.currentLocation = stop
        truck.mileage += distance

        FOR each package IN truck.packages
            IF package.address == stop
                table.update(package.packageID, STATUS.DELIVERED, currentTime)

                logEvent(eventLog,
                        package.packageID,
                        STATUS.DELIVERED,
                        currentTime,
                        truck.truckID)
            END IF
        END FOR
    END FOR
    RETURN currentTime, eventLog
END FUNCTION

FUNCTION selectNextTrip(trucks, drivers, currentTime)
    FOR each driver IN drivers
        IF driver.availableTime <= currentTime
            assignedTruck = driver.assignedTruck

            IF assignedTruck.currentLocation == "HUB"
            AND assignedTruck.packages.isEmpty == FALSE
                RETURN(assignedTruck, driver)
            END IF

            spareTruck = trucks[2] // trucks[2] is always the spare
            IF spareTruck.currentLocation == "HUB"
            AND spareTruck.packages.isEmpty == FALSE
                RETURN(spareTruck, driver)
            END IF
        END IF
    END FOR
    RETURN NULL
END FUNCTION

FUNCTION undeliveredPackages(table)
    FOR each bucket IN table
        FOR each package IN bucket
            IF package.status != STATUS.DELIVERED
                RETURN TRUE
            END IF
        END FOR
    END FOR
    RETURN FALSE
END FUNCTION

FUNCTION markTruckReturn(truck)
    truck.currentLocation = "HUB"
END FUNCTION

FUNCTION markPackagesOnRoute(truck, table, currentTime, eventLog)
    FOR each package in truck.packages
        table.update(package.packageID, STATUS.ON_ROUTE, currentTime)
        logEvent(eventLog,
                package.packageID,
                STATUS.ON_ROUTE,
                currentTime,
                truck.truckID)
    END FOR
END FUNCTION

FUNCTION markDriverActive(driver)
    driver.availableTime = infinity
END FUNCTION

FUNCTION markDriverReturn(driver, time)
    driver.availableTime = time
END FUNCTION'''
from logistics.routing import buildRoute, getDistance
from logistics.truck_management import loadAllTrucks, loadTruck
from models.status import Status
from simulation.event_log import logEvent


def undeliveredPackages(table):
    for truck in table:
        for package in table[truck]:
            if package.status != Status.DELIVERED:
                return True
    return False

def selectNextTrip(trucks, drivers, currentTime):
    for driver in drivers:
        if driver.availableTime <= currentTime:
            assignedTruck = driver.assignedTruck

            if assignedTruck.currentLocation == "HUB" and assignedTruck.packages.isEmpty == False:
                return assignedTruck, driver

            spareTruck = trucks[2]
            if spareTruck.currentLocation == "HUB" and spareTruck.packages.isEmpty == False:
                return spareTruck, driver
    return None

def markTruckActive(truck):
    truck.currentLocation = "ON ROUTE"

def markTruckReturn(truck):
    truck.currentLocation = "HUB"

def markPackagesOnRoute(truck, table, currentTime, eventLog):
    for package in truck.packages:
        table.update(package.packageID, Status.ON_ROUTE, currentTime)
        logEvent(eventLog,
                package.packageID,
                Status.ON_ROUTE,
                currentTime,
                truck.truckID)

def markDriverActive(driver):
    driver.availableTime = float('inf')

def markDriverReturn(driver, time):
    driver.availableTime = time

def simulateDelivery(trucks, drivers, table, distanceTable):
    currentTime = 8.0
    eventLog = []
    pendingReturns = []

    queues = loadAllTrucks(trucks, drivers, table, distanceTable)

    while undeliveredPackages(table):
        trip = selectNextTrip(trucks, drivers, currentTime)

        while trip is not None:
            driver = drivers[trip]
            truck = trucks[trip]
            markTruckActive(truck)
            markDriverActive(driver)
            markPackagesOnRoute(truck, table, currentTime, eventLog)

            tripEndTime, eventLog = runTrip(truck, driver, table, currentTime, eventLog, distanceTable)
            pendingReturns.append({"returnTime": tripEndTime, "truck": truck, "driver": driver})

            trip = selectNextTrip(trucks, drivers, currentTime)

        if pendingReturns is not None:
            pendingReturns.sort(reverse=True)
            nextReturn = pendingReturns[0]
            pendingReturns.pop(nextReturn)

            currentTime = nextReturn.returnTime

            markTruckReturn(nextReturn.truck)
            markDriverReturn(nextReturn.driver, currentTime)
            nextReturn.truck.packages = []
            nextReturn.truck.route = []
            loadTruck(nextReturn.truck, queues, currentTime, table)
            buildRoute(nextReturn.truck, distanceTable)
        else:
            currentTime += 0.1

    return eventLog

def runTrip(truck, driver, table, currentTime, eventLog, distanceTable):
    for stop in truck.route:
        distance = getDistance(truck.currentLocation, stop, distanceTable)
        travelTime = distance / 18
        currentTime += travelTime
        truck.currentLocation = stop
        truck.mileage += distance

        for package in truck.packages:
            if package.address == stop:
                table.update(package.packageID, Status.ON_ROUTE, currentTime)

                logEvent(eventLog,
                        package.packageID,
                        Status.DELIVERED,
                        currentTime,
                        truck.truckID)
    return currentTime, eventLog
