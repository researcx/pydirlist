#
# Copyright (c) 2020 by unendingPattern (https://unendingpattern.github.io). All Rights Reserved.
# You may use, distribute and modify this code under WTFPL.
# The full license is included in LICENSE.md, which is distributed as part of this project.
#

import keiDirList

intervals = (
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
    )

def display_time(seconds, granularity=2):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])

#Code for the "page generation took x seconds" thing.
@keiDirList.app.before_request
def before_request():
    keiDirList.g.request_start_time = keiDirList.time.time()
    keiDirList.g.request_time = lambda: "%.5f" % (keiDirList.time.time() - keiDirList.g.request_start_time)

#Current time as a part of the code
@keiDirList.app.context_processor
def inject_now():
    return {'now': keiDirList.datetime.utcnow()}

#Current time in UNIX format
def unix_time_current():
    return int(keiDirList.time.time())
keiDirList.app.jinja_env.globals.update(unix_time_current=unix_time_current)

#Display how long ago something happened in a readable format
@keiDirList.app.template_filter('time_ago')
def time_ago(unixtime):
    return keiDirList.humanize.naturaltime(keiDirList.datetime.now() - keiDirList.timedelta(seconds=unix_time_current() - int(unixtime)))
keiDirList.app.jinja_env.globals.update(time_ago=time_ago)

#Display a somewhat normal date
@keiDirList.app.template_filter('human_date')
def human_date(unixtime):
    return keiDirList.datetime.fromtimestamp(int(unixtime)).strftime('%Y-%m-%d %H:%M:%S')
keiDirList.app.jinja_env.globals.update(human_date=human_date)

#Display a somewhat normal size
@keiDirList.app.template_filter('human_size')
def human_size(filesize):
    return keiDirList.humanize.naturalsize(filesize)
keiDirList.app.jinja_env.globals.update(human_size=human_size)
