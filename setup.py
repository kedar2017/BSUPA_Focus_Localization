try:
        from setuptools import setup
except ImportError:
        from distutils.core import setup

install_requires = ['blist', 'cassandra-driver', 'numpy', 'pyyaml']

config = {
    'description'      : 'Summer internship python project',
    'author'           : 'Manoj Gudi',
    'url'              : 'getfocus.in',
    'download_url'     : 'https://bitbucket.org/focusanalytics/summer_internship_15',
    'author_email'     : 'manoj@getfocus.in',
    'version'          : '0.1',
    'install_requires' : install_requires,
    'packages'         : ['bsupa'],
    'scripts'          : [],
    'name'             : 'bsupa'
}

setup(**config)
