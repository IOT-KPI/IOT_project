import os


def try_parse(type, value: str):
    try:
        return type(value)
    except Exception:
        return None


USER_ID = 1
# MQTT config
MQTT_BROKER_HOST = os.environ.get("MQTT_BROKER_HOST") or "mqtt"
MQTT_BROKER_PORT = try_parse(int, os.environ.get("MQTT_BROKER_PORT")) or 1883
MQTT_AGENT_TOPIC = os.environ.get("MQTT_AGENT_TOPIC") or "agent"
MQTT_PARKING_TOPIC = os.environ.get("MQTT_PARKING_TOPIC") or "parking"
MQTT_TRAFFIC_TOPIC = os.environ.get("MQTT_TRAFFIC_TOPIC") or "traffic"


# Delay for sending data to mqtt in seconds
DELAY = try_parse(float, os.environ.get("DELAY")) or 1
