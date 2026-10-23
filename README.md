# Maze Generation and Solving with BFS

A beginner-friendly Python project that generates a random maze and solves it
using **Breadth-First Search (BFS)**. It uses only Python's standard library,
so no third-party packages are required.

## Features

- Generates a maze with randomized depth-first search (recursive backtracking).
- Finds a shortest route from `S` (start) to `E` (exit) using BFS.
- Displays the original maze and the solved maze in the terminal.
- Supports custom dimensions and a random seed for repeatable output.
- Uses `#` for walls and `.` to show the solution path.

## Requirements

- Python 3.8 or newer
- No external dependencies

## How to run

Open a terminal in the project folder and run:

```bash
python maze_bfs.py
```

Choose a larger maze:

```bash
python maze_bfs.py --width 31 --height 21
```

Generate the same maze again using a fixed seed:

```bash
python maze_bfs.py --width 31 --height 21 --seed 42
```

The program adjusts width and height to odd values (minimum 5) so the maze
layout works correctly.

## Symbols

| Symbol | Meaning |
|---|---|
| `#` | Wall |
| ` ` (space) | Open passage |
| `S` | Start |
| `E` | Exit |
| `.` | Shortest path found by BFS |

## How maze generation works

The generator starts at an interior cell and explores cells two steps away.
When it finds an unvisited cell, it removes the wall between the current cell
and that cell, then moves forward. When no unvisited neighbor remains, it
backtracks. This is randomized depth-first search with an explicit stack.

## How BFS solves the maze

BFS explores reachable cells in layers: first the start, then all cells one
move away, then all cells two moves away, and so on. A queue (`collections.deque`)
stores cells waiting to be explored. A `parent` dictionary records how each
cell was reached. Once the exit is found, the program follows these parent
links backward to reconstruct the route.

Because every move has the same cost, BFS guarantees a shortest path.

### Complexity

Let `V` be the number of traversable cells and `E` the number of neighboring
cell connections.

- **Time:** `O(V + E)`
- **Space:** `O(V)`

For a grid maze, each cell has at most four neighbors, so both time and space
are effectively linear in the number of cells.

## Project structure

```text
maze_bfs_project/
├── maze_bfs.py
└── README.md
```

## Example output (format)

```text
MAZE (S = start, E = exit, # = wall)
#####################
#S    #             #
### # # ########### #
#   # #       #     #
# ### ####### # #####
#       #     #     #
####### # ######### #
#       #           #
# ############### # #
#                 #E#
#####################

SOLVED MAZE ( . = shortest path )
...
Shortest path length: 34 moves
Cells in path (including S and E): 35
```

Your actual maze and path length will vary unless you provide the same seed
and dimensions.

## Notes

- The start is at the upper-left interior passage.
- The exit is at the lower-right interior passage, connected to the right edge.
- BFS uses four-directional movement (up, right, down, left).
- This is a terminal-based implementation intended for learning and project
  demonstrations.
