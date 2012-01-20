import tempfile
import tarfile, zipfile
from simservice import service
from gensim import utils

def extract_from_archive(afile):
    tmp = tempfile.NamedTemporaryFile()
    tmp.file.write(afile.read())
    tmp.file.flush()
    if tarfile.is_tarfile(tmp.name):
        tmptf = tarfile.open(tmp.name)
        for ti in tmptf.getmembers():
            if ti.isfile() and ti.size > 0 :
                tf = tmptf.extractfile(ti)
                text = tf.read()
                id = ti.name
                tf.close()
                yield {'id': id, 'text': text}
    elif zipfile.is_zipfile(tmp.name):
        tmpzip = zipfile.ZipFile(tmp.file)
        for zi in tmpzip.infolist():
            tz = tmpzip.open(zi)
            text = tz.read()
            id = tz.name
            tz.close()
            yield {'id': id, 'text': text}
    tmp.close()

def find_similar(data, min_score, max_results):
    doc = data.strip()
    if max_results > 0:
        max = max_results
    if ' ' in doc:
        doc = {'tokens': utils.simple_preprocess(data)}
    try:
        return service.find_similar(doc, min_score=min_score, max_results=max_results)
    except ValueError:
        return []

def train(data):
    service.set_autosession(False)
    service.open_session()
    i = 0
    for d in data:
        service.buffer([{'id': d['id'], 'tokens': utils.simple_preprocess(d['text'])}])
        i+=1
        print i
    service.train(method='lsi')
    #logger.info('training complete commit changes')
    service.commit()
    return i

def index(data):
    service.set_autosession(False)
    service.open_session()
    i = 0
    for d in data:
        service.buffer([{'id': d['id'], 'tokens': utils.simple_preprocess(d['text'])}])
        i += 1
        print i
    service.index()
    #logger.info('training complete commit changes')
    service.commit()
    return i
