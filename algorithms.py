"""
algorithms.py
-------------
Manual implementation of pathfinding algorithms from first principles:
1. A* (A-Star) Search (Informed search using Min-Heap priority queue & admissible heuristics)
2. Breadth-First Search (BFS) (Uninformed search using FIFO Queue - guarantees minimum edge hops)
3. Depth-First Search (DFS) (Uninformed search using LIFO Stack - explores deep branches)

Also includes side-by-side comparative benchmarking for Pune delivery routing.
No third-party search libraries (networkx, scipy, etc.) are used.
"""

import math
import heapq
import time
from collections import deque
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from city_map import CityMap


# ============================================================================
# Heuristic Functions
# ============================================================================

def euclidean_distance(node_a: str, node_b: str, city_map: CityMap) -> float:
    """
    Computes straight-line Euclidean distance between two nodes:
    sqrt((x2 - x1)^2 + (y2 - y1)^2)

    Admissibility:
    In 2D plane coordinate space, straight-line distance is the physical minimum.
    Since graph edge costs represent road paths with curves and congestion,
    Euclidean distance is scaled such that h(n) <= h*(n) (never overestimates).
    This guarantees A* search finds the optimal (least-cost) route.
    """
    x1, y1 = city_map.get_coordinates(node_a)
    x2, y2 = city_map.get_coordinates(node_b)
    # Scale factor 0.8 ensures straight-line heuristic strictly under-approximates edge weights
    return round(math.hypot(x2 - x1, y2 - y1) * 0.8, 2)


def manhattan_distance(node_a: str, node_b: str, city_map: CityMap) -> float:
    """
    Computes grid-based Manhattan distance between two nodes:
    |x2 - x1| + |y2 - y1|
    """
    x1, y1 = city_map.get_coordinates(node_a)
    x2, y2 = city_map.get_coordinates(node_b)
    return round((abs(x2 - x1) + abs(y2 - y1)) * 0.6, 2)


# ============================================================================
# Data Structures for Search Results and Traces
# ============================================================================

@dataclass
class SearchStep:
    """Detailed record of an individual node expansion for tracing."""
    step_num: int
    node: str
    g_cost: float
    h_cost: float
    f_cost: float
    action: str
    updated_neighbors: List[str] = field(default_factory=list)


@dataclass
class SearchResult:
    """Structured report returned after running a pathfinding algorithm."""
    algorithm_name: str
    success: bool
    start_node: str
    goal_node: str
    path: List[str]
    total_cost: float
    explored_nodes: List[str]
    step_history: List[SearchStep]
    execution_time_ms: float
    heuristic_used: str
    message: str


# ============================================================================
# Path Reconstruction
# ============================================================================

def reconstruct_path(came_from: Dict[str, str], current: str) -> List[str]:
    """
    Reconstructs the optimal trajectory backwards from goal to start
    using parent pointers, then reverses it.
    """
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    total_path.reverse()
    return total_path


def compute_path_cost(city_map: CityMap, path: List[str]) -> float:
    """Calculates the cumulative edge cost along a given path of nodes."""
    if not path or len(path) < 2:
        return 0.0
    total = 0.0
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        total += city_map.adjacency.get(u, {}).get(v, 0.0)
    return round(total, 2)


# ============================================================================
# 1. A* Search Algorithm
# ============================================================================

