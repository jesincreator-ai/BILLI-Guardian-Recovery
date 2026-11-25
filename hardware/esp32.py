"""MicroPython hardware watchdog adapter."""


class ESP32Watchdog:
    def __init__(self, timeout_ms=8000):
        try:
            from machine import WDT
        except ImportError:
            raise RuntimeError("ESP32Watchdog requires MicroPython machine.WDT")
        self._wdt = WDT(timeout=int(timeout_ms))

    def feed(self):
        self._wdt.feed()
