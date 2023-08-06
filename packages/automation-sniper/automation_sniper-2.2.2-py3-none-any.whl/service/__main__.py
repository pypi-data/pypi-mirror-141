import argparse
import os
from service.parser import ParserHandler
from service.utils.logger import get_logger
from service.__version__ import __version__

logger = get_logger()

API_OPERATIONS = ("get", "post", "put", "patch", "delete", "head", "options", "trace")


def main():
    """Launching function"""
    parser = argparse.ArgumentParser(prog="automation-sniper",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='This tool help to convert API Specs into automation Framework',
                                     epilog="And that's how you'd like to use this tool. To know about more please "
                                            "read the documentation https://automation-sniper.readthedocs.io/")
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s {}'.format(__version__)
    )
    parser.add_argument(
            "-f",
            "--framework_name",
            help="Provide the name of the framework",
            required=True,
            type=str,
    )
    parser.add_argument(
            "-p",
            "--path",
            help="Provide the path to swagger file/postman file or provide swagger api-docs url/postman collection url",
            required=True,
            type=str,
    )
    parser.add_argument(
            "-r",
            "--results-path",
            help="path to store generated automation framework default: result",
            required=False,
            default='',
            type=str,
    )
    parser.add_argument(
        "-sp",
        "--script-path",
        help="provide script folder path as zip format",
        required=False,
        default='',
        type=str
    )
    parser.add_argument(
        "-o",
        "--operations",
        help="operations to use in api testing",
        required=False,
        nargs="+",
        choices=API_OPERATIONS,
        default=[]
    )
    parser.add_argument(
        "-v", "--verbose", help="verbose", required=False, action="store_true", default=False,
    )
    parser.add_argument(
        "-ba", "--blacklist-api", help="tags to use in api testing", required=False, nargs="+", type=str, default=[]
    )
    parser.add_argument(
        "-wa", "--whitelist-api", help="tags to use in api testing", required=False, nargs="+", type=str, default=[]
    )
    args = parser.parse_args()
    logger.debug("Command line args: {}".format(args))
    if args.verbose:
        os.environ["LOG_LEVEL"] = "DEBUG"
    else:
        os.environ["LOG_LEVEL"] = "INFO"
    payload = {
        'team_name': args.framework_name,
        'swagger_path': args.path,
        'results_path': args.results_path,
        'operations': args.operations,
        'blacklist_api': args.blacklist_api,
        'whitelist_api': args.whitelist_api,
        'script_path': args.script_path

    }
    ParserHandler().parser_cli_handler(**payload)


if __name__ == '__main__':
    main()

