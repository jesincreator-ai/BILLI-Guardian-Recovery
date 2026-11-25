import unittest
from billi_guardian.guardian import GuardianManager
from billi_guardian.recovery import RecoveryEngine
from billi_guardian.telemetry import Telemetry
from billi_guardian.logs import RingLog


class GuardianTests(unittest.TestCase):
    def test_motion_is_denied_until_safe_state_is_acknowledged(self):
        guardian = GuardianManager()
        self.assertFalse(guardian.allow_motion())
        safe = Telemetry(heartbeat_ms=0, battery_percent=90, tilt_deg=0)
        guardian.evaluate(safe, 10)
        self.assertFalse(guardian.allow_motion())
        self.assertTrue(guardian.clear_faults(safe, 10, operator_ack=True))
        self.assertTrue(guardian.allow_motion())

    def test_over_tilt_latches_motion_veto_until_acknowledged_safe(self):
        guardian = GuardianManager(max_tilt_deg=30)
        unsafe = Telemetry(heartbeat_ms=90, battery_percent=80, tilt_deg=45)
        decision = guardian.evaluate(unsafe, 100)
        self.assertFalse(decision["allow_motion"])
        self.assertTrue(guardian.is_latched())
        safe = Telemetry(heartbeat_ms=110, battery_percent=80, tilt_deg=2)
        self.assertFalse(guardian.clear_faults(safe, 120, operator_ack=False))
        self.assertTrue(guardian.clear_faults(safe, 120, operator_ack=True))
        self.assertTrue(guardian.allow_motion())

    def test_stale_heartbeat_denies_motion(self):
        guardian = GuardianManager(heartbeat_timeout_ms=100)
        snapshot = Telemetry(heartbeat_ms=0, battery_percent=90, tilt_deg=0)
        self.assertFalse(guardian.evaluate(snapshot, 150)["allow_motion"])

    def test_battery_and_sensor_faults_are_reported(self):
        guardian = GuardianManager(min_battery_percent=12)
        snapshot = Telemetry(heartbeat_ms=10, battery_percent=5, tilt_deg=0, sensors_ok=False)
        faults = guardian.evaluate(snapshot, 20)["faults"]
        codes = [fault["code"] for fault in faults]
        self.assertIn("LOW_BATTERY", codes)
        self.assertIn("SENSOR_FAILURE", codes)


class RecoveryTests(unittest.TestCase):
    def test_recovery_actions_are_safe_allowlisted_actions(self):
        engine = RecoveryEngine()
        actions = engine.plan([{"code": "LOW_BATTERY"}, {"code": "OVER_TILT"}])
        self.assertEqual(actions, ["STOP_MOTION", "ANNOUNCE_LOW_BATTERY", "WAIT_FOR_STABILITY"])
        self.assertNotIn("RESTART_BOARD", actions)
        self.assertNotIn("REWRITE_FIRMWARE", actions)


class LogTests(unittest.TestCase):
    def test_log_is_bounded_and_keeps_recent_entries(self):
        log = RingLog(2)
        log.append(1, "INFO", "boot")
        log.append(2, "WARN", "battery")
        log.append(3, "ERROR", "tilt")
        entries = log.items()
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0]["message"], "battery")
        self.assertEqual(entries[1]["message"], "tilt")


if __name__ == "__main__":
    unittest.main()
