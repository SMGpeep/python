import dfs
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

def print_maze(maze, start, end):
    color_map = {'#': 0, ' ': 1, '.': 2, 'S': 3, 'E': 4, 'X': 5}
    maze[start[0]][start[1]] = 'S'
    maze[end[0]][end[1]] = 'E'
    maze_color = np.array([[color_map[cell] for cell in row] for row in maze])
    cmap = ListedColormap(['black', 'white', 'lime', 'blue', 'red', 'gray'])

    plt.figure(figsize=(10, 5))
    plt.imshow(maze_color, cmap=cmap, interpolation='nearest')
    plt.xticks([]), plt.yticks([])
    plt.show()

# Gegebenes Labyrinth
maze = [
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

# Definiert den Start- und Endpunkt
maze = [list(row) for row in maze]
starts_ends = [((1, 15), (9, 17)), ((1, 2), (9, 17))]

# Prüft, ob ein Weg gefunden worden ist.
for start, end in starts_ends:
    path = []
    if dfs.dfs(maze, *start, *end, path):
        print("Weg gefunden von", start, "nach", end)
        print_maze(maze, start, end)
    else:
        print("Kein Weg gefunden von", start, "nach", end)

    # Labyrinth zurücksetzen
    maze = [list(row) for row in [
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
    ]]