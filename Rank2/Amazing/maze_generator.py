#!/usr/bin/env python3
"""Maze Generator Module with animation bonus.

Provides a class MazeGenerator that generates random mazes using recursive
backtracking algorithm, with options for perfect/non-perfect mazes, seed for
reproducibility, and methods to access cell walls and solve the maze.
Includes an animated generator for step-by-step visualization.
"""

import random
from collections import deque
from typing import Tuple, Optional, Set, Generator


class MazeGenerator:
    """A maze generator using recursive backtracking (DFS) with animation.

    The maze is represented as a grid of cells, each storing a 4-bit wall code.
    Bits: 0 = North, 1 = East, 2 = South, 3 = West. A bit set to 1 means the
    wall is closed.

    Attributes:
        width: Number of cells horizontally.
        height: Number of cells vertically.
        seed: Random seed for reproducibility (if provided).
        grid: 2D list of wall codes (0-15).
        entry: (x, y) entrance coordinates, or None.
        exit: (x, y) exit coordinates, or None.
        pattern_42_cells: Set of (x, y) that form the visible "42" pattern.
    """

    # Direction constants (bit positions)
    N, E, S, W = 0, 1, 2, 3
    # Direction vectors and opposite direction mapping
    DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # (dx, dy) for N, E, S, W
    OPPOSITE = {N: S, E: W, S: N, W: E}

    def __init__(self, width: int, height: int, seed: Optional[int] = None):
        """Initialize maze generator.

        Args:
            width: Number of cells horizontally.
            height: Number of cells vertically.
            seed: Random seed (optional). If provided, ensures reproducibility.
        """
        self.width = width
        self.height = height
        self.seed = seed
        if seed is not None:
            random.seed(seed)
        # Initialize all cells with all walls closed (1111 binary = 15)
        self.grid = [
            [15 for _ in range(self.width)]
            for _ in range(self.height)
        ]
        self.entry: Optional[Tuple[int, int]] = None
        self.exit: Optional[Tuple[int, int]] = None
        self.pattern_42_cells: Set[Tuple[int, int]] = set()

    def _remove_wall(self, x: int, y: int, nx: int, ny: int,
                     direction: int) -> None:
        """Remove wall between current cell (x,y) and neighbor (nx,ny).

        Both the current cell's wall in `direction` and the neighbor's
        opposite wall are cleared.

        Args:
            x: Current cell's x coordinate.
            y: Current cell's y coordinate.
            nx: Neighbor's x coordinate.
            ny: Neighbor's y coordinate.
            direction: Direction from current to neighbor (0=N,1=E,2=S,3=W).
        """
        # Remove wall in current cell
        self.grid[y][x] &= ~(1 << direction)
        # Remove opposite wall in neighbor
        opp = self.OPPOSITE[direction]
        self.grid[ny][nx] &= ~(1 << opp)

    def _carve(self, x: int, y: int) -> None:
        """Iterative DFS to carve passages starting from (x,y).

        Uses an explicit stack to avoid recursion limit errors on large mazes.
        Randomly chooses unvisited neighbors and removes the wall between them,
        then continues from the neighbor.

        Args:
            x: Starting x coordinate.
            y: Starting y coordinate.
        """
        stack = [(x, y)]
        while stack:
            cx, cy = stack[-1]
            dirs = list(range(4))
            random.shuffle(dirs)
            moved = False
            for direction in dirs:
                dx, dy = self.DIRS[direction]
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if self.grid[ny][nx] == 15:
                        self._remove_wall(cx, cy, nx, ny, direction)
                        stack.append((nx, ny))
                        moved = True
                        break
            if not moved:
                stack.pop()

    def generate(self) -> None:
        """Generate a perfect maze.

        All cells reachable, exactly one path between any two cells.
        Uses randomized depth-first search (recursive backtracker).
        """
        # Reset grid to all walls closed
        self.grid = [
            [15 for _ in range(self.width)]
            for _ in range(self.height)
        ]
        self.pattern_42_cells = set()
        # Start from a random cell
        start_x = random.randint(0, self.width - 1)
        start_y = random.randint(0, self.height - 1)
        self._carve(start_x, start_y)

    def set_entry_exit(self, entry: Tuple[int, int],
                       exit: Tuple[int, int]) -> None:
        """Set entry and exit coordinates.

        Args:
            entry: (x, y) coordinates of the entrance.
            exit: (x, y) coordinates of the exit.

        Raises:
            ValueError: If either coordinate is out of bounds.
        """
        if not (0 <= entry[0] < self.width and 0 <= entry[1] < self.height):
            raise ValueError(f"Entry {entry} out of bounds")
        if not (0 <= exit[0] < self.width and 0 <= exit[1] < self.height):
            raise ValueError(f"Exit {exit} out of bounds")
        self.entry = entry
        self.exit = exit

    def get_cell_walls(self, x: int, y: int) -> int:
        """Return the wall code (0-15) for the cell at (x,y).

        Args:
            x: Column index.
            y: Row index.

        Returns:
            Integer wall code.
        """
        return self.grid[y][x]

    def solve(self) -> Optional[str]:
        """Find shortest path from entry to exit using BFS.

        Returns:
            Direction string (e.g., "SENW") or None if no path exists.

        Raises:
            ValueError: If entry or exit is not set.
        """
        if self.entry is None or self.exit is None:
            raise ValueError("Entry and exit must be set before solving")

        start = self.entry
        goal = self.exit

        queue: deque[Tuple[int, int]] = deque()
        queue.append(start)
        visited = [[False] * self.width for _ in range(self.height)]
        visited[start[1]][start[0]] = True
        # parent: (x,y) -> (prev_x, prev_y, direction_from_prev)
        parent: dict[Tuple[int, int], Tuple[int, int, str]] = {}

        dir_chars = {self.N: 'N', self.E: 'E', self.S: 'S', self.W: 'W'}

        while queue:
            x, y = queue.popleft()
            if (x, y) == goal:
                # Reconstruct path
                path = []
                cur = (x, y)
                while cur != start:
                    px, py, d = parent[cur]
                    path.append(d)
                    cur = (px, py)
                path.reverse()
                return ''.join(path)

            for direction, (dx, dy) in enumerate(self.DIRS):
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if not visited[ny][nx]:
                        # Check if wall is open in current cell for this dir
                        if (self.grid[y][x] >> direction) & 1 == 0:
                            visited[ny][nx] = True
                            queue.append((nx, ny))
                            parent[(nx, ny)] = (x, y, dir_chars[direction])
        return None  # No path

    def _has_3x3_open_area(self) -> bool:
        """Check whether the current grid contains any 3x3 fully open area.

        A 3x3 open area means all internal passages between the 9 cells
        are open.

        Returns:
            True if a 3x3 open area exists, False otherwise.
        """
        for r in range(self.height - 2):
            for c in range(self.width - 2):
                open_area = True
                for dr in range(3):
                    for dc in range(2):
                        if (self.grid[r + dr][c + dc] >> self.E) & 1:
                            open_area = False
                            break
                    if not open_area:
                        break
                if open_area:
                    for dr in range(2):
                        for dc in range(3):
                            if (self.grid[r + dr][c + dc] >> self.S) & 1:
                                open_area = False
                                break
                        if not open_area:
                            break
                if open_area:
                    return True
        return False

    def add_cycles(self, probability: float = 0.1) -> None:
        """Add cycles by randomly removing internal walls.

        Makes the maze non-perfect. Skips wall removal if it would create
        a 3x3 open area (forbidden by maze requirements).

        Args:
            probability: Chance (0-1) for each internal wall to be removed.
        """
        for y in range(self.height):
            for x in range(self.width):
                for direction in range(4):
                    if (self.grid[y][x] >> direction) & 1 == 0:
                        continue
                    dx, dy = self.DIRS[direction]
                    nx, ny = x + dx, y + dy
                    if not (0 <= nx < self.width and 0 <= ny < self.height):
                        continue  # boundary wall, keep closed
                    if random.random() < probability:
                        self._remove_wall(x, y, nx, ny, direction)
                        if self._has_3x3_open_area():
                            # Revert: put the wall back
                            self.grid[y][x] |= (1 << direction)
                            opp = self.OPPOSITE[direction]
                            self.grid[ny][nx] |= (1 << opp)

    def embed_42(self) -> bool:
        """Attempt to embed a visible "42" pattern using fully walled cells.

        Uses 5x3 dot matrix for each digit. Tries multiple offsets to avoid
        blocking the entry-to-exit path. If no suitable location is found,
        prints a warning and returns False.

        Returns:
            True if successfully embedded, False otherwise.
        """
        # 5x3 templates for '4' and '2' (1 = fully closed cell)
        template_4 = [
            [1, 0, 1],
            [1, 0, 1],
            [1, 1, 1],
            [0, 0, 1],
            [0, 0, 1]
        ]

        # Updated template for '2' as requested by the user:
        template_2 = [
            [1, 1, 1],
            [0, 0, 1],
            [1, 1, 1],
            [1, 0, 0],
            [1, 1, 1]
        ]

        if self.width < 10 or self.height < 7:
            print("Warning: Maze too small to embed '42' pattern.")
            return False

        # First solve the current path (entry and exit must be set)
        if self.entry is None or self.exit is None:
            raise ValueError("Entry and exit must be set before embedding 42")
        path_str = self.solve()
        if path_str is None:
            # No path exists, cannot embed without breaking connectivity
            print("Warning: No path exists; cannot embed '42' pattern.")
            return False

        # Convert the path to a set of cell coordinates
        path_cells: Set[Tuple[int, int]] = set()
        cur = self.entry
        path_cells.add(cur)
        for d in path_str:
            if d == 'N':
                cur = (cur[0], cur[1] - 1)
            elif d == 'S':
                cur = (cur[0], cur[1] + 1)
            elif d == 'E':
                cur = (cur[0] + 1, cur[1])
            elif d == 'W':
                cur = (cur[0] - 1, cur[1])
            path_cells.add(cur)

        # Candidate offsets (top-left corners) to try
        offsets = [
            (2, 2), (5, 2), (8, 2),
            (2, 5), (5, 5), (8, 5),
            (2, 8), (5, 8), (8, 8)
        ]
        for off_x, off_y in offsets:
            # Compute all cells that would become fully closed for '4' and '2'
            pos_4 = [
                (off_x + x, off_y + y)
                for y in range(5) for x in range(3) if template_4[y][x]
            ]
            pos_2 = [
                (off_x + 5 + x, off_y + y)
                for y in range(5) for x in range(3) if template_2[y][x]
            ]
            all_pos = pos_4 + pos_2

            # Check boundaries
            if any(
                x < 0 or x >= self.width or y < 0 or y >= self.height
                for (x, y) in all_pos
            ):
                continue

            # Check if covers entry or exit
            if self.entry in all_pos or self.exit in all_pos:
                continue

            # Check if any of these cells lie on the path; if so, skip
            if any(cell in path_cells for cell in all_pos):
                continue

            # Found a suitable location; embed the pattern
            self.pattern_42_cells = set(all_pos)
            for (x, y) in all_pos:
                self.grid[y][x] = 15
                # Close the corresponding walls in neighbors
                for direction in range(4):
                    dx, dy = self.DIRS[direction]
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        opp = self.OPPOSITE[direction]
                        self.grid[ny][nx] |= (1 << opp)
            print(f"Embedded '42' pattern at offset ({off_x}, {off_y})")
            return True

        # No suitable location found
        msg = ("Warning: Could not find a suitable location for '42' pattern "
               "without blocking the path.")
        print(msg)
        return False

    # ---------- Animation Bonus Methods ----------
    def _carve_generator(
        self, start_x: int, start_y: int
    ) -> Generator[None, None, None]:
        """Generator version of _carve. Yields after every move or backtrack.

        Sets self.anim_frontier to the set of cells currently on the DFS
        stack so the renderer can highlight the active path in the animation.

        Args:
            start_x: Starting x coordinate.
            start_y: Starting y coordinate.

        Yields:
            None after each step (advance or backtrack).
        """
        visited = [[False] * self.width for _ in range(self.height)]
        for (px, py) in self.pattern_42_cells:
            visited[py][px] = True

        stack = [(start_x, start_y)]
        visited[start_y][start_x] = True
        self.anim_frontier: set[tuple[int, int]] = {(start_x, start_y)}

        while stack:
            x, y = stack[-1]
            neighbours = []
            for d, (dx, dy) in enumerate(self.DIRS):
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.width
                        and 0 <= ny < self.height
                        and not visited[ny][nx]):
                    neighbours.append((nx, ny, d))
            if neighbours:
                nx, ny, d = random.choice(neighbours)
                self.grid[y][x] &= ~(1 << d)
                self.grid[ny][nx] &= ~(1 << self.OPPOSITE[d])
                visited[ny][nx] = True
                stack.append((nx, ny))
                self.anim_frontier = set(stack)
                yield  # advance: wall removed, new frontier
            else:
                stack.pop()
                self.anim_frontier = set(stack)
                yield  # backtrack: show retreat

    def generate_animated(
        self, perfect: bool = True
    ) -> Generator[None, None, None]:
        """Generate the maze step by step, yielding after each move.

        Args:
            perfect: If True, generate a perfect maze; if False, cycles
                     are added after carving (not animated).

        Yields:
            None after each DFS step (advance or backtrack).
            self.anim_frontier is updated each yield so callers can
            highlight the active path.

        Raises:
            ValueError: If entry or exit not set.
        """
        if self.entry is None or self.exit is None:
            raise ValueError("Entry and exit must be set before generation")

        self._init_grid()

        # Start carving from entry
        start_x, start_y = self.entry
        gen = self._carve_generator(start_x, start_y)
        for _ in gen:
            yield

        # Open boundary walls for entry and exit
        for (x, y) in [self.entry, self.exit]:
            if x == 0:
                self.grid[y][x] &= ~(1 << self.W)
            elif x == self.width - 1:
                self.grid[y][x] &= ~(1 << self.E)
            if y == 0:
                self.grid[y][x] &= ~(1 << self.N)
            elif y == self.height - 1:
                self.grid[y][x] &= ~(1 << self.S)

        # Cycles and pattern embedding handled by caller after animation

    def _init_grid(self) -> None:
        """Helper to reset grid to all walls closed."""
        self.grid = [
            [15 for _ in range(self.width)]
            for _ in range(self.height)
        ]
        self.pattern_42_cells = set()
