"""This manages configuration for the application, saving the following
    - Credentials
    - Configuration Data
    asdfghjkai.co.uk 2020
"""

import configparser

CONFIG_FILE = 'config.ini'

#General Configuration
pollingInterval = 6
DCCperiod = 1800
verbose = False

#CONSTANTS
#GlowMarkt Config
glowmarkt_user = ""
glowmarkt_pass = ""

#MQTT Config
mqtt_broker = ""
mqtt_port = 1883
mqtt_user = ""
mqtt_pass = ""
mqtt_base_topic = ""

mqtt_suffix_daily_gas_total = ""
mqtt_suffix_daily_elec_total = ""
mqtt_suffix_current_elec_usage = ""

mqtt_topic_daily_gas = ""
mqtt_topic_daily_elec = ""
mqtt_topic_current_elec = ""

#Influx Container
influx_config = None

usesMQTT = False
usesInflux = False

"""Method which initialises the topics for use with MQTT
"""
def initTopics():
    global mqtt_topic_daily_gas
    global mqtt_topic_daily_elec
    global mqtt_topic_current_elec

    mqtt_topic_daily_gas = mqtt_base_topic + mqtt_suffix_daily_gas_total
    mqtt_topic_daily_elec = mqtt_base_topic + mqtt_suffix_daily_elec_total
    mqtt_topic_current_elec = mqtt_base_topic + mqtt_suffix_current_elec_usage

"""Method which prints the contents of the config file after reading
"""
def printConfig():
    print("GlowMarkt User:" + glowmarkt_user)
    print("GlowMarkt Pass:" + glowmarkt_pass)

    print("Uses MQTT: " + str(usesMQTT))
    print("MQTT Broker:" + mqtt_broker)
    print("MQTT Port:" + str(mqtt_port))
    print("MQTT User:" + mqtt_user)
    print("MQTT Pass:" + mqtt_pass)
    print("MQTT Base:" + mqtt_base_topic)

    print("Uses InfluxDB: " + usesInflux)

    print("Polling Interval(secs):" + str(pollingInterval))
    print("DCC Polling(secs):" + str(DCCperiod))

"""Method which reads the most recent config data from the specified config file
"""
def readConfig():
    global pollingInterval
    global DCCperiod, verbose
    global glowmarkt_user, glowmarkt_pass
    global mqtt_broker, mqtt_port, mqtt_user, mqtt_pass, mqtt_base_topic
    global mqtt_suffix_daily_elec_total, mqtt_suffix_daily_gas_total, mqtt_suffix_current_elec_usage
    global influx_config, usesInflux, usesMQTT
    try:
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)

        # General
        pollingInterval = int(config['General']['pollingInterval'])
        DCCperiod = int(config['General']['gasPeriod'])
        if config['General']['Verbose'] == "True":
            verbose = True

        # GlowMarkt
        glowmarkt_user = config['GlowMarkt']['user']
        glowmarkt_pass = config['GlowMarkt']['password']

        # MQTT
        mqtt_broker = config['MQTT']['broker']
        mqtt_port = int(config['MQTT']['port'])
        mqtt_user = config['MQTT']['user']
        mqtt_pass = config['MQTT']['password']
        mqtt_base_topic = config['MQTT']['base_topic']
        usesMQTT = config['MQTT']['Enabled']

        mqtt_suffix_daily_elec_total = config['MQTT']['suffix_daily_electric']
        mqtt_suffix_daily_gas_total = config['MQTT']['suffix_daily_gas']
        mqtt_suffix_current_elec_usage = config['MQTT']['suffix_current_electric']

        initTopics()

        influx_config = config['InfluxDB']
        usesInflux = config['InfluxDB']['Enabled']

        if verbose:
            printConfig()

    except:
        print("Failed to read config file")

def getInfluxConfig():
    return influx_config


