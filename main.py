#Tiernen Bunnell WGUPS Routing Program - STUDENT ID:001220970
import re

from data.distance_table import loadDistanceTable
from data.hash_table import HashTable
from data.package_loader import loadPackages
from models.driver import Driver
from models.truck import Truck
from simulation.event_log import queryEventLog
from simulation.simulate import simulateDelivery, getMileageAtTime


#defines the main control function
def main():
    #creates hash table, distance table, trucks, drivers, event log, and loads packages
    table = HashTable()
    distanceTable = loadDistanceTable("distanceFile.csv")
    trucks = [Truck(0), Truck(1), Truck(2)]
    drivers = [Driver(0), Driver(1)]
    loadPackages("packageFile.csv", table)
    eventLog, mileageLog = simulateDelivery(trucks, drivers, table, distanceTable)

    #loop for user input to list package info and total mileage
    while True:
        print("Enter time (HH:MM in 24-hour format) or EXIT")
        userInput = input()

        if userInput == "EXIT":
            break
        elif not re.match(r"^\d{1,2}:\d{2}$", userInput):
            print("Invalid input")
            continue

        queryTime = parseTime(userInput)
        result = queryEventLog(queryTime, eventLog, table)

        print(f"Mileage of All Trucks: {getMileageAtTime(queryTime, mileageLog):.1f} miles")
        for packageID, status, statusTime in result:
            print(f"Package ID: {packageID}: {status.value} (at {formatTime(statusTime)})")
#parse time function to convert the user time to a float. Floats are used in other parts of the program rather than time for simple calculation
def parseTime(timeString):
    hour, minute = timeString.split(":")
    hour = int(hour)
    minute = int(minute)
    return hour + (minute / 60)
#formats the time output from float to HH:MM
def formatTime(decimalTime):
    hours = int(decimalTime)
    minutes = int(round((decimalTime - hours) * 60))
    if minutes == 60:
        hours += 1
        minutes = 0
    return "{:02}:{:02}".format(hours, minutes)

if __name__ == "__main__":
    main()