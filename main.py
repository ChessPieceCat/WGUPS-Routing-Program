'''FUNCTION main()
	table = new HashTable()
	distanceTable = loadDistanceTable("DISTANCEFILE.csv")
	trucks = [truck(truckID = 0), truck(truckID = 1), truck(truckID = 2)]
	drivers = [driver(driverID = 0), driver(driverID = 1)]
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
from models.driver import driver
from models.truck import truck


def main():
    table = new HashTable()
    distanceTable = loadDistanceTable("distanceFile.csv")
    trucks = [truck(0), truck(1), truck(2)]
    drivers = [driver(0), driver(1)]
    loadPackages("packageFile.csv", table)
    eventLog = simulateDelivery(trucks, drivers, table, distanceTable)
