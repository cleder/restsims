import sys
import ConfigParser
from simserver import SessionServer

config = ConfigParser.SafeConfigParser()
config.read([c for c in sys.argv if c.endswith('.ini')])
try:
    path = config.get('simserver','path')
except:
    path = '/tmp/simserver/'

service = SessionServer(path)


