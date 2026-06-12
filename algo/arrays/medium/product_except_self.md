To help you visualize the **Prefix/Suffix Product** algorithm, let's break it down into a step-by-step visual logic
guide. This is exactly how you should "draw" it on a whiteboard during an interview to explain your strategy.

## **Infography: Product of Array Except Self (Strategy)**

### **The Core Concept: "The Sandwich"**

Instead of using division, we build the answer by multiplying two parts:

1. **Prefix:** The product of all numbers to the **left** of the index.
2. **Suffix:** The product of all numbers to the **right** of the index.

### **Step 1: The Prefix Pass (Left-to-Right)**

We initialize an output array with `1`. As we move right, each position stores the running product of everything that
came before it.

**Example Input:** `[1, 2, 3, 4]`

| Index | Calculation        | Prefix Value stored in `res` |
|-------|--------------------|------------------------------|
| **0** | (None to the left) | `1`                          |
| **1** | `1`                | `1`                          |
| **2** | `1 * 2`            | `2`                          |
| **3** | `1 * 2 * 3`        | `6`                          |

**`res` after Pass 1:** `[1, 1, 2, 6]`

### **Step 2: The Suffix Pass (Right-to-Left)**

Now we move backwards. We keep a `suffix` variable (starting at `1`). We multiply the existing value in our `res` array
by this `suffix`.

| Index | Existing `res[i]` | Suffix Variable | New `res[i]` | Update Suffix for next step |
|-------|-------------------|-----------------|--------------|-----------------------------|
| **3** | `6`               | `1`             | **6**        | `1 * 4 = 4`                 |
| **2** | `2`               | `4`             | **8**        | `4 * 3 = 12`                |
| **1** | `1`               | `12`            | **12**       | `12 * 2 = 24`               |
| **0** | `1`               | `24`            | **24**       | `24 * 1 = 24`               |

**Final `res`:** `[24, 12, 8, 6]`

### **The "Why" Behind the Logic**

* **Space Efficiency:** By using the `res` array to store the prefixes first, then updating it during the suffix pass,
  we avoid needing two separate auxiliary arrays. This achieves the ** extra space** requirement (since the result array
  usually doesn't count).
* **Robustness:** This method handles `0` perfectly. If there's a zero, it will eventually be multiplied into the
  `prefix` or `suffix` variables, correctly turning the other indices into zero.

### **Whiteboard Pro-Tip**

When you draw this, use two different colored markers if possible:

1. **Blue arrows** for the Left Right pass.
2. **Red arrows** for the Right Left pass.

This visual distinction shows the interviewer you have a deep mental model of the data flow.

**Would you like to try to code this specific "two-pass" logic now to see the tests pass, or are you ready for a new
Array challenge like "Longest Consecutive Sequence"?**