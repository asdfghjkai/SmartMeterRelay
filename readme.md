# Smart Meter Relay


This is a python project which allows the relay of data from a SMETS2 meter (Using the GlowMarkt API and [Glow IHD](https://shop.glowmarkt.com/products/display-and-cad-combined-for-smart-meter-customers)
## Requirements & Dependancies
- Requests `pip install requests`
- Paho MQTT `pip install paho-mqtt`
- Influx Python Client `pip install influxdb`

## How To Use
1. Clone the repo
2. Open config.ini, and configure as necessary
	- You can run both the MQTT and Influx clients if you want to squeeze lemons in your eyes
	- Update the credentials as necessary - you need to activate the IHD on the apps as per the given instructions
3. Should be golden!!! Just launch with `python SmartMeterRelay.py`
4. If you're still using python2, take the lemons from earlier and squeeze them again.

## To Do
- Create an MQTT Wrapper
- Create the configmgmt as an instantiable containedobject, versus just an open reference to methods and variables
- Whatever else comes to mind
- Integrated testing (CICD?)
- Provide release execs compiled from pyinstaller

## Notes:
There is a branch for InfluxDB2 development. You will need the following library
- Influx Client `pip install influxdb-client` - perhaps best to run `pip uninstall influxdb` first
- If doing the above on a Windows machine - you'll also need these binaries to compile dependancies (notably ciso8601) [here](http://go.microsoft.com/fwlink/?LinkId=691126&fixForIE=.exe)
