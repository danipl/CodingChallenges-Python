"""
A thread-safe Circuit Breaker implementing the Circuit Breaker pattern.

Protects downstream services from cascading failures by detecting repeated errors
and short-circuiting requests before they reach the failing service. Used extensively
at Netflix (Hystrix), Stripe (API resilience), and RevenueCat (subscription service reliability).

Key behaviors:
  - Transitions through CLOSED → OPEN → HALF_OPEN states based on failure thresholds
  - Allows test requests in HALF_OPEN to probe downstream recovery
  - Tracks failure counts and success counts with configurable thresholds
  - Thread-safe for concurrent access across multiple request handlers
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Callable, Any


class CircuitBreaker(ABC):
    """Circuit breaker implementing the resilience pattern. Thread-safe for concurrent access."""

    @classmethod
    def of(cls, config: "Config") -> "CircuitBreaker":
        """Factory method.

        Creates a new CircuitBreaker instance with the given configuration.

        Args:
            config: Configuration parameters including failure threshold, recovery timeout,
                    and half-open max calls.

        Returns:
            A new CircuitBreaker instance.
        """
        from .circuit_breaker_impl import CircuitBreakerImpl
        return CircuitBreakerImpl(config)

    @abstractmethod
    def call(self, func: Callable[[], Any]) -> Any:
        """Execute a function through the circuit breaker.

        If the circuit is OPEN, raises CircuitBreakerOpen immediately without calling func.
        If the circuit is CLOSED or HALF_OPEN, executes func and records success/failure.

        Args:
            func: A zero-argument callable representing the downstream call.

        Returns:
            The return value of func if successful.

        Raises:
            CircuitBreakerOpen: when the circuit is open and calls are rejected.
            Exception: Propagates any exception raised by func.
        """
        ...

    @abstractmethod
    def record_success(self) -> None:
        """Record a successful call.

        In HALF_OPEN state, enough successes will transition to CLOSED.
        Thread-safe.
        """
        ...

    @abstractmethod
    def record_failure(self) -> None:
        """Record a failed call.

        In CLOSED state, enough failures will transition to OPEN.
        In HALF_OPEN state, any failure transitions back to OPEN.
        Thread-safe.
        """
        ...

    @abstractmethod
    def get_state(self) -> "State":
        """Get the current state of the circuit breaker.

        Returns:
            The current State (CLOSED, OPEN, or HALF_OPEN).
        """
        ...

    @abstractmethod
    def get_failure_count(self) -> int:
        """Get the current failure count in the current state window.

        Returns:
            Number of recorded failures since last state transition.
        """
        ...

    @abstractmethod
    def get_success_count(self) -> int:
        """Get the current success count in the current state window.

        Returns:
            Number of recorded successes since last state transition.
        """
        ...

    @abstractmethod
    def reset(self) -> None:
        """Reset the circuit breaker to CLOSED state with zero counters.

        Useful for manual recovery or testing.
        Thread-safe.
        """
        ...

    # === Nested types ===

    @dataclass
    class Config:
        """Configuration for the circuit breaker.

        Attributes:
            failure_threshold: Number of failures before opening the circuit. Must be >= 1.
            recovery_timeout_sec: Seconds to wait in OPEN state before transitioning to HALF_OPEN. Must be >= 0.
            half_open_max_calls: Number of test calls allowed in HALF_OPEN state. Must be >= 1.
        """
        failure_threshold: int = 5
        recovery_timeout_sec: float = 30.0
        half_open_max_calls: int = 1

        def __post_init__(self):
            """Validate configuration parameters."""
            if self.failure_threshold < 1:
                raise ValueError("failure_threshold must be >= 1")
            if self.recovery_timeout_sec < 0:
                raise ValueError("recovery_timeout_sec must be >= 0")
            if self.half_open_max_calls < 1:
                raise ValueError("half_open_max_calls must be >= 1")

    class CircuitBreakerOpen(Exception):
        """Exception raised when the circuit breaker is open and rejects calls."""
        pass

    class State(Enum):
        """States of the circuit breaker."""
        CLOSED = auto()
        OPEN = auto()
        HALF_OPEN = auto()