def a_star_search(
    city_map: CityMap,
    start_node: str,
    goal_node: str,
    heuristic_name: str = "Euclidean"
) -> SearchResult:
    """
    Executes A* Search to find the lowest-cost path from start_node to goal_node.
    f(n) = g(n) + h(n)
    """
    start_time = time.perf_counter()

    if heuristic_name.lower() == "manhattan":
        h_func = lambda u, v: manhattan_distance(u, v, city_map)
        h_label = "Manhattan Distance"
    else:
        h_func = lambda u, v: euclidean_distance(u, v, city_map)
        h_label = "Euclidean Distance (Straight-line)"

    if start_node not in city_map.locations or goal_node not in city_map.locations:
        return SearchResult(
            algorithm_name="A* Search",
            success=False,
            start_node=start_node,
            goal_node=goal_node,
            path=[],
            total_cost=0.0,
            explored_nodes=[],
            step_history=[],
            execution_time_ms=0.0,
            heuristic_used=h_label,
            message="Error: Specified start or destination location does not exist in the Pune map."
        )

    if start_node == goal_node:
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        return SearchResult(
            algorithm_name="A* Search",
            success=True,
            start_node=start_node,
            goal_node=goal_node,
            path=[start_node],
            total_cost=0.0,
            explored_nodes=[start_node],
            step_history=[SearchStep(1, start_node, 0.0, 0.0, 0.0, "Start and Goal are identical.")],
            execution_time_ms=round(elapsed_ms, 3),
            heuristic_used=h_label,
            message=f"Trivial Case: Already located at destination '{start_node}'."
        )

    # Priority queue: (f_score, tie_breaker_counter, node_name)
    counter = 0
    open_set: List[Tuple[float, int, str]] = []

    g_score: Dict[str, float] = {node: float("inf") for node in city_map.locations}
    g_score[start_node] = 0.0

    initial_h = h_func(start_node, goal_node)
    f_score: Dict[str, float] = {node: float("inf") for node in city_map.locations}
    f_score[start_node] = initial_h

    heapq.heappush(open_set, (f_score[start_node], counter, start_node))
    came_from: Dict[str, str] = {}
    closed_set = set()

    explored_nodes: List[str] = []
    step_history: List[SearchStep] = []
    step_num = 0

    while open_set:
        current_f, _, current = heapq.heappop(open_set)

        if current in closed_set:
            continue

        closed_set.add(current)
        explored_nodes.append(current)
        step_num += 1

        cur_g = g_score[current]
        cur_h = h_func(current, goal_node)

        if current == goal_node:
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            path = reconstruct_path(came_from, current)

            step_history.append(
                SearchStep(
                    step_num=step_num,
                    node=current,
                    g_cost=cur_g,
                    h_cost=0.0,
                    f_cost=cur_g,
                    action=f"Goal reached! Optimal path verified with total cost {cur_g:.2f}."
                )
            )

            return SearchResult(
                algorithm_name="A* Search",
                success=True,
                start_node=start_node,
                goal_node=goal_node,
                path=path,
                total_cost=round(cur_g, 2),
                explored_nodes=explored_nodes,
                step_history=step_history,
                execution_time_ms=round(elapsed_ms, 3),
                heuristic_used=h_label,
                message=f"Optimal delivery route discovered: {len(path)} stops, total cost: {cur_g:.2f}."
            )

        neighbors = city_map.get_neighbors(current)
        updated_neighbors = []

        for neighbor, edge_weight in neighbors:
            if neighbor in closed_set:
                continue

            tentative_g = cur_g + edge_weight

            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                h_cost = h_func(neighbor, goal_node)
                neighbor_f = tentative_g + h_cost
                f_score[neighbor] = neighbor_f

                counter += 1
                heapq.heappush(open_set, (neighbor_f, counter, neighbor))
                updated_neighbors.append(f"{neighbor} (g={tentative_g:.1f}, f={neighbor_f:.1f})")

        step_history.append(
            SearchStep(
                step_num=step_num,
                node=current,
                g_cost=cur_g,
                h_cost=cur_h,
                f_cost=current_f,
                action=f"Expanded {current}; evaluated {len(updated_neighbors)} neighbors.",
                updated_neighbors=updated_neighbors
            )
        )

    elapsed_ms = (time.perf_counter() - start_time) * 1000
    return SearchResult(
        algorithm_name="A* Search",
        success=False,
        start_node=start_node,
        goal_node=goal_node,
        path=[],
        total_cost=0.0,
        explored_nodes=explored_nodes,
        step_history=step_history,
        execution_time_ms=round(elapsed_ms, 3),
        heuristic_used=h_label,
        message=f"No valid route found between '{start_node}' and '{goal_node}'. Blocked roads have severed all connectivity."
    )


