import json
import os
from service.utils.logger import get_logger

logger = get_logger()


class HeaderManager:
    def __init__(self):
        logger = get_logger(os.environ)

    @staticmethod
    def parser_header_cookies_swagger(request_payload, consumes):
        header = {}
        try:
            if bool(request_payload) > 0:
                for key, value in request_payload.items():
                    if value["in"] is not None:
                        if value["in"] == "header":
                            if key == "api_key":
                                continue
                            if "default" in value:
                                header[value["name"]] = value["default"]
                            else:
                                header[value["name"]] = None
        except Exception as E:
            logger.debug(E)
            raise Exception(E)
        if bool(consumes):
            header["Content-Type"] = consumes[0]
        else:
            header["Content-Type"] = 'application/json'
        return header

    def custom_parser_header_swagger(self, request_payload):
        header = {}
        return header

