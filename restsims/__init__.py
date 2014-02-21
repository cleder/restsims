import logging
from pyramid.config import Configurator
from restsims import utils

logger = logging.getLogger(__file__)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    try:
        f = open('stopwords.txt', 'r')
        utils.STOPWORDS = frozenset(w.encode('utf8') for w in f.read().split() if w)
        f.close()
        logger.info('using stopwords.txt file with %i stopwords' % len(utils.STOPWORDS))
    except:
        logger.warn('stopwords.txt not found using default english stopword list')
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.scan()
    return config.make_wsgi_app()
