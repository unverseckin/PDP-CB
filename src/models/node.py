from dataclasses import dataclass

from src.models.location import Location


@dataclass
class Node:
    id: int = None
    location: Location = None
    demand: int = 0
    node_type: str = None
    polar_angle: float = 0
