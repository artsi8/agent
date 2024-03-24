from paho.mqtt import client as mqtt_client
import json
import time
from schema.aggregated_data_schema import AggregatedDataSchema
from file_datasource import FileDatasource
import config
from schema.parking_schema import ParkingSchema


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


def publish(client, topic1, topic2, datasource, delay):
    datasource.startReading()
    while True:
        time.sleep(delay)

        data1 = datasource.readAggregatedData()
        msg1 = AggregatedDataSchema().dumps(data1)
        result1 = client.publish(topic1, msg1)

        data2 = datasource.readParking()
        msg2 = ParkingSchema().dumps(data2)
        result2 = client.publish(topic2, msg2)

        for result, topic,msg in zip([result1,result2], [topic1,topic2],[msg1,msg2]):
            # result: [0, 1]
            status = result[0]
            if status == 0:
                pass
                print(f"Send `{msg}` to topic `{topic}`")
            else:
                print(f"Failed to send `{msg}` to topic {topic}")


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
    publish(client, config.MQTT_TOPIC,config.MQTT_TOPIC2, datasource, config.DELAY)


if __name__ == "__main__":
    run()
