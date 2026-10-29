"""
city_map.py
-----------
Centralized, reusable data file and graph data structure for Pune City, Maharashtra.

Contains all 36 authentic Pune and PCMC locations:
- PCMC & North-West: Pimpri, Chinchwad, Akurdi, Nigdi, Talegaon, Alandi
- West Pune: Hinjawadi, Wakad, Baner, Balewadi, Aundh, Pashan, Susgaon, Pirangut, Lavale, Bavdhan
- Central Pune: Shivajinagar, Deccan, Pune Railway Station, FC Road, JM Road, Swargate, Erandwane, Kothrud
- South Pune: Katraj, Narhe, Warje, Kondhwa, NIBM, Wanowrie
- East Pune: Hadapsar, Magarpatta, Mundhwa, Kharadi, Wagholi, Viman Nagar, Lohegaon, Yerawada

Coordinates are normalized to visually reproduce the Pune City Connected Location Graph
while maintaining admissible Euclidean lower bounds for A* search.
"""

import math
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass


@dataclass
class Location:
    """Represents a Pune delivery location node with 2D graph coordinates."""
    name: str
    x: float
    y: float
    region: str
    icon: str
    description: str


# ============================================================================
# Centralized Pune Location Definitions
# ============================================================================
# Format: (Name, X, Y, Region, Icon, Description)
# Coordinates visually align with the provided Pune City Connected Location Graph diagram.
PUNE_LOCATIONS_DATA = [
    # PCMC & North-West
    ("Talegaon", 2.2, 9.8, "PCMC & North-West", "🏭", "Industrial and manufacturing hub on the old highway corridor"),
    ("Hinjawadi", 3.8, 8.2, "West Pune", "💻", "Rajiv Gandhi Infotech Park - Pune's primary IT / tech campus"),
    ("Wakad", 6.2, 8.8, "West Pune", "🏙️", "High-density residential and commercial node connecting PCMC and Pune"),
    ("Pimpri", 8.8, 9.2, "PCMC & North-West", "🏢", "Major industrial, commercial, and civic civic center in PCMC"),
    ("Chinchwad", 11.2, 9.6, "PCMC & North-West", "🏭", "Prominent automotive, industrial, and railway hub in PCMC"),
    ("Nigdi", 11.8, 11.6, "PCMC & North-West", "🚏", "Northern residential terminus and transportation junction (Bhakti-Shakti)"),
    ("Akurdi", 13.0, 8.8, "PCMC & North-West", "🚆", "Education and transit center with key suburban railway station"),
    ("Alandi", 14.8, 10.0, "PCMC & North-West", "🛕", "Historic pilgrim and cultural center on the Indrayani River"),

    # West Pune
    ("Baner", 4.2, 6.2, "West Pune", "🛍️", "Prime commercial corridor, startups, Baner High Street"),
    ("Balewadi", 5.6, 6.8, "West Pune", "🏟️", "Balewadi Sports Complex and modern commercial avenue"),
    ("Aundh", 7.4, 5.6, "West Pune", "🏬", "Established residential and upscale shopping suburb near SPPU"),
    ("Susgaon", 1.8, 7.2, "West Pune", "🏡", "Rapidly expanding western suburban valley near Baner hills"),
    ("Pirangut", 0.6, 5.6, "West Pune", "🏞️", "Industrial and scenic gateway to Lavasa and Mulshi"),
    ("Lavale", 1.2, 3.6, "West Pune", "🎓", "Symbiosis Knowledge Village hilltop university campus"),
    ("Pashan", 3.6, 4.6, "West Pune", "🔬", "National Chemical Laboratory (NCL), DRDO, and Pashan Lake"),
    ("Bavdhan", 4.2, 2.8, "West Pune", "⛰️", "Quiet suburban neighborhood between Kothrud and Paud Road"),

    # Central Pune
    ("Shivajinagar", 11.6, 4.6, "Central Pune", "🚉", "Major multi-modal transit hub, District Court, and COEP"),
    ("Deccan", 9.4, 4.6, "Central Pune", "☕", "Deccan Gymkhana, Fergusson College Road (FC Rd) & JM Road"),
    ("Pune Railway Station", 11.6, 7.2, "Central Pune", "🚂", "Central railway terminal and principal intercity transport gateway"),
    ("Erandwane", 8.2, 2.0, "Central Pune", "🌳", "Residential neighborhood, educational institutes, and Karve Road corridor"),
    ("Kothrud", 6.0, 1.6, "Central Pune", "🎬", "Prominent residential suburb, Paud Road, and FTII campus"),
    ("Swargate", 12.4, 2.2, "Central Pune", "🚌", "Main State Transport (MSRTC) bus hub and central junction"),

    # East Pune
    ("Yerawada", 13.4, 6.6, "East Pune", "🏛️", "Historical transit junction, Deccan College, and Ahmednagar Road entry"),
    ("Viman Nagar", 16.2, 6.6, "East Pune", "✈️", "Pune International Airport vicinity, shopping malls, and IT hub"),
    ("Lohegaon", 18.4, 8.4, "East Pune", "🛫", "Air Force base, domestic airport terminal, and upcoming suburbs"),
    ("Kharadi", 19.0, 5.6, "East Pune", "💼", "EON Free Zone IT Park, World Trade Center, and business hub"),
    ("Wagholi", 21.2, 7.2, "East Pune", "🏫", "Eastern residential suburb, engineering institutes on Nagar Road"),
    ("Mundhwa", 18.2, 4.0, "East Pune", "🏭", "Industrial and commercial riverfront connecting Kharadi and Hadapsar"),
    ("Magarpatta", 15.2, 4.0, "East Pune", "🏙️", "Planned cybercity, integrated corporate IT township"),
    ("Hadapsar", 17.6, 2.2, "East Pune", "🎯", "Eastern terminus, industrial zone, Solapur Highway gateway"),

    # South Pune
    ("Warje", 3.6, 0.6, "South Pune", "🏡", "Suburban node along the Mumbai-Bangalore highway and Mutha river"),
    ("Narhe", 4.8, -1.0, "South Pune", "🏘️", "Educational and residential sector near Katraj-Dehu bypass"),
    ("Katraj", 11.2, -1.2, "South Pune", "🦁", "Rajiv Gandhi Zoological Park, Katraj Ghat, and southern gateway"),
    ("Kondhwa", 13.8, -0.2, "South Pune", "🏬", "Expanding multicultural commercial and residential zone"),
    ("NIBM", 15.2, -1.6, "South Pune", "🛍️", "National Institute of Bank Management and upscale residential corridor"),
    ("Wanowrie", 15.2, 1.0, "South Pune", "🏥", "Command Hospital, Armed Forces Medical College, and Cantonment")
]


