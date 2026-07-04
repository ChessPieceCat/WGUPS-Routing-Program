#logs packages with their status, time, and truck as called
from models.status import Status


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
                status = package["initialStatus"]
                statusTime = queryTime
                truckID = None
            else:
                status = latest["status"]
                statusTime = latest["time"]
                if latest["truckID"] is not None:
                    truckID = latest["truckID"] + 1
                else: truckID = None

            output.append((package["packageID"], status, statusTime, truckID))
    return output