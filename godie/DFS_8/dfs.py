
def dfs(maze, x, y, end_x, end_y, path):
    # Boundary check first (fastest check)
    if x < 0 or x >= len(maze) or y < 0 or y >= len(maze[0]):
        return False
    
    cell = maze[x][y]
    
    # Check if cell is a wall or already marked as dead end
    if cell == '#' or cell == 'X':
        return False
    
    # Check if we reached the goal
    if x == end_x and y == end_y:
        path.append((x, y))
        return True
    
    # Check if cell is already visited (redundant path check removed - O(n) -> O(1))
    if cell == '.':
        return False
    
    # Mark current cell as visited
    maze[x][y] = '.'
    path.append((x, y))

    # Recursive DFS search in all four directions
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        if dfs(maze, x + dx, y + dy, end_x, end_y, path):
            return True
    
    # Backtrack: remove from path and mark as dead end
    path.pop()
    maze[x][y] = 'X'
    return False    

