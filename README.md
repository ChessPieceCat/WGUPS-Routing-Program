# WGUPS Routing Optimization

A route optimization and delivery simulation written in Python that models package deliveries for the fictional Western Governors University Parcel Service (WGUPS). The project implements routing heuristics and custom data structures to deliver all packages within their required deadlines while minimizing total travel distance.

This project was completed as part of the **Data Structures and Algorithms II** course at **Western Governors University**.

---

## Overview

The objective was to design and implement a routing system capable of delivering 40 packages while satisfying a variety of real-world delivery constraints, including package deadlines, delayed arrivals, incorrect addresses, truck capacity limits, and package grouping requirements.

The solution combines routing heuristics with a custom package management system to produce an efficient delivery schedule while remaining well under the project's maximum mileage requirement.

### Final Results

* **Total distance traveled:** **127.3 miles**
* **Project mileage limit:** **140 miles**
* **Final delivery completed:** **1:04 PM**
* **All package deadlines met**

---

## Features

* Custom package management data structure
* Delivery simulation with multiple trucks and drivers
* Route optimization using the **Nearest Neighbor** heuristic with **2-opt** optimization
* Time-based package events (delayed arrivals and address corrections)
* Package status lookup at any point during the delivery day
* Complete simulation of truck locations and package deliveries

---

## Project Requirements

The simulation models a realistic delivery environment with the following constraints:

* Three delivery trucks with a maximum capacity of 16 packages each
* Two drivers available throughout the day
* Trucks travel at an average speed of 18 mph
* Deliveries begin no earlier than **8:00 AM**
* Certain packages must remain together on the same truck
* Delayed packages cannot be loaded until they arrive at the hub
* Package #9 receives a corrected delivery address at **10:20 AM**
* All 40 packages must be delivered before their deadlines
* Total travel distance must remain under **140 miles**

---

## Algorithm

### Chosen Approach

The routing algorithm combines a **Nearest Neighbor** heuristic with **2-opt** optimization.

Nearest Neighbor provides an efficient initial route by repeatedly selecting the closest unvisited destination. The resulting route is then improved using the 2-opt heuristic, which removes inefficient edge crossings and shortens the overall travel distance.

For a problem of this size, the combination offers an excellent balance between solution quality and computational complexity.

### Performance

The completed solution:

* Delivered every package before its deadline
* Traveled only **127.3 miles**
* Correctly handled delayed packages and address corrections
* Maintained required package groupings

---

## Alternative Algorithms Considered

### 3-opt

3-opt extends the 2-opt heuristic by replacing three edges at a time instead of two. While this can produce shorter routes, the improvement would likely be marginal for a dataset containing only 40 packages.

### Lin-Kernighan

The Lin-Kernighan heuristic dynamically determines how many edges to replace during optimization, often producing solutions closer to the optimal Traveling Salesman route.

Although it generally outperforms 2-opt, its additional complexity is unnecessary for a problem of this scale.

---

## Data Structures

Package information is stored in a custom hash table implementation that supports efficient insertion, updating, and lookup operations without relying on external libraries.

### Complexity

| Operation | Average Complexity |
| --------- | -----------------: |
| Insert    |               O(1) |
| Search    |               O(1) |
| Update    |               O(1) |

### Alternative Data Structures

**Balanced Binary Search Tree**

A balanced BST would maintain sorted package data, simplifying some scheduling tasks, but average search performance would decrease to **O(log n)**.

**Heap**

A heap would provide efficient access to the highest-priority package, making priority scheduling easier. However, searching for arbitrary packages would become significantly less efficient than using a hash table.

---

## Lessons Learned

This project provided valuable experience designing algorithms and building larger software systems.

Some of the most significant lessons included:

* The importance of planning data structures before implementation.
* Designing simulations requires thinking about concurrent events rather than strictly sequential execution.
* Incremental testing dramatically reduces debugging time.
* Understanding the underlying mechanics of routing heuristics is more valuable than simply implementing an existing algorithm.

If revisiting the project, I would spend considerably more time designing the architecture and data structures before writing code, as this would reduce later refactoring and simplify testing.

---

## Technologies

* Python
* Custom hash table implementation
* Nearest Neighbor heuristic
* 2-opt route optimization
* Object-oriented programming

---

## References

* Python Software Foundation. *Python Language Reference.* https://docs.python.org/3.13/reference/index.html
* Stephens, R. (2024). *Understanding the 2-opt Algorithm for the Traveling Salesman Problem.* https://rodstephensbooks.com/tsp_2opt.html
* nandan7198. *Traveling Salesman Problem Solver using Nearest Neighbor and 2-opt.* https://github.com/nandan7198/TSP-Solver
* Olds, E., Lysecky, R., Vahid, F., & Lysecky, S. (2025). *Data Structures and Algorithms II (C950).* zyBooks.
