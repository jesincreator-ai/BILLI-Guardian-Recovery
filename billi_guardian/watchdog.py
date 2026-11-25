"""Small watchdog supervisor. Feed only after a healthy supervisor cycle."""


class WatchdogSupervisor:
    def __init__(self, watchdog):
        if watchdog is None or not hasattr(watchdog, "feed"):
            raise ValueError("watchdog must provide feed()")
        self.watchdog = watchdog
        self.feed_count = 0
        self.skipped_count = 0

    def supervisor_cycle(self, guardian_healthy):
        if not guardian_healthy:
            self.skipped_count += 1
            return False
        self.watchdog.feed()
        self.feed_count += 1
        return True
