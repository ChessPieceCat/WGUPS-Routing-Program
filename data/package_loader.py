'''FUNCTION loadPackages(fileName, table)
	OPEN package file

	FOR each row IN package file

		READ packageID
		READ address
		READ deadline
		READ city
		READ zip
		READ weight
		READ specialNotes

		availableTime, assignedTruckID, groupPackages, addressCorrectionTime, correctAddress, addressHold = parseNotes(specialNotes)

		CALL table.insert(packageID, address, deadline, city, zip, weight, availableTime, assignedTruckID, groupPackages, addressCorrectionTime, correctAddress, addressHold)

	END FOR
	CLOSE package file

END FUNCTION

FUNCTION
	parseNotes(specialNotes)

	SET availableTime = 8.0
	SET assignedTruckID = NULL
	SET groupPackages = NULL
	SET addressCorrectionTime = 8.0
	SET correctAddress = NULL
	SET addressHold = FALSE

	IF specialNotes contains “Delayed”
		availableTime = extract time from string

	END IF

	IF specialNotes contains “Can only be on truck”
	assignedTruckID = extract number from string

	END IF

	IF specialNotes contains “Must be delivered with”
		groupPackages = appropriate grouping
	END IF

	IF specialNotes contains “Wrong address”
		addressHold = TRUE
		addressCorrectionTime = 10.33
		correctAddress = "410 S.State St."

	END IF

	RETURN availableTime, assignedTruckID, groupPackages, addressCorrectionTime, correctAddress, addressHold

END FUNCTION'''
import re

def loadPackages(fileName, table):
	openFile = open(fileName)

	for line in openFile:
		packageID = line[0]
		address = line[1]
		deadline = line[2]
		city = line[3]
		zipCode = line[4]
		weight = line[5]
		specialNotes = line[6]

		availableTime, assignedTruckID, groupPackages, addressCorrectionTime, correctAddress, addressHold = parseNotes(specialNotes)
		table.insert(packageID, address, deadline, city, zipCode, weight, availableTime, assignedTruckID, groupPackages, addressCorrectionTime, correctAddress, addressHold)

def parseNotes(specialNotes):
	availableTime = 8.0
	assignedTruckID = None
	groupPackages = None
	addressCorrectionTime = 8.0
	correctAddress = None
	addressHold = False

	if specialNotes is None:
		return availableTime, assignedTruckID, groupPackages, addressCorrectionTime, correctAddress, addressHold

	m = re.search(r"(\d{1,2}):(\d{2})(?:\s*([ap]m))?", specialNotes, re.IGNORECASE)
	if "Delayed" in specialNotes:
		if m:
			hour = int(m.group(1))
			minute = int(m.group(2))
			ampm = m.group(3)
			ampm = ampm.lower()
			if ampm == "pm" and hour != 12:
				hour += 12
			if ampm == 'am' and hour == 12:
				hour = 0
			availableTime = hour + (minute / 60.0)

	if "Can only be on truck" in specialNotes:
		m2 = re.search(r"Can only be on truck\s*(\d+)", specialNotes)
		if m2:
			assignedTruckID = int(m2.group(1))

	if "Must be delivered with" in specialNotes:
		ids = re.findall(r"\d+", specialNotes)
		if ids:
			groupPackages = [int(i) for i in ids]

	if "Wrong address" in specialNotes:
		addressHold = True
		addressCorrectionTime = 10.33
		correctAddress = "410 S.State St."

	return availableTime, assignedTruckID, groupPackages, addressCorrectionTime, correctAddress, addressHold