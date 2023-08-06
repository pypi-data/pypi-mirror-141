"""Module: Base Strategy"""
import os

from service.parser_service.base_parser import SwaggerBaseParser
from service.parser_service.swagger_v2 import SwaggerV2Parser
from service.parser_service.swagger_v3 import SwaggerV3Parser
from service.generator_service.base_generator import BaseGenerator, VersionBaseGenerator
from service.utils.logger import get_logger

logger = get_logger()


class BaseStrategy:
    """Class: Base Strategy"""

    def __init__(self, file_content: dict, team_name: str, upload_path: str, operation: list,
                 whitelist: list, blacklist: list, script_path: str):
        logger = get_logger(env=os.environ)
        self.swagger_file_content = file_content
        self.operation = operation
        self.whitelist = whitelist
        self.blacklist = blacklist
        self.script_path = script_path
        if script_path:
            self.version_generator = VersionBaseGenerator(team_name=team_name, script_path=script_path, upload_path=upload_path)
        else:
            self.generator = BaseGenerator(team_name=team_name, upload_path=upload_path)

    def get_specific_version_parser(self) -> SwaggerBaseParser:
        """Method: get specific version parser"""

        swagger_version = self.swagger_file_content.get("swagger")
        openapi_version = self.swagger_file_content.get("openapi")
        version = swagger_version if swagger_version else openapi_version
        if not version:
            logger.error("No swagger version is specified")
            raise ValueError("No swagger version is specified")
        version = int(version[0])
        if version == 2:
            parser: SwaggerBaseParser = SwaggerV2Parser()
        elif version == 3:
            parser: SwaggerBaseParser = SwaggerV3Parser()
        else:
            logger.error("There is no support for %s version of swagger" % version)
            raise ValueError("There is no support for %s version of swagger" % version)
        return parser

    def process(self):
        """Method: process"""
        try:
            specific_version_parser = self.get_specific_version_parser()
            swagger_data = specific_version_parser.parse_swagger_file(self.swagger_file_content,
                                                                      operation=self.operation,
                                                                      whitelist=self.whitelist,
                                                                      blacklist=self.blacklist)
        except Exception as E:
            logger.error(E)
            raise Exception(E)
        if self.script_path:
            self.version_generator.base_generator(swagger_data)
        else:
            self.generator.generate_request_script(swagger_data)
            self.generator.generate_locust_script(swagger_data)
            return self.generator.get_storage_path()


