"""Show a latched fault and safe recovery recommendation on desktop Python."""
from billi_guardian.guardian import GuardianManager
from billi_guardian.telemetry import Telemetry
from billi_guardian.recovery import RecoveryEngine

manager = GuardianManager()
snapshot = Telemetry(heartbeat_ms=0, battery_percent=5, tilt_deg=48)
decision = manager.evaluate(snapshot, 100)
print(decision)
print(RecoveryEngine().plan(decision["faults"]))