# ============================================================================
# 2. Breadth-First Search (BFS)
# ============================================================================

def breadth_first_search(city_map: CityMap, start_node: str, goal_node: str) -> SearchResult:
    """
    Executes Breadth-First Search (BFS) using a FIFO queue.
    Explores neighbor nodes level by level.
    Guarantees finding the path with the fewest edges / hops (unweighted shortest path).
    """
    start_time = time.perf_counter()

    if start_node not in city_map.locations or goal_node not in city_map.locations:
        return SearchResult(
            algorithm_name="Breadth-First Search (BFS)",
            success=False,
            start_node=start_node,
            goal_node=goal_node,
            path=[],
            total_cost=0.0,
            explored_nodes=[],
            step_history=[],
            execution_time_ms=0.0,
            heuristic_used="None (Uninformed)",
            message="Error: Specified start or destination location does not exist in Pune map."
        )

    if start_node == goal_node:
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        return SearchResult(
            algorithm_name="Breadth-First Search (BFS)",
            success=True,
            start_node=start_node,
            goal_node=goal_node,
            path=[start_node],
            total_cost=0.0,
            explored_nodes=[start_node],
            step_history=[SearchStep(1, start_node, 0.0, 0.0, 0.0, "Start and Goal are identical.")],
            execution_time_ms=round(elapsed_ms, 3),
            heuristic_used="None (Uninformed)",
            message=f"Trivial Case: Already located at destination '{start_node}'."
        )

    queue = deque([start_node])
    visited = {start_node}
    came_from: Dict[str, str] = {}
    explored_nodes: List[str] = []
    step_history: List[SearchStep] = []
    step_num = 0

    while queue:
        current = queue.popleft()
        explored_nodes.append(current)
        step_num += 1

        if current == goal_node:
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            path = reconstruct_path(came_from, current)
            cost = compute_path_cost(city_map, path)

            step_history.append(
                SearchStep(
                    step_num=step_num,
                    node=current,
                    g_cost=cost,
                    h_cost=0.0,
                    f_cost=cost,
                    action=f"Goal reached! BFS found path with {len(path) - 1} hops."
                )
            )

            return SearchResult(
                algorithm_name="Breadth-First Search (BFS)",
                success=True,
                start_node=start_node,
                goal_node=goal_node,
                path=path,
                total_cost=cost,
                explored_nodes=explored_nodes,
                step_history=step_history,
                execution_time_ms=round(elapsed_ms, 3),
                heuristic_used="None (Uninformed)",
                message=f"BFS route discovered: {len(path)} stops ({len(path) - 1} hops), total cost: {cost:.2f}."
            )

        neighbors = city_map.get_neighbors(current)
        enqueued_neighbors = []

        for neighbor, _ in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)
                enqueued_neighbors.append(neighbor)

        step_history.append(
            SearchStep(
                step_num=step_num,
                node=current,
                g_cost=0.0,
                h_cost=0.0,
                f_cost=0.0,
                action=f"Dequeued {current}; enqueued {len(enqueued_neighbors)} neighbors.",
                updated_neighbors=enqueued_neighbors
            )
        )

    elapsed_ms = (time.perf_counter() - start_time) * 1000
    return SearchResult(
        algorithm_name="Breadth-First Search (BFS)",
        success=False,
        start_node=start_node,
        goal_node=goal_node,
        path=[],
        total_cost=0.0,
        explored_nodes=explored_nodes,
        step_history=step_history,
        execution_time_ms=round(elapsed_ms, 3),
        heuristic_used="None (Uninformed)",
        message=f"No valid route found between '{start_node}' and '{goal_node}'. Destination is unreachable."
    )


# ============================================================================
# 3. Depth-First Search (DFS)
# ============================================================================

