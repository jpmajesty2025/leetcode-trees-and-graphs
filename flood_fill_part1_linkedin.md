# Flood Fill: The Subtle Infinite Recursion Bug & Zero-Memory Visited Marking 🎨⚡

When implementing the classic "Flood Fill" algorithm (LeetCode 733) — the engine behind the "Paint Bucket" tool in graphics software — what is the most common bug that slips into production?

Consider this seemingly straightforward recursive DFS:
```python
def flood_fill(image, sr, sc, color):
    original = image[sr][sc]
    # dfs down, up, right, left...
```

If you forget one single edge-case guard at the top, your code will crash into an **infinite recursion loop**:
```python
# 🚨 CRITICAL GUARD:
if original == color:
    return image
```

---

### 🚨 Why the Same-Color Guard is Mandatory

When the replacement `color` is identical to `image[sr][sc]`:
1️⃣ The starting pixel is recolored to `color` (which is still `original`).
2️⃣ Adjacent pixels see that the neighbor still matches `original`, recursing back and forth endlessly between the same two coordinates.
3️⃣ Python instantly hits `RecursionError: maximum recursion depth exceeded`.

---

### 💡 The Clean Insight: Zero-Memory Visited Marking

Unlike problems like *Number of Islands*, **Flood Fill requires zero auxiliary `visited` matrix**:
• As long as `original != color`, overwriting `image[r][c] = color` **is** the visited marker!
• The cell no longer matches `original`, so it will never be explored again.
• Auxiliary memory drops to strictly $\mathcal{O}(1)$ (excluding the traversal stack/queue).

---

### ⚖️ Traversal Comparison

| Dimension | Recursive DFS | Iterative Stack DFS |
| :--- | :--- | :--- |
| **Time Complexity** | $\mathcal{O}(M \times N)$ | $\mathcal{O}(M \times N)$ |
| **Auxiliary Matrix** | **$\mathcal{O}(1)$ (In-place)** | **$\mathcal{O}(1)$ (In-place)** |
| **Call Stack Memory** | $\mathcal{O}(M \times N)$ OS stack | $\mathcal{O}(M \times N)$ heap stack |
| **Stack Safety** | Fails on large fills ($>1,000$ pixels) | ✅ **100% Stack-Safe** |

---

Check out the clean implementations in the attached snippet! 📸

In Part 2 tomorrow, we’ll explore how **Iterative BFS simulates natural paint bucket wavefronts at 4K resolution**!

Have you ever encountered the same-color infinite recursion trap? Let's discuss below! 👇

#Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #CleanCode #ComputerScience #Graphics
