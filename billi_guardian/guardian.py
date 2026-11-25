"""Fail-closed Guardian supervisor. A fault latches motion off until acknowledged."""


def _elapsed(now_ms, then_ms):
    delta = int(now_ms) - int(then_ms)
    if delta < 0:
        delta += 1 << 30
    return delta


class GuardianManager:
    def __init__(self, heartbeat_timeout_ms=500, min_battery_percent=12,
                 max_tilt_deg=35.0, max_temperature_c=75.0):
        self.heartbeat_timeout_ms = max(50, int(heartbeat_timeout_ms))
        self.min_battery_percent = int(min_battery_percent)
        self.max_tilt_deg = float(max_tilt_deg)
        self.max_temperature_c = float(max_temperature_c)
        self._latched = True  # Fail closed until a safe snapshot is explicitly acknowledged.
        self._last_faults = []
        self._last_evaluation_ms = 0

    def _collect_faults(self, telemetry, now_ms):
        faults = []
        heartbeat = telemetry.heartbeat_ms
        if heartbeat is None or _elapsed(now_ms, heartbeat) > self.heartbeat_timeout_ms:
            faults.append({"code": "HEARTBEAT_STALE", "severity": "critical"})
        if not telemetry.sensors_ok:
            faults.append({"code": "SENSOR_FAILURE", "severity": "critical"})
        battery = telemetry.battery_percent
        if battery is None:
            faults.append({"code": "BATTERY_READING_MISSING", "severity": "warning"})
        elif int(battery) <= self.min_battery_percent:
            faults.append({"code": "LOW_BATTERY", "severity": "critical"})
        tilt = telemetry.tilt_deg
        if tilt is None:
            faults.append({"code": "TILT_READING_MISSING", "severity": "critical"})
        elif abs(float(tilt)) > self.max_tilt_deg:
            faults.append({"code": "OVER_TILT", "severity": "critical"})
        if telemetry.servo_fault:
            faults.append({"code": "SERVO_FAULT", "severity": "critical"})
        temperature = telemetry.temperature_c
        if temperature is not None and float(temperature) >= self.max_temperature_c:
            faults.append({"code": "OVER_TEMPERATURE", "severity": "critical"})
        return faults

    def evaluate(self, telemetry, now_ms):
        self._last_evaluation_ms = int(now_ms)
        faults = self._collect_faults(telemetry, now_ms)
        self._last_faults = faults
        if faults:
            self._latched = True
        return {
            "allow_motion": (not self._latched and not faults),
            "latched": self._latched,
            "faults": list(faults),
            "evaluated_at_ms": self._last_evaluation_ms,
        }

    def allow_motion(self):
        return not self._latched

    def is_latched(self):
        return self._latched

    def last_faults(self):
        return list(self._last_faults)

    def clear_faults(self, telemetry, now_ms, operator_ack=False):
        if not operator_ack:
            return False
        remaining = self._collect_faults(telemetry, now_ms)
        self._last_faults = remaining
        if remaining:
            self._latched = True
            return False
        self._latched = False
        self._last_evaluation_ms = int(now_ms)
        return True
