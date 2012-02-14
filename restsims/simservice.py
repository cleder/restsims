import sys
import ConfigParser
from simserver import SessionServer
from gensim import utils

config = ConfigParser.SafeConfigParser()
config.read([c for c in sys.argv if c.endswith('.ini')])
try:
    path = config.get('simserver','path')
except:
    path = '/tmp/simserver/'

service = SessionServer(path)


def find_similar(data, min_score, max_results):
    if isinstance(data, basestring):
        doc = data.strip()
        if ' ' in doc:
            doc = {'tokens': utils.simple_preprocess(data)}
        try:
            return {'status': 'OK', 'response':
                                service.find_similar(doc,
                                min_score=min_score,
                                max_results=max_results)}
        except ValueError:
            return {'status': 'NOTFOUND', 'response':[]}
    else:
        result = {}
        for doc in data:
            try:
                result[doc] = (service.find_similar(
                                doc,
                                min_score=min_score,
                                max_results=max_results))
            except ValueError:
                pass
        if result:
            return {'status': 'OK', 'response': result}
        else:
            return {'status': 'NOTFOUND', 'response':[]}

def _buffer(aservice, data):
    i = 0
    for d in data:
        if 'tokens' in d:
            aservice.buffer([{'id': d['id'], 'tokens': d['tokens']}])
        else:
            aservice.buffer([{'id': d['id'],
                'tokens': utils.simple_preprocess(d['text'])}])
        i+=1
    return i


def train(data):
    service.set_autosession(False)
    service.open_session()
    i = _buffer(service, data)
    service.train(method='lsi')
    #logger.info('training complete commit changes')
    service.commit()
    service.set_autosession(True)
    return {'status': 'OK', 'response':i}

def index(data):
    service.set_autosession(False)
    service.open_session()
    i =_buffer(service, data)
    service.index()
    #logger.info('training complete commit changes')
    service.commit()
    service.set_autosession(True)
    return {'status': 'OK', 'response':i}



def optimize():
    service.set_autosession(False)
    service.open_session()
    service.optimize()
    service.commit()
    service.set_autosession(True)
    return {'status': 'OK', 'response': 'index optimized'}

def delete(data):
    service.set_autosession(False)
    service.open_session()
    service.delete(data)
    service.commit()
    service.set_autosession(True)
    return {'status': 'OK', 'response': 'documents deleted'}

def status():
    return {'status': 'OK', 'response': service.status()}

def indexed_documents():
    return {'status': 'OK', 'response': service.keys()}

def is_indexed(doc):
    return {'status': 'OK', 'response': doc in service.keys()}

