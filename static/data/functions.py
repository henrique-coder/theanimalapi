# Built-in modules
from typing import Any, Union, Dict
from http import HTTPStatus
from pathlib import Path

# Third-party modules
from faker import Faker
from flask import request as flask_request
from httpx import head, HTTPError
from orjson import loads as orjson_loads


# Constants
fake = Faker()


class CacheTools:
    """
    A class for cache tools.
    """

    @staticmethod
    def gen_cache_key(*args, **kwargs) -> str:
        """
        Generate a cache key for the current request.
        :param args: The arguments for the current request.
        :param kwargs: The keyword arguments for the current request.
        :return: A cache key for the current request.
        """

        return flask_request.url


def get_animal_images() -> Dict[Any, Any]:
    return orjson_loads(Path('dynamic', 'animal_images.json').read_bytes())

def get_animal_translations() -> Dict[Any, Any]:
    return orjson_loads(Path('dynamic', 'animal_translations.json').read_bytes())

def get_animal_translation(translations: Dict[Any, Any], name: str, language: str = None) -> Dict[str, Union[str, int]]:
    if name not in translations:
        return {'error': 'Animal not found in the database'}

    if language is None:
        language = 'en'

    elif language not in translations[name]:
        return {'message': 'Language not found in the database'}

    return {'name': translations[name][language]}
