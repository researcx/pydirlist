import pydirlist, random

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
@pydirlist.app.before_request
def before_request():
    pydirlist.g.request_start_time = pydirlist.time.time()
    pydirlist.g.request_time = lambda: "%.5f" % (pydirlist.time.time() - pydirlist.g.request_start_time)

def get_banner():
    banners = pydirlist.core_config['site']['banners']
    random_index = random.randint(0,len(banners)-1)
    return banners[random_index]
pydirlist.app.jinja_env.globals.update(get_banner=get_banner)

def get_footer():
    footers = pydirlist.core_config['site']['footers']
    random_index = random.randint(0,len(footers)-1)
    return footers[random_index]
pydirlist.app.jinja_env.globals.update(get_footer=get_footer)

def shorten_text(s, n):
    if len(s) <= n:
        # string is already short-enough
        return s
    # half of the size, minus the 3 .'s
    n_2 = int(n) / 2 - 3
    # whatever's left
    n_1 = n - n_2 - 3
    return '{0}...{1}'.format(s[:int(n_1)], s[-int(n_2):])
pydirlist.app.jinja_env.globals.update(shorten_text=shorten_text)

#Current time as a part of the code
@pydirlist.app.context_processor
def inject_now():
    return {'now': pydirlist.datetime.utcnow()}

#Current time in UNIX format
def unix_time_current():
    return int(pydirlist.time.time())
pydirlist.app.jinja_env.globals.update(unix_time_current=unix_time_current)

#Display how long ago something happened in a readable format
@pydirlist.app.template_filter('time_ago')
def time_ago(unixtime):
    return pydirlist.humanize.naturaltime(pydirlist.datetime.now() - pydirlist.timedelta(seconds=unix_time_current() - int(unixtime)))
pydirlist.app.jinja_env.globals.update(time_ago=time_ago)

#Display a somewhat normal date
@pydirlist.app.template_filter('human_date')
def human_date(unixtime):
    return pydirlist.datetime.fromtimestamp(int(unixtime)).strftime('%Y-%m-%d %H:%M:%S')
pydirlist.app.jinja_env.globals.update(human_date=human_date)

#Display a somewhat normal date
@pydirlist.app.template_filter('rss_date')
def rss_date(unixtime):
    return pydirlist.datetime.fromtimestamp(int(unixtime)).strftime('%a, %d %b %Y %H:%M:%S GMT')
pydirlist.app.jinja_env.globals.update(rss_date=rss_date)


@pydirlist.app.template_filter('recent_date')
#@pydirlist.cache.memoize(timeout=60) # recent_date
def recent_date(unixtime):
    dt = pydirlist.datetime.fromtimestamp(unixtime)
    today = pydirlist.datetime.now()
    today_start = pydirlist.datetime(today.year, today.month, today.day)
    yesterday_start = pydirlist.datetime.now() - pydirlist.timedelta(days=1)

    def day_in_this_week(date):
        startday = pydirlist.datetime.now() - pydirlist.timedelta(days=today.weekday())
        if(date >= startday):
            return True
        else:
            return False

    timeformat = '%b %d, %Y'
    if day_in_this_week(dt):
        timeformat = '%A at %H:%M'
    if(dt >= yesterday_start):
        timeformat = 'Yesterday at %H:%M'
    if(dt >= today_start):
        timeformat = 'Today at %H:%M'

    return(dt.strftime(timeformat))
pydirlist.app.jinja_env.globals.update(recent_date=recent_date)

#Display a somewhat normal size
@pydirlist.app.template_filter('human_size')
def human_size(filesize):
    return pydirlist.humanize.naturalsize(filesize)
pydirlist.app.jinja_env.globals.update(human_size=human_size)
