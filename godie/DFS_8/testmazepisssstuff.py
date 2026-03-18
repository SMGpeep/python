import dfs_human
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
import time
import random
from typing import List, Tuple, Set, Dict

def print_maze(
    maze: List[List[str]], 
    start: Tuple[int, int], 
    end: Tuple[int, int]
) -> None:
    """
    Display the maze using matplotlib with special colors for path, start, end, and dead-ends.
    
    Args:
        maze: 2D list representing the maze structure.
        start: Tuple of start coordinates (row, col).
        end: Tuple of end coordinates (row, col).
    """
    # Map each maze symbol to a color index.
    color_map: Dict[str, int] = {'#': 0, ' ': 1, '.': 2, 'S': 3, 'E': 4, 'X': 5}
    maze_copy = [row[:] for row in maze]  # Deep copy for display
    maze_copy[start[0]][start[1]] = 'S'
    maze_copy[end[0]][end[1]] = 'E'
    # Convert to numerical array for imshow
    maze_color = np.array([[color_map.get(cell, 1) for cell in row] for row in maze_copy])
    # Create a custom color map: wall, free, path, start, end, dead-end
    cmap = ListedColormap(['black', 'white', 'lime', 'blue', 'red', 'gray'])

    plt.clf()
    plt.imshow(maze_color, cmap=cmap, interpolation='nearest')
    plt.xticks([]), plt.yticks([])
    plt.draw()
    plt.pause(0.05)

def dfs_with_visualization(
    maze: List[List[str]],
    x: int,
    y: int,
    end_x: int,
    end_y: int,
    path: List[Tuple[int, int]],
    visited: Set[Tuple[int, int]],  # Unused, kept for signature compatibility
    start: Tuple[int, int],
    end: Tuple[int, int]
) -> bool:
    """
    Perform DFS in the maze, animating each step, by patching/animating in sync with the imported DFS.
    """
    # We want to animate the actual dfs, not reimplement it!
    # So: we wrap the dfs_human.dfs to show the maze on every path extension / pop.

    original_append = path.append
    original_pop = path.pop

    def animated_append(item):
        original_append(item)
        print_maze(maze, start, end)
        time.sleep(0.02)

    def animated_pop():
        original_pop()
        print_maze(maze, start, end)
        time.sleep(0.01)

    # Patch path modifications for animation by wrapping the list
    class AnimatedPath(list):
        def append(self, item):
            super().append(item)
            print_maze(maze, start, end)
            time.sleep(0.02)
        def pop(self, *args, **kwargs):
            result = super().pop(*args, **kwargs)
            print_maze(maze, start, end)
            time.sleep(0.01)
            return result

    # Replace path reference with AnimatedPath during DFS
    path_wrapper = AnimatedPath(path)
    result = dfs_human.dfs(maze, x, y, end_x, end_y, path_wrapper)
    path.clear()
    path.extend(path_wrapper)
    return result

def generate_large_open_maze(
    rows: int, 
    cols: int
) -> List[List[str]]:
    """
    Generate a large open maze with all free spaces, surrounded by walls.

    Args:
        rows: Number of rows in the maze.
        cols: Number of columns in the maze.

    Returns:
        2D list representing the maze.
    """
    maze = [[' ' for _ in range(cols)] for _ in range(rows)]
    # Add walls to borders
    for i in range(rows):
        maze[i][0] = '#'
        maze[i][-1] = '#'
    for j in range(cols):
        maze[0][j] = '#'
        maze[-1][j] = '#'
    return maze

def generate_dense_random_maze(
    rows: int, 
    cols: int, 
    wall_prob: float = 0.4
) -> List[List[str]]:
    """
    Generate a randomly filled dense maze.

    Args:
        rows: Number of rows.
        cols: Number of columns.
        wall_prob: Probability for each cell (not border) to be a wall.

    Returns:
        2D list representing the maze.
    """
    maze: List[List[str]] = []
    for i in range(rows):
        row: List[str] = []
        for j in range(cols):
            # Borders are always walls
            if i == 0 or i == rows-1 or j == 0 or j == cols-1:
                row.append('#')
            else:
                row.append('#' if random.random() < wall_prob else ' ')
        maze.append(row)
    return maze

def stress_test_large_open_maze() -> None:
    """
    Stress Test: Visualize solving a very large open maze.
    """
    print("Stress Test: Large Open Maze")
    rows, cols = 100, 120
    maze = generate_large_open_maze(rows, cols)
    start = (1, 1)
    end = (rows-2, cols-2)
    path: List[Tuple[int, int]] = []
    visited: Set[Tuple[int, int]] = set()
    plt.ion()
    fig = plt.figure(figsize=(8, 6))
    found = dfs_with_visualization(maze, start[0], start[1], end[0], end[1], path, visited, start, end)
    plt.ioff()
    plt.show()
    print("Weg gefunden." if found else "Kein Weg gefunden.")

