from utils.utils import *
import logging
import urllib
import re


class StringFunctionalTests:
    @staticmethod
    def ref2_1_a(url):
        """
        A profile that a resource representation conforms to is indicated by
        token which MUST be appended to the resource's URI as a Query String Argument.

        :param url: Url
        """
        messages = []
        url = f"{url}?_profile=alt"
        response = get_request(url)
        if response.status == 200:
            result = True
        else:
            result = False
            messages.append("Query String argument does not work")
        return result, messages

    @staticmethod
    def ref2_1_b(url):
        """
        Resource URLs for which QSA-based profile negotiation is taking place SHOULD NOT
        themselves be QSA values of other resource URIs in any QSA-based system.

        :param url: Url
        """
        messages = []
        url = f"{url}?_profile=alt&_mediatype=application/json"
        response = get_request(url)
        if response.status == 200:
            result = True
        else:
            result = False
            messages.append("")
        return result, messages

    @staticmethod
    def ref2_1_c(url):
        """
        Token MUST be mappable to a URI within one particular client/server session

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
        return True, messages

    @staticmethod
    def ref2_1_d(url):
        """
        Additional aspects of content negotiation MAY be included in such URIs by the use of additional
        QSA or by any other techniques (for example HTTP headers)

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

        success_alternate = False
        for h in h_link[1].split(','):
            if 'rel="alternate"' in h:
                success_alternate = True

        if success_alternate:
            result = True
        else:
            result = False
            if not success_alternate:
                messages.append("Additional aspects of content negotiation not included in Headers")
        return result, messages

    @staticmethod
    def ref2_2_a(url):
        """
        To conform to the "QSA Functional Profile", the QSA key _profile MUST be used to indicate a profile token

        :param url: Url
        """
        messages = []
        url = f"{url}?_profile=alt"
        response = get_request(url)
        if response.status == 200:
            result = True
        else:
            result = False
            messages.append("Fail to indicate _profile key in URI")
        return result, messages

    @staticmethod
    def ref2_2_b(url):
        """
        The key _mediatype SHOULD be used to indicate a resource representation's Media Type

        :param url: Url
        """
        messages = []
        url = f"{url}?_mediatype=application/json"
        response = get_request(url)
        if response.status == 200:
            result = True
        else:
            result = False
            messages.append("Fail to indicate _mediatype key in URI")
        return result, messages

    @staticmethod
    def ref2_2_c(url):
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
    def ref2_3_a(url):
        """
        The QSA key/value pair _profile=alt SHOULD be supported by the server to allow a client to
        make a list profiles request

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

        success_alternate = False
        for h in h_link[1].split(','):
            if 'rel="alternate"' in h:
                success_alternate = True

        if success_alternate:
            result = True
        else:
            result = False
            if not success_alternate:
                messages.append("Error with: _profile=alt.")
        return result, messages

    @staticmethod
    def ref2_3_b(url):
        """
        List of all profiles that it supports representations of the resource for and optionally also
        supported Media Types for those representations.

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

        success_type_profile = False
        for h in h_link[1].split(','):
            if 'type=' in h:
                success_type_profile = True

        if success_type_profile:
            result = True
        else:
            result = False
            messages.append("Type not included")
        return result, messages

    @staticmethod
    def ref2_3_c(url):
        """
        Alternate profiles information in the HTTP header of the response, as per the HTTP Headers functional profile

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

        success_alternate_profile = False
        for h in h_link[1].split(','):
            if 'rel="alternate"' in h:
                success_alternate_profile = True

        if success_alternate_profile:
            result = True
        else:
            result = False
            messages.append("Alternate not provided in headers")
        return result, messages

    @staticmethod
    def ref2_3_d(url):
        """
        The server MAY also represent the information in the response body in place of the default profile
        representation of a resource.

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

        success_alternate_profile = False
        for h in h_link[1].split(','):
            if 'rel="alternate"' in h:
                success_alternate_profile = True

        if success_alternate_profile:
            result = True
        else:
            result = False
            messages.append("Alternate not provided in headers")
        return result, messages

    @staticmethod
    def ref2_3_e(url):
        """
        The server MAY allow clients to negotiate for particular Media Types of the response by
        using the same Media Type.

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
    def ref2_4_a(url):
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
                messages.append("'format=' not found in alternatives, 'profile=' found it. 'profile=' should be change to 'format='")
            else:
                messages.append("'format=' not found in alternatives.")
        return result, messages

    @staticmethod
    def ref2_4_b(url):
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
    tests_list = [method for method in dir(StringFunctionalTests) if method.startswith('__') is False]
    pass_tests = 0
    results = []
    for test in tests_list:
        r = getattr(StringFunctionalTests, test)(url)
        results.append(r)
        if r[0]:
            pass_tests += 1
        logging.info(f"Test: {test} - Result: {r}")
    logging.info("Total passed tests: {} - Total tests: {}".format(pass_tests, len(tests_list)))
    return tests_list, results, pass_tests, len(tests_list)
