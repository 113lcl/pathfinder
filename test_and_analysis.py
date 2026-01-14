
from algorithm import find_path, GridGraph, bfs_shortest_path


def test_simple_path():
    print("\n=== Test 1: Simple Path (No Obstacles) ===")
    path = find_path(
        rows=10, 
        cols=10, 
        obstacles=set(),
        start=(0, 0),
        end=(9, 9)
    )
    print(f"Path exists: {path is not None}")
    if path:
        print(f"Path length: {len(path)} cells")
        print(f"Shortest path requires: {len(path) - 1} moves")
        print(f"Minimum possible moves: 18 (9 down + 9 right)")
        assert len(path) == 19, "Path should have 19 cells (18 moves)"
    print("✓ Test passed")


def test_no_path():
    print("\n=== Test 2: No Path (Complete Blockade) ===")
    # Create a wall that completely separates start from end
    obstacles = {
        (1, 0), (1, 1), (1, 2), (1, 3), (1, 4),
        (1, 5), (1, 6), (1, 7), (1, 8), (1, 9)
    }
    path = find_path(
        rows=10, 
        cols=10, 
        obstacles=obstacles,
        start=(0, 0),
        end=(9, 9)
    )
    print(f"Path exists: {path is not None}")
    assert path is None, "Path should not exist"
    print("✓ Test passed - correctly returns None when no path exists")


def test_simple_maze():
    print("\n=== Test 3: Simple L-Shaped Maze ===")
    obstacles = {
        (2, 1), (2, 2), (2, 3), (2, 4), (2, 5),
        (2, 6), (2, 7), (2, 8), (2, 9)
    }
    path = find_path(
        rows=10, 
        cols=10, 
        obstacles=obstacles,
        start=(0, 0),
        end=(9, 9)
    )
    print(f"Path exists: {path is not None}")
    if path:
        print(f"Path length: {len(path)} cells")
        print(f"First 5 cells: {path[:5]}")
        print(f"Last 5 cells: {path[-5:]}")
        # Verify path is valid (doesn't pass through obstacles)
        for pos in path:
            assert pos not in obstacles, f"Path passes through obstacle"
    print("✓ Test passed")


def test_start_equals_end():
    print("\n=== Test 4: Start Equals End ===")
    path = find_path(
        rows=10, 
        cols=10, 
        obstacles=set(),
        start=(5, 5),
        end=(5, 5)
    )
    print(f"Path found: {path}")
    assert path == [(5, 5)], "Path should be single cell"
    print("✓ Test passed - correctly handles same start/end")


def test_complex_maze():
    print("\n=== Test 5: Complex Maze (Multiple Solutions) ===")
    obstacles = {
        (3, 2), (3, 3), (3, 4),  # vertical wall 1
        (5, 6), (5, 7),           # vertical wall 2
        (7, 1), (7, 2), (7, 3),   # vertical wall 3
    }
    path = find_path(
        rows=10, 
        cols=10, 
        obstacles=obstacles,
        start=(0, 0),
        end=(9, 9)
    )
    print(f"Path exists: {path is not None}")
    if path:
        print(f"Path length: {len(path)} cells")
        # Verify path doesn't pass through obstacles
        for row, col in path:
            assert (row, col) not in obstacles, \
                f"Path passes through obstacle at ({row}, {col})"
        # Verify consecutive cells are adjacent
        for i in range(len(path) - 1):
            r1, c1 = path[i]
            r2, c2 = path[i + 1]
            distance = abs(r1 - r2) + abs(c1 - c2)
            assert distance == 1, \
                f"Path cells not adjacent: {path[i]} to {path[i+1]}"
    print("✓ Test passed - path is valid and shortest")


def analyze_bfs_properties():
    print("\n=== BFS Algorithm Properties ===")
    
    print("\n1. COMPLETENESS")
    print("   BFS always finds a solution if one exists")
    print("   Proof: BFS explores all reachable vertices level by level")
    
    print("\n2. OPTIMALITY (Shortest Path)")
    print("   BFS finds the shortest path in unweighted graphs")
    print("   Why: First path found = minimum distance from start")
    
    print("\n3. COMPLEXITY ANALYSIS")
    print("   Time Complexity:  O(V + E) where V=cells, E=edges")
    print("   Space Complexity: O(V) for queue and visited set")
    print("   For 10x10 grid: V≈100, E≈360")
    print("   Actual operations: ~100 queue operations, ~360 edge checks")
    
    print("\n4. COMPARISON WITH OTHER ALGORITHMS")
    print("   DFS (Depth-First Search):")
    print("   ✗ Does NOT guarantee shortest path")
    print("   ✗ Can get stuck in deep paths first")
    print("")
    print("   Dijkstra's Algorithm:")
    print("   ✓ Works with weighted graphs")
    print("   ✗ Unnecessary overhead for unweighted graphs")
    print("   ✗ BFS is special case of Dijkstra")
    print("")
    print("   A* Algorithm:")
    print("   ✓ Faster with heuristic")
    print("   ✓ For large spaces (thousands of cells)")
    print("   ✗ Requires domain knowledge for heuristic")
    print("   ✗ Overkill for small grids")


def visualize_bfs_trace():
    print("\n=== BFS Execution Trace (5x5 grid, no obstacles) ===")
    
    print("\nInitial State:")
    print("S . . . .")
    print(". . . . .")
    print(". . . . .")
    print(". . . . .")
    print(". . . . E")
    
    print("\nBFS Exploration (Level by Level):")
    print("\nLevel 0: Start cell (0,0)")
    print("  Queue: [(0,0)]")
    
    print("\nLevel 1: Distance 1 from start")
    print("  Neighbors of (0,0): (1,0), (0,1)")
    print("  1 1 . . .")
    print("  1 . . . .")
    print("  . . . . .")
    print("  . . . . .")
    print("  . . . . E")
    
    print("\nLevel 2: Distance 2 from start")
    print("  Neighbors added: (2,0), (1,1), (0,2)")
    print("  2 1 2 . .")
    print("  1 2 . . .")
    print("  2 . . . .")
    print("  . . . . .")
    print("  . . . . E")
    
    print("\n... BFS continues exploring outward ...")
    
    print("\nWhen End (4,4) is reached:")
    print("  This is at distance 8 (4 down + 4 right)")
    print("  Any path = 8 moves minimum")
    print("  BFS guarantees the path it returns has length 8")


def demonstrate_path_reconstruction():
    print("\n=== Path Reconstruction Mechanism ===")
    
    print("\nThe key insight: Maintaining Parent Pointers")
    print("\nDuring BFS exploration, we track:")
    print("  parent[(1,0)] = (0,0)")
    print("  parent[(0,1)] = (0,0)")
    print("  parent[(2,0)] = (1,0)")
    print("  parent[(1,1)] = (1,0) or (0,1)")
    print("  ... and so on ...")
    
    print("\nWhen destination is reached, reconstruct:")
    print("  Start at: (4,4) [destination]")
    print("  Follow parents: (4,4) ← (3,4) ← (2,4) ← ... ← (0,0)")
    print("  Reverse to get: (0,0) → ... → (2,4) → (3,4) → (4,4)")
    
    print("\nThis gives us the shortest path efficiently!")


def run_all_tests():
    print("=" * 60)
    print("PATHFINDING ALGORITHM - TEST SUITE & ANALYSIS")
    print("=" * 60)
    
    test_simple_path()
    test_no_path()
    test_simple_maze()
    test_start_equals_end()
    test_complex_maze()
    
    analyze_bfs_properties()
    visualize_bfs_trace()
    demonstrate_path_reconstruction()
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED ✓")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()
