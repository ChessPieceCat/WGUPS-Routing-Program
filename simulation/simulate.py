'''FUNCTION simulateDelivery(trucks, drivers, table, distanceTable)
    SET currentTime = 8.0
    SET eventLog = {}
    SET pendingReturns = []

    queues = loadAllTrucks(trucks, drivers, table, distanceTable)

    WHILE undeliveredPackages(table)
        trip = selectNextTrip(trucks, drivers, currentTime)

        WHILE trip != NULL
            Driver = trip.Driver
            Truck = trip.Truck
            markTruckActive(Truck)
            markDriverActive(Driver)
            markPackagesOnRoute(Truck, table, currentTime, eventLog)

            tripEndTime, eventLog = runTrip(Truck, Driver, table, currentTime, eventLog, distanceTable)
            ADD(returnTime: tripEndTime, Truck: Truck, Driver: Driver) TO pendingReturns

            trip = selectNextTrip(trucks, drivers, currentTime)
        END WHILE
        IF pendingReturns.isEmpty == FALSE
            SORT pendingReturns BY returnTime // ascending
            nextReturn = pendingReturns[0]
            REMOVE nextReturn FROM pendingReturns

            currentTime = nextReturn.returnTime

            markTruckReturn(nextReturn.Truck)
            markDriverReturn(nextReturn.Driver, currentTime)
            nextReturn.Truck.packages = []
            nextReturn.Truck.route = []
            loadTruck(nextReturn.Truck, queues, currentTime, table)
            buildRoute(nextReturn.Truck, distanceTable)
        ELSE
            currentTime += 0.1
        END IF
    END WHILE
    RETURN eventLog
END FUNCTION

FUNCTION runTrip(Truck, Driver, table, currentTime, eventLog, distanceTable)
    FOR each stop IN Truck.route
        distance = getDistance(Truck.currentLocation, stop, distanceTable)
        travelTime = distance / 18 mph
        currentTime += travelTime
        Truck.currentLocation = stop
        Truck.mileage += distance

        FOR each package IN Truck.packages
            IF package.address == stop
                table.update(package.packageID, STATUS.DELIVERED, currentTime)

                logEvent(eventLog,
                        package.packageID,
                        STATUS.DELIVERED,
                        currentTime,
                        Truck.truckID)
            END IF
        END FOR
    END FOR
    RETURN currentTime, eventLog
END FUNCTION

FUNCTION selectNextTrip(trucks, drivers, currentTime)
    FOR each Driver IN drivers
        IF Driver.availableTime <= currentTime
            assignedTruck = Driver.assignedTruck

            IF assignedTruck.currentLocation == "HUB"
            AND assignedTruck.packages.isEmpty == FALSE
                RETURN(assignedTruck, Driver)
            END IF

            spareTruck = trucks[2] // trucks[2] is always the spare
            IF spareTruck.currentLocation == "HUB"
            AND spareTruck.packages.isEmpty == FALSE
                RETURN(spareTruck, Driver)
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

FUNCTION markTruckReturn(Truck)
    Truck.currentLocation = "HUB"
END FUNCTION

FUNCTION markPackagesOnRoute(Truck, table, currentTime, eventLog)
    FOR each package in Truck.packages
        table.update(package.packageID, STATUS.ON_ROUTE, currentTime)
        logEvent(eventLog,
                package.packageID,
                STATUS.ON_ROUTE,
                currentTime,
                Truck.truckID)
    END FOR
END FUNCTION

FUNCTION markDriverActive(Driver)
    Driver.availableTime = infinity
END FUNCTION

FUNCTION markDriverReturn(Driver, time)
    Driver.availableTime = time
END FUNCTION'''
from logistics.routing import buildRoute, getDistance
from logistics.truck_management import loadAllTrucks, loadTruck
from models.status import Status
from simulation.event_log import logEvent

def updateArrivals(table, currentTime, eventLog=None):
    for bucket in table.table:
        for package in bucket:
            if package["status"] == Status.DELAYED and package["availableTime"] <= currentTime:
                table.update(package["packageID"], Status.AT_HUB, None)
                if eventLog is not None:
                    logEvent(eventLog, package["packageID"], Status.AT_HUB, currentTime, None)

def undeliveredPackages(table):
    for bucket in table.table:
        for package in bucket:
            if package["status"] != Status.DELIVERED:
                return True
    return False

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

def markTruckActive(truck):
    truck.isActive = True

def markTruckReturn(truck):
    truck.currentLocation = "HUB"
    truck.isActive = False

def markPackagesOnRoute(truck, table, currentTime, eventLog):
    for package in truck.packages:
        table.update(package["packageID"], Status.ON_ROUTE, currentTime)
        logEvent(eventLog,
                package["packageID"],
                Status.ON_ROUTE,
                currentTime,
                truck.truckID)

def markDriverReturn(driver, time):
    driver.availableTime = time

def simulateDelivery(trucks, drivers, table, distanceTable):
    currentTime = 8.0
    eventLog = {}
    pendingReturns = []

    updateArrivals(table, currentTime, eventLog)
    queues = loadAllTrucks(trucks, drivers, table, distanceTable, eventLog)

    while undeliveredPackages(table):
        updateArrivals(table, currentTime, eventLog)
        madeProgress = False
        trip = selectNextTrip(trucks, drivers, currentTime)

        while trip:
            madeProgress = True
            truck, driver = trip
            markTruckActive(truck)
            markPackagesOnRoute(truck, table, currentTime, eventLog)

            tripEndTime, eventLog = runTrip(truck, driver, table, currentTime, eventLog, distanceTable)
            currentTime = tripEndTime
            pendingReturns.append({"returnTime": tripEndTime, "Truck": truck, "Driver": driver})

            trip = selectNextTrip(trucks, drivers, currentTime)

        if pendingReturns:
            pendingReturns.sort(key=lambda r: r["returnTime"])
            nextReturn = pendingReturns.pop(0)

            currentTime = nextReturn["returnTime"]
            updateArrivals(table, currentTime, eventLog)

            markTruckReturn(nextReturn["Truck"])
            markDriverReturn(nextReturn["Driver"], currentTime)
            nextReturn["Truck"].packages = []
            nextReturn["Truck"].route = []
            loadTruck(nextReturn["Truck"], queues, currentTime, table, eventLog)
            buildRoute(nextReturn["Truck"], distanceTable)
            madeProgress = True

        if not madeProgress:
            currentTime += 1
            updateArrivals(table, currentTime, eventLog)

    return eventLog

def runTrip(truck, driver, table, currentTime, eventLog, distanceTable):
    for stop in truck.route:
        distance = getDistance(truck.currentLocation, stop, distanceTable)
        travelTime = distance / 18
        currentTime += travelTime
        truck.currentLocation = stop
        truck.mileage += distance

        for package in truck.packages:
            if package["address"] == stop:
                table.update(package["packageID"], Status.DELIVERED, currentTime)

                logEvent(eventLog,
                        package["packageID"],
                        Status.DELIVERED,
                        currentTime,
                        truck.truckID)
    return currentTime, eventLog
