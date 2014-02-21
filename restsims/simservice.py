import logging
import sys
import ConfigParser
from simserver import SessionServer

config = ConfigParser.SafeConfigParser()
config.read([c for c in sys.argv if c.endswith('.ini')])
try:
    path = config.get('simserver','path')
except:
    path = '/tmp/simserver/'

logger = logging.getLogger(__file__)


class SimService(object):

    def __init__(self, path, preprocess, deaccent=True, lowercase=True,
        stemmer=None, stopwords=None):
        self.service = SessionServer(path)
        self.deaccent = deaccent
        self.lowercase = lowercase
        self.preprocess = preprocess
        self.stemmer = stemmer
        self.stopwords = stopwords

    def find_similar(self, data, min_score, max_results):
        if isinstance(data, basestring):
            doc = data.strip()
            if ' ' in doc:
                doc = {'tokens': self.preprocess(data, deacc=self.deaccent,
                    lowercase=self.lowercase, errors='ignore',
                    stemmer=self.stemmer, stopwords=self.stopwords)}
            try:
                return {'status': 'OK', 'response':
                                    self.service.find_similar(doc,
                                    min_score=min_score,
                                    max_results=max_results)}
            except ValueError:
                return {'status': 'NOTFOUND', 'response':[]}
        else:
            result = {}
            for doc in data:
                try:
                    result[doc] = (self.service.find_similar(
                                    doc,
                                    min_score=min_score,
                                    max_results=max_results))
                except ValueError:
                    pass
            if result:
                return {'status': 'OK', 'response': result}
            else:
                return {'status': 'NOTFOUND', 'response':[]}

    def _buffer(self, data):
        i = 0
        for d in data:
            if 'tokens' in d:
                self.service.buffer([{'id': d['id'], 'tokens': d['tokens']}])
            else:
                self.service.buffer([{'id': d['id'],
                    'tokens': list(self.preprocess(d['text'], deacc=self.deaccent,
                    lowercase=self.lowercase, errors='ignore',
                    stemmer=self.stemmer, stopwords=self.stopwords))}])
            i+=1
        return i

    def train(self, data):
        self.service.set_autosession(False)
        self.service.open_session()
        i = self._buffer(data)
        self.service.train(method='lsi')
        logger.info('training complete commit changes')
        self.service.commit()
        self.service.set_autosession(True)
        return {'status': 'OK', 'response':i}

    def index(self, data):
        self.service.set_autosession(False)
        self.service.open_session()
        i = self._buffer(data)
        self.service.index()
        logger.info('indexing complete commit changes')
        self.service.commit()
        self.service.set_autosession(True)
        return {'status': 'OK', 'response':i}

    def optimize(self):
        self.service.set_autosession(False)
        self.service.open_session()
        self.service.optimize()
        self.service.commit()
        self.service.set_autosession(True)
        return {'status': 'OK', 'response': 'index optimized'}

    def delete(self, data):
        self.service.set_autosession(False)
        self.service.open_session()
        self.service.delete(data)
        self.service.commit()
        self.service.set_autosession(True)
        return {'status': 'OK', 'response': 'documents deleted'}

    def status(self):
        return {'status': 'OK', 'response': self.service.status()}

    def indexed_documents(self):
        return {'status': 'OK', 'response': self.service.keys()}

    def is_indexed(self, doc):
        return {'status': 'OK', 'response': doc in self.service.keys()}

