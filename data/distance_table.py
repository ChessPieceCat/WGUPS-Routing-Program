'''FUNCTION loadDistanceTable(fileName)
	CREATE distanceTable = {}
	OPEN fileName
	READ header
	locations = header[1:]

	FOR each row IN fileName
			locationName = row[0]
			distanceTable[locationName] = {}

			FOR i from 0 to length(locations) - 1
				otherLocation = locations[i]
				distance = row[i + 1]
				distanceTable[locationName][otherLocation] = distance
			END FOR
	END FOR
	CLOSE fileName
	RETURN distanceTable
END FUNCTION'''
import csv


def loadDistanceTable(fileName):
	distanceTable = {}
	with open(fileName, newline='') as csvfile:
		reader = csv.reader(csvfile)
		header = next(reader)
		locations = header[1:]

		for row in reader:
			locationName = row[0]
			distanceTable[locationName] = {}

			for i in range(0, len(locations)):
				otherLocation = locations[i]
				distance = float(row[i + 1])
				distanceTable[locationName][otherLocation] = distance
	return distanceTable