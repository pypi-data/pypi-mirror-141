"""Module: This is main module that activates library"""

import json
import os
import yaml
import requests
import validators
from service.strategy.base_strategy import BaseStrategy
from service.utils.logger import get_logger

logger = get_logger()


class ParserHandler:
    def __init__(self):
        logger = get_logger(env=os.environ)

    def parser_service(self, **kwargs):
        logger = get_logger(env=os.environ)
        storage_path = None
        logger.debug("Request data {}".format(kwargs))
        team_name = kwargs.get("team_name")
        upload_path = kwargs.get("results_path")
        operation = kwargs.get("operations")
        blacklist_api = kwargs.get("blacklist_api")
        whitelist_api = kwargs.get("whitelist_api")
        script_path = kwargs.get("script_path")
        logger.info("Got request for team_name {} and upload_path {}".format(team_name, upload_path))
        if "swagger_url" in kwargs:
            swagger_url = kwargs["swagger_url"]
            try:
                swagger_response = requests.get(swagger_url)
            except requests.exceptions.SSLError:
                swagger_response = requests.get(swagger_url, verify=False)
            except Exception as E:
                logger.error("failure to get swagger data from {} with error {}".format(swagger_url, E))
                return None
            if swagger_response.status_code != 200:
                logger.error("Not able to get swagger json from the link {} as url return {}".format(swagger_url, swagger_response.status_code))
                return None
            else:
                swagger_data = swagger_response.json()
                logger.debug("swagger data is {}".format(swagger_data))
        else:
            swagger_file_path = kwargs["swagger_path"]
            ext = os.path.splitext(swagger_file_path)[-1]
            if ext == ".json":
                with open(swagger_file_path) as file:
                    swagger_data = json.load(file)
                    logger.debug("swagger data is {}".format(swagger_data))
            elif ext in (".yaml", ".yml"):
                with open(swagger_file_path) as file:
                    swagger_data = yaml.safe_load(file)
            else:
                logger.error("Incorrect file has been passed. Accepted file type is YML or JSON format")
                return None
        base_obj = BaseStrategy(swagger_data, team_name, upload_path, operation, whitelist_api, blacklist_api, script_path)
        storage_path = base_obj.process()
        return storage_path

    def parser_cli_handler(self, **kwargs):
        try:
            payload = ValidatorAndSerializer(**kwargs).serializer_call()
        except Exception as E:
            logger.error("Failure from serializer {}".format(E))
            return
        response = self.parser_service(**payload)
        if response is not None:
            logger.info("Framework is generated in this path : {}".format(response))

    def parser_api_handler(self):
        pass


class ValidatorAndSerializer:
    """

    """
    def __init__(self, **kwargs):
        self.payload = kwargs

    def serializer_call(self):
        self._result_path_serializer()
        self._swagger_path_serializer()
        return self.payload

    def _swagger_path_serializer(self):
        if self._url_validator():
            self.payload["swagger_url"] = self.payload["swagger_path"]
            self.payload.pop("swagger_path")

    def _result_path_serializer(self):
        if not bool(self.payload.get("results_path")):
            self.payload["results_path"] = os.path.join(os.getcwd(), "result")

    def _url_validator(self):
        return validators.url(self.payload["swagger_path"])
