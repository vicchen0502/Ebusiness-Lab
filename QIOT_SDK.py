#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os,random,json,serial,time,binascii,datetime,threading,numpy
import paho.mqtt.client as mqtt
import RPi.GPIO
from collections import deque
class Mqtt():
    mqtt_client,mqtt_options,resource_info,callbacks, get_number  = None,None,None,None,None
    def __init__(self):
        print ("正在建立連線")
    def on_connect(self, client, userdata, flags, rc):
        if (rc == 0):
            data = {'client': client,'userdata': userdata,'flags': flags,'rc': rc}
            self.trigger("connect", data)
    def on_message(self, client, userdata, msg):
        data = {'client': client,'userdata': userdata,'message': msg,'id': None}
        resources = self.resource_info['resources']
        for res in resources:
            if (msg.topic == str(res["topic"])):
                data['id'] = res["resourceid"]
                break
        self.trigger("message", data)
    def read_resource(self, resfile):
        with open(resfile, 'r') as f:
            data = f.read()
            self.resource_info = json.loads(data)
            try:
                options = {'host': str(self.resource_info['host'][0]),'port': int(self.resource_info['port']),'username': str(self.resource_info['username']),'password': str(self.resource_info['password']),'clientId': str(self.resource_info['clientId']),'ca': None,'key': None,'cert': None}
            except Exception as e:
                options = None
        self.mqtt_options = options
        f.close()
        return self.mqtt_options
    def connect(self, option):
        if (option is None):
            sys.exit()
        self.mqtt_client = mqtt.Client(self.mqtt_options["clientId"])
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.username_pw_set(self.mqtt_options["username"], self.mqtt_options["password"])
        try:
            self.mqtt_client.connect(self.mqtt_options["host"], self.mqtt_options["port"], 60)
        except Exception as e:
            sys.exit(e)
        print("連線建立完成")
        self.mqtt_client.loop_start()
    def publish_by_id(self, resource_id, value):
        resources = self.resource_info['resources']
        for res in resources:
            if (resource_id == str(res["resourceid"])):
                vals = {"values":values}
                vals = json.dump(vals)
                self.mqtt_client.publish(str(res["topic"]), vals, 0, True)
                break
    def subscribe_by_id(self, resource_id):
        resources = self.resource_info['resources']
        for res in resources:
            if (resource_id == str(res["resourceid"])):
                self.mqtt_client.subscribe(str(res["topic"]))
                print("add subscribe :" + str(res["topic"]))
                break
            elif res == resources[-1]:
                print("can't find the id " + resource_id + " in resourceinfo file")
    def on(self, event_name, callback):
        if self.callbacks is None:
            self.callbacks = {}

        if event_name not in self.callbacks:
            self.callbacks[event_name] = [callback]
        else:
            self.callbacks[event_name].append(callback)

    def trigger(self, event_name, data):
        if self.callbacks is not None and event_name in self.callbacks:
            for callback in self.callbacks[event_name]:
                callback(self, data)

def on_connect(event_trigger, data):
    #add subscribe TOPIC here
    connection.subscribe_by_id("TOPIC")

def on_message(event_trigger,data):
    #write script for received data x in here
    print(data["message"].payload.decode())
    print("------------------")

connection = Mqtt()
connection_options = connection.read_resource('./res/resourceinfo.json')
connection.on("connect",on_connect)
connection.on("message",on_message)
connection.connect(connection_options)

while True:
    #write publish script here
    connection.publish_by_id('TOPIC',TOPIC_Value)
    pass
