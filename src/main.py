import argparse
import logging
from prettytable import PrettyTable
from utils.utils import build_response_table
from tests.http_functional_profile_tests import run_tests as run_tests_http
from tests.query_string_functional_profile import run_tests as run_tests_qs_functional
from tests.query_string_alternate_functional_profile import run_tests as run_tests_qs_alternate_functional

available_tests = ['http_functional', 'qs_string_functional', 'qs_alternate_functional']


def config_logging(file_opt=None, log_dir=None):
    if file_opt and not log_dir:
        log_dir = '/tmp'
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(filename)s - %(message)s',
        filename=f"{log_dir}/logs.log" if file_opt else None)
    return


def main(tests: list, url: str):
    status_tests = PrettyTable()
    status_tests.field_names = ["Test Type", "Test Name", "Status", "Messages"]

    total_table = PrettyTable()
    total_table.field_names = ["Test Type", "Total Tests", "Passed Tests", "Failed Tests"]

    for test in tests:
        logging.info(f'Running tests: {test}')

        if test not in available_tests:
            raise Exception(f"Test {test} not found. Available tests: {available_tests}")
        if test == 'http_functional':
            test_list_http, results_http, pass_tests_http, len_tests_http = run_tests_http(url)

            # Generate output table
            content_table = build_response_table(test_list_http, results_http)
            for el in content_table:
                status_tests.add_row([test] + el)
            # Add output results
            total_table.add_row([test, len_tests_http, pass_tests_http, len_tests_http - pass_tests_http])

        elif test == 'qs_alternate_functional':
            test_list_qs_alternate_functional, \
            results_qs_alternate_functional, \
            pass_tests_qs_alternate_functional, \
            len_tests_qs_alternate_functional = run_tests_qs_alternate_functional(url)

            # Generate output table
            content_table = build_response_table(test_list_qs_alternate_functional, results_qs_alternate_functional)
            for el in content_table:
                status_tests.add_row([test] + el)
            # Add output results
            total_table.add_row([test,
                                 len_tests_qs_alternate_functional,
                                 pass_tests_qs_alternate_functional,
                                 len_tests_qs_alternate_functional - pass_tests_qs_alternate_functional])

        elif test == 'qs_string_functional':
            test_list_qs_string_functional, \
            results_qs_string_functional, \
            pass_tests_qs_string_functional, \
            len_tests_qs_string_functional = run_tests_qs_functional(url)

            # Generate output table
            content_table = build_response_table(test_list_qs_string_functional, results_qs_string_functional)
            for el in content_table:
                status_tests.add_row([test] + el)
            # Add output results
            total_table.add_row([test,
                                 len_tests_qs_string_functional,
                                 pass_tests_qs_string_functional,
                                 len_tests_qs_string_functional - pass_tests_qs_string_functional])
        logging.info(f"{'-' * 70}")

    logging.info(f"Tests Status: \n{status_tests}")
    logging.info(f"Result Values: \n{total_table}")
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Connegp Test API')
    parser.add_argument('--tests', nargs='+', default=['http_functional',
                                                       'qs_string_functional',
                                                       'qs_alternate_functional'],
                        help='Lists of tests you want to run - Options: [http_functional, qs_alternate_functional, '
                             'qs_string_functional]')
    parser.add_argument('--log_file', type=bool, help='Save logs to logs.log file')
    parser.add_argument('--url', type=str, required=True,
                        help='URI to perform tests against.')
    args = parser.parse_args()

    config_logging(file_opt=args.log_file)
    main(args.tests, args.url)
