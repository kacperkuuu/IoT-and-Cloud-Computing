import torch
import cv2
import paho.mqtt.client as mqtt
import ssl

# Ustawienia MQTT
broker = "i78343e1.ala.eu-central-1.emqxsl.com"  # Broker
port = 8883  # Port TLS
topic = "object-detection"
username = "student"
password = "student"

# Połączenie MQTT
client = mqtt.Client()

# Ustawienie połączenia z TLS
client.username_pw_set(username, password)
client.tls_set_context(ssl.create_default_context())  # Domyślny SSL, dla bezpieczeństwa dodaj certyfikaty, jeśli wymagane

# Funkcja wywołania po połączeniu z brokerem
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Połączono z brokerem MQTT")
    else:
        print(f"Nie udało się połączyć z brokerem MQTT, kod: {rc}")

# Funkcja do publikowania wiadomości do MQTT
def publish_to_mqtt(text):
    try:
        result = client.publish(topic, text)
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"Wysłano do MQTT: {text}")
        else:
            print(f"Błąd podczas wysyłania do MQTT: {text}")
    except Exception as e:
        print(f"Błąd MQTT: {e}")

# Model YOLO
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)  # Używa YOLOv5s
model.classes = [0, 2, 67, 63, 39, 49]  # Wykrywanie określonych klas

# Funkcja do wykrywania obiektów
def detect_objects(frame):
    results = model(frame)
    labels = results.pandas().xyxy[0]["name"].tolist()  # Pobranie nazw obiektów

    if labels:
        message = ", ".join(set(labels))  # Usuwanie duplikatów
        publish_to_mqtt(message)

# Funkcja główna
def main():
    cap = cv2.VideoCapture(0)  # Pobranie klatek z kamery
    if not cap.isOpened():
        print("Nie można otworzyć kamery")
        return

    # Połączenie z MQTT
    client.on_connect = on_connect
    try:
        client.connect(broker, port, 60)
        client.loop_start()  # Uruchamia pętlę MQTT w tle
    except Exception as e:
        print(f"Nie udało się połączyć z brokerem MQTT: {e}")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        detect_objects(frame)  # Wykrywanie obiektów i wysyłanie tekstu
        cv2.imshow("Wideo", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()