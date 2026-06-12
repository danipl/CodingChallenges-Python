# Challenge 01: Circuit Breaker — Live Coding Guidelines

## 1. Challenge Presentation

### What You're Building

A thread-safe Circuit Breaker that protects downstream services from cascading failures. When a downstream service
starts failing repeatedly, the circuit breaker "trips" and rejects calls immediately, giving the failing service time to
recover. This pattern is foundational at Netflix (Hystrix), Stripe (API resilience), and every platform team handling
external dependencies.

### Core Contract

```
CLOSED ──(failures >= threshold)──> OPEN ──(timeout elapsed)──> HALF_OPEN
  ▲                                    │                              │
  │                                    │                              │
  └────(successes in HALF_OPEN)────────┘                              │
                                                                      │
                                   (any failure in HALF_OPEN) ────────┘
```

- **CLOSED**: Normal operation. Calls pass through. Failures are counted.
- **OPEN**: Calls are rejected immediately with `CircuitBreakerOpen`. After `recovery_timeout_sec`, transitions to
  HALF_OPEN.
- **HALF_OPEN**: Limited test calls allowed. Success → CLOSED. Any failure → OPEN.

### Interface Summary

| Method                | Purpose                                                                  |
|-----------------------|--------------------------------------------------------------------------|
| `of(config)`          | Factory — creates CircuitBreaker with validated config                   |
| `call(func)`          | Execute a function through the breaker; rejects if OPEN                  |
| `record_success()`    | Increment success counter; may trigger HALF_OPEN → CLOSED                |
| `record_failure()`    | Increment failure counter; may trigger CLOSED → OPEN or HALF_OPEN → OPEN |
| `get_state()`         | Return current State (CLOSED, OPEN, HALF_OPEN)                           |
| `get_failure_count()` | Return failure count in current window                                   |
| `get_success_count()` | Return success count in current window                                   |
| `reset()`             | Manually reset to CLOSED with zeroed counters                            |

### What Interviewers Evaluate (Staff-Level)

1. **Failure Mode Reasoning** — Can you identify the three states and their transitions? Do you handle the HALF_OPEN
   probe correctly?
2. **Thread Safety** — State transitions are concurrent; can you protect them without over-locking?
3. **Observability Mindset** — Do you expose counters (failure_count, success_count) for monitoring?
4. **Testability** — Do you inject `time_func` so tests can control time without sleeping?
5. **Tradeoff Articulation** — Why `Lock` vs `RLock`? What happens if recovery_timeout is 0?

---

## 2. Edge & Corner Cases

### How to Identify Them Before Coding

Think about each state transition boundary and what happens at the edges: exact threshold values, time boundaries, and
concurrent access patterns.

| # | Edge Case                                               | How It Surfaces                              | How to Handle                                                   |
|---|---------------------------------------------------------|----------------------------------------------|-----------------------------------------------------------------|
| 1 | **Exact threshold boundary**                            | 2 failures out of 3 — should still be CLOSED | Use `>=` comparison, not `>`                                    |
| 2 | **Recovery timeout of 0**                               | Should transition to HALF_OPEN immediately   | Treat as valid; check `now >= opened_at + 0`                    |
| 3 | **Multiple threads checking OPEN state simultaneously** | Race on timeout check                        | Check transition inside the lock                                |
| 4 | **Failure in HALF_OPEN with multiple allowed calls**    | Should immediately go back to OPEN           | Any failure in HALF_OPEN → OPEN, regardless of call count       |
| 5 | **Success count not reset on state change**             | Old successes pollute new state window       | Reset counters on every state transition                        |
| 6 | **func raises non-Exception (e.g., KeyboardInterrupt)** | Should not be swallowed                      | Let BaseException propagate; only catch Exception for recording |

### Quick Pre-Implementation Checklist

```
▢ State transitions are atomic (under lock)
▢ Counters reset on every state change
▢ get_state() checks timeout and may trigger OPEN → HALF_OPEN
▢ call() checks state before executing func
▢ Time is injectable for testability
```

---

## 3. First Approach — Chain of Thinking

### Minute 0-2: Clarify Requirements

- "Should the circuit breaker track successes in CLOSED state, or only failures?"
- "What happens if the downstream call times out — is that a failure?"
- "Should HALF_OPEN allow multiple test calls or just one?"
- "Do we need metrics beyond failure/success counts?"

### Minute 2-5: Design

```python
# Fields
_state: State = CLOSED
_failure_count: int = 0
_success_count: int = 0
_half_open_calls: int = 0
_opened_at: float | None = None
_lock: threading.Lock
_time_func: Callable[[], float]
_config: Config
```

