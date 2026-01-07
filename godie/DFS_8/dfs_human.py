def dfs(maze, x, y, end_x, end_y, path):

    if x >= len(maze) or x < 0 or y >= len(maze[0]) or y < 0:
        return False
    
    if x == end_x and y == end_y:
        path.append((x, y))
        return True
    
    match maze[x][y]:
        case '.': 
                    return False
        case '#':   
                    return False
        case 'X': 
                    return False
                

    maze[x][y] = '.'
    path.append((x,y))    
  
    for (d_x, d_y) in ([1,0], [-1,0], [0,1], [0,-1]):
        if dfs(maze, x+d_x, y+d_y,end_x,end_y,path):
            return True

    path.pop()
    maze[x][y] = 'X'
    return False

