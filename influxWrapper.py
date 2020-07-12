from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

from datetime import datetime

class influxWrapper:

    __HOST = ''
    __BUCKET = ''
    __TOKEN = ''

    __measurement = ''
    __tag_daily_electric = ''
    __tag_daily_gas = ''
    __tag_current_electric = ''

    __verbose = False

    __CONN = None

    def __init__(self, config, verbose):
        global __HOST
        global __BUCKET
        global __TOKEN
        global __CONN

        global __measurement
        global __tag_daily_gas
        global __tag_daily_electric
        global __tag_current_electric

        global __verbose

        try:
            self.__verbose = verbose
            self.__HOST = config['host']
            self.__TOKEN = config['token']
            self.__BUCKET = config['bucket']
            self.__ORG = config['org']

            self.__measurement = config['measurement']
            self.__tag_daily_gas = config['tag_daily_gas']
            self.__tag_daily_electric = config['tag_daily_electric']
            self.__tag_current_electric = config['tag_current_electric']
            if verbose:
                self.__printConfig()
            try:
                self.__CONN = InfluxDBClient(url=self.__HOST, token=self.__TOKEN)
            except:
                print("Connection Failed - check server/credentials")
        except:
            print("Exception thrown - check configuration")


    def updateElectricReadingNow(self, value):
        self.__writeToDatabase(self.__buildPoint(self.__measurement, self.__tag_current_electric, value))

    def updateElectricReadingToday(self, value):
        self.__writeToDatabase(self.__buildPoint(self.__measurement, self.__tag_daily_electric, value))

    def updateGasReadingToday(self, value):
        self.__writeToDatabase(self.__buildPoint(self.__measurement, self.__tag_daily_gas, value))

    def __buildPoint(self, measurement, reading_tag, value):
        point = Point(measurement)\
            .tag("reading", reading_tag)\
            .field("value", float(value))\
            .time(datetime.utcnow(), WritePrecision.NS)
        return point

    def __writeToDatabase(self, point):
        if not self.__verbose:
            write_api = self.__CONN.write_api(write_options=SYNCHRONOUS)
            write_api.write(self.__BUCKET, self.__ORG, point)
        else:
            write_api = self.__CONN.write_api(write_options=SYNCHRONOUS)
            write_api.write(self.__BUCKET, self.__ORG, point)

    def __printConfig(self):
        print("Influx Host: " + self.__HOST)
        print("Influx Org: " + self.__ORG)
        print("Influx Bucket: " + self.__BUCKET)
        print("Influx Token: " + self.__TOKEN)
        print("TAG: Daily Electric: " + self.__tag_daily_electric)
        print("TAG: Daily Gas: " + self.__tag_daily_gas)
        print("TAG: Current Electric: " + self.__tag_current_electric)
