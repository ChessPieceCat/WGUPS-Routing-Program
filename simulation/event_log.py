#logs packages with their status, time, and truck as called
def logEvent(eventLog, packageID, status, time, truckID):
    if packageID not in eventLog:
        eventLog[packageID] = []

    eventLog[packageID].append({"status": status, "time": time, "truckID": truckID})
#query interface that takes input from the main controller and outputs event log info
def queryEventLog(queryTime, eventLog, table):
    output = []

    for bucket in table.table:
        for package in bucket:
            latest = None

            if package["packageID"] in eventLog:
                for event in eventLog[package["packageID"]]:
                    if event["time"] <= queryTime:
                        if latest is None or event["time"] > latest["time"]:
                            latest = event
            if latest is None:
                status = package["status"]
                statusTime = queryTime
            else:
                status = latest["status"]
                statusTime = latest["time"]

            output.append((package["packageID"], status, statusTime))
    return output