# ============================================================================
# Centralized Pune Road Network Connections (Edges & Costs)
# ============================================================================
# Exactly matches the user specification and Pune City Connected Location Graph diagram:
PUNE_ROADS_DATA = [
    # North-West / PCMC
    ("Talegaon", "Hinjawadi", 12.0),
    ("Hinjawadi", "Wakad", 5.0),
    ("Hinjawadi", "Baner", 4.0),
    ("Wakad", "Baner", 4.0),
    ("Wakad", "Pimpri", 6.0),
    ("Wakad", "Aundh", 4.0),
    ("Pimpri", "Chinchwad", 4.0),
    ("Pimpri", "Deccan", 6.0),
    ("Chinchwad", "Akurdi", 3.0),
    ("Chinchwad", "Nigdi", 4.0),
    ("Akurdi", "Nigdi", 4.0),
    ("Akurdi", "Alandi", 12.0),
    ("Akurdi", "Yerawada", 5.0),

    # West Pune Connections
    ("Baner", "Balewadi", 4.0),
    ("Balewadi", "Aundh", 5.0),
    ("Baner", "Aundh", 5.0),
    ("Baner", "Pashan", 6.0),
    ("Susgaon", "Baner", 6.0),
    ("Susgaon", "Pirangut", 7.0),
    ("Pirangut", "Lavale", 8.0),
    ("Pashan", "Aundh", 4.0),
    ("Pashan", "Bavdhan", 6.0),
    ("Bavdhan", "Kothrud", 6.0),

    # West to Central Corridors
    ("Aundh", "Shivajinagar", 5.0),
    ("Aundh", "Deccan", 5.0),
    ("Deccan", "Shivajinagar", 3.0),
    ("Deccan", "Kothrud", 7.0),
    ("Deccan", "Swargate", 4.0),
    ("Kothrud", "Erandwane", 5.0),
    ("Kothrud", "Warje", 5.0),
    ("Erandwane", "Swargate", 4.0),

    # Central Core & Railway
    ("Shivajinagar", "Pune Railway Station", 2.0),
    ("Shivajinagar", "Yerawada", 4.0),
    ("Shivajinagar", "Swargate", 4.0),
    ("Shivajinagar", "Magarpatta", 6.0),
    ("Shivajinagar", "Viman Nagar", 6.0),
    ("Pune Railway Station", "Yerawada", 3.0),

    # South Pune
    ("Warje", "Narhe", 7.0),
    ("Narhe", "Katraj", 8.0),
    ("Katraj", "Swargate", 8.0),
    ("Katraj", "Kondhwa", 6.0),
    ("Swargate", "Kondhwa", 6.0),
    ("Swargate", "Wanowrie", 4.0),
    ("Swargate", "Hadapsar", 8.0),
    ("Kondhwa", "Wanowrie", 4.0),
    ("Kondhwa", "NIBM", 6.0),
    ("Kondhwa", "Hadapsar", 6.0),

    # East Pune & Airport Corridors
    ("Yerawada", "Viman Nagar", 4.0),
    ("Viman Nagar", "Lohegaon", 5.0),
    ("Viman Nagar", "Kharadi", 5.0),
    ("Lohegaon", "Kharadi", 5.0),
    ("Kharadi", "Wagholi", 8.0),
    ("Kharadi", "Mundhwa", 4.0),
    ("Magarpatta", "Mundhwa", 3.0),
    ("Magarpatta", "Hadapsar", 5.0),
    ("Mundhwa", "Hadapsar", 5.0)
]


