from collections import deque
from typing import List, Tuple, Set, Optional
import heapq
import heapq


class GridGraph:

    def __init__(self, rows: int, cols: int, obstacles: Set[Tuple[int, int]]):
        
        self.rows = rows
        self.cols = cols
        self.obstacles = obstacles
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


def heuristic(pos: Tuple[int, int], end: Tuple[int, int]) -> int:
    """Манхэттенское расстояние - эвристика для A*"""
    return abs(pos[0] - end[0]) + abs(pos[1] - end[1])


def a_star_shortest_path(grid: GridGraph, 
                         start: Tuple[int, int], 
                         end: Tuple[int, int]) -> Optional[Tuple[List[Tuple[int, int]], int]]:
    """
    A* алгоритм поиска кратчайшего пути.
    Возвращает: (путь, количество посещённых клеток)
    """
    
    if not grid.is_valid(start[0], start[1]) or not grid.is_valid(end[0], end[1]):
        return None, 0
    
    if start == end:
        return [start], 1
    
    open_set = [(0, start)]
    parent = {start: None}
    g_score = {start: 0}  
    visited_count = 0
    visited_set = set()
    
    while open_set:
        current_f, current = heapq.heappop(open_set)
        
        if current in visited_set:
            continue
        
        visited_set.add(current)
        visited_count += 1
        
        if current == end:
            path = []
            node = end
            while node is not None:
                path.append(node)
                node = parent[node]
            return path[::-1], visited_count
        
        for neighbor in grid.get_neighbors(current[0], current[1]):
            new_g = g_score[current] + 1
            
            if neighbor not in g_score or new_g < g_score[neighbor]:
                g_score[neighbor] = new_g
                f_score = new_g + heuristic(neighbor, end)
                parent[neighbor] = current
                heapq.heappush(open_set, (f_score, neighbor))
    
    return None, visited_count

def heuristic(pos: Tuple[int, int], end: Tuple[int, int]) -> int:
    """Манхэттенское расстояние"""
    return abs(pos[0] - end[0]) + abs(pos[1] - end[1])


def a_star_shortest_path(grid: GridGraph, 
                         start: Tuple[int, int], 
                         end: Tuple[int, int]) -> Optional[Tuple[List[Tuple[int, int]], int]]:
    """
    A* алгоритм поиска кратчайшего пути.
    Возвращает: (путь, количество посещённых клеток)
    """
    
    if not grid.is_valid(start[0], start[1]) or not grid.is_valid(end[0], end[1]):
        return None, 0
    
    if start == end:
        return [start], 1
    
    open_set = [(0, start)]
    parent = {start: None}
    g_score = {start: 0} 
    visited_count = 0
    
    while open_set:
        current_f, current = heapq.heappop(open_set)
        visited_count += 1
        
        if current == end:
            path = []
            node = end
            while node is not None:
                path.append(node)
                node = parent[node]
            return path[::-1], visited_count
        
        for neighbor in grid.get_neighbors(current[0], current[1]):
            new_g = g_score[current] + 1
            
            if neighbor not in g_score or new_g < g_score[neighbor]:
                g_score[neighbor] = new_g
                f_score = new_g + heuristic(neighbor, end)
                parent[neighbor] = current
                heapq.heappush(open_set, (f_score, neighbor))
    
    return None, visited_count
