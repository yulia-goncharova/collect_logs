import ConfigParser
import glob
import os
import re
from datetime import datetime, timedelta
from bottle import SimpleTemplate
from bottle import run, template, get, request

from utils.read_file import reverse_readline
from settings.settings import HOST, PORT

config = ConfigParser.RawConfigParser()


def get_log(date_bound, line_filter=''):
    config.read('settings/collect_logs.cfg')
    dataset = []

    for name in config.sections():
        path = config.get(name, 'path')
        mask = config.get(name, 'mask')
        time_regexp = config.get(name, 'time_regexp')
        time_format = config.get(name, 'time_format')

        os.chdir(path)
        for file in glob.glob(mask):
            print 'loading {},{}'.format(file, datetime.now())
            for line in reverse_readline(file):
                if line_filter and not (line_filter in line or line_filter in name):
                    continue
                dt = re.search(time_regexp, line)
                if not dt:
                    continue
                dt = dt.group(0)
                dt = datetime.strptime(dt, time_format)
                if dt < date_bound:
                    break
                dataline = {'name': name, 'file': file, "dt": dt, "line": '<b>'+name+'</b>: '+line}
                dataset.append(dataline)


            print 'loaded {},{}'.format(file, datetime.now())
    dataset_sorted= sorted(dataset, key=lambda k: k['dt'], reverse=True)
    return '<br>'.join([l['line'] for l in dataset_sorted])


@get('/<mins:int>')
def index(mins):
    filter = request.query.get('filter', '')
    try:
        log = get_log( datetime.now() - timedelta(minutes=int(mins)), filter)
    except Exception, e:
        return template(str(e))
    if not log:
        return template('logs not found')
    return SimpleTemplate('<b>Data from logs for {} minutes:</b><br><br>{}'.format(mins, log)).render()

if __name__ == '__main__':
    run(host=HOST, port=PORT)
