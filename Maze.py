"""
Maze Generation and Solving with Breadth-First Search (BFS)
-----------------------------------------------------------
A self-contained, terminal-based maze project using only the Python standard
library. It generates a random maze, then finds the shortest path from S to E
using Breadth-First Search (BFS).

Run:
    python maze_bfs.py
    python maze_bfs.py --width 31 --height 15 --seed 42
"""

import argparse
import random
from collections import deque
from typing import Dict, List, Optional, Tuple

Cell = Tuple[int, int]
WALL = "#"
OPEN = " "
START = "S"
END = "E"
PATH = "."


def odd_at_least(value: int, minimum: int = 5) -> int:
    """Return an odd dimension of at least `minimum`."""
    value = max(minimum, value)
    return value if value % 2 else value + 1


def generate_maze(width: int = 21, height: int = 15,
                  seed: Optional[int] = None) -> List[List[str]]:
    """
    Generate a perfect maze using randomized depth-first search (recursive
    backtracking implemented with an explicit stack).

    Width and height are adjusted to odd values so maze passages and walls
    alternate cleanly. The returned grid contains walls and open cells.
    """
    width = odd_at_least(width)
    height = odd_at_least(height)
    rng = random.Random(seed)
    grid = [[WALL for _ in range(width)] for _ in range(height)]

    start = (1, 1)
    grid[start[1]][start[0]] = OPEN
    stack = [start]
    directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]

    while stack:
        x, y = stack[-1]
        candidates = []
        shuffled = directions[:]
        rng.shuffle(shuffled)

        for dx, dy in shuffled:
            nx, ny = x + dx, y + dy
            if 1 <= nx < width - 1 and 1 <= ny < height - 1:
                if grid[ny][nx] == WALL:
                    candidates.append((nx, ny, dx, dy))

        if candidates:
            nx, ny, dx, dy = candidates[0]
            grid[y + dy // 2][x + dx // 2] = OPEN
            grid[ny][nx] = OPEN
            stack.append((nx, ny))
        else:
            stack.pop()

    # Use the top-left interior passage as start and bottom-right interior
    # passage as the exit, connecting the exit to the outer boundary.
    grid[1][1] = START
    exit_x, exit_y = width - 2, height - 2
    grid[exit_y][exit_x] = OPEN
    grid[height - 2][width - 1] = END
    return grid


def find_marker(grid: List[List[str]], marker: str) -> Cell:
    """Find a marker's (x, y) coordinate or raise a helpful error."""
    for y, row in enumerate(grid):
        for x, value in enumerate(row):
            if value == marker:
                return x, y
    raise ValueError(f"Maze does not contain marker {marker!r}")


def bfs_solve(grid: List[List[str]]) -> Optional[List[Cell]]:
    """
    Find the shortest path from S to E using Breadth-First Search.

    Returns a list of (x, y) coordinates, including start and end, or None
    when no path exists. BFS is optimal here because each move has equal cost.
    """
    start = find_marker(grid, START)
    end = find_marker(grid, END)
    height, width = len(grid), len(grid[0])

    queue = deque([start])
    parent: Dict[Cell, Optional[Cell]] = {start: None}
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    while queue:
        current = queue.popleft()
        if current == end:
            break

        x, y = current
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            neighbor = (nx, ny)

            if not (0 <= nx < width and 0 <= ny < height):
                continue
            if grid[ny][nx] == WALL or neighbor in parent:
                continue

            parent[neighbor] = current
            queue.append(neighbor)

    if end not in parent:
        return None

    path = []
    current: Optional[Cell] = end
    while current is not None:
        path.append(current)
        current = parent[current]
    path.reverse()
    return path


def render_maze(grid: List[List[str]], path: Optional[List[Cell]] = None) -> str:
    """Render the maze as readable terminal text, optionally showing the path."""
    rendered = [row[:] for row in grid]
    if path:
        for x, y in path:
            if rendered[y][x] not in (START, END):
                rendered[y][x] = PATH
    return "\n".join("".join(row) for row in rendered)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a random maze and solve it using BFS."
    )
    parser.add_argument("--width", type=int, default=21,
                        help="maze width (default: 21; adjusted to odd)")
    parser.add_argument("--height", type=int, default=15,
                        help="maze height (default: 15; adjusted to odd)")
    parser.add_argument("--seed", type=int, default=None,
                        help="optional random seed for repeatable mazes")
    args = parser.parse_args()

    maze = generate_maze(args.width, args.height, args.seed)
    print("MAZE (S = start, E = exit, # = wall)")
    print(render_maze(maze))

    path = bfs_solve(maze)
    print("\nSOLVED MAZE ( . = shortest path )")
    if path is None:
        print("No path found.")
    else:
        print(render_maze(maze, path))
        print(f"\nShortest path length: {len(path) - 1} moves")
        print(f"Cells in path (including S and E): {len(path)}")


if __name__ == "__main__":
    main()
