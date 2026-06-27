"""Async implementation of CircuitBreaker.

Coroutine-safety: All state transitions and counter updates protected by asyncio.Lock.
State machine: CLOSED -> OPEN (on failure_threshold failures)
               OPEN -> HALF_OPEN (after recovery_timeout_sec elapsed)
               HALF_OPEN -> CLOSED (on half_open_max_calls successes)
               HALF_OPEN -> OPEN (on any failure)
"""
import asyncio
from typing import Any, Awaitable, Callable

from .async_circuit_breaker import AsyncCircuitBreaker, Config, State, CircuitBreakerOpen


class AsyncCircuitBreakerImpl(AsyncCircuitBreaker):
    """Async circuit breaker implementation using ``asyncio.Lock``."""

    def __init__(
        self,
        config: Config,
        time_func: Callable[[], float] | None = None,
    ):
        self._config = config
        self._lock = asyncio.Lock()
        self._state = State.CLOSED
        self._failure_count = 0
        self._success_count = 0
        self._half_open_calls = 0
        self._opened_at: float | None = None
        if time_func is not None:
            self._time_func = time_func
        else:
            import time
            self._time_func = time.time

    async def call(self, func: Callable[[], Awaitable[Any]]) -> Any:
        async with self._lock:
            state = self._get_effective_state()
            if state == State.OPEN:
                raise CircuitBreakerOpen()
            if state == State.HALF_OPEN:
                if self._half_open_calls >= self._config.half_open_max_calls:
                    raise CircuitBreakerOpen()
                self._half_open_calls += 1

        try:
            result = await func()
            await self.record_success()
            return result
        except CircuitBreakerOpen:
            raise
        except Exception:
            await self.record_failure()
            raise

    async def record_success(self) -> None:
        async with self._lock:
            self._success_count += 1
            if self._state == State.HALF_OPEN:
                if self._success_count >= self._config.half_open_max_calls:
                    self._transition_to(State.CLOSED)

    async def record_failure(self) -> None:
        async with self._lock:
            self._failure_count += 1
            if self._state == State.CLOSED:
                if self._failure_count >= self._config.failure_threshold:
                    self._transition_to(State.OPEN)
            elif self._state == State.HALF_OPEN:
                self._transition_to(State.OPEN)

    async def get_state(self) -> State:
        async with self._lock:
            return self._get_effective_state()

    async def get_failure_count(self) -> int:
        async with self._lock:
            return self._failure_count

    async def get_success_count(self) -> int:
        async with self._lock:
            return self._success_count

    async def reset(self) -> None:
        async with self._lock:
            self._transition_to(State.CLOSED)

    # === Private helpers (must be called with self._lock held) ===

    def _transition_to(self, state: State) -> None:
        self._state = state
        self._failure_count = 0
        self._success_count = 0
        self._half_open_calls = 0
        if state == State.OPEN:
            self._opened_at = self._time_func()
        else:
            self._opened_at = None

    def _get_effective_state(self) -> State:
        """Return the effective state, handling OPEN->HALF_OPEN timeout transition.

        Must be called with self._lock held.
        """
        if self._state == State.OPEN and self._opened_at is not None:
            if self._time_func() - self._opened_at >= self._config.recovery_timeout_sec:
                self._transition_to(State.HALF_OPEN)
        return self._state
