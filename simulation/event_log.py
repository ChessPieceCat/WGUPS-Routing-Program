'''FUNCTION
queryEventLog(queryTime, eventLog, table)
output = []

FOR each bucket
IN
table
FOR
each
package
IN
bucket
latest = NULL

IF
eventLog[package.packageID]
exists
FOR
each
event
IN
eventLog[package.packageID]
IF
event.time <= queryTime
IF latest == NULL
OR
event.time > latest.time
latest = event
END
IF
END
IF
END
FOR
END
IF

IF
latest == NULL
status = STATUS.AT_HUB
ELSE
status = latest.status
END
IF

ADD(package.packageID, status)
TO
output
END
FOR
END
FOR
RETURN
output
END
FUNCTION

FUNCTION
logEvent(eventLog, packageID, status, time, truckID)
IF
eventLog[packageID]
does
not exist
eventLog[packageID] = []
END
IF

APPEND
{status: status, time: time, truckID: truckID}
TO
eventLog[packageID]
END
FUNCTION

'''
from models.status import Status


def logEvent(eventLog, packageID, status, time, truckID):
    if packageID not in eventLog:
        eventLog[packageID] = []

    eventLog[packageID].append({"status": status, "time": time, "truckID": truckID})

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
            else:
                status = latest["status"]

            output.append((package["packageID"], status))
    return output