"""
Async Circuit Breaker — asyncio-based variant of the Circuit Breaker pattern.

Mirrors the sync API but uses ``asyncio.Lock`` for state protection and accepts
async callables (``Callable[[], Awaitable[Any]]``).

Reuses ``Config``, ``State``, and ``CircuitBreakerOpen`` from the sync
``circuit_breaker.py`` to avoid duplication.
"""
from abc import ABC, abstractmethod
from typing import Awaitable, Callable, Any

from platform_challenges.resilience.circuitbreaker.circuit_breaker import CircuitBreaker

# Re-export shared types so consumers can import from either module.
Config = CircuitBreaker.Config
State = CircuitBreaker.State
CircuitBreakerOpen = CircuitBreaker.CircuitBreakerOpen


class AsyncCircuitBreaker(ABC):
    """Async circuit breaker. Coroutine-safe via ``asyncio.Lock``."""

    @classmethod
    def of(cls, config: Config) -> "AsyncCircuitBreaker":
        """Factory method.

        Args:
            config: Configuration parameters (failure_threshold, recovery_timeout_sec,
                    half_open_max_calls).

        Returns:
            A new AsyncCircuitBreaker instance.
        """
        from .async_circuit_breaker_impl import AsyncCircuitBreakerImpl
        return AsyncCircuitBreakerImpl(config)

    @abstractmethod
    async def call(self, func: Callable[[], Awaitable[Any]]) -> Any:
        """Execute an async function through the circuit breaker.

        If the circuit is OPEN, raises CircuitBreakerOpen immediately.
        If CLOSED or HALF_OPEN, awaits func and records success/failure.

        Args:
            func: A zero-argument async callable representing the downstream call.

        Returns:
            The return value of func if successful.

        Raises:
            CircuitBreakerOpen: when the circuit is open and calls are rejected.
            Exception: Propagates any exception raised by func.
        """
        ...

    @abstractmethod
    async def record_success(self) -> None:
        """Record a successful call. Coroutine-safe."""
        ...

    @abstractmethod
    async def record_failure(self) -> None:
        """Record a failed call. Coroutine-safe."""
        ...

    @abstractmethod
    async def get_state(self) -> State:
        """Get the current state of the circuit breaker."""
        ...

    @abstractmethod
    async def get_failure_count(self) -> int:
        """Get the current failure count in the current state window."""
        ...

    @abstractmethod
    async def get_success_count(self) -> int:
        """Get the current success count in the current state window."""
        ...

    @abstractmethod
    async def reset(self) -> None:
        """Reset the circuit breaker to CLOSED state with zero counters. Coroutine-safe."""
        ...
