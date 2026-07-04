
import csv
import re
#loads packages from package file into hash table
def loadPackages(fileName, table):
	with open(fileName, newline='') as openFile:
		reader = csv.reader(openFile)
		next(reader)

		for row in reader:
			if len(row) < 6:
				continue
			packageID = int(row[0])
			address = row[1]
			deadline = row[2]
			city = row[3]
			zipCode = row[4]
			weight = int(row[5])
			specialNotes = row[6] if len(row) > 6 else None

			availableTime, assignedTruckID, groupPackages, addressCorrectionTime, correctAddress, addressHold = parseNotes(packageID, specialNotes)
			table.insert(packageID, address, deadline, city, zipCode, weight, availableTime, assignedTruckID, groupPackages, addressCorrectionTime, correctAddress, addressHold)
#parses the special notes section
def parseNotes(packageID, specialNotes):
	availableTime = 8.0
	assignedTruckID = None
	groupPackages = None
	addressCorrectionTime = 8.0
	correctAddress = None
	addressHold = False

	if specialNotes is None:
		return availableTime, assignedTruckID, groupPackages, addressCorrectionTime, correctAddress, addressHold
	#searches for "Delayed" and parses out the available time
	m = re.search(r"(\d{1,2}):(\d{2})(?:\s*([ap]m))?", specialNotes, re.IGNORECASE)
	if "Delayed" in specialNotes:
		if m:
			hour = int(m.group(1))
			minute = int(m.group(2))
			ampm = m.group(3)
			if ampm:
				ampm = ampm.lower()
				if ampm == "pm" and hour != 12:
					hour += 12
				if ampm == 'am' and hour == 12:
					hour = 0
			availableTime = hour + (minute / 60.0)
	#searches for packages that are assigned to specific trucks and parses the IDs
	if "Can only be on truck" in specialNotes:
		m2 = re.search(r"Can only be on truck\s*(\d+)", specialNotes)
		if m2:
			assignedTruckID = int(m2.group(1)) - 1
	#searches packages that must be grouped together
	if "Must be delivered with" in specialNotes:
		ids = re.findall(r"\d+", specialNotes)
		if ids:
			allIDs = [packageID] + [int(i) for i in ids]
			#sets the group ID to the lowest package ID in the group for simplicity
			groupPackages = min(allIDs)
	#searches for packages with the wrong address
	if "Wrong address" in specialNotes:
		addressHold = True
		#for scale, this section would need to be addressed as it currently only works if package addresses are updated at this specific time with the specific address listed
		addressCorrectionTime = 10.33
		correctAddress = "410 S.State St."

	return availableTime, assignedTruckID, groupPackages, addressCorrectionTime, correctAddress, addressHold