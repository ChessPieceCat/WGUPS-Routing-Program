'''FUNCTION main()
	table = new HashTable()
	distanceTable = loadDistanceTable("DISTANCEFILE.csv")
	trucks = [Truck(truckID = 0), Truck(truckID = 1), Truck(truckID = 2)]
	drivers = [Driver(driverID = 0), Driver(driverID = 1)]
	loadPackages("PACKAGEFILE.csv", table)
	eventLog = simulateDelivery(trucks, drivers, table, distanceTable)

	WHILE TRUE
			PRINT "Enter time (HH:MM in 24-hour format) or EXIT"
			input = INPUT time

			IF input == "EXIT"
				BREAK
			END IF

			queryTime = parseTime(input)
			result = queryEventLog(queryTime, eventLog, table)

			PRINT result
	END WHILE
END FUNCTION

FUNCTION parseTime(timeString)
	hour, minute = split(timeString, ":")
	hour = convertToInt(hour)
	minute = convertToInt(minute)

	RETURN hour + (minute / 60)
END FUNCTION'''
from data.distance_table import loadDistanceTable
from data.hash_table import HashTable
from data.package_loader import loadPackages
from models.driver import Driver
from models.truck import Truck
from simulation.event_log import queryEventLog
from simulation.simulate import simulateDelivery


def main():
    table = HashTable()
    distanceTable = loadDistanceTable("distanceFile.csv")
    trucks = [Truck(0), Truck(1), Truck(2)]
    drivers = [Driver(0), Driver(1)]
    loadPackages("packageFile.csv", table)
    eventLog = simulateDelivery(trucks, drivers, table, distanceTable)

    while True:
        print("Enter time (HH:MM in 24-hour format) or EXIT")
        userInput = input()

        if input == "EXIT":
            break

        queryTime = parseTime(userInput)
        result = queryEventLog(queryTime, eventLog, table)

        print(result)

def parseTime(timeString):
    hour, minute = timeString.split(":")
    hour = int(hour)
    minute = int(minute)
    return hour + (minute / 60)

if __name__ == "__main__":
    main()