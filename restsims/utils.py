import tempfile
import tarfile, zipfile
from gensim.utils import tokenize

# improved list from Stone, Denis, Kwantes (2010)
STOPWORDS = """
a about above across after afterwards again against all almost alone along already also although always am among amongst amoungst amount an and another any anyhow anyone anything anyway anywhere are around as at back be
became because become becomes becoming been before beforehand behind being below beside besides between beyond bill both bottom but by call can
cannot cant co computer con could couldnt cry de describe
detail did do doesn done down due during
each eg eight either eleven else elsewhere empty enough etc even ever every everyone everything everywhere except few fifteen
fify fill find fire first five for former formerly forty found four from front full further get give go
had has hasnt have he hence her here hereafter hereby herein hereupon hers herself him himself his how however hundred i ie
if in inc indeed interest into is it its itself keep last latter latterly least less ltd
just
kg km
made many may me meanwhile might mill mine more moreover most mostly move much must my myself name namely
neither never nevertheless next nine no nobody none noone nor not nothing now nowhere of off
often on once one only onto or other others otherwise our ours ourselves out over own part per
perhaps please put rather re
quite
rather really regarding
same see seem seemed seeming seems serious several she should show side since sincere six sixty so some somehow someone something sometime sometimes somewhere still such system take ten
than that the their them themselves then thence there thereafter thereby therefore therein thereupon these they thick thin third this those though three through throughout thru thus to together too top toward towards twelve twenty two un under
until up unless upon us used using
various very very via
was we well were what whatever when whence whenever where whereafter whereas whereby wherein whereupon wherever whether which while whither who whoever whole whom whose why will with within without would yet you
your yours yourself yourselves
"""
STOPWORDS = frozenset(w for w in STOPWORDS.split() if w)


def simple_preprocess(doc, deacc=True, lowercase=True):
    """
    Convert a document into a list of tokens.

    This lowercases, tokenizes, stems, normalizes etc. -- the output are final,
    utf8 encoded strings that won't be processed any further.
    """
    tokens = [token.encode('utf8') for token in
                tokenize(doc, lowercase=lowercase, deacc=deacc, errors='ignore')
            if 2 <= len(token) <= 25 and
                not token.startswith('_') and
                token not in STOPWORDS]
    return tokens


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

