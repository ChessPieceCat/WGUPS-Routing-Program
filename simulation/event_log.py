'''FUNCTION
queryEventLog(queryTime, eventLog, table)
output = []

FOR
each
bucket
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
IF
latest == NULL
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

FUNCTION
markTruckActive(truck)
truck.currentLocation = "ON ROUTE"
END
FUNCTION'''