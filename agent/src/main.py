from paho.mqtt import client as mqtt_client
import json
import time
from schema.aggregated_data_schema import AggregatedDataSchema
from schema.parking_schema import ParkingSchema
from file_datasource import FileDatasource
import config


def connect_mqtt(broker, port):
    """Create MQTT client"""
    print(f"CONNECT TO {broker}:{port}")

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected to MQTT Broker ({broker}:{port})!")
        else:
            print("Failed to connect {broker}:{port}, return code %d\n", rc)
            exit(rc)  # Stop execution

    client = mqtt_client.Client()
    client.on_connect = on_connect
    client.connect(broker, port)
    client.loop_start()
    return client


def publish(client, agent_topic, parking_topic, datasource, delay):
    accelerometer_data, gps_data, parking_data, accelerometer_file, gps_file, parking_file = datasource.startReading()

    while gps_data:
        time.sleep(delay)
        agent_data, parking_agent_data = datasource.read(accelerometer_data, gps_data, parking_data)
        agent_msg, parking_msg = AggregatedDataSchema().dumps(agent_data), ParkingSchema().dumps(parking_agent_data)

        # result: [0, 1]
        agent_result = client.publish(agent_topic, agent_msg)
        agent_status = agent_result[0]
        if agent_status == 0:
            pass
            # print(f"Send `{agent_msg}` to topic `{agent_topic}`")
        else:
            print(f"Failed to send message to topic {agent_topic}")

        parking_result = client.publish(parking_topic, parking_msg)
        parking_status = agent_result[0]
        if parking_status == 0:
            pass
            # print(f"Send `{parking_msg}` to topic `{parking_topic}`")
        else:
            print(f"Failed to send message to topic {parking_topic}")

    datasource.stopReading(accelerometer_file, gps_file, parking_file)


def run():
    # Prepare mqtt client
    client = connect_mqtt(config.MQTT_BROKER_HOST, config.MQTT_BROKER_PORT)
    # Prepare datasource
    datasource = FileDatasource(
        "data/accelerometer.csv",
        "data/gps.csv",
        "data/parking.csv"
    )
    # Infinity publish data
    publish(client, config.MQTT_AGENT_TOPIC, config.MQTT_PARKING_TOPIC, datasource, config.DELAY)


if __name__ == "__main__":
    run()
