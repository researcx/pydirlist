#
# Copyright (c) 2020 by unendingPattern (https://unendingpattern.github.io). All Rights Reserved.
# You may use, distribute and modify this code under WTFPL.
# The full license is included in LICENSE.md, which is distributed as part of this project.
#

from flask import request, session, g, redirect, url_for, abort, \
     render_template, flash
from flask import Flask
from flask.views import MethodView

import uuid, time, os, time, re, signal
import pkg_resources, platform
from datetime import datetime, timedelta
import humanize

app = Flask(__name__)
app.jinja_env.cache = {}
import keiDirList.initialize