class CityMap:
    """
    Connected graph data structure representing Pune City's road network.
    Nodes are delivery locations with (x, y) coordinates.
    Edges are bidirectional roads with illustrative weights (travel distance/cost).
    Supports dynamic road blocking and neighbor discovery.
    """

    def __init__(self):
        self.locations: Dict[str, Location] = {}
        # Adjacency list: {node_a: {node_b: cost, ...}}
        self.adjacency: Dict[str, Dict[str, float]] = {}
        # Blocked roads stored as normalized sorted tuples (u, v) where u < v
        self.blocked_roads: Set[Tuple[str, str]] = set()

        self._build_pune_graph()

    def _normalize_edge(self, u: str, v: str) -> Tuple[str, str]:
        """Returns edge with alphabetically sorted endpoints for consistency."""
        return (u, v) if u < v else (v, u)

    def add_location(self, name: str, x: float, y: float, region: str, icon: str, description: str):
        """Adds a location node to the graph."""
        self.locations[name] = Location(name, x, y, region, icon, description)
        if name not in self.adjacency:
            self.adjacency[name] = {}

    def add_road(self, u: str, v: str, cost: float):
        """Adds a bidirectional road connection with a travel cost weight."""
        if u not in self.locations or v not in self.locations:
            raise ValueError(f"Locations {u} and/or {v} not registered in map.")

        c = round(float(cost), 2)
        self.adjacency[u][v] = c
        self.adjacency[v][u] = c

    def block_road(self, u: str, v: str):
        """Marks a road as blocked (e.g. traffic gridlock, construction, waterlogging)."""
        edge = self._normalize_edge(u, v)
        self.blocked_roads.add(edge)

    def unblock_road(self, u: str, v: str):
        """Unblocks a road, restoring normal delivery robot transit."""
        edge = self._normalize_edge(u, v)
        self.blocked_roads.discard(edge)

    def is_road_blocked(self, u: str, v: str) -> bool:
        """Checks if the road between u and v is currently blocked."""
        return self._normalize_edge(u, v) in self.blocked_roads

    def reset_blocked_roads(self):
        """Clears all road blockades."""
        self.blocked_roads.clear()

    def get_neighbors(self, node: str) -> List[Tuple[str, float]]:
        """
        Returns accessible adjacent neighbors for a given node:
        [(neighbor_name, edge_cost), ...]
        Blocked roads are strictly excluded.
        """
        if node not in self.adjacency:
            return []

        accessible_neighbors = []
        for neighbor, cost in self.adjacency[node].items():
            if not self.is_road_blocked(node, neighbor):
                accessible_neighbors.append((neighbor, cost))
        return accessible_neighbors

    def get_all_roads(self) -> List[Tuple[str, str, float, bool]]:
        """
        Returns all unique roads in Pune:
        [(node_a, node_b, cost, is_blocked), ...]
        """
        roads = []
        visited_edges = set()

        for u in self.adjacency:
            for v, cost in self.adjacency[u].items():
                edge = self._normalize_edge(u, v)
                if edge not in visited_edges:
                    visited_edges.add(edge)
                    is_blocked = edge in self.blocked_roads
                    roads.append((edge[0], edge[1], cost, is_blocked))

        # Alphabetical sorting for clean UI presentation
        roads.sort(key=lambda r: (r[0], r[1]))
        return roads

    def get_coordinates(self, node: str) -> Tuple[float, float]:
        """Returns the (x, y) coordinates of a location."""
        loc = self.locations[node]
        return (loc.x, loc.y)

    def _build_pune_graph(self):
        """Populates all 36 Pune locations and road connections."""
        for name, x, y, region, icon, desc in PUNE_LOCATIONS_DATA:
            self.add_location(name, x, y, region, icon, desc)

        for u, v, cost in PUNE_ROADS_DATA:
            self.add_road(u, v, cost)


def create_city_map() -> CityMap:
    """Factory function returning a freshly initialized Pune CityMap."""
    return CityMap()
