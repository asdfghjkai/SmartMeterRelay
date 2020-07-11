"""SMETS2 Relay Client - by asdfghjkai (2020)

Handles the following:
    - Connection to GlowMarkt, and retrieval of live/half hourly data
    - Pushing to a defined MQTT client (locally)
    - Support for pushing to Influx DB
"""

import time
import paho.mqtt.client as mqtt
import configmgmt as cfgs
import glowmarktAPIHandler as gm
import influxWrapper

gas_increment = 0

gmAPI = None
influxDB = None

client = mqtt.Client()
isMQTTConnected = False

def mqttIsConnected(client, userdata, flags, rc):
    global isMQTTConnected
    if rc==0:
        isMQTTConnected = True
        print("Reconnect Successful | Returned Code:", rc)
    else:
        print("Reconnect Unsuccessful | Returned Code:", rc)


def mqttIsDisconnected():
    global isMQTTConnected
    isMQTTConnected = False


def initMQTT(broker, port, user, passw):
    client.username_pw_set(username=user, password=passw)
    client.on_connect = mqttIsConnected
    client.on_disconnect = mqttIsDisconnected
    client.connect(broker, port, 60)
    client.loop_start()


def init():
    global gmAPI
    global influxDB
    cfgs.readConfig()
    if cfgs.verbose:
        print("Verbose Operating Mode")
    if cfgs.usesMQTT == "True":
        print("Using MQTT")
        try:
            initMQTT(cfgs.mqtt_broker, cfgs.mqtt_port, cfgs.mqtt_user, cfgs.mqtt_pass)
            print("MQTT: Connection Successful")
        except:
            print("Failed to init MQTT Connection")

    if cfgs.usesInflux == "True":
        print("Using InfluxDB")
        try:
            influxDB = influxWrapper.influxWrapper(cfgs.getInfluxConfig(), cfgs.verbose)
            print("InfluxDB Connection Successful")
        except:
            print("Failed to connect to InfluxDB - check credentials and config")

    try:
        gmAPI = gm.GlowMarktAPI(cfgs.glowmarkt_user, cfgs.glowmarkt_pass)
    except:
        print("Failed to init GlowMarkt API - Check credentials and connection")

    print("Init Complete")


def run():
    global gas_increment
    while True:
        try:
            if gas_increment == 0 or gas_increment % cfgs.DCCperiod == 0:
                gasReading = gmAPI.getGasToday()
                print("Gas Reading (So Far Today): " + str(gasReading[1]) + "kWh")

                electricReading = gmAPI.getElectricToday()
                print("Electric Reading (So Far Today): " + str(electricReading[1]) + "kWh")

                if cfgs.usesMQTT == "True":
                    client.publish(cfgs.mqtt_topic_daily_gas, str(gasReading[1]))
                    client.publish(cfgs.mqtt_topic_daily_elec, str(electricReading[1]))
                if cfgs.usesInflux == "True":
                    influxDB.updateElectricReadingToday(electricReading[1])
                    influxDB.updateGasReadingToday(gasReading[1])

                #This is of no-relative use - as the gas meter is battery powered and only updates half hourly anyway
                # gasReading = gm.getReadingNow(gasId)
                # print("Gas Reading: " + str(gasReading[1]) + "kWh")
                # gas_increment = 0

            electricReading = gmAPI.getElectricNow()
            print("Electric Reading: " + str(electricReading[1]) + "Watts")
            if cfgs.usesMQTT == "True":
                client.publish((cfgs.mqtt_topic_current_elec), str(electricReading[1]))
            if cfgs.usesInflux == "True":
                influxDB.updateElectricReadingNow(electricReading[1])
        except:
            print("Failure during submissions of readings, potentially lost connection?")

        gas_increment += cfgs.pollingInterval
        time.sleep(cfgs.pollingInterval)


init()
run()





