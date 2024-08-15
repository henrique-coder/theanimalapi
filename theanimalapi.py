# Built-in modules
from http import HTTPStatus
from pathlib import Path
from typing import *

# Third-party modules
from flask import *
from flask_caching import Cache
from flask_compress import Compress
from flask_cors import CORS
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect
from orjson import loads as orjson_loads
from werkzeug.middleware.proxy_fix import ProxyFix

from PIL import Image
from httpx import get
from io import BytesIO
from random import choice
from typing import Union

# Local modules
from static.data.functions import CacheTools, get_animal_images, get_animal_translations, get_animal_translation
from static.data.logger import logger


# Setup Flask application and debugging mode
app = Flask(__name__)

# Setup Flask cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
logger.info(f'Flask cache enabled. Cache type: {cache.config["CACHE_TYPE"]}')

# Setup Talisman for security headers
talisman = Talisman(app, content_security_policy={'default-src': ["'self'", 'https://cdnjs.cloudflare.com'], 'style-src': ["'self'", "'unsafe-inline'", 'https://cdnjs.cloudflare.com'], 'script-src': ["'self'", 'https://cdnjs.cloudflare.com']})
logger.info('Talisman security headers enabled')

# Setup Flask CSRF protection
CSRFProtect(app)
logger.info('CSRF protection enabled')

# Setup Flask Compress for GZIP compression
Compress(app)
logger.info('Response compression enabled')

# Setup Flask CORS
CORS(app, resources={r'*': {'origins': '*'}})
logger.info('CORS enabled')

# Fix for Flask behind a reverse proxy
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# Load the animal data
animal_images = get_animal_images()
animal_translations = get_animal_translations()

url_path = animal_images['path']
image_ext = 'jpg'


# Setup API routes
@app.route('/', methods=['GET'])
@cache.cached(timeout=86400, make_cache_key=CacheTools.gen_cache_key)
def index() -> Tuple[Response, HTTPStatus]:
    return redirect('/docs', code=HTTPStatus.MOVED_PERMANENTLY), HTTPStatus.MOVED_PERMANENTLY


@app.route('/docs', methods=['GET'])
@cache.cached(timeout=86400, make_cache_key=CacheTools.gen_cache_key)
def docs() -> Tuple[str, render_template]:
    return render_template('docs.html'), HTTPStatus.OK


@app.route('/api', methods=['GET'])
@cache.cached(timeout=1, make_cache_key=CacheTools.gen_cache_key)
def api() -> Tuple[Response, HTTPStatus]:
    return jsonify({'message': 'API working successfully', 'availableVersions': ['v1']}), HTTPStatus.OK


@app.route('/api/<version>')
@cache.cached(timeout=1, make_cache_key=CacheTools.gen_cache_key)
def v1_api_version(version: str) -> Tuple[Response, HTTPStatus]:
    if version != 'v1':
        return jsonify({'message': 'Invalid API version'}), HTTPStatus.NOT_FOUND

    return jsonify({'message': f'The {version} API working successfully'}), HTTPStatus.OK


@app.route('/api/v1/<function>')
@cache.cached(timeout=1, make_cache_key=CacheTools.gen_cache_key)
def v1_api_version_function(function: str) -> Tuple[Response, HTTPStatus]:
    if function != 'search':
        return jsonify({'message': 'Invalid API function'}), HTTPStatus.NOT_FOUND

    return jsonify({'message': 'API function working successfully'}), HTTPStatus.OK


@app.route('/api/v1/search/<endpoint>')
@cache.cached(timeout=1, make_cache_key=CacheTools.gen_cache_key)
def v1_api_version_function_endpoint(endpoint: str) -> Tuple[Response, HTTPStatus]:
    if endpoint != 'animal':
        return jsonify({'message': 'Invalid API endpoint'}), HTTPStatus.NOT_FOUND

    return jsonify({'message': 'API endpoint working successfully'}), HTTPStatus.OK


@app.route('/api/v1/search/animal', methods=['GET'])
@cache.cached(timeout=1, make_cache_key=CacheTools.gen_cache_key)
def v1_api_search_animal() -> Union[Any, HTTPStatus]:
    input_name = request.args.get('name')
    input_id = request.args.get('id')
    input_lang = request.args.get('lang')


if __name__ == '__main__':
    # Load the configuration file
    current_path = Path(__file__).parent
    config_path = Path(current_path, 'config.json')
    config = orjson_loads(config_path.read_text())

    # Setting up Flask default configuration
    app.static_folder = Path(current_path, config['flask']['staticFolder'])
    app.template_folder = Path(current_path, config['flask']['templateFolder'])

    # Run the web server with the specified configuration
    logger.info(f'Starting web server at {config["flask"]["host"]}:{config["flask"]["port"]}')
    app.run(debug=True, host=config['flask']['host'], port=config['flask']['port'], threaded=config['flask']['threadedServer'])
