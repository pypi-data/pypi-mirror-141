"""Module: Base Parser"""
import json
import os
from abc import ABC
from service.utils.logger import get_logger

logger = get_logger()


class SwaggerBaseParser(ABC):
    """Class: Swagger Base Parser"""
    def __init__(self):
        logger = get_logger(env=os.environ)

    def parse_swagger_file(self, file_content: dict, operation: list, whitelist: list, blacklist: list) -> dict:
        """Method: parse swagger file"""
        data = {
            "host": self._parse_host_data(file_content),
            "info": self._parse_info(file_content),
            "security": self._parse_security_data(file_content),
            "paths": self._parse_paths_data(file_content, operation, whitelist, blacklist),
            "payload_schema": self._parse_payload(file_content)
        }
        return data

    @staticmethod
    def _parse_host_data(file_content: dict) -> str:
        raise NotImplementedError

    @staticmethod
    def _parse_security_data(file_content: dict) -> dict:
        raise NotImplementedError

    @staticmethod
    def _parse_paths_data(file_content: dict, operation: list, whitelist: list, blacklist: list) -> dict:
        raise NotImplementedError

    @staticmethod
    def _parse_params(params: dict) -> dict:
        raise NotImplementedError

    @staticmethod
    def _parse_consumers(consumes: list) -> list:
        raise NotImplementedError

    @staticmethod
    def _parse_payload(file_content: dict) -> dict:
        raise NotImplementedError

    @staticmethod
    def _parse_info(file_content: dict) -> dict:
        raise NotImplementedError

