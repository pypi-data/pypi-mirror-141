"""Module: SwaggerV2 parser"""
import copy
import os
from copy import deepcopy

from service.parser_service.base_parser import SwaggerBaseParser
from service.utils.logger import get_logger

logger = get_logger()

http_method = ["get", "post", "put", "patch", "delete", "head", "options", "trace"]

class SwaggerV2Parser(SwaggerBaseParser):
    """Class: SwaggerV2 parser"""
    def __init__(self):
        super().__init__()
        logger = get_logger(env=os.environ)

    @staticmethod
    def _parse_host_data(file_content: dict) -> str:
        """Method: parse host data"""
        return file_content.get("host", "")

    @staticmethod
    def _parse_security_data(file_content: dict) -> dict:
        """Method: parse security data"""

        security = {}
        security_definitions = file_content.get("securityDefinitions", {})
        for security_config in security_definitions.values():
            security_type = security_config.get("type", "")
            security[security_type] = security_config
        return security

    def _parse_paths_data(self, file_content: dict, operation: list, whitelist: list, blacklist: list) -> dict:
        """Method: parse paths data"""

        api_details = {}
        paths = file_content.get("paths")
        if paths is None:
            logger.error("Empty path found in swagger file {}".format(paths))
            return {}
        path_copy = copy.deepcopy(paths)
        for path, path_data in paths.items():
            if bool(blacklist):
                if path in blacklist:
                    path_copy.pop(path)
            elif bool(whitelist):
                if path not in whitelist:
                    path_copy.pop(path)
        final_path_copy = copy.deepcopy(path_copy)
        for path, path_data in path_copy.items():
            if bool(path_data):
                for path_method, method_data in path_data.items():
                    if bool(operation):
                        if path_method not in operation:
                            final_path_copy[path].pop(path_method)
        for path, path_data in final_path_copy.items():
            if bool(path_data):
                for path_method, method_data in path_data.items():
                    if path_method in http_method:
                        if "deprecated" not in method_data:
                            # logger.warning("Swagger spec doesnt have deprecated tag. Please check and fix it")
                            method_data["deprecated"] = False
                        if "tags" in method_data and method_data["tags"][0] is not None:
                            if method_data["tags"][0] in api_details:
                                api_details[method_data["tags"][0]].append({
                                    "method": path_method,
                                    "path": path,
                                    "consumers": self._parse_consumers(method_data.get("consumes", [])),
                                    "params": self._parse_params(method_data.get("parameters", [])),
                                    "responses": method_data.get("responses", {}),
                                    "deprecated": method_data.get("deprecated", None)
                                })
                            else:
                                api_details[method_data["tags"][0]] = [{
                                    "method": path_method,
                                    "path": path,
                                    "consumers": self._parse_consumers(method_data.get("consumes", [])),
                                    "params": self._parse_params(method_data.get("parameters", [])),
                                    "responses": method_data.get("responses", {}),
                                    "deprecated": method_data.get("deprecated", None)
                                }]
                        else:
                            logger.warning("Empty tag received from payload i.e. {}".format(method_data))
            else:
                logger.warning("Request specs body is empty from payload i.e. {}".format(path_data))
        return api_details

    @staticmethod
    def _parse_params(params: dict) -> dict:
        param_data = {}
        for param in params:
            param_name = param.get("name") if "name" in param else None
            if not param_name or not param.get("in"):
                if param.get("required"):
                    logger.error("Not full info about required param")
                    return {}
                continue
            param_data[param_name] = deepcopy(param)
        return param_data

    @staticmethod
    def _parse_consumers(consumes: list) -> list:
        return consumes

    @staticmethod
    def _parse_payload(file_content: dict) -> dict:
        return file_content.get("definitions", {})

    @staticmethod
    def _parse_info(file_content: dict) -> dict:
        return file_content.get("info", {})
