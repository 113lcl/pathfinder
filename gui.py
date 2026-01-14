
import tkinter as tk
from tkinter import messagebox
from typing import Set, Tuple, Optional, List
import time

from algorithm import find_path


class PathfindingGUI:
 
    GRID_SIZE = 10 
    CELL_SIZE = 50
    
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
    
    def __init__(self, root: tk.Tk):
        
        self.root = root
        self.root.title("Pathfinding Application - BFS Algorithm")
        self.root.geometry("800x700")
        self.root.resizable(False, False)
        
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
        
        control_frame = tk.Frame(root)
        control_frame.pack(pady=10)
        
        self.status_label = tk.Label(root, 
                                    text="Click cells to place obstacles (cannot modify start/end cells)",
                                    fg="blue",
                                    font=("Arial", 10))
        self.status_label.pack()
        
        button_frame = tk.Frame(control_frame)
        button_frame.pack()
        
        self.start_button = tk.Button(button_frame,
                                     text="Start Pathfinding",
                                     command=self.find_path,
                                     bg="green",
                                     fg="white",
                                     font=("Arial", 11, "bold"),
                                     width=15)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.clear_button = tk.Button(button_frame,
                                     text="Clear Grid",
                                     command=self.clear_grid,
                                     bg="orange",
                                     fg="white",
                                     font=("Arial", 11, "bold"),
                                     width=15)
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        self.info_label = tk.Label(root,
                                  text="BFS Algorithm: Finds shortest path in unweighted grid",
                                  font=("Arial", 9),
                                  fg="gray")
        self.info_label.pack()
        
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
            messagebox.showwarning("Cannot Modify",
                                 "Start and end cells cannot be modified!")
            return
        
        if (row, col) in self.obstacles:
            self.obstacles.remove((row, col))
            self.grid_state[row][col] = self.EMPTY
        else:
            self.obstacles.add((row, col))
            self.grid_state[row][col] = self.OBSTACLE
        
        self.current_path = None
        self.path_index = 0
        
        self.draw_grid()
    
    def find_path(self):
        
        self.reset_visualization()
        
        path = find_path(self.GRID_SIZE, self.GRID_SIZE, 
                        self.obstacles, self.start_pos, self.end_pos)
        
        if path is None:
            self.status_label.config(text="❌ No path found! Obstacles block all routes.",
                                    fg="red")
            messagebox.showwarning("No Path",
                                 "No path exists from start to finish.\n"
                                 "The obstacles completely block all routes.")
        else:
            self.current_path = path
            self.path_index = 0
            self.status_label.config(text=f"✓ Path found! Length: {len(path)} cells",
                                    fg="green")
            self.animate_path()
    
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
        
        # Reset grid state
        self.grid_state = [[self.EMPTY for _ in range(self.GRID_SIZE)] 
                          for _ in range(self.GRID_SIZE)]
        self.grid_state[0][0] = self.START
        self.grid_state[self.GRID_SIZE - 1][self.GRID_SIZE - 1] = self.END
        
        self.status_label.config(text="Grid cleared. Ready to place new obstacles.",
                                fg="blue")
        self.draw_grid()


def run_application():
    root = tk.Tk()
    app = PathfindingGUI(root)
    root.mainloop()


if __name__ == "__main__":
    run_application()
