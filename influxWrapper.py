from influxdb import InfluxDBClient
from datetime import datetime

class influxWrapper:

    __HOST = ''
    __PORT = ''
    __USER = ''
    __PASSWORD = ''
    __DATABASE = ''

    __measurement = ''
    __location = ''
    __tag_daily_electric = ''
    __tag_daily_gas = ''
    __tag_current_electric = ''

    __verbose = False

    __CONN = None

    def __init__(self, config, verbose):
        global __HOST
        global __PORT
        global __USER
        global __PASSWORD
        global __DATABASE
        global __CONN

        global __measurement
        global __tag_daily_gas
        global __tag_daily_electric
        global __tag_current_electric
        global __location

        global __verbose

        try:
            self.__verbose = verbose
            self.__HOST = config['host']
            self.__PORT = config['port']
            self.__USER = config['user']
            self.__PASSWORD = config['password']
            self.__DATABASE = config['database']

            self.__measurement = config['measurement']
            self.__location = config['location']
            self.__tag_daily_gas = config['tag_daily_gas']
            self.__tag_daily_electric = config['tag_daily_electric']
            self.__tag_current_electric = config['tag_current_electric']
            if verbose:
                self.__printConfig()
            try:
                self.__CONN = InfluxDBClient(host=self.__HOST, port=self.__PORT, username=self.__USER, password=self.__PASSWORD, database=self.__DATABASE, retries=0)
            except:
                print("Connection Failed - check server/credentials")
        except:
            print("Exception thrown - check configuration")


    def updateElectricReadingNow(self, value):
        self.__writeToDatabase(self.__buildJson(self.__measurement, self.__tag_current_electric, value))

    def updateElectricReadingToday(self, value):
        self.__writeToDatabase(self.__buildJson(self.__measurement, self.__tag_daily_electric, value))

    def updateGasReadingToday(self, value):
        self.__writeToDatabase(self.__buildJson(self.__measurement, self.__tag_daily_gas, value))

    def __buildJson(self, measurement, reading_tag, value):
        time_now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        json_body = [
            {
                "measurement" : measurement,
                "tags": {"property": self.__location, "reading": reading_tag},
                "time": time_now,
                "fields": {
                    "value" : float(value)
                }
            }
        ]
        if self.__verbose:
            print(json_body)
        return json_body;

    def __writeToDatabase(self, json_body):
        if not self.__verbose:
            self.__CONN.write_points(json_body)
        else:
            print(self.__CONN.write_points(json_body))

    def __printConfig(self):
        print("Influx Host: " + self.__HOST)
        print("Influx Port: " + self.__PORT)
        print("Influx Database: " + self.__DATABASE)
        print("Influx User: " + self.__USER)
        print("Influx Pass: " + self.__PASSWORD)
        print("Measurement: " + self.__MEASUREMENT)
        print("Location: " + self.__location)
        print("TAG: Daily Electric: " + self.__tag_daily_electric)
        print("TAG: Daily Gas: " + self.__tag_daily_gas)
        print("TAG: Current Electric: " + self.__tag_current_electric)
