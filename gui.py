
import tkinter as tk
from tkinter import messagebox
from typing import Set, Tuple, Optional, List
import time
import random

from algorithm import find_path, a_star_shortest_path, GridGraph


class PathfindingGUI:
    
    COLOR_EMPTY = "white"
    COLOR_OBSTACLE = "black"
    COLOR_START = "green"
    COLOR_END = "red"
    COLOR_PATH = "blue"
    COLOR_VISITED = "lightblue"
    
    EMPTY = 0
    OBSTACLE = 1
    START = 2
    END = 3
    PATH = 4
    VISITED = 5
    
    def calculate_cell_size(self, grid_size):
        if grid_size <= 10:
            return 50
        elif grid_size <= 15:
            return 40
        elif grid_size <= 20:
            return 35
        else:
            return 30
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Pathfinding Application - BFS Algorithm")
        self.root.resizable(False, False)
        
        self.GRID_SIZE = 10
        self.CELL_SIZE = self.calculate_cell_size(self.GRID_SIZE)
        
        self.grid_state = [[self.EMPTY for _ in range(self.GRID_SIZE)] 
                          for _ in range(self.GRID_SIZE)]
        
        self.start_pos = (0, 0)
        self.end_pos = (self.GRID_SIZE - 1, self.GRID_SIZE - 1)
        self.grid_state[0][0] = self.START
        self.grid_state[self.GRID_SIZE - 1][self.GRID_SIZE - 1] = self.END
        
        self.obstacles: Set[Tuple[int, int]] = set()
        
        self.current_path: Optional[List[Tuple[int, int]]] = None
        self.path_index = 0
        
        self.canvas = tk.Canvas(root, 
                               width=self.GRID_SIZE * self.CELL_SIZE,
                               height=self.GRID_SIZE * self.CELL_SIZE,
                               bg=self.COLOR_EMPTY,
                               cursor="cross")
        self.canvas.pack(pady=10)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Button-3>", self.on_canvas_right_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<B3-Motion>", self.on_canvas_right_drag)
        
        control_frame = tk.Frame(root)
        control_frame.pack(pady=10)
        
        self.status_label = tk.Label(root, 
                                    text="LPM - dodać, PPM - usunąć, Przeciągnij - rysować (Start/End nie można zmieniać)",
                                    fg="blue",
                                    font=("Arial", 10))
        self.status_label.pack()
        
        button_frame = tk.Frame(control_frame)
        button_frame.pack()
        
        size_frame = tk.Frame(control_frame)
        size_frame.pack(pady=5)
        
        tk.Label(size_frame, text="Rozmiar siatki:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        
        self.size_var = tk.StringVar(value="10x10")
        size_options = ["10x10", "15x15", "20x20", "25x25"]
        self.size_menu = tk.OptionMenu(size_frame, self.size_var, *size_options, command=self.change_grid_size)
        self.size_menu.config(font=("Arial", 9))
        self.size_menu.pack(side=tk.LEFT, padx=5)
        
        self.start_button = tk.Button(button_frame,
                                     text="Rozpocznij wyszukiwanie",
                                     command=self.find_path,
                                     bg="green",
                                     fg="white",
                                     font=("Arial", 11, "bold"),
                                     width=20)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.clear_button = tk.Button(button_frame,
                                     text="Wyczyść siatkę",
                                     command=self.clear_grid,
                                     bg="orange",
                                     fg="white",
                                     font=("Arial", 11, "bold"),
                                     width=15)
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        self.random_button = tk.Button(button_frame,
                                      text="Losowe przeszkody",
                                      command=self.generate_random_obstacles,
                                      bg="purple",
                                      fg="white",
                                      font=("Arial", 11, "bold"),
                                      width=15)
        self.random_button.pack(side=tk.LEFT, padx=5)
        
        self.info_label = tk.Label(root,
                                  text="BFS: Przeszukiwanie wszerz - eksploruje wszystkie kierunki równomiernie",
                                  font=("Arial", 9),
                                  fg="gray")
        self.info_label.pack()
        
        self.astar_info_label = tk.Label(root,
                                        text="A*: Używa heurystyki (odległość Manhattan) aby znaleźć ścieżkę szybciej",
                                        font=("Arial", 9),
                                        fg="gray")
        self.astar_info_label.pack()
        
        self.comparison_frame = tk.Frame(root)
        self.comparison_frame.pack(pady=10)
        
        self.bfs_label = tk.Label(self.comparison_frame,
                                 text="BFS: - | Odwiedzone: - | Czas: -ms",
                                 font=("Arial", 9),
                                 fg="green")
        self.bfs_label.pack()
        
        self.astar_label = tk.Label(self.comparison_frame,
                                   text="A*: - | Odwiedzone: - | Czas: -ms",
                                   font=("Arial", 9),
                                   fg="blue")
        self.astar_label.pack()
        
        self.draw_grid()
    
    def draw_grid(self):
        
        self.canvas.delete("all")
        
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                x1 = col * self.CELL_SIZE
                y1 = row * self.CELL_SIZE
                x2 = x1 + self.CELL_SIZE
                y2 = y1 + self.CELL_SIZE
                
                cell_type = self.grid_state[row][col]
                if cell_type == self.START:
                    color = self.COLOR_START
                elif cell_type == self.END:
                    color = self.COLOR_END
                elif cell_type == self.OBSTACLE:
                    color = self.COLOR_OBSTACLE
                elif cell_type == self.PATH:
                    color = self.COLOR_PATH
                elif cell_type == self.VISITED:
                    color = self.COLOR_VISITED
                else:
                    color = self.COLOR_EMPTY
                
                # Draw rectangle
                self.canvas.create_rectangle(x1, y1, x2, y2,
                                            fill=color,
                                            outline="gray",
                                            width=1)
    
    def on_canvas_click(self, event):
        col = event.x // self.CELL_SIZE
        row = event.y // self.CELL_SIZE
        
        if not (0 <= row < self.GRID_SIZE and 0 <= col < self.GRID_SIZE):
            return
        
        if (row, col) == self.start_pos or (row, col) == self.end_pos:
            messagebox.showwarning("Nie można zmodyfikować",
                                 "Komórek startowych i końcowych nie można modyfikować!")
            return
        if (row, col) not in self.obstacles:
            self.obstacles.add((row, col))
            self.grid_state[row][col] = self.OBSTACLE
        
        self.current_path = None
        self.path_index = 0
        
        self.draw_grid()
    
    def on_canvas_right_click(self, event):
        col = event.x // self.CELL_SIZE
        row = event.y // self.CELL_SIZE
        
        if not (0 <= row < self.GRID_SIZE and 0 <= col < self.GRID_SIZE):
            return
        
        if (row, col) == self.start_pos or (row, col) == self.end_pos:
            return
        if (row, col) in self.obstacles:
            self.obstacles.remove((row, col))
            self.grid_state[row][col] = self.EMPTY
        self.current_path = None
        self.path_index = 0
        self.draw_grid()
    
    def on_canvas_drag(self, event):
        col = event.x // self.CELL_SIZE
        row = event.y // self.CELL_SIZE
        
        if not (0 <= row < self.GRID_SIZE and 0 <= col < self.GRID_SIZE):
            return
        
        if (row, col) == self.start_pos or (row, col) == self.end_pos:
            return
        if (row, col) not in self.obstacles:
            self.obstacles.add((row, col))
            self.grid_state[row][col] = self.OBSTACLE
            self.current_path = None
            self.path_index = 0
            self.draw_grid()
    
    def on_canvas_right_drag(self, event):
        col = event.x // self.CELL_SIZE
        row = event.y // self.CELL_SIZE
        
        if not (0 <= row < self.GRID_SIZE and 0 <= col < self.GRID_SIZE):
            return
        
        if (row, col) == self.start_pos or (row, col) == self.end_pos:
            return
        if (row, col) in self.obstacles:
            self.obstacles.remove((row, col))
            self.grid_state[row][col] = self.EMPTY
            self.current_path = None
            self.path_index = 0
            self.draw_grid()
    
    def find_path(self):
        self.reset_visualization()
        start_time_bfs = time.perf_counter()
        path_bfs = find_path(self.GRID_SIZE, self.GRID_SIZE, 
                            self.obstacles, self.start_pos, self.end_pos)
        time_bfs = (time.perf_counter() - start_time_bfs) * 1000
        graph = GridGraph(self.GRID_SIZE, self.GRID_SIZE, self.obstacles)
        start_time_astar = time.perf_counter()
        path_astar, visited_astar = a_star_shortest_path(graph, self.start_pos, self.end_pos)
        time_astar = (time.perf_counter() - start_time_astar) * 1000
        visited_bfs = len(self.get_bfs_visited_count())
        
        if path_bfs is None or path_astar is None:
            self.status_label.config(text="❌ Nie znaleziono ścieżki! Przeszkody blokują wszystkie trasy.",
                                    fg="red")
            messagebox.showwarning("Brak ścieżki",
                                 "Nie istnieje ścieżka od początku do końca.\n"
                                 "Przeszkody całkowicie blokują wszystkie trasy.")
            self.bfs_label.config(text=f"BFS: Brak ścieżki | Czas: {time_bfs:.2f}ms")
            self.astar_label.config(text=f"A*: Brak ścieżki | Czas: {time_astar:.2f}ms")
        else:
            self.current_path = path_bfs
            self.path_index = 0
            path_len = len(path_bfs)
            self.status_label.config(text=f"✓ Znaleziono ścieżkę! Długość: {path_len} komórek",
                                    fg="green")
            self.bfs_label.config(
                text=f"BFS: {path_len} komórek | Odwiedzone: ~{visited_bfs} | Czas: {time_bfs:.2f}ms",
                fg="green"
            )
            self.astar_label.config(
                text=f"A*: {path_len} komórek | Odwiedzone: {visited_astar} | Czas: {time_astar:.2f}ms",
                fg="blue"
            )
            self.visualize_path(path_bfs)
    
    def get_bfs_visited_count(self):
        visited = set()
        from collections import deque
        queue = deque([self.start_pos])
        visited.add(self.start_pos)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        while queue:
            row, col = queue.popleft()
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                if (0 <= new_row < self.GRID_SIZE and 
                    0 <= new_col < self.GRID_SIZE and
                    (new_row, new_col) not in visited and
                    (new_row, new_col) not in self.obstacles):
                    visited.add((new_row, new_col))
                    queue.append((new_row, new_col))
        
        return visited
    
    def visualize_path(self, path):
        for row, col in path:
            if (row, col) != self.start_pos and (row, col) != self.end_pos:
                self.grid_state[row][col] = self.PATH
        self.draw_grid()
    
    def animate_path(self):
        if self.current_path is None or self.path_index >= len(self.current_path):
            return
        
        row, col = self.current_path[self.path_index]
        
        if (row, col) != self.start_pos and (row, col) != self.end_pos:
            self.grid_state[row][col] = self.PATH
        
        self.draw_grid()
        self.path_index += 1
        
        self.root.after(100, self.animate_path)
    
    def reset_visualization(self):
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                if self.grid_state[row][col] == self.PATH or \
                   self.grid_state[row][col] == self.VISITED:
                    if (row, col) not in self.obstacles:
                        self.grid_state[row][col] = self.EMPTY
        self.draw_grid()
    
    def clear_grid(self):
        self.obstacles.clear()
        self.current_path = None
        self.path_index = 0
        self.grid_state = [[self.EMPTY for _ in range(self.GRID_SIZE)] 
                          for _ in range(self.GRID_SIZE)]
        self.grid_state[0][0] = self.START
        self.grid_state[self.GRID_SIZE - 1][self.GRID_SIZE - 1] = self.END
        
        self.status_label.config(text="Siatka wyczyszczona. Gotowa do umieszczania nowych przeszkód.",
                                fg="blue")
        self.draw_grid()
    
    def generate_random_obstacles(self):
        self.obstacles.clear()
        self.current_path = None
        self.path_index = 0
        
        self.grid_state = [[self.EMPTY for _ in range(self.GRID_SIZE)] 
                          for _ in range(self.GRID_SIZE)]
        self.grid_state[0][0] = self.START
        self.grid_state[self.GRID_SIZE - 1][self.GRID_SIZE - 1] = self.END
        
        start_neighbors = self.get_cell_neighbors(self.start_pos[0], self.start_pos[1])
        end_neighbors = self.get_cell_neighbors(self.end_pos[0], self.end_pos[1])
        
        total_cells = self.GRID_SIZE * self.GRID_SIZE
        obstacle_count = random.randint(int(total_cells * 0.15), int(total_cells * 0.25))
        
        added = 0
        max_attempts = obstacle_count * 10
        attempts = 0
        
        while added < obstacle_count and attempts < max_attempts:
            row = random.randint(0, self.GRID_SIZE - 1)
            col = random.randint(0, self.GRID_SIZE - 1)
            attempts += 1
            
            if (row, col) == self.start_pos or (row, col) == self.end_pos:
                continue
            if (row, col) in self.obstacles:
                continue
            
            self.obstacles.add((row, col))
            
            free_start_neighbors = [n for n in start_neighbors if n not in self.obstacles]
            free_end_neighbors = [n for n in end_neighbors if n not in self.obstacles]
            
            if len(free_start_neighbors) == 0 or len(free_end_neighbors) == 0:
                self.obstacles.remove((row, col))
                continue
            
            self.grid_state[row][col] = self.OBSTACLE
            added += 1
        
        self.status_label.config(text=f"Wygenerowano {added} losowych przeszkód!",
                                fg="purple")
        self.draw_grid()
    
    def get_cell_neighbors(self, row, col):
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < self.GRID_SIZE and 0 <= new_col < self.GRID_SIZE:
                neighbors.append((new_row, new_col))
        return neighbors
    
    def change_grid_size(self, selection):
        size = int(selection.split('x')[0])
        self.GRID_SIZE = size
        self.CELL_SIZE = self.calculate_cell_size(size)
        
        new_canvas_size = self.GRID_SIZE * self.CELL_SIZE
        self.canvas.config(width=new_canvas_size, height=new_canvas_size)
        
        self.obstacles.clear()
        self.current_path = None
        self.path_index = 0
        
        self.grid_state = [[self.EMPTY for _ in range(self.GRID_SIZE)] 
                          for _ in range(self.GRID_SIZE)]
        
        self.start_pos = (0, 0)
        self.end_pos = (self.GRID_SIZE - 1, self.GRID_SIZE - 1)
        self.grid_state[0][0] = self.START
        self.grid_state[self.GRID_SIZE - 1][self.GRID_SIZE - 1] = self.END
        
        self.status_label.config(text=f"Rozmiar siatki zmieniony na {size}x{size}",
                                fg="blue")
        self.draw_grid()


def run_application():
    root = tk.Tk()
    app = PathfindingGUI(root)
    root.mainloop()


if __name__ == "__main__":
    run_application()
