import sys
from pathlib import Path

filename = Path(__file__).parent / "input.txt" if len(sys.argv) < 2 else sys.argv[1]

with open(filename) as f:
    data = f.read().strip()  # noqa: F841

size = len(data.splitlines())
grid = list(map(int, data.replace("\n", "")))


def idx_to_pos(i):
    return i // size, i % size


def pos_to_idx(row, col):
    return row * size + col


def count_peaks_and_paths(i0):
    h0 = grid[i0]
    r0, c0 = idx_to_pos(i0)
    if h0 == 9:
        return {i0}, 1
    # Recursively check 4-directional neighborhood
    all_peaks = set()
    total_paths = 0
    for dr, dc in [[0, 1], [1, 0], [0, -1], [-1, 0]]:
        r1, c1 = r0 + dr, c0 + dc
        # Out of bounds of the grid
        if r1 < 0 or r1 >= size or c1 < 0 or c1 >= size:
            continue
        # Get the new height
        i1 = pos_to_idx(r1, c1)
        h1 = grid[i1]
        # The next position must be one higher
        if h1 != h0 + 1:
            continue
        peaks, n_paths = count_peaks_and_paths(i1)
        all_peaks.update(peaks)
        total_paths += n_paths
    if h0 > 0:
        return all_peaks, total_paths
    return len(all_peaks), total_paths


# Main loop
trailheads = [idx for idx, cell in enumerate(grid) if cell == 0]
answer_1 = 0
answer_2 = 0
for trailhead in trailheads:
    n_peaks, n_paths = count_peaks_and_paths(trailhead)
    answer_1 += n_peaks
    answer_2 += n_paths
print(answer_1)
print(answer_2)
