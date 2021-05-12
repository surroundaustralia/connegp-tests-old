import urllib
import logging
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from enum import Enum
import json

media_type_iana = None


class MediaType(Enum):
    HTML = "text/html"
    JSON = "application/json"
    GEOJSON = "application/geo+json"
    TURTLE = "text/turtle"
    OAI3 = "application/vnd.oai.openapi+json;version=3.0"
    NT = "application/n-triples"


def build_response_table(list_tests, list_tests_results):
    table_list = []
    for t, r in zip(list_tests, list_tests_results):
        if len(r[1]) >= 1:
            if len(r[1][0]) > 40:
                message = r[1][0][:120] + '...'
            else:
                message = r[1][0]
        else:
            message = r[1]
        table_list.append([f"{t}", f"{r[0]}", f"{message}"])
    return table_list


def get_request(url):
    try:
        with urlopen(Request(url)) as response:
            return response
    except Exception as e:
        return e.code, str(e), None


def get_body(url):
    try:
        contents = urllib.request.urlopen(url).read()
        return contents
    except Exception as e:
        return e.code, str(e), None


def get_url_content(url: str, media_type: MediaType = None):
    if media_type is None:
        media_type = MediaType.JSON

    try:
        with urlopen(Request(url, headers={"Accept": media_type.value})) as response:
            if response.code == 200:
                if media_type == MediaType.JSON \
                        or media_type == MediaType.GEOJSON \
                        or media_type == MediaType.OAI3:
                    x = response.read().decode()
                    try:
                        return 200, json.loads(x), response.headers
                    except:
                        return 500, "", response.headers
                else:
                    return 200, response.read().decode(), response.headers
            else:
                return response.code, None, response.headers
    except HTTPError as e:
        return e.code, str(e), None
    except URLError as e:
        if hasattr(e, 'reason'):
            return 500, e.reason, None
        elif hasattr(e, 'code'):
            return 500, e.code, None


def get_media_type_iana():
    global media_type_iana

    try:
        media_type_iana = urllib.request.urlopen('https://www.iana.org/assignments/media-types/media-types.txt').read()
        return media_type_iana
    except Exception as e:
        logging.error(e)


# Get media type from iana
media_type_iana = get_media_type_iana()
