import threading
import random
import time
from typing import List, Callable


# ---------- Shared utilities ----------

def is_sorted(a: List[int]) -> bool:
    return all(a[i] <= a[i+1] for i in range(len(a) - 1))


def print_state(step, label, a):
    print(f"{label:20s} step {step:3d}: {a}")


# ---------- Cell-view Bubble Sort ----------

class CellViewBubbleSorter:
    """
    Each cell is a thread with a local index.
    Rule:
      - Can view left and right neighbor.
      - If a[i] < a[i-1]: move left (swap with left).
      - If a[i] > a[i+1]: move right (swap with right).
    """

    def __init__(self, data: List[int], max_steps=200, delay=0.0):
        self.a = data
        self.n = len(data)
        self.lock = threading.Lock()
        self.positions = list(range(self.n))  # logical positions of each cell-id
        self.stop_flag = False
        self.max_steps = max_steps
        self.delay = delay

    def cell_thread(self, cell_id: int):
        steps = 0
        while not self.stop_flag and steps < self.max_steps:
            steps += 1
            if self.delay:
                time.sleep(self.delay * random.random())
            with self.lock:
                # logical index of this cell in the array
                i = self.positions.index(cell_id)

                # check left
                moved = False
                if i > 0:
                    if self.a[i] < self.a[i-1]:
                        self.a[i], self.a[i-1] = self.a[i-1], self.a[i]
                        self.positions[i], self.positions[i-1] = (
                            self.positions[i-1],
                            self.positions[i],
                        )
                        moved = True

                # check right (recompute i after potential left move)
                i = self.positions.index(cell_id)
                if not moved and i < self.n - 1:
                    if self.a[i] > self.a[i+1]:
                        self.a[i], self.a[i+1] = self.a[i+1], self.a[i]
                        self.positions[i], self.positions[i+1] = (
                            self.positions[i+1],
                            self.positions[i],
                        )

            if is_sorted(self.a):
                self.stop_flag = True
                return

    def run(self, verbose=False):
        threads = []
        for cid in range(self.n):
            t = threading.Thread(target=self.cell_thread, args=(cid,))
            t.start()
            threads.append(t)

        step = 0
        while not self.stop_flag and step < self.max_steps:
            step += 1
            if verbose:
                with self.lock:
                    print_state(step, "bubble", self.a)
            time.sleep(self.delay or 0.01)

        self.stop_flag = True
        for t in threads:
            t.join()
        return self.a


# ---------- Cell-view Insertion Sort ----------

class CellViewInsertionSorter:
    """
    Each cell is a thread.
    Rule:
      - A cell can 'view' all cells to its left but only swap with its left neighbor.
      - An active cell moves left if:
          * all cells to its left are already sorted among themselves, and
          * a[i] < a[i-1].
    """

    def __init__(self, data: List[int], max_steps=400, delay=0.0):
        self.a = data
        self.n = len(data)
        self.lock = threading.Lock()
        self.positions = list(range(self.n))
        self.stop_flag = False
        self.max_steps = max_steps
        self.delay = delay

    def left_region_sorted(self, up_to_index: int) -> bool:
        # check a[0:up_to_index] is sorted
        return all(self.a[i] <= self.a[i+1] for i in range(up_to_index - 1))

    def cell_thread(self, cell_id: int):
        steps = 0
        while not self.stop_flag and steps < self.max_steps:
            steps += 1
            if self.delay:
                time.sleep(self.delay * random.random())
            with self.lock:
                i = self.positions.index(cell_id)
                if i > 0:
                    if self.left_region_sorted(i) and self.a[i] < self.a[i-1]:
                        self.a[i], self.a[i-1] = self.a[i-1], self.a[i]
                        self.positions[i], self.positions[i-1] = (
                            self.positions[i-1],
                            self.positions[i],
                        )

            if is_sorted(self.a):
                self.stop_flag = True
                return

    def run(self, verbose=False):
        threads = []
        for cid in range(self.n):
            t = threading.Thread(target=self.cell_thread, args=(cid,))
            t.start()
            threads.append(t)

        step = 0
        while not self.stop_flag and step < self.max_steps:
            step += 1
            if verbose:
                with self.lock:
                    print_state(step, "insertion", self.a)
            time.sleep(self.delay or 0.01)

        self.stop_flag = True
        for t in threads:
            t.join()
        return self.a


