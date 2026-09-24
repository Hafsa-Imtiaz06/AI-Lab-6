import math
import heapq


# ==========================================
# HOSPITAL LOCATIONS
# ==========================================

locations = {
    "Pharmacy": (0, 0),
    "Main_Corridor": (2, 1),
    "Patient_Wing": (1, 4),
    "Nursing_Station": (4, 2),
    "Laboratory": (5, 5),
    "Emergency_Ward": (8, 6)
}


# ==========================================
# HOSPITAL GRAPH
# ==========================================

hospital_graph = {
    "Pharmacy": {
        "Main_Corridor": 2.2,
        "Patient_Wing": 4.1
    },

    "Main_Corridor": {
        "Nursing_Station": 2.2
    },

    "Patient_Wing": {
        "Laboratory": 5.0
    },

    "Nursing_Station": {
        "Laboratory": 3.2,
        "Emergency_Ward": 6.0
    },

    "Laboratory": {
        "Emergency_Ward": 3.2
    },

    "Emergency_Ward": {}
}


# ==========================================
# EUCLIDEAN HEURISTIC
# ==========================================

def heuristic(current, goal):

    x1, y1 = locations[current]
    x2, y2 = locations[goal]

    return math.sqrt(
        (x2 - x1) ** 2 +
        (y2 - y1) ** 2
    )


# ==========================================
# RECONSTRUCT PATH
# ==========================================

def reconstruct_path(came_from, current):

    path = []

    while current is not None:
        path.append(current)
        current = came_from[current]

    path.reverse()

    return path


# ==========================================
# GREEDY BEST-FIRST SEARCH
# ==========================================

def gbfs(start, goal):

    priority_queue = []

    heapq.heappush(
        priority_queue,
        (heuristic(start, goal), start)
    )

    came_from = {
        start: None
    }

    visited = set()

    while priority_queue:

        _, current = heapq.heappop(priority_queue)

        if current in visited:
            continue

        visited.add(current)

        if current == goal:

            path = reconstruct_path(
                came_from,
                current
            )

            cost = 0

            for i in range(len(path) - 1):

                cost += hospital_graph[
                    path[i]
                ][
                    path[i + 1]
                ]

            return path, cost

        for neighbor in hospital_graph[current]:

            if neighbor not in visited:

                if neighbor not in came_from:
                    came_from[neighbor] = current

                heapq.heappush(
                    priority_queue,
                    (
                        heuristic(neighbor, goal),
                        neighbor
                    )
                )

    return None, None


# ==========================================
# A* SEARCH
# ==========================================

def a_star(start, goal):

    priority_queue = []

    g_cost = {
        start: 0
    }

    came_from = {
        start: None
    }

    heapq.heappush(
        priority_queue,
        (
            heuristic(start, goal),
            start
        )
    )

    while priority_queue:

        f_current, current = heapq.heappop(
            priority_queue
        )

        expected_f = (
            g_cost[current]
            + heuristic(current, goal)
        )

        if abs(f_current - expected_f) > 1e-9:
            continue

        if current == goal:

            path = reconstruct_path(
                came_from,
                current
            )

            return path, g_cost[current]

        for neighbor, edge_cost in hospital_graph[current].items():

            tentative_g = (
                g_cost[current]
                + edge_cost
            )

            if tentative_g < g_cost.get(
                neighbor,
                float("inf")
            ):

                came_from[neighbor] = current

                g_cost[neighbor] = tentative_g

                f_neighbor = (
                    tentative_g
                    + heuristic(neighbor, goal)
                )

                heapq.heappush(
                    priority_queue,
                    (
                        f_neighbor,
                        neighbor
                    )
                )

    return None, None