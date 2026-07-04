
from copy import copy
#gets the distance between two locations using the distance table
def getDistance(locationOne, locationTwo, distanceTable):
    if locationTwo in distanceTable[locationOne]:
        return distanceTable[locationOne][locationTwo]
    #flips the input if original input isn't found
    else:
        return distanceTable[locationTwo][locationOne]
#runs a nearest neighbor algorithm to create initial route
def nearestNeighbor(truck, distanceTable):
    location = "4001 South 700 East,  Salt Lake City, UT 84107"
    route = []
    unvisited = list(truck.packages)
    #runs loop while there are still unvisited packages
    while len(unvisited) > 0:
        nearestPackage = None
        #sets shortest distance to infinity to account for lack of assigned package in initialization
        shortestDistance = float('inf')
        #gets the distance of each package address and compares to the currently stored shortest distance
        for package in unvisited:
            distance = getDistance(location, package["address"], distanceTable)
            if distance < shortestDistance:
                shortestDistance = distance
                nearestPackage = package
        #append the nearest package to the route and remove it from "unvisited"
        if nearestPackage is not None:
            route.append(nearestPackage["address"])
            unvisited.remove(nearestPackage)
            #sets the new location in the algorithm to the nearest package address
            location = nearestPackage["address"]
        else:
            break
    #adds the hub to the end of the route
    route.append("4001 South 700 East,  Salt Lake City, UT 84107")
    return route
#calculates the total distance in the route
def calculateTotalDistance(route, distanceTable):
    total = getDistance("4001 South 700 East,  Salt Lake City, UT 84107", route[0], distanceTable)
    for i in range(len(route) - 1):
        total += getDistance(route[i], route[i + 1], distanceTable)
    return total
#a two-opt algorithm to swap locations in the route. Starts with the calculated nearest neighbor route and its distance
def twoOpt(route, distanceTable):
    bestRoute = route
    bestDistance = calculateTotalDistance(bestRoute, distanceTable)
    #tries all pairs of edges to swap
    for i in range(1, len(route) - 2):
        for j in range(i + 2, len(route) - 1):
            oldCost = getDistance(bestRoute[i - 1], bestRoute[i], distanceTable) + getDistance(bestRoute[j], bestRoute[j + 1], distanceTable)
            newCost = getDistance(bestRoute[i - 1], bestRoute[j], distanceTable) + getDistance(bestRoute[i], bestRoute[j + 1], distanceTable)
            #changes new route and distance if improvement is found
            if newCost < oldCost:
                newRoute = copy(bestRoute)
                newRoute[i:j + 1] = newRoute[i:j + 1][::-1]
                newDistance = bestDistance - oldCost + newCost

                if newDistance < bestDistance:
                    bestDistance = newDistance
                    bestRoute = newRoute
                    route = newRoute

    return bestRoute
#builds the route using the functions above. First runs nearest neighbor and then uses two opt until it fails to find an improvement.
#Two opt could run longer to further optimize, but this would increase processing time
def buildRoute(truck, distanceTable):
    route = nearestNeighbor(truck, distanceTable)
    while True:
        newRoute = twoOpt(route, distanceTable)
        if calculateTotalDistance(newRoute, distanceTable) >= calculateTotalDistance(route, distanceTable):
            break
        route = newRoute
    truck.route = route
