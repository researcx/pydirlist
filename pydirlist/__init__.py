from flask import request, session, g, redirect, url_for, abort, \
     render_template, flash, json
from flask import Flask
from flask.views import MethodView

import uuid, time, os, time, re, signal, logging
import pkg_resources, platform
from datetime import datetime, timedelta
import humanize

logger = logging.getLogger('werkzeug')
# loading config
core_config = ""
config_path = "config.json"

with open(config_path) as config_file:
    core_config = json.load(config_file)

app = Flask(__name__)

app.config.update(dict(
    SECRET_KEY=core_config['server']['secret']
))

app.jinja_env.cache = {}
import pydirlist.initialize