def stress_test_dense_random_maze() -> None:
    """
    Stress Test: Visualize solving a randomly generated dense maze. May not always be solvable.
    """
    print("Stress Test: Dense Random Maze")
    rows, cols = 40, 60
    maze = generate_dense_random_maze(rows, cols, wall_prob=0.45)
    start = (1, 1)
    end = (rows-2, cols-2)
    # Ensure start and end are open
    maze[start[0]][start[1]] = ' '
    maze[end[0]][end[1]] = ' '
    path: List[Tuple[int, int]] = []
    visited: Set[Tuple[int, int]] = set()
    plt.ion()
    fig = plt.figure(figsize=(8, 6))
    found = dfs_with_visualization(maze, start[0], start[1], end[0], end[1], path, visited, start, end)
    plt.ioff()
    plt.show()
    print("Weg gefunden." if found else "Kein Weg gefunden.")

def example_test() -> None:
    """
    Run classic example test cases on small mazes and visualize pathfinding.
    """
    maze_source: List[str] = [
        "######################",
        "#       #           ##",
        "# #### # ##### ##### #",
        "#    # #     #     # #",
        "# # ## # ### ##### # #",
        "# # ## #     #     # #",
        "# # ## ##### ####### #",
        "# #           #      #",
        "####### ########## ###",
        "#                   ##",
        "######################"
    ]

    starts_ends: List[Tuple[Tuple[int, int], Tuple[int, int]]] = [
        ((1, 15), (9, 17)), 
        ((1, 2), (9, 17))
    ]

    plt.ion()
    fig = plt.figure(figsize=(10, 5))

    for start, end in starts_ends:
        # Convert string to list of character cells
        maze = [list(row) for row in maze_source]
        path: List[Tuple[int, int]] = []
        visited: Set[Tuple[int, int]] = set()
        found = dfs_with_visualization(
            maze, start[0], start[1],
            end[0], end[1], path, visited, start, end
        )
        if found:
            print("Weg gefunden von", start, "nach", end)
        else:
            print("Kein Weg gefunden von", start, "nach", end)
        plt.pause(1)

    plt.ioff()
    plt.show()


def test_multiple_large_mazes(
    runs: int = 5,
    rows: int = 60,
    cols: int = 100,
    wall_prob: float = 0.4,
    visualize: bool = True,
    max_attempts_per_run: int = 30  # Prevents infinite loops if not enough solvable mazes
) -> None:
    """
    Generate and attempt to solve several large random mazes with randomized start/end points.
    Ensures only solvable mazes are included (unsolvable mazes are retried).
    """
    print(f"Testing {runs} randomly generated *solvable* large mazes ({rows}x{cols}), wall_prob={wall_prob}...")
    plt.ion()
    fig = plt.figure(figsize=(10, 6))
    successes = 0
    attempts = 0

    for run_idx in range(1, runs + 1):
        found = False
        for attempt in range(max_attempts_per_run):
            maze = generate_dense_random_maze(rows, cols, wall_prob=wall_prob)

            open_cells = [
                (i, j)
                for i in range(1, rows-1)
                for j in range(1, cols-1)
                if maze[i][j] == ' '
            ]
            if len(open_cells) < 2:
                continue  # Try new maze if not enough open space

            start, end = random.sample(open_cells, 2)
            maze[start[0]][start[1]] = ' '
            maze[end[0]][end[1]] = ' '
            path: List[Tuple[int, int]] = []
            visited: Set[Tuple[int, int]] = set()
 
            # Do not show failed visualizations during retries
            if visualize:
                plt.clf()
            found = dfs_human.dfs(
                [row[:] for row in maze],  # Make a copy to avoid side-effect
                start[0], start[1], end[0], end[1], []
            )
            attempts += 1
            if found:
                # Actually visualize (or run) the successful one, 
                # using the real maze (with the side-effects as intended)
                path = []
                visited = set()
                if visualize:
                    plt.clf()
                    found_vis = dfs_with_visualization(
                        maze, start[0], start[1], end[0], end[1], path, visited, start, end
                    )
                else:
                    found_vis = dfs_human.dfs(
                        maze, start[0], start[1], end[0], end[1], path
                    )
                print(f"\nRun {run_idx} | Start: {start}  End: {end}")
                if found_vis:
                    print(f"[SUCCESS] Path found ({len(path)} steps).")
                    successes += 1
                else:
                    print(f"[ERROR] Unexpected: DFS failed to find path on a previously-verified solvable maze!")
                if visualize:
                    plt.pause(1.0)
                break  # Only count successful, solvable maze for the run
        else:
            print(f"Run {run_idx}: Could not generate solvable maze after {max_attempts_per_run} attempts.")

    if visualize:
        plt.ioff()
        plt.show()
    print(f"\nRuns attempted: {run_idx} | Successful solves: {successes}")

if __name__ == '__main__':
    # The following tests can be commented/uncommented as desired to execute:
    #example_test()              # Typical maze run
    #stress_test_large_open_maze()   # Large open maze (uncomment to try, will be slow)
    #stress_test_dense_random_maze() # Dense maze (uncomment to try, can be slow or unsolvable)
    # Uncomment to run several large random mazes with randomized start/end points:
    test_multiple_large_mazes(runs=5, rows=60, cols=100, wall_prob=0.43)