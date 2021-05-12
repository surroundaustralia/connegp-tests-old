from utils.utils import *
import logging
import urllib
import json
import re

media_types = ["text/html",
               "application/json",
               "application/geo+json",
               "text/turtle",
               "application/vnd.oai.openapi+json;version=3.0",
               "application/n-triples"]


class AlternateFunctionalTests:
    @staticmethod
    def ref3_1_a(url):
        """
        Profile requested for the resource representation is indicated by [a] token ...
        which MUST be appended to the resource's URI as a Query String Argument.

        :param url: Url
        """
        messages = []
        url = f"{url}?_profile=alt"
        response = get_request(url)
        headers = response.getheaders()
        # Check if 'link' in headers
        h_link = None
        for h in headers:
            if 'link' in h:
                h_link = h

        if h_link is None:
            return False, messages.append('Link header not found')

        success_token = False
        for h in h_link[1].split(','):
            if 'token="alt"' in h:
                success_token = True

        if success_token:
            result = True
        else:
            result = False
            messages.append("Token alt not found.")
        return result, messages

    @staticmethod
    def ref3_1_b(url):
        """
        Resource URLs for which QSA-based profile negotiation is taking place SHOULD NOT
        themselves be QSA values of other resource URIs in any QSA-based system.

        :param url: Url
        """
        messages = []
        url = f"{url}?_profile=alt"
        response = get_request(url)
        headers = response.getheaders()
        # Check if 'link' in headers
        h_link = None
        for h in headers:
            if 'link' in h:
                h_link = h

        if h_link is None:
            return False, messages.append('Link header not found')

        success_token = False
        for h in h_link[1].split(','):
            if 'token="alt"' in h:
                success_token = True

        if success_token:
            result = True
        else:
            result = False
            messages.append("Token alt not found.")
        return result, messages

    @staticmethod
    def ref3_1_c(url):
        """
        The token MUST be mappable to a profile URI within one particular client/server session

        :param url: Url
        """
        messages = []
        url = f"{url}?_profile=alt"
        response = get_request(url)
        headers = response.getheaders()
        # Check if 'link' in headers
        h_link = None
        for h in headers:
            if 'link' in h:
                h_link = h

        if h_link is None:
            return False, messages.append('Link header not found')

        success_profile = False
        for h in h_link[1].split(','):
            if 'token="alt"' in h:
                anchor_url = re.findall(
                    'anchor=<http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+>', h)
                if len(anchor_url) >= 1:
                    success_profile = True

        if success_profile:
            result = True
        else:
            result = False
            messages.append("Token is not mappeable to profile URI")
        return result, messages

    @staticmethod
    def ref3_1_d(url):
        """
        Additional aspects of content negotiation MAY be included in such URIs by the use of additional QSA
        or by any other techniques (for example HTTP headers).

        :param url: Url
        """
        messages = []
        url = f"{url}?_profile=alt"
        response = get_request(url)
        headers = response.getheaders()
        # Check if 'link' in headers
        h_link = None
        for h in headers:
            if 'link' in h:
                h_link = h

        if h_link is None:
            return False, messages.append('Link header not found')

        success_additional_info = False
        for h in h_link[1].split(','):
            if 'rel="alternate"' in h:
                success_additional_info = True

        if success_additional_info:
            result = True
        else:
            result = False
            messages.append('Error with additional aspects in content negotiation.')
        return result, messages

    @staticmethod
    def ref3_2_a(url):
        """
        A QSA key MUST be used to indicate a profile token

        :param url: Url
        """
        messages = []
        url = f"{url}?_profile=alt"
        response_1 = get_request(url)

        url = f"{url}?_profile=oai"
        response_2 = get_request(url)

        url = f"{url}?_profile=geosp"
        response_3 = get_request(url)

        if response_1.status != 200 or response_2.status != 200 or response_3.status != 200:
            result = False
            messages.append("Fail to negotiate for particular token profile.")
        else:
            result = True
        return result, messages

    @staticmethod
    def ref3_2_b(url):
        """
        The server MUST implement methods to allow clients to discover the QSA key used in place of
        the "QSA Functional Profile"'s _profile

        :param url: Url
        """
        messages = []
        url = f"{url}?_profile=alt&_mediatype=application/json"
        content = json.load(urllib.request.urlopen(url))
        success_profile_methods = False
        if content:
            if content['profiles']:
                profiles = content['profiles']
                if len(profiles) >= 1:
                    success_profile_methods = True

        if success_profile_methods:
            result = True
        else:
            result = False
            messages.append("Server does not show a method to show profile methods.")
        return result, messages

    @staticmethod
    def ref3_2_c(url):
        """
        A QSA key SHOULD be used to indicate a resource representation's Media Type

        :param url: Url
        """
        messages = []
        url = f"{url}?_profile=alt&_mediatype=text/html"
        response_1 = get_request(url)

        url = f"{url}?_profile=alt&_mediatype=application/geo+json"
        response_2 = get_request(url)

        url = f"{url}?_profile=alt&_mediatype=application/json"
        response_3 = get_request(url)

        if response_1.status != 200 or response_2.status != 200 or response_3.status != 200:
            result = False
            messages.append("Fail to negotiate for particular Media Types.")
        else:
            result = True
        return result, messages

    @staticmethod
    def ref3_2_d(url):
        """
        The server MUST implement methods to allow clients to discover the QSA key used in
        place of the "QSA Functional Profile"'s _mediatype

        :param url: Url
        """

        messages = []
        url = f"{url}?_profile=oai"
        response = get_request(url)
        headers = response.getheaders()
        # Check if 'link' in headers
        h_link = None
        for h in headers:
            if 'link' in h:
                h_link = h

        if h_link is None:
            return False, messages.append('Link header not found')

        success_type = True
        not_found = []
        for h in h_link[1].split(','):
            if 'type=' in h:
                group = re.findall('[ \t]*_mediatype=[ \t]*([^\n\r]*)>', h)
                if group:
                    if group[0].split(' ')[0] not in media_types:
                        success_type = False
                        not_found.append(group[0].split(' ')[0])

        if success_type:
            result = True
        else:
            result = False
            if not success_type:
                messages.append(f"'type='{not_found} not found in alternatives.")
        return result, messages

    @staticmethod
    def ref3_2_e(url):
        """
        Tokens registered at IANA's Media Types list SHOULD be used as tokens for Media Type identifiers

        :param url: Url
        """

        # Get mediatypes from IANA
        messages = []
        url = f"{url}?_profile=alt"
        response = get_request(url)
        headers = response.getheaders()
        # Check if 'link' in headers
        h_link = None
        for h in headers:
            if 'link' in h:
                h_link = h

        if h_link is None:
            return False, messages.append('Link header not found')

        success_media_type_iana = True
        media_type_not_included = []
        for h in h_link[1].split(','):
            if 'type=' in h:
                group = re.findall('[ \t]*_mediatype=[ \t]*([^\n\r]*)>', h)
                if group:
                    if group[0] not in str(media_type_iana):
                        success_media_type_iana = False
                        media_type_not_included.append(group[0])

        if success_media_type_iana:
            result = True
        else:
            result = False
            messages.append(f"Mediatype not included: {media_type_not_included}")
        return result, messages

    @staticmethod
    def ref3_3_b(url):
        """
        The server MUST implement methods to allow clients to discover the QSA key/value pair
        used in place of the "QSA Functional Profile"'s _profile=alt

        :param url: Url
        """
        messages = []
        url = f"{url}?_profile=alt&_mediatype=application/json"
        content = json.load(urllib.request.urlopen(url))
        success_profile_methods = False
        if content:
            if content['profiles']:
                profiles = content['profiles']
                if len(profiles) >= 1:
                    success_profile_methods = True

        if success_profile_methods:
            result = True
        else:
            result = False
            messages.append("Server does not show a method to show profile methods.")
        return result, messages

    @staticmethod
    def ref3_3_c(url):
        """
        The server's response to a list profiles request SHOULD be to present a list of
        all profiles that it supports representations of the resource for and
        optionally also supported Media Types for those representations.

        :param url: Url
        """

        messages = []
        url = f"{url}?_profile=oai"
        response = get_request(url)
        headers = response.getheaders()
        # Check if 'link' in headers
        h_link = None
        for h in headers:
            if 'link' in h:
                h_link = h

        if h_link is None:
            return False, messages.append('Link header not found')

        profiles = []
        for h in h_link[1].split(','):
            if 'profile=' in h:
                group = re.findall('[ \t]*profile="[ \t]*([^\n\r]*)"', h)
                if group:
                    profiles.append(group[0])
        if len(profiles) >= 1:
            result = True
        else:
            result = False
            messages.append("List profiles not presented.")
        return result, messages

    @staticmethod
    def ref3_3_d(url):
        """
        The server SHOULD represent the alternate profiles information in the HTTP header of
        the response, as per the HTTP Headers functional profile (using a Link header)

        :param url: Url
        """

        messages = []
        url = f"{url}?_profile=oai"
        response = get_request(url)
        headers = response.getheaders()
        # Check if 'link' in headers
        h_link = None
        for h in headers:
            if 'link' in h:
                h_link = h

        if h_link is None:
            return False, messages.append('Link header not found')

        success_alternate = False
        for h in h_link[1].split(','):
            if 'rel="alternate"' in h:
                success_alternate = True

        if success_alternate:
            result = True
        else:
            result = False
            messages.append("Alternate profiles not found in Headers")
        return result, messages

    @staticmethod
    def ref3_3_e(url):
        """
        The server MAY also represent the information in the response body in place
        of the default profile representation of a resource

        :param url: Url
        """

        messages = []
        url = f"{url}"
        content = json.load(urllib.request.urlopen(url))

        # Check if 'link' in headers
        if 'collection' in content:
            res = content['collection']['links']

        if len(content) >= 1:
            result = True
        else:
            result = False

        return result, messages

    @staticmethod
    def ref3_3_f(url):
        """
        Media Types of the response by using the same Media Type negotiation method used
        for the get resource by profile function.

        :param url: Url
        """
        messages = []
        url = f"{url}?_profile=alt&_mediatype=text/html"
        response_1 = get_request(url)

        url = f"{url}?_profile=alt&_mediatype=application/geo+json"
        response_2 = get_request(url)

        url = f"{url}?_profile=alt&_mediatype=application/json"
        response_3 = get_request(url)

        if response_1.status != 200 or response_2.status != 200 or response_3.status != 200:
            result = False
            messages.append("Fail to negotiate for particular Media Types.")
        else:
            result = True
        return result, messages

    @staticmethod
    def ref3_4_a(url):
        """
        Implementations of this specification according to the QSA Functional Profiles MUST communicate
        their alternate representations information as per the Alternate Representations Data Model.

        :param url: Url
        """
        messages = []
        url = f"{url}?_profile=alt"
        response = get_request(url)
        headers = response.getheaders()
        # Check if 'link' in headers
        h_link = None
        for h in headers:
            if 'link' in h:
                h_link = h

        if h_link is None:
            return False, messages.append('Link header not found')

        success_rel = False
        success_type = False
        success_format = False
        profile = False
        for h in h_link[1].split(','):
            if 'rel=' in h:
                success_rel = True
            if 'type=' in h:
                success_type = True
            if 'format=' in h:
                success_format = True
            if 'profile=' in h:
                profile = True

        if success_rel and success_type and success_format:
            result = True
        else:
            result = False
            if not success_rel:
                messages.append("'rel=' not found in alternatives.")
            if not success_type:
                messages.append("'type=' not found in alternatives.")
            if not success_format and profile:
                messages.append(
                    "'format=' not found in alternatives, 'profile=' found it. 'profile=' should be change to 'format='")
            else:
                messages.append("'format=' not found in alternatives.")
        return result, messages

    @staticmethod
    def ref3_4_b(url):
        """
        They MAY do so using HTTP Link headers, as per the HTTP Headers functional profile,
        or they MAY use other approaches.

        :param url: Url
        """
        messages = []
        url = f"{url}?_profile=alt"
        response = get_request(url)
        headers = response.getheaders()
        # Check if 'link' in headers
        h_link = None
        for h in headers:
            if 'link' in h:
                h_link = h

        if h_link is None:
            return False, messages.append('Link header not found')

        success_rel = False
        success_type = False
        success_format = False
        profile = False
        for h in h_link[1].split(','):
            if 'rel=' in h:
                success_rel = True
            if 'type=' in h:
                success_type = True
            if 'format=' in h:
                success_format = True
            if 'profile=' in h:
                profile = True

        if success_rel and success_type and success_format:
            result = True
        else:
            result = False
            if not success_rel:
                messages.append("'rel=' not found in alternatives.")
            if not success_type:
                messages.append("'type=' not found in alternatives.")
            if not success_format and profile:
                messages.append("'format=' not found in alternatives, 'profile=' found it. 'profile=' should be change to 'format='")
            else:
                messages.append("'format=' not found in alternatives.")
        return result, messages

def run_tests(url):
    tests_list = [method for method in dir(AlternateFunctionalTests) if method.startswith('__') is False]
    pass_tests = 0
    results = []
    for test in tests_list:
        r = getattr(AlternateFunctionalTests, test)(url)
        results.append(r)
        if r[0]:
            pass_tests += 1
        logging.info(f"Test: {test} - Result: {r}")
    logging.info("Total passed tests: {} - Total tests: {}".format(pass_tests, len(tests_list)))
    return tests_list, results, pass_tests, len(tests_list)
