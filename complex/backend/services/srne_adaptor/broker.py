import paho.mqtt.client as mqtt
import logging
import utils as u
import time
import json
import glb_consts as glb

MQTT_SERVER_ADDR = "192.168.1.199"
MQTT_PORT = 1883
MQTT_USER = 'srne_user'
MQTT_PASS = 'qwe123'

TOPIC_TELEMETRY = "srne/dynamic_information"
TOPIC_SETTINGS = "srne/settings"
TOPIC_SYS_INFO = "srne/system_information"

# mosquitto_sub -h localhost -t "test/topic" -u "srne_user" -P "qwe123"
# mosquitto_pub -h localhost -t "test/topic" -m "Hello MQTT!" -u "srne_user" -P "qwe123"

def connectMqtt():
    def onConnect(client, userdata, flags, rc):
        if rc != 0:
            u.logmsg(f"Failed to mqtt broker connect, return code {rc}")

    if glb.PUBLISH_BROKER_ENABLED:
        try:
            client = mqtt.Client()
            client.username_pw_set(MQTT_USER, MQTT_PASS)
            client.on_connect = onConnect
            client.connect(MQTT_SERVER_ADDR, MQTT_PORT)
            return client
        except Exception as e:
            u.logmsg(f"connectMqtt, error occurred: {str(e)}", u.L_ERROR)
            return None




def publish(topic_name, message_text):
    if glb.PUBLISH_BROKER_ENABLED:
        client = connectMqtt()
        if client:
            if client.is_connected:
                message = json.loads(message_text)
                message['serialNumber'] = glb.DEVICE_SERIAL_NUMBER
                message['MAC'] = u.get_mac_addr()
                message['deviceId'] = glb.DEVICE_ID
                message['ts'] = time.time()

                result = client.publish(topic_name, json.dumps(message))
                status = result[0]
                if status != 0:
                    u.logmsg(f"Failed to send message to topic {topic_name}")
                client.disconnect()


