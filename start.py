# -*- coding: utf-8 -*-

import glob
import os
import re
from datetime import datetime, timedelta
from bottle import SimpleTemplate
from bottle import run, template, get, request

from utils.read_file import reverse_readline
from utils.gen_reg_exp import generate_regexp_by_format
from settings.settings import HOST, PORT
from settings.configs import CONFIGS


def get_log(config_name, date_bound, line_filter=''):
    current_conf = CONFIGS.get(config_name)
    if not current_conf:
        raise Exception('Не найдена конфигурация {}',format(config_name))

    dataset = []

    for conf in current_conf:
        if not conf.get('enabled'):
            continue
        name = conf.get('name')
        time_format = conf.get('time_format')
        time_regexp = generate_regexp_by_format(time_format)
        print conf, time_regexp

        os.chdir(conf.get('path'))
        print os.curdir, glob.glob('*')
        print glob.glob(conf.get('mask'))
        for file in glob.glob(conf.get('mask')):
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


@get('/<config>/<mins:int>')
def index(config, mins):


    filter = request.query.get('filter', '')
    try:
        log = get_log(config, datetime.now() - timedelta(minutes=int(mins)), filter)
    except Exception, e:
        return str(e)
    if not log:
        return 'logs not found'
    return SimpleTemplate('<b>Data from logs for {} minutes:</b><br><br>{}'.format(mins, log)).render()

if __name__ == '__main__':
    run(host=HOST, port=PORT)
