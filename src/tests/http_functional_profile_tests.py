from utils.utils import *
import logging
import re


class HttpFunctionalTests:

    @staticmethod
    def ref1_1_a(url):
        """
        Profile SHOULD return an HTTP Link header containing information about the default
        and any alternate representations of that resource including profiles they conform to.

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

        success_default = False
        success_alternate = False
        for h in h_link[1].split(','):
            if 'rel="alternate"' in h:
                success_alternate = True
            if 'rel="default"' in h:
                success_default = True

        if success_alternate and success_default:
            result = True
        else:
            result = False
            if not success_default:
                messages.append("Default profile not found.")
            if not success_alternate:
                messages.append("Alternate profiles not found.")
        return result, messages

    @staticmethod
    def ref1_1_b(url):
        """
        The default representation SHOULD be identified by rel="canonical", other representations by rel="alternate"

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

        success_default_canonical = False
        success_alternate = False
        for h in h_link[1].split(','):
            if 'rel="canonical"' in h:
                success_default_canonical = True
            if 'rel="alternate"' in h:
                success_alternate = True

        if success_alternate and success_default_canonical:
            result = True
        else:
            result = False
            if not success_default_canonical:
                messages.append("Default profile not found. Or rel=canonical not found.")
            if not success_alternate:
                messages.append("Alternate profiles not found.")
        return result, messages

    @staticmethod
    def ref1_2_a(url):
        """
        HTTP Response header containing a Link header with rel="profile" indicating the profile returned.

        :param url: Url
        """
        messages = []
        url = f"{url}"
        response = get_request(url)
        headers = response.getheaders()
        # Check if 'link' in headers
        h_link = None
        for h in headers:
            if 'link' in h:
                h_link = h

        if h_link is None:
            return False, messages.append('Link header not found')

        success_link_profile = False
        for h in h_link[1].split(','):
            if 'rel="profile"' in h:
                success_link_profile = True

        if success_link_profile:
            result = True
        else:
            result = False
            messages.append('ref="profile" not found in Link header.')
        return result, messages

    @staticmethod
    def ref1_2_b(url):
        """
        URIs referenced in Accept-Profile headers MUST be enclosed in angled brackets, '<' & '>'.

        :param url: Url
        """
        messages = []
        url = f"{url}"
        response = get_request(url)
        headers = response.getheaders()
        # Check if 'link' in headers
        h_link = None
        for h in headers:
            if 'link' in h:
                h_link = h

        if h_link is None:
            return False, messages.append('Link header not found')

        success_link_brackets_profile = False
        for h in h_link[1].split(','):
            if 'rel="profile"' in h:
                url_angled_brackets = re.findall('<http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+>', h)
                if url_angled_brackets:
                    success_link_brackets_profile = True

        if success_link_brackets_profile:
            result = True
        else:
            result = False
            messages.append("URI not enclosed in angled brackets")
        return result, messages

    @staticmethod
    def ref1_2_c(url):
        """
        Acceptable profile URIs MUST be delimited by a comma or be in separate Accept-Profile headers.

        :param url: Url
        """
        messages = []
        url = f"{url}"
        response = get_request(url)
        headers = response.getheaders()
        # Check if 'link' in headers
        h_link = None
        for h in headers:
            if 'link' in h:
                h_link = h

        if h_link is None:
            return False, messages.append('Link header not found')

        success_comma_link = False
        suppliers = [h for h in h_link[1].split(',')]
        if len(suppliers) >= 1:
            success_comma_link = True

        if success_comma_link:
            result = True
        else:
            result = False
            messages.append("URI not delimited by a comma.")
        return result, messages

    # @staticmethod
    # def ref1_2_d(url):
    #     """
    #     Acceptable profile URIs MUST be delimited by a comma or be in separate Accept-Profile headers.
    #
    #     :param url: Url
    #     """
    #     messages = []
    #     url = f"{url}"
    #     response = get_request(url)
    #     headers = response.getheaders()
    #     # Check if 'link' in headers
    #     h_link = None
    #     for h in headers:
    #         if 'link' in h:
    #             h_link = h
    #
    #     if h_link is None:
    #         return False, messages.append('Link header not found')
    #
    #     success_comma_profile = False
    #     for h in h_link[1].split(','):
    #         if 'rel="profile"' in h:
    #             comma_split = h.split(';')
    #             for c in comma_split:
    #                 if 'q=' in c:
    #                     success_comma_profile = True
    #
    #     if success_comma_profile:
    #         result = True
    #     else:
    #         result = False
    #         messages.append("Q-value not found in URIs.")
    #     return result, messages


def run_tests(url):
    tests_list = [method for method in dir(HttpFunctionalTests) if method.startswith('__') is False]
    pass_tests = 0
    results = []
    for test in tests_list:
        r = getattr(HttpFunctionalTests, test)(url)
        results.append(r)
        if r[0]:
            pass_tests += 1
        logging.info(f"Test: {test} - Result: {r}")
    logging.info("Total passed tests: {} - Total tests: {}".format(pass_tests, len(tests_list)))
    return tests_list, results, pass_tests, len(tests_list)
