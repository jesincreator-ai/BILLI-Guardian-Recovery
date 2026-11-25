"""Offline concise diagnostic phrases for the voice layer."""

MESSAGES = {
    "en": {"HEARTBEAT_STALE": "Controller heartbeat lost", "SENSOR_FAILURE": "Sensor failure",
           "LOW_BATTERY": "Battery is low", "OVER_TILT": "Robot tilt is unsafe",
           "SERVO_FAULT": "Servo fault", "OVER_TEMPERATURE": "Temperature is too high"},
    "ta": {"HEARTBEAT_STALE": "கட்டுப்பாட்டு தொடர்பு இழந்தது", "SENSOR_FAILURE": "சென்சார் பிழை",
           "LOW_BATTERY": "மின்கலம் குறைவாக உள்ளது", "OVER_TILT": "ரோபோ சாய்வு பாதுகாப்பற்றது",
           "SERVO_FAULT": "சர்வோ பிழை", "OVER_TEMPERATURE": "வெப்பநிலை அதிகமாக உள்ளது"},
    "si": {"HEARTBEAT_STALE": "පාලක සම්බන්ධතාව නැතිවුණා", "SENSOR_FAILURE": "සංවේදක දෝෂයක්",
           "LOW_BATTERY": "බැටරිය අඩුයි", "OVER_TILT": "රොබෝවගේ ඇලවීම අනාරක්ෂිතයි",
           "SERVO_FAULT": "සර්වෝ දෝෂයක්", "OVER_TEMPERATURE": "උෂ්ණත්වය වැඩියි"},
}


def message(code, language="en"):
    table = MESSAGES.get(language, MESSAGES["en"])
    return table.get(code, MESSAGES["en"].get(code, code))
