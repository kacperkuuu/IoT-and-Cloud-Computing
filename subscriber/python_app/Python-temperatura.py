#!/usr/bin/env python3

import ssl
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt

DEV = False

# Ustawienia MQTT
broker = "i78343e1.ala.eu-central-1.emqxsl.com"
port = 8883
username = "student"
password = "student"
topic = "emqx/esp8266"

# Ustawienia InfluxDB (dla v2.x)
influxdb_url = "http://influxdb:8086"  # Adres InfluxDB
influxdb_token = "vx9-n5W2ZxrCsOdsyL3R-hnKqBgLcaBgM0dNlyrqUZR5SN4_z3wklaqi3H4GsxyUMoaVvR-r-ZKSELXc2nZ0PA=="      # Token autoryzacji
influxdb_org = "test"          # Organizacja
influxdb_bucket = "mqtt_data"         # Bucket



# Ścieżka do certyfikatu CA
if DEV:
    CA_CERT = "python_app/MQTTcert.crt"
else:
    CA_CERT = "/app/MQTTcert.crt"


# Połączenie z InfluxDB
influx_client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN)
write_api = influx_client.write_api(write_options=SYNCHRONOUS)

# Funkcja przetwarzająca wiadomości MQTT
def on_message(client, userdata, message):
    try:
        payload = message.payload.decode()
        # Sprawdź, czy wiadomość to liczba
        temperature = float(payload) if payload.replace('.', '', 1).isdigit() else None
        if temperature is not None:
            print(f"Received temperature: {temperature}")
            # Zapis do InfluxDB
            point = Point("test_topic").field("value", temperature)
            write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point, write_precision=WritePrecision.NS)
        else:
            print(f"Ignored non-numeric message: '{payload}'")
    except Exception as e:
        print(f"Error processing message: {e}")

def main():
    # Konfiguracja klienta MQTT
    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

    # Konfiguracja SSL/TLS
    client.tls_set(ca_certs=CA_CERT)

    # Podłącz funkcję obsługi wiadomości
    client.on_message = on_message

    # Połącz z brokerem
    try:
        client.connect(MQTT_BROKER, MQTT_PORT)
        print("Connected to MQTT broker")
    except Exception as e:
        print(f"Failed to connect to MQTT broker: {e}")
        return

    # Subskrybuj temat
    client.subscribe(MQTT_TOPIC)
    print(f"Subscribed to topic: {MQTT_TOPIC}")

    # Start loop
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("Program interrupted")
    finally:
        client.disconnect()

if __name__ == "__main__":
    main()