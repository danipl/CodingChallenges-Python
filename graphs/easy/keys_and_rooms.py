import collections
import unittest
from typing import List

"""
PYTHON INTERVIEW CHEAT-SHEET: GRAPHS (EASY - TRAVERSAL)
------------------------------------------
1. `collections.deque`: O(1) popleft() for BFS. Never use `list.pop(0)` — it's O(n).
2. `set` for visited tracking: O(1) average lookup to check if a node was already explored.
3. Adjacency list as `List[List[int]]`: each index is a node, its value is a list of neighbors.
4. BFS vs DFS: BFS uses a queue (deque), DFS uses a stack (list with append/pop).
   Both visit every reachable node — choose based on whether you need shortest path (BFS).
5. `len(visited) == n`: Quick way to check if all nodes in an n-node graph were reached.
"""


class Solution:
    def canVisitAllRooms(self, rooms: List[List[int]]) -> bool:
        """
        PROBLEM: Keys and Rooms
        There are n rooms labeled from 0 to n - 1. All rooms are locked except room 0.
        You start in room 0 and each room contains a set of room_keys to other rooms.
        When you visit a room, you collect all its room_keys. Each key opens exactly one room.

        Determine if you can visit every room.

        REQUIREMENTS:
        - Return True if all rooms can be visited, False otherwise.
        - Room 0 is always accessible (you start there).
        - Keys can be collected in any order — this is a graph reachability problem.
        - Time Complexity must be O(N + K) where N = number of rooms, K = total room_keys.
        - Space Complexity must be O(N) for visited set and queue/stack.

        :param rooms: List of lists where rooms[i] contains room_keys found in room i.
        :return: True if all rooms are reachable from room 0, False otherwise.

        Example 1:
            Input: [[1], [2], [3], []]
            Output: True
            Explanation: Room 0 → key to 1 → key to 2 → key to 3. All visited.

        Example 2:
            Input: [[1, 3], [3, 0, 1], [2], [0]]
            Output: False
            Explanation: Room 2 is unreachable — no key to room 2 exists in any room.
        """
        if not rooms:
            return True

        visited_rooms = {0}
        keys = collections.deque(rooms[0])

        # Space: O(N) - visited set + deque, both bounded by number of rooms
        # Time: O(N + K) - each room visited once, each key processed once
        while keys:
            if len(visited_rooms) == len(rooms):
                return True
            current_key = keys.popleft()
            if current_key not in visited_rooms:
                visited_rooms.add(current_key)
                keys.extend(rooms[current_key])

        # Overall Time Complexity: O(N + K) - visit each room once, process each key once
        # Overall Space Complexity: O(N) - visited set + deque bounded by room count
        if len(visited_rooms) == len(rooms):
            return True

        return False


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_linear_chain(self):
        """Each room has key to the next — all reachable."""
        self.assertTrue(self.sol.canVisitAllRooms([[1], [2], [3], []]))

    def test_unreachable_room(self):
        """No key exists for room 2 — cannot visit all."""
        self.assertFalse(self.sol.canVisitAllRooms([[1, 3], [3, 0, 1], [2], [0]]))

    def test_single_room(self):
        """Only room 0 exists — trivially true."""
        self.assertTrue(self.sol.canVisitAllRooms([[]]))

    def test_all_keys_in_room_zero(self):
        """Room 0 has keys to every other room."""
        self.assertTrue(self.sol.canVisitAllRooms([[1, 2, 3], [], [], []]))

    def test_cyclic_keys(self):
        """Rooms form a cycle — all reachable."""
        self.assertTrue(self.sol.canVisitAllRooms([[1], [2], [0]]))

    def test_disconnected_components(self):
        """Two separate groups of rooms — second group unreachable."""
        self.assertFalse(self.sol.canVisitAllRooms([[1], [0], [3], [2]]))

    def test_duplicate_keys(self):
        """Duplicate keys should not affect traversal."""
        self.assertTrue(self.sol.canVisitAllRooms([[1, 1], [2, 2], [0, 0]]))

    def test_self_loop(self):
        """Room contains key to itself — should not cause infinite loop."""
        self.assertTrue(self.sol.canVisitAllRooms([[0, 1], [2], [1]]))


if __name__ == "__main__":
    unittest.main()
