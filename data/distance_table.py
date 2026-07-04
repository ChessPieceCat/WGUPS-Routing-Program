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
				if i + 1 >= len(row):
					continue

				cell = row[i + 1].strip()
				if cell == "":
					continue
				otherLocation = locations[i]
				distanceValue = float(row[i + 1])
				distanceTable[locationName][otherLocation] = distanceValue
	return distanceTable