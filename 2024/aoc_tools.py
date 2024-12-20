dirs4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
dirs8 = dirs4 + [(1, 1), (1, -1), (-1, 1), (-1, -1)]

arrows4 = {
    "^": (0, -1),
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0),
}


# Grid tools
def grid_parse(data: str):
    grid = [list(row) for row in data.split("\n")]
    n_rows = len(grid)
    n_cols = len(grid[0])
    return grid, n_rows, n_cols


def grid_iter(grid: list[list[str]], value: str):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == value:
                yield (x, y)
                continue


def grid_pos(grid: list[list[str]], value: str):
    return next(grid_iter(grid, value))


def grid_all(grid: list[list[str]], value: str):
    return list(grid_iter(grid, value))


def pos_to_idx(r: int, c: int, n_cols: int) -> int:
    return r * n_cols + c


def idx_to_pos(k: int, n_cols: int) -> tuple[int, int]:
    return k // n_cols, k % n_cols


def manhattan(x0, y0, x1, y1):
    return abs(x1 - x0) + abs(y1 - y0)
