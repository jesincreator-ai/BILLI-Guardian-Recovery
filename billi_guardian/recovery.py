"""Whitelisted deterministic recovery suggestions; never rewrites firmware."""


class RecoveryEngine:
    ACTIONS = {
        "HEARTBEAT_STALE": ("STOP_MOTION",),
        "SENSOR_FAILURE": ("STOP_MOTION", "ANNOUNCE_SENSOR_FAILURE"),
        "BATTERY_READING_MISSING": ("STOP_MOTION",),
        "LOW_BATTERY": ("STOP_MOTION", "ANNOUNCE_LOW_BATTERY"),
        "TILT_READING_MISSING": ("STOP_MOTION",),
        "OVER_TILT": ("STOP_MOTION", "WAIT_FOR_STABILITY"),
        "SERVO_FAULT": ("STOP_MOTION", "DISABLE_SERVO_OUTPUT"),
        "OVER_TEMPERATURE": ("STOP_MOTION", "ANNOUNCE_OVER_TEMPERATURE"),
    }

    def plan(self, faults):
        result = []
        seen = {}
        for fault in faults:
            code = fault.get("code", "")
            actions = self.ACTIONS.get(code, ("STOP_MOTION",))
            for action in actions:
                if action not in seen:
                    seen[action] = True
                    result.append(action)
        return result

    def execute(self, actions, handlers):
        """Execute only explicitly supplied local handlers for allowlisted actions."""
        outcomes = []
        for action in actions:
            if action not in self._allowed_actions():
                continue
            handler = handlers.get(action)
            if handler is None:
                outcomes.append({"action": action, "status": "NO_HANDLER"})
                continue
            try:
                handler()
                outcomes.append({"action": action, "status": "OK"})
            except Exception:
                outcomes.append({"action": action, "status": "FAILED"})
        return outcomes

    @classmethod
    def _allowed_actions(cls):
        allowed = {}
        for actions in cls.ACTIONS.values():
            for action in actions:
                allowed[action] = True
        return allowed
