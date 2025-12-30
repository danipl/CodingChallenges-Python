In Python, slicing is a powerful way to access and copy parts of sequences like lists. While it looks simple, the
underlying mechanics impact both memory (space) and performance (time).

## 1. Understanding the Syntax

Slicing follows the general syntax `array[start:stop:step]`. When you omit a value, Python uses defaults (start=0,
stop=length, step=1).

* **`array[:]` (Full Slice):** Creates a copy of the entire list from the first element to the last.
* **`array[x:]` (Slice from index x):** Creates a copy starting at index `x` and going to the very end.
* **`array[:x]` (Slice up to index x):** Creates a copy starting from the beginning and stopping **just before** index
  `x` (index `x` is excluded).

### Visual Representation of Slicing

| Syntax | Starting Point | Ending Point | Resulting Length |
|--------|----------------|--------------|------------------|
| `[:]`  | Index 0        | End of list  | `n`              |
| `[x:]` | Index `x`      | End of list  | `n - x`          |
| `[:x]` | Index 0        | Index `x-1`  | `x`              |

## 2. Time and Space Implications

In Python, slicing a list **always creates a new list object**.

### Space Complexity:

Slicing requires allocating memory for a new list. If the slice contains `k` elements, the space complexity is **O(k)**.

* `array[:]` takes **O(n)** space (where n is the length of the array).
* `array[:x]` takes **O(x)** space.
* `array[x:]` takes **O(n - x)** space.

### Time Complexity:

Python must iterate through the original list and copy the references to the new list.

* The time complexity is **O(k)**, where **k** is the number of elements in the slice.
* Note: While it is **O(k)**, this operation is highly optimized in CPython and is much faster than a manual `for` loop.

## 3. Shallow Copy vs. Deep Copy in Slicing

This is the most critical part to understand: **Slicing performs a shallow copy.**

### Shallow Copy (Slicing)

When you slice a list, Python creates a new list container, but it does **not** create new copies of the objects
*inside* that list. It simply copies the "references" (pointers) to those objects.

* **If the elements are immutable** (integers, strings, tuples): It feels like a deep copy because you can't change the
  original values by modifying the slice.
* **If the elements are mutable** (nested lists, dictionaries, custom objects): Both the original list and the slice
  will point to the **same** inner objects.

### Comparison Table

| Feature                | Slicing (`[:]`)          | Deep Copy (`copy.deepcopy()`)      |
|------------------------|--------------------------|------------------------------------|
| **New Outer List?**    | Yes                      | Yes                                |
| **New Inner Objects?** | **No** (References only) | **Yes** (Recursive copies)         |
| **Performance**        | Very Fast (O(k))         | Slower (Significant overhead)      |
| **Use Case**           | Most standard operations | When you have nested, mutable data |

### Example of the "Shallow" Trap

```python
import copy

original = [[1, 2], [3, 4]]
sliced = original[:]  # Shallow copy

# Modifying the outer list (sliced) doesn't affect original
sliced.append([5, 6])

# Modifying an INNER mutable object DOES affect original
sliced[0][0] = "CHANGED"

print(original)
# Output: [['CHANGED', 2], [3, 4]] -> The original was mutated!
```

## Summary

* **`[:]`** is a shorthand for a full shallow copy.
* **Time/Space** are both proportional to the size of the slice ().
* **Slicing is shallow:** If your list contains other lists or dictionaries, changes to those nested items will reflect
  in both the original and the slice.

Would you like me to show you how to use the `copy` module to perform a true deep copy on a nested list?