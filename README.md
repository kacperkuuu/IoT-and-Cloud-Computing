# IoT-and-Cloud-Computing

### Description
This application utilizes the OpenAI Whisper model to capture 2-second audio segments from the default input device and display the transcribed speech. It is compatible with both CPU and CUDA, with a dedicated function for selecting the appropriate mode to prevent crashes. The application requires Linux for dockerization. Although there are tokens and SSL certificates in the code, they are included solely for testing purposes, so no worries.

```mermaid
graph TD
    subgraph ESP8266
        A[ESP8266] -->|Temperature Measurement| B[DS18B20 Sensor]
        A -->|MQTT Data Transmission| C[MQTT Broker]
        A -->|Receive MQTT Text| D[LCD Display]
    end

    subgraph Docker
        E[InfluxDB] <-->|Store Temperature Data| F[Python Subscriber]
        F -->|Subscribe to MQTT| C
        G[Grafana] -->|Visualize Data| E
    end

    subgraph Speech-to-Text
        H[Whisper Model] -->|Speech to Text Conversion| C
    end

    subgraph Video-to-Text
        I[YOLO Model] -->|Object Detection to Text| C
    end

    C -->|Send Text| D
```

```mermaid
graph TD
    %% ESP8266 Subgraph
    subgraph ESP8266_System
        ESP8266 -->|Read Temperature| DS18B20_Sensor
        ESP8266 -->|Process Data| Process_Sensor_Data
        Process_Sensor_Data -->|Publish Temperature via MQTT| MQTT_Broker
        ESP8266 -->|Receive Text Data| Subscribe_MQTT
        Subscribe_MQTT -->|Display Text| LCD_Display
    end

    %% Docker Subgraph for InfluxDB
    subgraph Docker_System
        InfluxDB <-->|Store Sensor Data| Python_Subscriber
        Python_Subscriber -->|Subscribe to MQTT| MQTT_Broker
        Grafana -->|Query and Visualize Data| InfluxDB
        NVIDIA_Toolkit -->|Enable GPU for Docker| Whisper_YOLO_Containers
    end

    %% Speech-to-Text Subgraph
    subgraph Speech_to_Text
        Audio_Input -->|Capture 2s Audio| Whisper_Model
        Whisper_Model -->|Convert Speech to Text| Speech_Text
        Speech_Text -->|Publish to MQTT| MQTT_Broker
    end

    %% Video-to-Text Subgraph
    subgraph Video_to_Text
        Camera_Input -->|Capture Frames| YOLO_Model
        YOLO_Model -->|Detect Objects & Convert to Text| Object_Text
        Object_Text -->|Publish to MQTT| MQTT_Broker
    end

    %% MQTT Broker and Connections
    MQTT_Broker -->|Forward Text & Temperature| LCD_Display
    MQTT_Broker -->|Send Data to Subscriber| Python_Subscriber
    MQTT_Broker -->|Broadcast Speech Text| Subscribe_MQTT
    MQTT_Broker -->|Broadcast Object Text| Subscribe_MQTT

    %% External Tools and Dependencies
    Whisper_YOLO_Containers -->|Run Whisper Model| Whisper_Model
    Whisper_YOLO_Containers -->|Run YOLO Model| YOLO_Model
```

### Linux required for easier installation, making docker can read microphone from windows is quite complicated

## Installation on linux Debian12

### Requirements:
- Python 3.11.8 !! important
- Make venv and
- Install requirements.txt
- SSL cert for MQTT connection in /python_scripts/MQTTcert.crt

### CUDA Requirements
- CUDA 12.6, V12.6.77
- nvhpc_2024_2411_Linux_x86_64_cuda_12.6.tar.gz
- cudnn/9.5.1/local_installers/cudnn-local-repo-debian12-9.5.1_1.0-1_amd64.deb
### Run
1. Set correct values main.py
2. Using >Real_Time_whisper_IoT/python_scripts/.venv/bin/Python3.11 main.py

## DOCKER install
### Requirements
1. Docker
2. NVIDIA Container Toolkit for docker so it can read GPU
3. SSL cert for MQTT connection in /python_scripts/MQTTcert.crt

### Instructions whisper_RealTime
1. cd whisper_realTime
2. sudo docker build -t whisper_realTime .

### Whisper_RealTime run:
sudo docker run --gpus all --device /dev/snd:/dev/snd --rm -it whisper-audio-app

### Instructions YOLOv8
1. cd YOLOv8
2. sudo docker build -t yolo-app .

### YOLOv8 run:
sudo docker run --rm --device=/dev/video0:/dev/video0 yolo-app

## Grafana 'n influx stats server setup and run
1. cd grafana_influx_stats
2. sudo docker compose up --build

## Temperature setup

### I2C LCD wireing
VCC -> VV GND -> G SCL -> D1 SDA -> D2

### DallasTemperature sensor wireing
Middle Pin (data) -> D3 GND -> GND VCC -> 3V with resistor