def depth_first_search(city_map: CityMap, start_node: str, goal_node: str) -> SearchResult:
    """
    Executes Depth-First Search (DFS) using a LIFO stack.
    Explores deep into each branch before backtracking.
    Neither guarantees minimum hops nor minimum cost.
    """
    start_time = time.perf_counter()

    if start_node not in city_map.locations or goal_node not in city_map.locations:
        return SearchResult(
            algorithm_name="Depth-First Search (DFS)",
            success=False,
            start_node=start_node,
            goal_node=goal_node,
            path=[],
            total_cost=0.0,
            explored_nodes=[],
            step_history=[],
            execution_time_ms=0.0,
            heuristic_used="None (Uninformed)",
            message="Error: Specified start or destination location does not exist in Pune map."
        )

    if start_node == goal_node:
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        return SearchResult(
            algorithm_name="Depth-First Search (DFS)",
            success=True,
            start_node=start_node,
            goal_node=goal_node,
            path=[start_node],
            total_cost=0.0,
            explored_nodes=[start_node],
            step_history=[SearchStep(1, start_node, 0.0, 0.0, 0.0, "Start and Goal are identical.")],
            execution_time_ms=round(elapsed_ms, 3),
            heuristic_used="None (Uninformed)",
            message=f"Trivial Case: Already located at destination '{start_node}'."
        )

    # Stack stores (current_node, [path_so_far])
    stack: List[Tuple[str, List[str]]] = [(start_node, [start_node])]
    visited = set()
    explored_nodes: List[str] = []
    step_history: List[SearchStep] = []
    step_num = 0

    while stack:
        current, current_path = stack.pop()

        if current in visited:
            continue

        visited.add(current)
        explored_nodes.append(current)
        step_num += 1

        if current == goal_node:
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            cost = compute_path_cost(city_map, current_path)

            step_history.append(
                SearchStep(
                    step_num=step_num,
                    node=current,
                    g_cost=cost,
                    h_cost=0.0,
                    f_cost=cost,
                    action=f"Goal reached! DFS completed branch with {len(current_path)} stops."
                )
            )

            return SearchResult(
                algorithm_name="Depth-First Search (DFS)",
                success=True,
                start_node=start_node,
                goal_node=goal_node,
                path=current_path,
                total_cost=cost,
                explored_nodes=explored_nodes,
                step_history=step_history,
                execution_time_ms=round(elapsed_ms, 3),
                heuristic_used="None (Uninformed)",
                message=f"DFS path discovered: {len(current_path)} stops, total cost: {cost:.2f}."
            )

        neighbors = city_map.get_neighbors(current)
        pushed_neighbors = []

        # Iterate in reverse to explore in canonical order
        for neighbor, _ in reversed(neighbors):
            if neighbor not in visited:
                stack.append((neighbor, current_path + [neighbor]))
                pushed_neighbors.append(neighbor)

        step_history.append(
            SearchStep(
                step_num=step_num,
                node=current,
                g_cost=0.0,
                h_cost=0.0,
                f_cost=0.0,
                action=f"Popped {current}; pushed {len(pushed_neighbors)} neighbors onto stack.",
                updated_neighbors=pushed_neighbors
            )
        )

    elapsed_ms = (time.perf_counter() - start_time) * 1000
    return SearchResult(
        algorithm_name="Depth-First Search (DFS)",
        success=False,
        start_node=start_node,
        goal_node=goal_node,
        path=[],
        total_cost=0.0,
        explored_nodes=explored_nodes,
        step_history=step_history,
        execution_time_ms=round(elapsed_ms, 3),
        heuristic_used="None (Uninformed)",
        message=f"No valid route found between '{start_node}' and '{goal_node}'. Destination is unreachable."
    )


# ============================================================================
# Side-by-Side Algorithm Comparison Benchmarking
# ============================================================================

def compare_all_algorithms(
    city_map: CityMap,
    start_node: str,
    goal_node: str,
    heuristic_name: str = "Euclidean"
) -> List[SearchResult]:
    """
    Executes BFS, DFS, and A* Search sequentially on the same start-goal pair
    to produce a direct comparative benchmark.
    """
    res_bfs = breadth_first_search(city_map, start_node, goal_node)
    res_dfs = depth_first_search(city_map, start_node, goal_node)
    res_astar = a_star_search(city_map, start_node, goal_node, heuristic_name)

    return [res_astar, res_bfs, res_dfs]
