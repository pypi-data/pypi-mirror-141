"""Module: SwaggerV3 parser"""

from service.parser_service.base_parser import SwaggerBaseParser


class SwaggerV3Parser(SwaggerBaseParser):
    """Class: SwaggerV3 parser"""

    @staticmethod
    def _parse_params(params: dict) -> dict:
        raise NotImplementedError()
