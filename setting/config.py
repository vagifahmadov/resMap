from flask import Flask, jsonify, request, Blueprint, make_response, url_for, render_template
from flask_cors import CORS
import requests, json, bson
import calendar
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from jsondiff import diff
import random
from hashlib import sha256
import base64
from datetime import datetime, timedelta, date
from time import gmtime, strftime, localtime
import pandas
from functools import reduce

from flask_jwt_extended import JWTManager, create_access_token

apps = Flask(__name__, static_folder='../static', template_folder='../templates')

jwt = JWTManager(apps)

apps.secret_key = "AJSSsdCC25"
