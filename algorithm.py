from collections import deque
from typing import List, Tuple, Set, Optional


class GridGraph:

    def __init__(self, rows: int, cols: int, obstacles: Set[Tuple[int, int]]):
        
        self.rows = rows
        self.cols = cols
        self.obstacles = obstacles
        # Allowed movements: up, down, left, right
        self.directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    def is_valid(self, row: int, col: int) -> bool:
        
        return (0 <= row < self.rows and 
                0 <= col < self.cols and 
                (row, col) not in self.obstacles)
    
    def get_neighbors(self, row: int, col: int) -> List[Tuple[int, int]]:
        
        neighbors = []
        for dr, dc in self.directions:
            new_row, new_col = row + dr, col + dc
            if self.is_valid(new_row, new_col):
                neighbors.append((new_row, new_col))
        return neighbors


def bfs_shortest_path(grid: GridGraph, 
                      start: Tuple[int, int], 
                      end: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
    
    
    if not grid.is_valid(start[0], start[1]) or not grid.is_valid(end[0], end[1]):
        return None
    
    if start == end:
        return [start]
    
    queue = deque([start]) 
    visited = {start} 
    parent = {start: None}
    
    while queue:
        current = queue.popleft()
        
        if current == end:
            
            path = []
            node = end
            while node is not None:
                path.append(node)
                node = parent[node]
            return path[::-1] 
        
        for neighbor in grid.get_neighbors(current[0], current[1]):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)
    
    return None


def find_path(rows: int, 
              cols: int, 
              obstacles: Set[Tuple[int, int]], 
              start: Tuple[int, int], 
              end: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:

    graph = GridGraph(rows, cols, obstacles)
    return bfs_shortest_path(graph, start, end)
