#
# Copyright (c) 2020 by unendingPattern (https://unendingpattern.github.io). All Rights Reserved.
# You may use, distribute and modify this code under WTFPL.
# The full license is included in LICENSE.md, which is distributed as part of this project.
#

import keiDirList, logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request, jsonify
from time import strftime
import traceback

# Core
import keiDirList.views.dir

# Error Logging
if keiDirList.app.debug:
    error_log = "logs/error.log"
    access_log = "logs/access.log"

    logger = logging.getLogger('werkzeug')
    logFormatStr = '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
    formatter = logging.Formatter(logFormatStr,'%m-%d %H:%M:%S')

    logging.basicConfig(format = '%(message)s', filename = access_log, level=logging.INFO)

    fileHandler = logging.FileHandler(error_log)
    fileHandler.setLevel(logging.ERROR)
    fileHandler.setFormatter(formatter)

    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logging.DEBUG)
    streamHandler.setFormatter(formatter)

    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)

    @keiDirList.app.after_request
    def after_request(response):
        timestamp = strftime('%Y-%b-%d %H:%M:%S')
        useragent = request.user_agent
        logger.info('[%s] [%s] [%s] [%s] [%s] [%s] [%s] [%s]',
            timestamp, request.remote_addr, useragent, request.method,
            request.scheme, request.full_path, response.status, request.referrer)
        return response

    @keiDirList.app.errorhandler(Exception)
    def exceptions(e):
        tb = traceback.format_exc()
        timestamp = strftime('[%Y-%b-%d %H:%M]')
        logger.error('%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s',
            timestamp, request.remote_addr, request.method,
            request.scheme, request.full_path, tb)
        return e.status_code

#Run the main app...
if __name__ == '__main__':
    keiDirList.app.run(threaded=True)

#Run the main app...
if __name__ == '__main__':
    keiDirList.app.run()
