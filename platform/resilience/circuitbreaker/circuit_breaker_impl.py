"""Implementation of CircuitBreaker.

Thread-safety: All state transitions and counter updates protected by threading.Lock.
State machine: CLOSED -> OPEN (on failure_threshold failures)
               OPEN -> HALF_OPEN (after recovery_timeout_sec elapsed)
               HALF_OPEN -> CLOSED (on half_open_max_calls successes)
               HALF_OPEN -> OPEN (on any failure)
"""
import threading
from time import time
from typing import Any, Callable

from .circuit_breaker import CircuitBreaker


class CircuitBreakerImpl(CircuitBreaker):
    """Implementation of CircuitBreaker.

    Thread-safety: All state transitions and counter updates protected by threading.Lock.
    """

    def __init__(
            self,
            config: CircuitBreaker.Config,
            time_func: Callable[[], float] | None = None,
    ):
        self._config = config
        self._lock = threading.Lock()
        self._state = CircuitBreaker.State.CLOSED
        self._failure_count = 0
        self._success_count = 0
        self._half_open_calls = 0
        self._opened_at: float | None = None
        self._time_func: Callable[[], float] = time_func or time

    def call(self, func: Callable[[], Any]) -> Any:
        with self._lock:
            state = self._get_effective_state()
            if state == CircuitBreaker.State.OPEN:
                raise CircuitBreaker.CircuitBreakerOpen()
            if state == CircuitBreaker.State.HALF_OPEN:
                if self._half_open_calls >= self._config.half_open_max_calls:
                    raise CircuitBreaker.CircuitBreakerOpen()
                self._half_open_calls += 1

        try:
            result = func()
            self.record_success()
            return result
        except CircuitBreaker.CircuitBreakerOpen:
            raise
        except Exception:
            self.record_failure()
            raise

    def record_success(self) -> None:
        with self._lock:
            self._success_count += 1
            if self._state == CircuitBreaker.State.HALF_OPEN:
                if self._success_count >= self._config.half_open_max_calls:
                    self._transition_to(CircuitBreaker.State.CLOSED)

    def record_failure(self) -> None:
        with self._lock:
            self._failure_count += 1
            if self._state == CircuitBreaker.State.CLOSED:
                if self._failure_count >= self._config.failure_threshold:
                    self._transition_to(CircuitBreaker.State.OPEN)
            elif self._state == CircuitBreaker.State.HALF_OPEN:
                self._transition_to(CircuitBreaker.State.OPEN)

    def get_state(self) -> CircuitBreaker.State:
        with self._lock:
            return self._get_effective_state()

    def get_failure_count(self) -> int:
        with self._lock:
            return self._failure_count

    def get_success_count(self) -> int:
        with self._lock:
            return self._success_count

    def reset(self) -> None:
        with self._lock:
            self._transition_to(CircuitBreaker.State.CLOSED)

    # === Private helpers ===

    def _transition_to(self, state: CircuitBreaker.State) -> None:
        self._state = state
        self._failure_count = 0
        self._success_count = 0
        self._half_open_calls = 0
        if state == CircuitBreaker.State.OPEN:
            self._opened_at = self._time_func()
        else:
            self._opened_at = None

    def _get_effective_state(self) -> CircuitBreaker.State:
        """Return the effective state, handling OPEN->HALF_OPEN timeout transition.

        Must be called with self._lock held.
        """
        if self._state == CircuitBreaker.State.OPEN and self._opened_at is not None:
            if self._time_func() - self._opened_at >= self._config.recovery_timeout_sec:
                self._transition_to(CircuitBreaker.State.HALF_OPEN)
        return self._state