# ---------- Cell-view Selection Sort ----------

class CellViewSelectionSorter:
    """
    Each cell has an ideal target position it wants to move to.
    Spec simplification:
      - Ideal position of each cell initially = 0 (most-left position).
      - A cell can view and swap with the cell currently at its ideal position.
      - If a[cell_id] < a[ideal_position_cell]: swap.
    Here, we approximate 'cell has ideal target position' by assigning each
    cell a target index that moves right after successful placements.
    """

    def __init__(self, data: List[int], max_steps=400, delay=0.0):
        self.a = data
        self.n = len(data)
        self.lock = threading.Lock()
        self.positions = list(range(self.n))
        # each cell starts by wanting to be at the far-left
        self.ideal_pos = [0 for _ in range(self.n)]
        self.stop_flag = False
        self.max_steps = max_steps
        self.delay = delay

    def cell_thread(self, cell_id: int):
        steps = 0
        while not self.stop_flag and steps < self.max_steps:
            steps += 1
            if self.delay:
                time.sleep(self.delay * random.random())
            with self.lock:
                i = self.positions.index(cell_id)
                ideal = self.ideal_pos[cell_id]
                if ideal < 0 or ideal >= self.n:
                    # no valid target
                    pass
                else:
                    # who is at my ideal position?
                    occupying_cell_id = self.positions[ideal]
                    occupying_index = ideal
                    if self.a[i] < self.a[occupying_index]:
                        # swap cells in the array
                        self.a[i], self.a[occupying_index] = (
                            self.a[occupying_index],
                            self.a[i],
                        )
                        # update positions
                        self.positions[i], self.positions[occupying_index] = (
                            self.positions[occupying_index],
                            self.positions[i],
                        )
                        # push my ideal position rightwards (like selection placing minima)
                        self.ideal_pos[cell_id] = min(self.ideal_pos[cell_id] + 1, self.n - 1)

            if is_sorted(self.a):
                self.stop_flag = True
                return

    def run(self, verbose=False):
        threads = []
        for cid in range(self.n):
            t = threading.Thread(target=self.cell_thread, args=(cid,))
            t.start()
            threads.append(t)

        step = 0
        while not self.stop_flag and step < self.max_steps:
            step += 1
            if verbose:
                with self.lock:
                    print_state(step, "selection", self.a)
            time.sleep(self.delay or 0.01)

        self.stop_flag = True
        for t in threads:
            t.join()
        return self.a


# ---------- Experiment harness ----------

def run_experiment_once(
    sorter_cls: Callable,
    n=8,
    value_range=(0, 99),
    max_steps=400,
    delay=0.0,
    verbose=False,
):
    arr = [random.randint(*value_range) for _ in range(n)]
    print(f"\nInitial: {arr}")
    sorter = sorter_cls(arr, max_steps=max_steps, delay=delay)
    res = sorter.run(verbose=verbose)
    print(f"Final:   {res}")
    print(f"Sorted?  {is_sorted(res)}")


def main():
    random.seed(0)

    print("=== Cell-view Bubble ===")
    run_experiment_once(CellViewBubbleSorter, n=8, delay=0.01, verbose=True)

    print("\n=== Cell-view Insertion ===")
    run_experiment_once(CellViewInsertionSorter, n=8, delay=0.01, verbose=True)

    print("\n=== Cell-view Selection ===")
    run_experiment_once(CellViewSelectionSorter, n=8, delay=0.01, verbose=True)


if __name__ == "__main__":
    main()