Data structures: plain integers (protected by lock), Enum for state, float for timestamp.

### Minute 5-10: Sketch the Core Flow

```python
def call(self, func):
    with self._lock:
        self._check_state_transition()  # OPEN -> HALF_OPEN if timeout elapsed
        if self._state == OPEN:
            raise CircuitBreakerOpen()
        if self._state == HALF_OPEN:
            self._half_open_calls += 1
    try:
        result = func()
        self.record_success()
        return result
    except Exception:
        self.record_failure()
        raise
```

### Minute 10-25: Implement

1. `__init__` — set fields, lock, time_func
2. `_transition_to` — set state, reset all counters
3. `get_state` — check timeout, trigger OPEN → HALF_OPEN
4. `record_failure` — increment, check threshold, transition if needed
5. `record_success` — increment, check half_open threshold, transition if needed
6. `call` — state check, execute func, record result
7. `reset` — force CLOSED, zero everything

---

## 4. Communication Approach During the Interview

### What to Say Out Loud

| Moment                  | Say This                                                                                                                         |
|-------------------------|----------------------------------------------------------------------------------------------------------------------------------|
| Starting                | "I'll model this as a state machine with three states: CLOSED, OPEN, HALF_OPEN. All transitions are protected by a single lock." |
| About state transitions | "I check the timeout in get_state() so the OPEN → HALF_OPEN transition is lazy — no background thread needed."                   |
| About thread safety     | "Single Lock is sufficient here — we have one writer pattern (state changes) and the critical section is small."                 |
| About failure handling  | "call() wraps the func execution: on success, record_success; on exception, record_failure and re-raise."                        |
| About tradeoffs         | "RLock would work too but adds overhead. Since we don't have reentrant calls, Lock is simpler and faster."                       |

### When Stuck

```
I notice the call() method needs to check state, execute, and record — but recording also acquires the lock.
The risk is deadlock if I nest lock acquisitions.
Two options: (A) use RLock, or (B) release lock before calling func and re-acquire for recording.
I'll go with (B) because it minimizes lock hold time during the actual downstream call. Does that align with your expectations?
```

---

## 5. Implementation Structure

### Recommended File Layout

```python
class CircuitBreakerImpl(CircuitBreaker):
    def __init__(self, config, time_func=None):

    # === Fields ===
    # === Lock ===
    # === Time injection ===

    def call(self, func):

    # === Check state (may trigger OPEN -> HALF_OPEN) ===
    # === Reject if OPEN ===
    # === Execute func (outside lock) ===
    # === Record result ===

    def record_success(self):

    # === Increment counter ===
    # === Check HALF_OPEN -> CLOSED threshold ===

    def record_failure(self):

    # === Increment counter ===
    # === Check CLOSED -> OPEN or HALF_OPEN -> OPEN threshold ===

    def get_state(self):

    # === Check OPEN -> HALF_OPEN timeout ===
    # === Return current state ===

    def _transition_to(self, state):
# === Set state ===
# === Reset all counters ===
```

### Key Implementation Pattern

```python
def call(self, func):
    with self._lock:
        self._check_state_transition()
        if self._state == CircuitBreaker.State.OPEN:
            raise CircuitBreaker.CircuitBreakerOpen()

    try:
        result = func()
    except Exception:
        self.record_failure()
        raise

    self.record_success()
    return result
```

Note: The lock is released before calling `func()` to avoid holding it during the potentially slow downstream call.
`record_success()` and `record_failure()` acquire their own lock internally.

---

## 6. Technical Pro Tips

### State Machine Design

| Pattern      | Lazy Check (this challenge)           | Active Timer                           |
|--------------|---------------------------------------|----------------------------------------|
| How it works | Check timeout on get_state()/call()   | Background thread fires after timeout  |
| Pros         | No threads, simpler, no race on timer | Immediate transition                   |
| Cons         | Transition delayed until next call    | Thread overhead, shutdown complexity   |
| Used by      | Most in-process implementations       | Distributed systems with health probes |

### Python-Specific

- `threading.Lock` is non-reentrant — if `call()` holds the lock and calls `record_failure()` which also acquires it,
  you get a deadlock. Solution: release lock before calling `func()`.
- Use `Callable[[], Any]` for the func parameter — zero args, any return type.
- `dataclass.__post_init__` is the idiomatic place for config validation.

### What Staff Engineers Demonstrate

