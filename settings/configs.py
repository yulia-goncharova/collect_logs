CONFIGS = {
    'default': [
      {
        'enabled': True,
        'name': 'nginx.access',
        'path': '/var/log/nginx/',
        'mask': 'access.log',
        'time_format': '%d/%b/%Y:%X'
      },

      {
        'enabled': True,
        'name': 'nginx.error',
        'path': '/var/log/nginx/',
        'mask': 'error.log',
        'time_format': '%Y/%m/%d %X'
      },

      {
        'enabled': True,
        'name': 'supervisor',
        'path': '/var/log/supervisor/',
        'mask': 'supervisord.log',
        'time_format': '%Y-%m-%d %H:%M:%S,%f'
      },

      {
        'enabled': True,
        'name': 'supervisor.mfs.output',
        'path': '/var/log/supervisor/',
        'mask': 'mfs-stdout*.log',
        'time_format': '%Y-%m-%d %H:%M:%S,%f'
      },

      {
        'enabled': True,
        'name': 'supervisor.mfs.errors',
        'path': '/var/log/supervisor/',
        'mask': 'mfs-stderr*.log',
        'time_format': '%Y-%m-%d %H:%M:%S,%f'
      },

      {
        'enabled': True,
        'name': 'supervisor.controller.output',
        'path': '/var/log/supervisor/',
        'mask': 'controller-stdout*.log',
        'time_format': '%Y-%m-%d %H:%M:%S,%f'
      },

      {
        'enabled': True,
        'name': 'supervisor.controller.errors',
        'path': '/var/log/supervisor/',
        'mask': 'controller-stderr*.log',
        'time_format': '%Y-%m-%d %H:%M:%S,%f'
      },

      {
        'enabled': True,
        'name': 'gunicorn',
        'path': '/var/log/gunicorn/',
        'mask': 'gunicorn-back-end.conf.log',
        'time_format': '%Y-%m-%d %H:%M:%S,%f'
      },

      {
        'enabled': True,
        'name': 'postgresql',
        'path': '/var/log/postgresql/',
        'mask': 'postgresql*.log',
        'time_format': '%Y-%m-%d %X'
      },


    ]
  }