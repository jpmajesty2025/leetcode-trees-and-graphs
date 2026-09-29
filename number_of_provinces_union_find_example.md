# How Union-Find Works: Illustrated Example (`number_of_provinces_union_find.py`) 🌐🔍

## 1. The Mental Model of Union-Find (Disjoint Set Union)

Imagine every city starts as its own **independent province**.
* In the beginning, each city chooses itself as the **"leader"** (the root of its group).
* Whenever we discover a road between City $A$ and City $B$, we find the leaders of both cities.
* If their leaders are different, we merge the two groups under one common leader and **decrement our total province count by 1**.
* If their leaders are already the same, they are already part of the same province (a redundant connection or cycle), so we do nothing.

---

## 2. Concrete Example: 4 Cities

Suppose we have $N = 4$ cities labeled `0, 1, 2, 3` with the following connections:
* City `0` is connected to City `1`
* City `1` is connected to City `2`
* City `3` is completely isolated (no connections)

```python
isConnected = [
    [1, 1, 0, 0],  # City 0 connects to 1
    [1, 1, 1, 0],  # City 1 connects to 0 and 2
    [0, 1, 1, 0],  # City 2 connects to 1
    [0, 0, 0, 1]   # City 3 has no outside connections
]
```

---

## 3. Step-by-Step Execution Walkthrough

### Step 0: Initialization (`__init__`)

```python
class UnionFind:
    def __init__(self, size: int):
        self.parent = list(range(size))  # [0, 1, 2, 3]
        self.rank = [0] * size           # [0, 0, 0, 0] (tree height estimate)
        self.count = size                # 4 provinces
```

* **`parent` array**: `parent[i]` tells us who City `i` points to as its immediate parent.
  * Initially: `parent = [0, 1, 2, 3]` (City `0` points to `0`, `1` to `1`, etc.)
* **`count`**: Starts at `4` separate groups: `{0}`, `{1}`, `{2}`, `{3}`.

```text
Initial State (4 Provinces):
 (0)      (1)      (2)      (3)
```

---

### Step 1: Process Edge between City `0` and City `1` (`isConnected[0][1] == 1`)

We call `uf.union(0, 1)`:

1. **Find Leaders**:
   * `find(0)` $\to$ `parent[0] == 0` $\implies$ Leader is **`0`**.
   * `find(1)` $\to$ `parent[1] == 1` $\implies$ Leader is **`1`**.
2. **Are they in different groups?**
   * Yes (`0 != 1`).
3. **Merge them (`Union by Rank`)**:
   * Both have `rank = 0` (tie). We attach City `1` under City `0`: `parent[1] = 0` and increment `rank[0] = 1`.
4. **Update Province Count**:
   * `self.count -= 1` $\implies$ `count = 3`.

```text
After union(0, 1) (3 Provinces):
    (0)         (2)      (3)
     |
    (1)

State: parent = [0, 0, 2, 3], count = 3
Groups: {0, 1}, {2}, {3}
```

---

### Step 2: Process Edge between City `1` and City `2` (`isConnected[1][2] == 1`)

We call `uf.union(1, 2)`:

1. **Find Leaders**:
   * `find(1)`:
     * City `1` points to `0`. City `0` points to `0`.
     * Leader of City `1` is **`0`**.
   * `find(2)`:
     * City `2` points to `2`.
     * Leader of City `2` is **`2`**.
2. **Are they in different groups?**
   * Yes (`0 != 2`). Even though City `2` directly connects to `1`, City `1` belongs to City `0`'s group.
3. **Merge them (`Union by Rank`)**:
   * `rank[0] = 1`, `rank[2] = 0`.
   * Group `0` has a higher rank, so we attach `2` under `0`: `parent[2] = 0`.
4. **Update Province Count**:
   * `self.count -= 1` $\implies$ `count = 2`.

```text
After union(1, 2) (2 Provinces):
      (0)               (3)
     /   \
   (1)   (2)

State: parent = [0, 0, 0, 3], count = 2
Groups: {0, 1, 2}, {3}
```

---

### Step 3: Check Remaining Pairs

* `(0, 2)`: `isConnected[0][2] == 0` (no road, skip).
* `(0, 3)`: `isConnected[0][3] == 0` (no road, skip).
* `(1, 3)`: `isConnected[1][3] == 0` (no road, skip).
* `(2, 3)`: `isConnected[2][3] == 0` (no road, skip).

---

### Final Return Value

`number_of_provinces_union_find` simply returns `uf.count`, which is **`2`**:
1. **Province 1**: `{0, 1, 2}`
2. **Province 2**: `{3}`

---

## 4. Why Union-Find is Blazing Fast: The Two Secret Weapons

### 1. Path Compression (in `find`):
```python
def find(self, x: int) -> int:
    if self.parent[x] != x:
        self.parent[x] = self.find(self.parent[x])  # Flattens the tree!
    return self.parent[x]
```
Whenever we look up a leader, every node on the path updates its parent pointer to point **directly to the root**. After the first lookup, future queries take strictly $\mathcal{O}(1)$ time.

### 2. Union by Rank (in `union`):
```python
if self.rank[root_x] < self.rank[root_y]:
    self.parent[root_x] = root_y
elif self.rank[root_x] > self.rank[root_y]:
    self.parent[root_y] = root_x
else:
    self.parent[root_y] = root_x
    self.rank[root_x] += 1
```
Instead of randomly attaching trees (which could create a degenerate chain like $0 \to 1 \to 2 \to 3$), we always attach the shorter tree under the taller tree, keeping the tree depth minimal.

Together, these two optimizations make almost any sequence of operations run in **$\mathcal{O}(\alpha(N))$ amortized time** (where $\alpha \le 4$ for all numbers in the universe).