1. **Failure in Mind** — The circuit breaker exists because networks fail. Design for the failure case first.
2. **Lazy over Eager** — No background thread for timeout; check on demand. Simpler, fewer failure modes.
3. **Lock Minimization** — Don't hold the lock during the downstream call. Acquire for state check, release, call func,
   re-acquire for recording.
4. **Testability Built-In** — Inject `time_func` so tests can control time without `time.sleep()`.

---

## 7. Common Mistakes to Avoid

| Mistake                                               | Why It Fails                                                               | Fix                                                                   |
|-------------------------------------------------------|----------------------------------------------------------------------------|-----------------------------------------------------------------------|
| Holding lock during func() call                       | Deadlock if record_failure re-acquires; blocks other threads unnecessarily | Release lock before calling func(), re-acquire for recording          |
| Using `>` instead of `>=` for threshold               | Off-by-one: needs N+1 failures to trip                                     | Use `>= failure_threshold`                                            |
| Not resetting counters on state change                | Old counts pollute new state window                                        | Reset failure_count, success_count, half_open_calls in _transition_to |
| No time injection                                     | Tests must sleep or mock time globally                                     | Accept `time_func` in __init__, default to `time.time`                |
| Transitioning OPEN → HALF_OPEN in a background thread | Adds complexity, shutdown issues, race conditions                          | Check lazily in get_state() or call()                                 |
| Swallowing exceptions from func()                     | Caller never knows the call failed                                         | Re-raise after recording failure                                      |

---

## 8. Verification Checklist

### Functional

- [ ] Initial state is CLOSED with zero counters
- [ ] call() executes func and returns result in CLOSED state
- [ ] call() raises CircuitBreakerOpen when circuit is OPEN
- [ ] Circuit transitions to OPEN after failure_threshold failures
- [ ] Circuit transitions to HALF_OPEN after recovery_timeout
- [ ] HALF_OPEN success transitions to CLOSED
- [ ] HALF_OPEN failure transitions back to OPEN
- [ ] reset() returns to CLOSED with zeroed counters

### Resilience / Failure Modes

- [ ] Exceptions from func() are propagated (not swallowed)
- [ ] Timeout of 0 works (immediate HALF_OPEN transition)
- [ ] Config validation rejects invalid values

### Observability

- [ ] get_failure_count() returns accurate count
- [ ] get_success_count() returns accurate count
- [ ] get_state() reflects current state (including lazy timeout check)

### Thread Safety

- [ ] Concurrent record_success calls are safe (no lost updates)
- [ ] Concurrent record_failure calls are safe
- [ ] Concurrent mixed reads/writes are safe

### Edge Cases

- [ ] func returning None is handled
- [ ] Exact threshold boundary (N-1 failures = still CLOSED)
- [ ] Counters reset on state transition

---

## 9. Extension Points (Bonus Discussion)

- **How would you add metrics?** — Integrate with a metrics library (Prometheus counters, histograms for call duration).
- **How would you make this distributed?** — Use Redis or etcd for shared state; multiple processes need coordinated
  circuit state.
- **How would you handle per-endpoint breakers?** — Factory that creates one breaker per endpoint key; consider memory
  limits for unbounded endpoints.
- **What about async support?** — `async def call()` with `await func()`; same state machine, but use `asyncio.Lock`
  instead of `threading.Lock`.
- **How would you add a sliding window?** — Instead of raw counters, track timestamps of failures in a
  `collections.deque`; only count failures within the last N seconds.

---

## 10. Production References

| Resource                                                                                  | Why It Matters                                                         |
|-------------------------------------------------------------------------------------------|------------------------------------------------------------------------|
| [Netflix Hystrix](https://github.com/Netflix/Hystrix)                                     | Original circuit breaker implementation; inspired the entire pattern   |
| [Resilience4j CircuitBreaker](https://resilience4j.readme.io/docs/circuitbreaker)         | Modern Java implementation with sliding window, metrics, and events    |
| [AWS Retry Mode](https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-mode.html) | Standard retry strategies that complement circuit breakers             |
| [Stripe API Resilience](https://stripe.com/docs/api/errors)                               | How Stripe handles API failures and recommends client-side resilience  |
| [Polly.NET](https://github.com/App-vNext/Polly)                                           | .NET resilience library with circuit breaker, retry, bulkhead patterns |
| [Martin Fowler - Circuit Breaker](https://martinfowler.com/bliki/CircuitBreaker.html)     | Original pattern description; foundational reading                     |

---

*This guideline follows the standard platform challenge template: presentation → edge cases → chain of thinking →
communication → implementation → pro tips → mistakes → verification → extensions → references.*
