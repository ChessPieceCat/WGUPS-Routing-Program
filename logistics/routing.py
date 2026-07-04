'''FUNCTION
getDistance(locationOne, locationTwo, distanceTable)
IF
distanceTable[locationOne]
CONTAINS
locationTwo
RETURN
distanceTable[locationOne][locationTwo]
ELSE
RETURN
distanceTable[locationTwo][locationOne]
END
IF
END
FUNCTION

FUNCTION
nearestNeighbor(truck, distanceTable)
location = "HUB"

WHILE
unvisited
packages > 0

nearestPackage = NULL
shortestDistance = infinity

FOR
each
unvisited
package
distance = getDistance(location, package.address, distanceTable)

IF
distance < shortestDistance
shortestDistance = distance
nearestPackage = package
END
IF
END
FOR

ADD
nearestPackage
to
route

Mark
nearestPackage as visited

location = nearestPackage.address

END
WHILE

ADD
HUB
to
end
of
route

RETURN
route

END
FUNCTION

FUNCTION
calculateTotalDistance(route, distanceTable)
total = getDistance(HUB, route[0], distanceTable)
FOR
i
FROM
0
TO
length(route) - 2
total += getDistance(route[i], route[i + 1], distanceTable)
END
FOR
RETURN
total
END
FUNCTION

FUNCTION
twoOpt(route, distanceTable)
bestRoute = route
bestDistance = calculateTotalDistance(route, distanceTable)

FOR
i
FROM
1
TO
length(route) - 3
FOR
j
FROM
i + 2
TO
length(route) - 2
oldCost = getDistance(route[i - 1], route[i], distanceTable) + getDistance(route[j], route[j + 1], distanceTable)
newCost = getDistance(route[i - 1], route[j], distanceTable) + getDistance(route[i], route[j + 1], distanceTable)

IF
newCost < oldCost
newRoute = copy(route)
REVERSE
newRoute[i:j]
newDistance = bestDistance - oldCost + newCost

IF
newDistance < bestDistance
bestDistance = newDistance
bestRoute = newRoute
route = newRoute
END
IF
END
IF
END
FOR
END
FOR

RETURN
bestRoute
END
FUNCTION

FUNCTION
buildRoute(truck, distanceTable)
route = nearestNeighbor(truck, distanceTable)
route = twoOpt(route, distanceTable)
truck.route = route
END
FUNCTION'''