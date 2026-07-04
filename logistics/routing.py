'''FUNCTION
getDistance(locationOne, locationTwo, distanceTable)
    IF distanceTable[locationOne] CONTAINS locationTwo
        RETURN distanceTable[locationOne][locationTwo]
    ELSE
        RETURN distanceTable[locationTwo][locationOne]
    END IF
END FUNCTION

FUNCTION nearestNeighbor(truck, distanceTable)
    location = "HUB"

    WHILE unvisited packages > 0
        nearestPackage = NULL
        shortestDistance = infinity

        FOR each unvisited package
            distance = getDistance(location, package.address, distanceTable)
            IF distance < shortestDistance
                shortestDistance = distance
                nearestPackage = package
            END IF
        END FOR

        ADD nearestPackage to route

        Mark nearestPackage as visited

        location = nearestPackage.address

    END WHILE

    ADD HUB to end of route

    RETURN route

END FUNCTION

FUNCTION calculateTotalDistance(route, distanceTable)
    total = getDistance(HUB, route[0], distanceTable)
    FOR i FROM 0 TO length(route) - 2
        total += getDistance(route[i], route[i + 1], distanceTable)
    END FOR
    RETURN total
END FUNCTION

FUNCTION twoOpt(route, distanceTable)
    bestRoute = route
    bestDistance = calculateTotalDistance(route, distanceTable)

    FOR i FROM 1 TO length(route) - 3
        FOR j FROM i + 2 TO length(route) - 2
            oldCost = getDistance(route[i - 1], route[i], distanceTable) + getDistance(route[j], route[j + 1], distanceTable)
            newCost = getDistance(route[i - 1], route[j], distanceTable) + getDistance(route[i], route[j + 1], distanceTable)

            IF newCost < oldCost
                newRoute = copy(route)
                REVERSE newRoute[i:j]
                newDistance = bestDistance - oldCost + newCost

                IF newDistance < bestDistance
                    bestDistance = newDistance
                    bestRoute = newRoute
                    route = newRoute
                END IF
            END IF
        END FOR
    END FOR

    RETURN bestRoute
END FUNCTION

FUNCTION buildRoute(truck, distanceTable)
    route = nearestNeighbor(truck, distanceTable)
    route = twoOpt(route, distanceTable)
    truck.route = route
END FUNCTION'''
from copy import copy

def getDistance(locationOne, locationTwo, distanceTable):
    if locationTwo in distanceTable[locationOne]:
        return distanceTable[locationOne][locationTwo]
    else:
        return distanceTable[locationTwo][locationOne]

def nearestNeighbor(truck, distanceTable):
    location = "HUB"
    route = []
    unvisited = set(truck.packages)

    while len(unvisited) > 0:
        nearestPackage = None
        shortestDistance = float('inf')

        for package in unvisited:
            distance = getDistance(location, package.address, distanceTable)
            if distance < shortestDistance:
                shortestDistance = distance
                nearestPackage = package

        if nearestPackage is not None:
            route.append(nearestPackage)
            unvisited.remove(nearestPackage)
            location = nearestPackage.address
        else:
            break

    route.append("HUB")
    return route

def calculateTotalDistance(route, distanceTable):
    total = getDistance("Hub", route[0], distanceTable)
    for i in range(len(route) - 2):
        total += getDistance(route[i], route[i + 1], distanceTable)
    return total

def twoOpt(route, distanceTable):
    bestRoute = route
    bestDistance = getDistance("Hub", bestRoute[0], distanceTable)

    for i in range(1, len(route) - 3):
        for j in range(i + 2, len(route) - 2):
            oldCost = getDistance(bestRoute[i - 1], bestRoute[i], distanceTable) + getDistance(bestRoute[j], bestRoute[j + 1], distanceTable)
            newCost = getDistance(bestRoute[i - 1], bestRoute[j], distanceTable) + getDistance(bestRoute[i], bestRoute[j + 1], distanceTable)

            if newCost < oldCost:
                newRoute = copy(bestRoute)
                newRoute[i:j] = newRoute[i:j][::-1]
                newDistance = bestDistance - oldCost + newCost

                if newDistance < bestDistance:
                    bestDistance = newDistance
                    bestRoute = newRoute
                    route = newRoute

    return bestRoute

def buildRoute(truck, distanceTable):
    route = nearestNeighbor(truck, distanceTable)
    route = twoOpt(route, distanceTable)
    truck.route = route
