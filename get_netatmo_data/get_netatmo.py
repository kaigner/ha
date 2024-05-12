#!/usr/bin/env python

import requests
from sys import version_info
from os import getenv
from os.path import expanduser, exists
import json, time
import imghdr
import warnings

CREDENTIALS = expanduser("~/.netatmo_credentials")

cred = {                       # You can hard code authentication information in the following lines
        "CLIENT_ID" :  "",     #   Your client ID from Netatmo app registration at http://dev.netatmo.com/dev/listapps
        "CLIENT_SECRET" : "",  #   Your client app secret   '     '
        "USERNAME" : "",       #   Your netatmo account username
        "PASSWORD" : ""        #   Your netatmo account password
}

def getParameter(key, default):
    return getenv(key, default[key])

if exists(CREDENTIALS) :
    with open(CREDENTIALS, "r") as f:
        cred.update({k.upper():v for k,v in json.loads(f.read()).items()})

_CLIENT_ID     = getParameter("CLIENT_ID", cred)
_CLIENT_SECRET = getParameter("CLIENT_SECRET", cred)
_USERNAME      = getParameter("USERNAME", cred)
_PASSWORD = getParameter("PASSWORD", cred)

BASE_URL = "https://api.netatmo.com/"
_AUTH_REQ              = _BASE_URL + "oauth2/token"
_GETMEASURE_REQ        = _BASE_URL + "api/getmeasure"
_GETSTATIONDATA_REQ    = _BASE_URL + "api/getstationsdata"
_GETTHERMOSTATDATA_REQ = _BASE_URL + "api/getthermostatsdata"
_GETHOMEDATA_REQ       = _BASE_URL + "api/gethomedata"
_GETCAMERAPICTURE_REQ  = _BASE_URL + "api/getcamerapicture"
_GETEVENTSUNTIL_REQ = _BASE_URL + "api/geteventsuntil"


