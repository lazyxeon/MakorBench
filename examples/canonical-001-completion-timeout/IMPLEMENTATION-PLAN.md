# Executable Fixture Implementation Plan

## Objective

Convert the paper case into a deterministic-enough local distributed-system fixture without making the causal mechanism obvious from toy code.

## Proposed implementation language

Python is acceptable for the first public development fixture because:
- fast iteration;
- easy subprocess/service orchestration;
- easy deterministic fake clock/token rotation;
- straightforward pytest integration.

The benchmark concept must not depend on Python-specific behavior.

## Minimal services

1. **scheduler**
   - creates jobs and leases;
   - records completion transitions;
   - expires overdue leases;
   - runs optional reconciliation.

2. **worker**
   - consumes jobs;
   - writes artifact;
   - records billing side effect;
   - publishes completion through pooled client.

3. **completion gateway**
   - authenticates completion RPC;
   - forwards valid state transition to scheduler.

4. **token issuer / manager**
   - rotates service token under deterministic fake clock.

External dependencies should be simulated locally.

## Failure implementation

The bug should arise from composition:

- `TokenManager` refreshes correctly.
- `CompletionChannel` is correct when newly constructed.
- `ChannelPool` correctly reuses healthy channels.
- `AuthInterceptor` incorrectly snapshots the token at construction.

No individual subsystem should contain an obviously named `BUG` branch.

## Deterministic reproduction hook

The development fixture may expose an internal test-only fake clock so maintainers can force:

1. initial completion success;
2. token rotation;
3. post-rotation use of the same channel;
4. auth rejection.

The evaluated agent should not receive a "reproduce bug" helper that names the mechanism.

## Agent-visible data

Provide:
- source repository;
- multi-service logs;
- metrics CSV/JSON;
- sampled traces;
- normal test suite;
- shell and pytest.

Do not provide:
- oracle;
- counterfactual configs;
- reference patch;
- hidden mechanism-specific test name.

## Hidden tests

At minimum:

1. original scenario;
2. auth freshness across live-channel rotation;
3. valid auth still required;
4. duplicate completion remains idempotent;
5. billing not duplicated;
6. counterfactual rotation jitter;
7. counterfactual reconciliation disabled;
8. counterfactual pool-size/concurrency change;
9. non-auth transient retry behavior remains bounded.

## Reference repair

Preferred patch:
- interceptor obtains token from manager on each RPC metadata construction.

Equivalent patch:
- safe atomic pool invalidation on token refresh.

The grader should accept behavior, not exact diff.

## Difficulty tuning

If the case is too easy:
- reduce direct auth error verbosity;
- increase unrelated transport noise;
- sample traces;
- neutralize variable names that scream "stale token".

If too hard:
- expose channel age in logs/metrics;
- improve trace linkage;
- add local documentation for status code interpretation.

Difficulty should be tuned by human validation, not by hiding required evidence.

## Completion gate

The executable fixture is ready for pilot use when:
- oracle reproduction is deterministic;
- reference repair passes all hidden variants;
- >=3 human reviewers judge the prompt genuinely ambiguous;
- >=2 solve the root cause without hidden information;
- trivial baselines fail;
- CI reproduces the environment cleanly.
