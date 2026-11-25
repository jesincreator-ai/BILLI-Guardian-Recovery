# BILLI Guardian & Recovery (M8)

Offline safety supervisor for BILLI R-20. It checks local telemetry, latches a motion veto on unsafe or missing data, records bounded diagnostic logs, and proposes a small allowlisted set of recovery actions. No cloud connection, network service, LLM or automatic firmware rewrite is used.

## Safety behavior

- Fail-closed: missing heartbeat, battery reading or tilt reading denies movement.
- Trips and latches on stale heartbeat, sensor failure, low battery, over-tilt, servo fault or over-temperature.
- `allow_motion()` remains false after a trip until an operator acknowledgment is supplied and a fresh telemetry snapshot passes all checks.
- Recovery suggestions are fixed local actions. No code writes firmware, changes calibration, clears faults automatically or restarts the board.
- Diagnostic ring buffer has a fixed capacity.
- Watchdog feed helper feeds only after a healthy supervisor cycle. The ESP32 hardware WDT is an additional reset mechanism, not a substitute for power-stage safety.

## Desktop tests and simulation

```bash
python -m unittest discover -s tests -v
python examples/simulate_fault.py
```

## Hardware integration

1. Call `GuardianManager.evaluate(telemetry, now_ms)` at a steady interval.
2. Use live sensor data, not the empty demonstration snapshot.
3. Pass `guardian.allow_motion` via a small gate adapter to M7. M7 must check this gate before every servo update.
4. Wire a physical emergency stop / servo power-enable circuit independently of Python.
5. Only call `clear_faults(..., operator_ack=True)` after inspecting the robot and confirming all reported conditions have cleared.
6. Feed the hardware watchdog only after the supervisor cycle finishes successfully.

The thresholds in `config.py` are conservative placeholders. Validate them against actual IMU orientation, battery chemistry, loaded pack voltage, board temperature limits and mechanical geometry before enabling live movement.

## Telemetry contract

`Telemetry(heartbeat_ms, battery_percent, tilt_deg, sensors_ok, servo_fault, temperature_c)` is the M8 input. `heartbeat_ms` must come from the most recent M7 health heartbeat using the same monotonic millisecond clock domain. Do not mix wall-clock time and `ticks_ms()` values.

## Recovery action policy

Actions include `STOP_MOTION`, `WAIT_FOR_STABILITY`, local announcements and `DISABLE_SERVO_OUTPUT`. They execute only when the application supplies an explicit handler for an allowlisted action. Integrators must ensure handlers are bounded and safe. The default engine is a planner; it does not directly control GPIO.

## License

MIT. See `LICENSE`.
