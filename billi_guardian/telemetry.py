"""Hardware-neutral, immutable-by-convention telemetry snapshot."""


class Telemetry:
    def __init__(self, heartbeat_ms=None, battery_percent=None, tilt_deg=None,
                 sensors_ok=True, servo_fault=False, temperature_c=None):
        self.heartbeat_ms = heartbeat_ms
        self.battery_percent = battery_percent
        self.tilt_deg = tilt_deg
        self.sensors_ok = bool(sensors_ok)
        self.servo_fault = bool(servo_fault)
        self.temperature_c = temperature_c

    def as_dict(self):
        return {
            "heartbeat_ms": self.heartbeat_ms,
            "battery_percent": self.battery_percent,
            "tilt_deg": self.tilt_deg,
            "sensors_ok": self.sensors_ok,
            "servo_fault": self.servo_fault,
            "temperature_c": self.temperature_c,
        }
