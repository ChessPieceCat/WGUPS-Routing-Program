This project was created for Data Structures and Algorithms II at Western Governors University. The scenario details are listed below:

This task is the implementation phase of the WGUPS Routing Program. The Western Governors University Parcel Service (WGUPS) needs to determine an efficient route and delivery distribution for their daily local deliveries (DLD) because packages are not currently being consistently delivered by their promised deadline. The Salt Lake City DLD route has three trucks, two drivers, and an average of 40 packages to deliver each day. Each package has specific criteria and delivery requirements that are listed in the attached “WGUPS Package File.” Your task is to determine an algorithm, write code, and present a solution where all 40 packages will be delivered on time while meeting each package’s requirements and keeping the combined total distance traveled under 140 miles for all trucks. The specific delivery locations are shown on the attached “Salt Lake City Downtown Map,” and distances to each location are given in the attached “WGUPS Distance Table.” The intent is to use the program for this specific location and also for many other cities in each state where WGU has a presence. As such, you will need to include detailed comments to make your code easy to follow and to justify the decisions you made while writing your scripts. The supervisor should be able to see, at assigned points, the progress of each truck and its packages by any of the variables listed in the “WGUPS Package File,” including what has been delivered and at what time the delivery occurred.

•  Each truck can carry a maximum of 16 packages, and the ID number of each package is unique.
•  The trucks travel at an average speed of 18 miles per hour and have an infinite amount of gas with no need to stop.
•  There are no collisions.
•  Three trucks and two drivers are available for deliveries. Each driver stays with the same truck as long as that truck is in service.
•  Drivers leave the hub no earlier than 8:00 a.m., with the truck loaded, and can return to the hub for packages if needed.
•  The delivery and loading times are instantaneous (i.e., no time passes while at a delivery or when moving packages to a truck at the hub). This time is factored into the calculation of the average speed of the trucks.
•  There is up to one special note associated with a package.
•  The delivery address for package #9, Third District Juvenile Court, is wrong and will be corrected at 10:20 a.m. WGUPS is aware that the address is incorrect and will be updated at 10:20 a.m. However, WGUPS does not know the correct address (410 S. State St., Salt Lake City, UT 84111) until 10:20 a.m.
•  The distances provided in the “WGUPS Distance Table” are equal regardless of the direction traveled.
•  The day ends when all 40 packages have been delivered.

Strengths of the Chosen Algorithm
At only 127.3 miles total, this algorithm is well under the project's mileage limit. The final delivery at 1:04 pm also shows that the algorithm is efficient not only in mileage but also in time.

Verification of Algorithm
This algorithm delivers all packages before their deadlines pass, finishes with 127.3 miles, keeps all packages that must be delivered together on the same route, and waits to deliver delayed packages until they arrive at the hub or have their addresses corrected.

Other Possible Algorithms
Two algorithms that could have been used instead are 3-opt and Lin-Kernighan.

Algorithm Differences
The algorithms mentioned are extensions of the 2-opt heuristic used in this program. While 2-opt removes edge crossings and replaces two edges at a time, 3-opt removes three edges at a time. This increases efficiency, but it would be a marginal improvement for the data size and increase processing speed.
Lin-Kernighan is a further, dynamic expansion of these algorithms. This algorithm continues to remove edges as long as there is an improvement. This means it could result in something like 2 or 3-opt, or it could go much farther than that. This would likely result in lower mileage, but the algorithm's complexity is still unreasonable for such a small data set.

Different Approach
If I were to redo this project, I would focus most on proper planning. I planned a detailed program in pseudocode, but I had to adjust the structure as I moved away from a sequential design toward a concurrent one. This issue arose because I failed to plan the simulation properly. I should also have clearly defined each data structure beforehand, as this caused issues later when I needed to change them. The two-opt section caused many issues as I learned how it worked, but ultimately, the trial and error was very useful in deepening my understanding of the algorithm. Another major issue with my work structure was failing to test each file as it was written properly. This resulted in hours of debugging that may have been faster if I had tested each file as I finished it.

Verification of Data Structure
The data structure used to hold package data is an array of lists and does not require any additional libraries or classes. It has an insert function that adds all relevant components, as well as update and search functions.

Other Data Structures
One alternative data structure is a balanced binary search tree. Another option is a heap.

Data Structure Differences
Unlike a hash table, a balanced BST would keep packages sorted by the specified component (ID, deadline, weight, etc.). This would allow for easier loading later in the program, since much of the sorting would already be done. However, searching this structure would be slower, O(log n), than searching the hash table, O(1) (average).
A heap would provide faster access to packages based on priority. The insertion and update functions would be on the order of the BST, but accessing the highest/lowest-priority package would be O(1). This would make delivery scheduling easier, but cause issues when searching for other packages that are not at the top or bottom of the heap.

I. Sources
The Python Language Reference. (2026). Python Documentation. https://docs.python.org/3.13/reference/index.html (Syntax and behavior)

‌Stephens, R. (2024). HowTo: Understand the 2-opt algorithm for solving the traveling salesman problem. Rodstephensbooks.com. https://rodstephensbooks.com/tsp_2opt.html (To understand 2-opt)
‌
nandan7198. (2023). GitHub - nandan7198/TSP-Solver: Traveling Salesman Problem Solver using Nearest Neighbor and 2-OPT Algorithm. GitHub. https://github.com/nandan7198/TSP-Solver/tree/main (Reference to further understand 2-opt, coded in Java
‌
Olds, E., Lysecky, R., Vahid, F., & Lysecky, S. (2025). C 950: Data structures and algorithms II (zyBook, ISBN 979-8-203-08225-1). zyBooks (zyante Inc.). https://learn.zybooks.com/zybook/WGUC950v5 (Used frequently for coding references and learning concepts)
