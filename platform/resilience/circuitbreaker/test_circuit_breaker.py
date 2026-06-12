"""Tests for CircuitBreaker."""
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import Mock, patch

from .circuit_breaker import CircuitBreaker


def _make_instance():
    return CircuitBreaker.of(CircuitBreaker.Config(
        failure_threshold=3,
        recovery_timeout_sec=30.0,
        half_open_max_calls=1,
    ))


class TestBasicBehavior(unittest.TestCase):
    def setUp(self):
        self.instance = _make_instance()

    def test_initial_state_is_closed(self):
        self.assertEqual(CircuitBreaker.State.CLOSED, self.instance.get_state())

    def test_initial_counters_are_zero(self):
        self.assertEqual(0, self.instance.get_failure_count())
        self.assertEqual(0, self.instance.get_success_count())

    def test_call_succeeds_in_closed_state(self):
        func = Mock(return_value="ok")
        result = self.instance.call(func)
        self.assertEqual("ok", result)
        func.assert_called_once()

    def test_call_propagates_exception(self):
        func = Mock(side_effect=ValueError("downstream error"))
        with self.assertRaises(ValueError):
            self.instance.call(func)

    def test_record_success_increments_counter(self):
        self.instance.record_success()
        self.instance.record_success()
        self.assertEqual(2, self.instance.get_success_count())

    def test_record_failure_increments_counter(self):
        self.instance.record_failure()
        self.instance.record_failure()
        self.assertEqual(2, self.instance.get_failure_count())

    def test_reset_returns_to_closed(self):
        self.instance.record_failure()
        self.instance.record_failure()
        self.instance.reset()
        self.assertEqual(CircuitBreaker.State.CLOSED, self.instance.get_state())
        self.assertEqual(0, self.instance.get_failure_count())
        self.assertEqual(0, self.instance.get_success_count())


class TestEdgeCases(unittest.TestCase):
    def setUp(self):
        self.instance = _make_instance()

    def test_config_validation_rejects_zero_threshold(self):
        with self.assertRaises(ValueError):
            CircuitBreaker.of(CircuitBreaker.Config(failure_threshold=0))

    def test_config_validation_rejects_negative_threshold(self):
        with self.assertRaises(ValueError):
            CircuitBreaker.of(CircuitBreaker.Config(failure_threshold=-1))

    def test_config_validation_rejects_negative_timeout(self):
        with self.assertRaises(ValueError):
            CircuitBreaker.of(CircuitBreaker.Config(recovery_timeout_sec=-1.0))

    def test_config_validation_rejects_zero_half_open_calls(self):
        with self.assertRaises(ValueError):
            CircuitBreaker.of(CircuitBreaker.Config(half_open_max_calls=0))

    def test_config_accepts_zero_timeout(self):
        cb = CircuitBreaker.of(CircuitBreaker.Config(recovery_timeout_sec=0))
        self.assertIsNotNone(cb)

    def test_call_with_none_return_value(self):
        func = Mock(return_value=None)
        result = self.instance.call(func)
        self.assertIsNone(result)


class TestFailureModes(unittest.TestCase):
    def setUp(self):
        self.instance = _make_instance()

    def test_opens_after_threshold_failures(self):
        self.instance.record_failure()
        self.instance.record_failure()
        self.instance.record_failure()
        self.assertEqual(CircuitBreaker.State.OPEN, self.instance.get_state())

    def test_rejects_calls_when_open(self):
        self.instance.record_failure()
        self.instance.record_failure()
        self.instance.record_failure()
        func = Mock(return_value="ok")
        with self.assertRaises(CircuitBreaker.CircuitBreakerOpen):
            self.instance.call(func)

    def test_transitions_to_half_open_after_timeout(self):
        with patch.object(self.instance, "_time_func", return_value=100.0):
            self.instance.record_failure()
            self.instance.record_failure()
            self.instance.record_failure()
            self.assertEqual(CircuitBreaker.State.OPEN, self.instance.get_state())
        with patch.object(self.instance, "_time_func", return_value=131.0):
            state = self.instance.get_state()
        self.assertEqual(CircuitBreaker.State.HALF_OPEN, state)

    def test_half_open_failure_returns_to_open(self):
        with patch.object(self.instance, "_time_func", return_value=100.0):
            self.instance.record_failure()
            self.instance.record_failure()
            self.instance.record_failure()
        with patch.object(self.instance, "_time_func", return_value=131.0):
            self.instance.get_state()
        self.instance.record_failure()
        self.assertEqual(CircuitBreaker.State.OPEN, self.instance.get_state())

    def test_half_open_success_closes_circuit(self):
        with patch.object(self.instance, "_time_func", return_value=100.0):
            self.instance.record_failure()
            self.instance.record_failure()
            self.instance.record_failure()
        with patch.object(self.instance, "_time_func", return_value=131.0):
            self.instance.get_state()
        self.instance.record_success()
        self.assertEqual(CircuitBreaker.State.CLOSED, self.instance.get_state())

    def test_failure_count_resets_on_state_change(self):
        self.instance.record_failure()
        self.instance.record_failure()
        self.instance.record_failure()
        self.assertEqual(CircuitBreaker.State.OPEN, self.instance.get_state())
        self.instance.reset()
        self.assertEqual(0, self.instance.get_failure_count())


class TestThreadSafety(unittest.TestCase):
    def setUp(self):
        self.instance = CircuitBreaker.of(CircuitBreaker.Config(
            failure_threshold=100,
            recovery_timeout_sec=30.0,
            half_open_max_calls=1,
        ))

    def test_concurrent_record_success(self):
        thread_count = 20
        ops_per_thread = 100
        errors = []
        barrier = threading.Barrier(thread_count)

        def worker():
            barrier.wait()
            for _ in range(ops_per_thread):
                try:
                    self.instance.record_success()
                except Exception as e:
                    errors.append(e)

        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            futures = [executor.submit(worker) for _ in range(thread_count)]
            for f in futures:
                f.result(timeout=30)

        self.assertEqual([], errors, "No exceptions during concurrent access")
        self.assertEqual(
            thread_count * ops_per_thread,
            self.instance.get_success_count(),
        )

    def test_concurrent_record_failure(self):
        thread_count = 20
        ops_per_thread = 100
        errors = []
        barrier = threading.Barrier(thread_count)

        def worker():
            barrier.wait()
            for _ in range(ops_per_thread):
                try:
                    self.instance.record_failure()
                except Exception as e:
                    errors.append(e)

        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            futures = [executor.submit(worker) for _ in range(thread_count)]
            for f in futures:
                f.result(timeout=30)

        self.assertEqual([], errors, "No exceptions during concurrent access")

    def test_concurrent_mixed_operations(self):
        thread_count = 20
        ops_per_thread = 50
        errors = []
        barrier = threading.Barrier(thread_count)

        def worker():
            barrier.wait()
            for i in range(ops_per_thread):
                try:
                    if i % 2 == 0:
                        self.instance.record_success()
                    else:
                        self.instance.record_failure()
                    self.instance.get_state()
                    self.instance.get_failure_count()
                    self.instance.get_success_count()
                except Exception as e:
                    errors.append(e)

        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            futures = [executor.submit(worker) for _ in range(thread_count)]
            for f in futures:
                f.result(timeout=30)

        self.assertEqual([], errors, "No exceptions during concurrent access")


if __name__ == "__main__":
    unittest.main()
