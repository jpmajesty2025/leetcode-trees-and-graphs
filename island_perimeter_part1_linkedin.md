# Computational Geometry on 2D Grids: Island Perimeter (Part 1 of 2) 🏝️📐

How do you compute the exact boundary length of a discrete shape on a pixel grid?

In the "Island Perimeter" problem, we are given a binary grid of land (`1`) and water (`0`). One cell represents a 1x1 square. Our goal is to calculate the total perimeter of the island.

Let's break down the mathematical invariants and the edge-subtraction approach!

---

### 💡 The Core Invariant: Discrete Surface Area

Every isolated 1x1 land cell contributes **4 units** of perimeter.

When two land cells are adjacent:
1. They share an internal border segment.
2. This shared segment is no longer exposed to water.
3. Placing two cells together removes **2 units** of perimeter (1 from each cell).

This gives an exact closed-form formula:
`Perimeter = 4 * (Total Land Cells) - 2 * (Shared Internal Edges)`

---

### ⚙️ Forward-Neighbor Optimization (O(1) Space)

A naive scan checks all 4 orthogonal neighbors for every cell.

Instead, scanning top-to-bottom, left-to-right requires checking only **two neighbors**:
- For every land cell, add `+4`.
- If the cell above is land, subtract `2`.
- If the cell to the left is land, subtract `2`.

Because every vertical edge connects to the top cell and every horizontal edge connects to the left cell, we count every shared edge **exactly once** without extra memory or sets!

---

### 📊 Complexity Profile

- **Time: O(R * C)** — Linear scan over all grid cells.
- **Space: O(1)** — Zero auxiliary memory allocated.

---

### 🧠 Engineering Takeaway

Translating geometric boundaries into algebraic invariants eliminates duplicate checks while keeping memory at O(1).

👉 **In Part 2**, we will compare **Raster Scanning vs. DFS Boundary Tracing** in **Computer Vision & GIS mapping**!

What is your preferred approach for discrete boundary detection?

#LearningInPublic #Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #ComputationalGeometry #CleanCode #PerformanceOptimization
