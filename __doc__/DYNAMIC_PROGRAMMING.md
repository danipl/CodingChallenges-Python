# Dynamic Programming (DP)

Dynamic Programming is a powerful algorithmic technique used to solve complex problems by breaking them down into
simpler, **overlapping subproblems**. It is particularly useful for optimization problems where you want to find the "
best" (maximum or minimum) solution.

In a whiteboard interview, think of DP as **"Recursion with a Memory."** Instead of recalculating the same result
multiple times, you compute it once, store it, and look it up later.

---

## The Two Pillars of DP

For a problem to be solvable using Dynamic Programming, it must satisfy two specific properties:

1. **Optimal Substructure:** The optimal solution to a large problem can be constructed from the optimal solutions of
   its subproblems.
    - *Example:* To find the shortest path from City A to City C, you might find the shortest path from A to B and then
      the shortest path from B to C.
2. **Overlapping Subproblems:** The same subproblems are solved multiple times.
    - *Example:* In Fibonacci, $F(n) = F(n-1) + F(n-2)$. Calculating $F(5)$ requires $F(4)$ and $F(3)$. But $F(4)$
      *also* requires $F(3)$. Without DP, $F(3)$ is calculated twice.

### Visualizing Overlapping Subproblems

Recursion tree for `fib(4)` without memoization:

```text
          fib(4)
        /        \
     fib(3)      fib(2)  <-- repeated
    /      \    /      \
 fib(2)  fib(1)fib(1)  fib(0)
 /    \
fib(1) fib(0)
```

---

## The DP Recipe (5-Step Strategy)

1. **Identify the State:** What parameters uniquely define a subproblem? (e.g., `i` = current step).
2. **Recurrence Relation:** How do you solve the big problem using smaller ones? (e.g., `dp[i] = dp[i-1] + dp[i-2]`).
3. **Base Cases:** What are the smallest possible subproblems? (e.g., `dp[0] = 1`).
4. **Choose Approach:** Top-Down (Memoization) or Bottom-Up (Tabulation)?
5. **Complexity Analysis:** Determine Time and Space complexity. Can we optimize space?

---

## The Two Approaches

| Feature       | **Top-Down (Memoization)**                      | **Bottom-Up (Tabulation)**                                     |
|:--------------|:------------------------------------------------|:---------------------------------------------------------------|
| **Method**    | Starts with the big problem and uses recursion. | Starts with the smallest subproblems and uses a loop.          |
| **Storage**   | Uses a Hash Map or Array to cache results.      | Usually fills up an array (`dp` table).                        |
| **Intuition** | Natural extension of recursion.                 | Often more space-efficient and faster (no recursion overhead). |
| **State**     | `memo[n] = solve(n-1) + solve(n-2)`             | `dp[i] = dp[i-1] + dp[i-2]`                                    |

---

## Example: Climbing Stairs

> **Problem:** You are climbing a staircase. It takes `n` steps to reach the top. Each time you can either take **1** or
**2** steps. In how many distinct ways can you climb to the top?

### 1. Top-Down (Memoization)

We use a dictionary to store results. If we see the same `n` again, we return the cached value.

```python
def climb_stairs(n: int, memo: dict[int, int] = None) -> int:
    if memo is None:
        memo = {}  # Time: O(1), Space: O(1) - initialize memoization dictionary

    # Base cases
    # Time: O(1), Space: O(1) - constant time check and return
    if n <= 2:
        return n

    # Check if we've already calculated this step
    # Time: O(1), Space: O(1) - dictionary lookup is O(1) average case
    if n in memo:
        return memo[n]

    # Calculate recursively and store the result
    # Time: O(n), Space: O(n) - we calculate each unique value of n once and store it
    # Overall: O(n) time due to memoization preventing redundant calculations
    # Overall: O(n) space for memo dictionary + O(n) recursion stack depth
    memo[n] = climb_stairs(n - 1, memo) + climb_stairs(n - 2, memo)
    return memo[n]
```

### 2. Bottom-Up (Tabulation)

We build a table from the ground up.

```python
def climb_stairs(n: int) -> int:
    if n <= 2:
        return n  # Time: O(1), Space: O(1) - base case check and return

    # dp[i] stores the number of ways to reach step i
    # Time: O(n), Space: O(n) - allocate array of size n+1
    dp = [0] * (n + 1)
    dp[1] = 1  # Time: O(1), Space: O(1) - initialize base case
    dp[2] = 2  # Time: O(1), Space: O(1) - initialize base case

    # Time: O(n), Space: O(1) - iterate from 3 to n, constant space per iteration
    for i in range(3, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]  # Time: O(1), Space: O(1) - array lookup and addition

    # Overall Time Complexity: O(n), Space Complexity: O(n)
    return dp[n]  # Time: O(1), Space: O(1) - array lookup and return
```

### 3. Space Optimization (Bonus)

Notice that `dp[i]` only depends on the **previous two** values. We don't need the whole array!

```python
def climb_stairs(n: int) -> int:
    if n <= 2:
        return n  # Time: O(1), Space: O(1) - base case check and return

    first = 1  # ways to reach step 1, Time: O(1), Space: O(1)
    second = 2  # ways to reach step 2, Time: O(1), Space: O(1)

    # Time: O(n-2) ≈ O(n), Space: O(1) - iterate from 3 to n, constant space per iteration
    for i in range(3, n + 1):
        current = first + second  # Time: O(1), Space: O(1) - addition of two variables
        first = second  # Time: O(1), Space: O(1) - variable assignment
        second = current  # Time: O(1), Space: O(1) - variable assignment

    # Overall Time Complexity: O(n), Space Complexity: O(1)
    return second  # Time: O(1), Space: O(1) - return stored value
```

---

## 📊 Complexity Analysis

| Approach                    | Time Complexity | Space Complexity     |
|:----------------------------|:----------------|:---------------------|
| **Recursion (Brute Force)** | $O(2^n)$        | $O(n)$ (stack depth) |
| **Memoization**             | $O(n)$          | $O(n)$               |
| **Tabulation**              | $O(n)$          | $O(n)$               |
| **Optimized Tabulation**    | $O(n)$          | $O(1)$               |

