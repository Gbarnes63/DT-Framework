
from __future__ import annotations

import json
import time
from typing import Any, Optional

import paho.mqtt.client as mqtt
import generator.cobot_stasts as cobot_gen
import generator.shelf_parts as shelf_gen



class MqttPublisher:
    def __init__(
        self,
        host="localhost",
        port=  1883,
        client_id= "Dt-Framework-Demo",
        username = None,
        password = None,
        keepalive = 60,
        tls = False,
    ) :
        self.client = mqtt.Client(client_id=client_id, clean_session=True)
        if username and password:
            self.client.username_pw_set(username=username, password=password)
        if tls:
            self.client.tls_set()  

        self.host = host
        self.port = port
        self.keepalive = keepalive

      
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect

       
        self._connect_with_retry()

    def _connect_with_retry(self, attempts: int = 5, delay_s: float = 1.5) -> None:
        for i in range(attempts):
            try:
                self.client.connect(self.host, self.port, self.keepalive)
                self.client.loop_start()  # background network loop
                return
            except Exception as ex:
                if i == attempts - 1:
                    raise
                time.sleep(delay_s)

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected")
        else:
            print(f"Connect failed rc={rc}")

    def _on_disconnect(self, client, userdata, rc):
        print(f"Disconnected rc={rc}")

    def publish(self, topic, payload, qos = 1, retain = False) :
       
        data = json.dumps(payload, ensure_ascii=False)
        print(data)
        result = self.client.publish(topic=payload['topic'], payload=data, qos=qos, retain=retain)
        
        if result.rc != mqtt.MQTT_ERR_SUCCESS:
            print(f"Publish error rc={result.rc} topic={topic}")

    def close(self):
        self.client.loop_stop()
        self.client.disconnect()


def publish_cobot_stats():
    sample = cobot_generator.sample()
    publisher.publish(topic=sample["topic"], payload=sample)

def publish_shelf_stats():
    sample = shelf_generator.sample()
    publisher.publish(topic=sample["topic"], payload=sample)

publisher = MqttPublisher(host="localhost", port=1883)
cobot_generator = cobot_gen.CobotStatsGenerator.from_config(
    cobot_gen.cfg, seed=cobot_gen.cfg.get("seed")
)
shelf_generator = shelf_gen.ShelfStatsGenerator.from_config(
    shelf_gen.cfg, seed=shelf_gen.cfg.get("seed"))

while True:

    publish_cobot_stats()
    publish_shelf_stats()

    time.sleep(2) 
    # publisher.close()