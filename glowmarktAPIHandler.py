"""Glowmarket API Client - by asdfghjkai (2020)
"""
import requests
import json
from datetime import date

"""This class manages authentication and interaction with the GlowMarkt API

    asdfghjkai 2020
"""
class GlowMarktAPI:
    __APPLICATIONID = 'b0f1b774-a586-4f72-9edd-27ead8aa7a8d'  # This does not change, keep it as a constant
    __APIBASE = 'https://api.glowmarkt.com/api/v0-1/'
    __HEADER = {'Content-Type': 'application/json', 'applicationId': __APPLICATIONID}
    __TOKENIZEDHEADER = ""
    __name = ""
    __token = ""

    __gasclassifier = 'gas.consumption'
    __costclassifier = '.cost'
    __electricclassifier = 'electricity.consumption'
    __gasId = ''
    __electricId = ''
    __resources = ""

    __glowUser = ""
    __glowPw = ""

    """Initializer method for GlowMarktAPI Class

    :param user: Username for GlowMarkt API
    :param password: Password for GlowMarkt API
    """
    def __init__(self, user, password):
        global __electricId
        global __gasId

        self.__getToken(user, password)
        self.__electricId = self.__getResource(self.__electricclassifier)
        self.__gasId = self.__getResource(self.__gasclassifier)

    """Method for caching the initial credentials for use to retrieve 
    tokens later, as well as calling the update token method to retrieve initial token

    :param user: Username for GlowMarkt API
    :param password: Password for GlowMarkt API
    """
    def __getToken(self, user, password):
        global __glowUser
        global __glowPw
        self.__glowUser = user
        self.__glowPw = password
        self.__updateToken()

    """Method for updating the current token, based on cached credentials.
    """
    def __updateToken(self):
        global __token
        global __TOKENIZEDHEADER
        apiurl = self.__APIBASE + 'auth'
        payload = {'username': self.__glowUser, 'password': self.__glowPw}
        try:
            r = self.__postRequest(apiurl, self.__HEADER, payload);
            jsonout = json.loads(r.text)
            self.__token = jsonout["token"]
            self.__TOKENIZEDHEADER = {'Content-Type': 'application/json', 'token': self.__token, 'applicationId': self.__APPLICATIONID}
            print(">INFO: Token update successful")
            self.__getResources()
        except:
            print(">ERROR: Updating Token Failed - check connection/credentials")

    """Method for retrieving the current list of resources avaliable
    """
    def __getResources(self):
        global __resources
        apiurl = self.__APIBASE + 'resource'
        r = self.__getRequest(apiurl, self.__TOKENIZEDHEADER)
        self.__resources = json.loads(r.text)

    """Method for retrieving the matching resource based on supplied classifier
    :param classifier: The classifier to match the resource to
    :returns: Resource ID for resource which matches classifier
    """
    def __getResource(self, classifier):
        for i in range(3):
            resource = self.__resources[i]
            if resource["classifier"] == classifier:
                return resource["resourceId"]

        return ""

    """Method which returns the most recent value for a given resource ID
    :returns: Current value in kWh
    """
    def __getReadingNow(self, resourceid):
        apiurl = self.__APIBASE + 'resource/' + resourceid + '/current'
        r = self.__getRequest(apiurl, self.__TOKENIZEDHEADER);
        jsonout = json.loads(r.text)
        data = jsonout["data"]
        if jsonout["units"] == "m3":
            data[0][1] = self.__convertToSI(data[0][1], "m3")
        #    jsonout["unit"] = "kWh"
        return data[0]

    """For a given resource, returns the most recent half-hourly usage from the GlowMarkt API

    :param resourceid: ID of the resource to be polled
    :returns: Reading (in kWh)
    """
    def __getDailyRunningTotal(self, resourceid):
        dateNow = date.today()
        apiurl = self.__APIBASE + 'resource/' + resourceid + '/readings?period=P1D&function=sum&from=' + str(
            dateNow) + 'T00:00:00&to=' + str(dateNow) + 'T23:59:59'

        r = self.__getRequest(apiurl, self.__TOKENIZEDHEADER);
        jsonout = json.loads(r.text)
        data = jsonout["data"]

        data[0][1] = self.__convertToSI(data[0][1], jsonout["units"])
        return data[0]

    """Public function which returns the current electricity reading (in Watts)

    :returns: Reading (in W)
    """
    def getElectricNow(self):
        return self.__getReadingNow(self.__electricId)

    """Public function which returns the most recent reading to date from the DCC

    :returns: Reading (in kWh)
    """
    def getElectricToday(self):
        return self.__getDailyRunningTotal(self.__electricId)

    """Public function which returns the most recent reading to date from the DCC

    :returns: Reading (in kWh)
    """
    def getGasToday(self):
        return self.__getDailyRunningTotal(self.__gasId)

    """Converts non-SI Units to SI Units

    Current supported units:
        - m3 to kWh

    :param value: The value to be converted
    :param unit: The unit of the supplied value
    :returns: Converted unit
    """
    def __convertToSI(self, value, unit):
        if (unit == 'm3'):
            volumecorrection = 1.022640
            calorificvalue = 39.4
            return (value * volumecorrection * calorificvalue) / 3.6
        else:
            return value

    """Method that checks the response is valid for the HTTP GET request, and attempts to resolve the issue if not.

    Does the following
    - Attempts a native request
    - Checks status of request
    - If this is likely due to an out of date token, requests a new token and attempts again

    :param apiurl: The URL of the REST API to be queried
    :param headers: Header value for the request
    :returns: Response
    """
    def __getRequest(self, apiurl, headers):
        r = requests.get(apiurl, headers=headers)
        if r.status_code == 200:
            return r
        else:
            print(">INFO (GlowMarkt): GET Request Failed, attempting to update token")
            self.__updateToken()
            r = requests.get(apiurl, headers=headers)
            if r.status_code == 200:
                return r

    """Method that checks the response is valid for the HTTP POST request, and attempts to resolve the issue if not.

    Does the following
    - Attempts a native request
    - Checks status of request
    - If this is likely due to an out of date token, requests a new token and attempts again

    :param apiurl: The URL of the REST API to be queried
    :param headers: Header value for the request
    :returns: Response
    """
    def __postRequest(self, apiurl, headers, payload):
        r = requests.post(apiurl, headers=headers, json=payload);
        if r.status_code == 200:
            print(">INFO (GlowMarkt): POST Request Succesful")
            return r
        else:
            print(">ERROR (GlowMarkt): Post Request Failed - Check Credentials and/or connection")
