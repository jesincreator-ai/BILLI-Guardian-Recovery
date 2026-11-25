"""Guardian wiring example. Feed fresh telemetry every supervisor cycle."""
from config import HEARTBEAT_TIMEOUT_MS, MIN_BATTERY_PERCENT, MAX_TILT_DEG
from config import MAX_TEMPERATURE_C, LOG_CAPACITY
from billi_guardian.guardian import GuardianManager
from billi_guardian.telemetry import Telemetry
from billi_guardian.logs import RingLog
from billi_guardian.recovery import RecoveryEngine


def create_guardian():
    guardian = GuardianManager(HEARTBEAT_TIMEOUT_MS, MIN_BATTERY_PERCENT,
                               MAX_TILT_DEG, MAX_TEMPERATURE_C)
    return guardian, RingLog(LOG_CAPACITY), RecoveryEngine()


def supervise(guardian, log, telemetry, now_ms):
    decision = guardian.evaluate(telemetry, now_ms)
    if decision["faults"]:
        for fault in decision["faults"]:
            log.append(now_ms, fault["severity"], fault["code"])
    return decision


if __name__ == "__main__":
    guardian, log, recovery = create_guardian()
    # This empty snapshot deliberately fails closed until live sensors are wired.
    print(supervise(guardian, log, Telemetry(), 0))
