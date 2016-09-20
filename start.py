import glob, os
from datetime import datetime, timedelta
import re
import pandas as pd
from bottle import route, run, template, get, request
from bottle import SimpleTemplate

import ConfigParser

config = ConfigParser.RawConfigParser()

def reverse_readline(filename, buf_size=8192):
    """a generator that returns the lines of a file in reverse order"""
    with open(filename) as fh:
        segment = None
        offset = 0
        fh.seek(0, os.SEEK_END)
        file_size = remaining_size = fh.tell()
        while remaining_size > 0:
            offset = min(file_size, offset + buf_size)
            fh.seek(file_size - offset)
            buffer = fh.read(min(remaining_size, buf_size))
            remaining_size -= buf_size
            lines = buffer.split('\n')
            # the first line of the buffer is probably not a complete line so
            # we'll save it and append it to the last line of the next buffer
            # we read
            if segment is not None:
                # if the previous chunk starts right from the beginning of line
                # do not concact the segment to the last line of new chunk
                # instead, yield the segment first
                if buffer[-1] is not '\n':
                    lines[-1] += segment
                else:
                    yield segment
            segment = lines[0]
            for index in range(len(lines) - 1, 0, -1):
                if len(lines[index]):
                    yield lines[index]
        # Don't yield None if the file was empty
        if segment is not None:
            yield segment

def get_log(date_bound, line_filter=''):
    config.read('collect_logs.cfg')
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
                if line_filter and not line_filter in line:
                    continue
                dt = re.search(time_regexp, line)
                if not dt:
                    continue
                dt = dt.group(0)
                dt = datetime.strptime(dt, time_format)
                if dt < date_bound:
                    break

                dataset.append([name, file, dt,line])

            print 'loaded {},{}'.format(file, datetime.now())

    pds = pd.DataFrame(dataset, columns=('name', 'file', 'datetime', 'line'))
    pds['fulline'] = '<b>'+pds.name+'</b>: '+pds.line
    pds_filtered= pds.sort_values('datetime', ascending=False)
    return '<br>'.join(pds_filtered.fulline)


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


run(host='0.0.0.0', port=8880)
