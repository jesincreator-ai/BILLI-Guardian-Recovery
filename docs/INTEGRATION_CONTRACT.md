# M8 integration contract

M8 is the movement safety veto and diagnostics authority.

- Instantiate `GuardianManager` before enabling M7.
- It starts fail-closed (`allow_motion() == False`).
- Every supervisor cycle, create fresh `Telemetry` from the M7 heartbeat and verified sensors, then call `evaluate(telemetry, now_ms)`.
- Pass the manager object to M7 as its `guardian` dependency.
- Only after checking the robot and confirming a fresh safe snapshot may the operator path call `clear_faults(snapshot, now_ms, operator_ack=True)`.
- `RecoveryEngine.plan(faults)` produces allowlisted suggestions; integrate handlers explicitly and keep them bounded.
- Feed the independent hardware watchdog only after a successful supervisor cycle. Use a physical servo-power cut/enable circuit as a separate safety layer.

Missing or stale telemetry is treated as unsafe. Thresholds are starting values only and require hardware validation.
