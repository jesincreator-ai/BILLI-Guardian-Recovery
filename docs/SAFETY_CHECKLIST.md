# Pre-motion safety checklist

- [ ] Four servo GPIOs checked against the actual ESP32-WROOM board and every connected peripheral.
- [ ] Servo supply is separate from the ESP32 3.3 V rail, correctly rated, fused as appropriate, and shares signal ground.
- [ ] Each joint has measured mechanical limits; software angle bounds do not replace physical stops.
- [ ] Servo pulse widths and PWM frequency verified for the exact servo model, initially using conservative pulse range.
- [ ] Physical emergency stop / servo-enable cutoff tested with the ESP32 software unresponsive.
- [ ] Battery divider, ADC attenuation, pack chemistry and voltage thresholds measured with a multimeter.
- [ ] IMU axes and tilt sign verified in every robot orientation.
- [ ] Sensor freshness and M7 heartbeat use one monotonic millisecond clock.
- [ ] M8 starts fail-closed, trips on missing telemetry and requires operator acknowledgment to clear.
- [ ] Four-servo movement first tested with the robot supported and unloaded.

Do not enable live movement until every item relevant to the installed hardware is verified.
