import dfs

def test_mazes(mazes, starts_ends_list):
    results = []
    for maze, starts_ends in zip(mazes, starts_ends_list):
        original_maze = [list(row) for row in maze]
        for start, end in starts_ends:
            path = []
            maze = [row[:] for row in original_maze]
            if dfs.dfs(maze, *start, *end, path):
                results.append((start, end, True))
            else:
                results.append((start, end, False))
    return results


mazes = [
    [
        "###############",
        "#             #",
        "# ##### #######",
        "# #   #       #",
        "# # # ####### #",
        "# # #       # #",
        "# # ####### # #",
        "# #       # # #",
        "# ######### # #",
        "#           # #",
        "# ########### #",
        "#             #",
        "# #############",
        "#             #",
        "###############"
    ],
    [
        "###############",
        "#             #",
        "# ##### ##### #",
        "# #   #     # #",
        "# # ### ### # #",
        "# # #       # #",
        "# # # ##### # #",
        "# # # #   # # #",
        "# # # # # ### #",
        "# # # # #     #",
        "# # # # #######",
        "# #     #     #",
        "# ########### #",
        "#             #",
        "###############"
    ]
]

starts_ends_list = [
    [((1, 1), (13, 13)), ((1, 13), (13, 1))],
    [((1, 1), (13, 13)), ((1, 13), (13, 1))]
]

test_results = test_mazes(mazes, starts_ends_list)

for result in test_results:
    print(f"Path from {result[0]} to {result[1]} found: {result[2]}")
