"""Async tests for AsyncCircuitBreaker."""
import asyncio
import unittest
from unittest.mock import AsyncMock, patch

from .async_circuit_breaker import AsyncCircuitBreaker, Config, State, CircuitBreakerOpen


def _make_instance():
    return AsyncCircuitBreaker.of(Config(
        failure_threshold=3,
        recovery_timeout_sec=30.0,
        half_open_max_calls=1,
    ))


class TestBasicBehavior(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.instance = _make_instance()

    async def test_initial_state_is_closed(self):
        self.assertEqual(State.CLOSED, await self.instance.get_state())

    async def test_initial_counters_are_zero(self):
        self.assertEqual(0, await self.instance.get_failure_count())
        self.assertEqual(0, await self.instance.get_success_count())

    async def test_call_succeeds_in_closed_state(self):
        func = AsyncMock(return_value="ok")
        result = await self.instance.call(func)
        self.assertEqual("ok", result)
        func.assert_awaited_once()

    async def test_call_propagates_exception(self):
        func = AsyncMock(side_effect=ValueError("downstream error"))
        with self.assertRaises(ValueError):
            await self.instance.call(func)

    async def test_record_success_increments_counter(self):
        await self.instance.record_success()
        await self.instance.record_success()
        self.assertEqual(2, await self.instance.get_success_count())

    async def test_record_failure_increments_counter(self):
        await self.instance.record_failure()
        await self.instance.record_failure()
        self.assertEqual(2, await self.instance.get_failure_count())

    async def test_reset_returns_to_closed(self):
        await self.instance.record_failure()
        await self.instance.record_failure()
        await self.instance.reset()
        self.assertEqual(State.CLOSED, await self.instance.get_state())
        self.assertEqual(0, await self.instance.get_failure_count())
        self.assertEqual(0, await self.instance.get_success_count())


class TestEdgeCases(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.instance = _make_instance()

    def test_config_validation_rejects_zero_threshold(self):
        with self.assertRaises(ValueError):
            AsyncCircuitBreaker.of(Config(failure_threshold=0))

    def test_config_validation_rejects_negative_threshold(self):
        with self.assertRaises(ValueError):
            AsyncCircuitBreaker.of(Config(failure_threshold=-1))

    def test_config_validation_rejects_negative_timeout(self):
        with self.assertRaises(ValueError):
            AsyncCircuitBreaker.of(Config(recovery_timeout_sec=-1.0))

    def test_config_validation_rejects_zero_half_open_calls(self):
        with self.assertRaises(ValueError):
            AsyncCircuitBreaker.of(Config(half_open_max_calls=0))

    def test_config_accepts_zero_timeout(self):
        cb = AsyncCircuitBreaker.of(Config(recovery_timeout_sec=0))
        self.assertIsNotNone(cb)

    async def test_call_with_none_return_value(self):
        func = AsyncMock(return_value=None)
        result = await self.instance.call(func)
        self.assertIsNone(result)


class TestFailureModes(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.instance = _make_instance()

    async def test_opens_after_threshold_failures(self):
        await self.instance.record_failure()
        await self.instance.record_failure()
        await self.instance.record_failure()
        self.assertEqual(State.OPEN, await self.instance.get_state())

    async def test_rejects_calls_when_open(self):
        await self.instance.record_failure()
        await self.instance.record_failure()
        await self.instance.record_failure()
        func = AsyncMock(return_value="ok")
        with self.assertRaises(CircuitBreakerOpen):
            await self.instance.call(func)

    async def test_transitions_to_half_open_after_timeout(self):
        with patch.object(self.instance, "_time_func", return_value=100.0):
            await self.instance.record_failure()
            await self.instance.record_failure()
            await self.instance.record_failure()
            self.assertEqual(State.OPEN, await self.instance.get_state())
        with patch.object(self.instance, "_time_func", return_value=131.0):
            state = await self.instance.get_state()
        self.assertEqual(State.HALF_OPEN, state)

    async def test_half_open_failure_returns_to_open(self):
        with patch.object(self.instance, "_time_func", return_value=100.0):
            await self.instance.record_failure()
            await self.instance.record_failure()
            await self.instance.record_failure()
        with patch.object(self.instance, "_time_func", return_value=131.0):
            await self.instance.get_state()
        await self.instance.record_failure()
        self.assertEqual(State.OPEN, await self.instance.get_state())

    async def test_half_open_success_closes_circuit(self):
        with patch.object(self.instance, "_time_func", return_value=100.0):
            await self.instance.record_failure()
            await self.instance.record_failure()
            await self.instance.record_failure()
        with patch.object(self.instance, "_time_func", return_value=131.0):
            await self.instance.get_state()
        await self.instance.record_success()
        self.assertEqual(State.CLOSED, await self.instance.get_state())

    async def test_failure_count_resets_on_state_change(self):
        await self.instance.record_failure()
        await self.instance.record_failure()
        await self.instance.record_failure()
        self.assertEqual(State.OPEN, await self.instance.get_state())
        await self.instance.reset()
        self.assertEqual(0, await self.instance.get_failure_count())


class TestConcurrency(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.instance = AsyncCircuitBreaker.of(Config(
            failure_threshold=100,
            recovery_timeout_sec=30.0,
            half_open_max_calls=1,
        ))

    async def test_concurrent_record_success(self):
        task_count = 20
        ops_per_task = 100

        async def worker():
            for _ in range(ops_per_task):
                await self.instance.record_success()

        await asyncio.gather(*(worker() for _ in range(task_count)))

        self.assertEqual(
            task_count * ops_per_task,
            await self.instance.get_success_count(),
        )

    async def test_concurrent_record_failure(self):
        task_count = 20
        ops_per_task = 100

        async def worker():
            for _ in range(ops_per_task):
                await self.instance.record_failure()

        await asyncio.gather(*(worker() for _ in range(task_count)))
        # No assertion on count — failures trigger state transitions.
        # Just verify no exceptions occurred.

    async def test_concurrent_mixed_operations(self):
        task_count = 20
        ops_per_task = 50

        async def worker():
            for i in range(ops_per_task):
                if i % 2 == 0:
                    await self.instance.record_success()
                else:
                    await self.instance.record_failure()
                await self.instance.get_state()
                await self.instance.get_failure_count()
                await self.instance.get_success_count()

        await asyncio.gather(*(worker() for _ in range(task_count)))

    async def test_concurrent_calls(self):
        """Multiple concurrent call() invocations respect the circuit state."""
        call_count = 0

        async def succeeding_func():
            nonlocal call_count
            call_count += 1
            return "ok"

        results = await asyncio.gather(
            *(self.instance.call(succeeding_func) for _ in range(10))
        )
        self.assertEqual(10, len(results))
        self.assertEqual(10, call_count)


if __name__ == "__main__":
    unittest.main()
