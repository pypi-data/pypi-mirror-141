import json
import os
from service.utils.logger import get_logger

logger = get_logger()


class PayloadGenerator:
    def __init__(self):
        logger = get_logger(os.environ)

    def _parser_params_or_payload_swagger(self, request_payload, payload_schema):
        params = {}
        payload = {}
        path = {}
        if len(request_payload) > 0:
            try:
                for key, value in request_payload.items():
                    if value["in"] is not None:
                        if value["in"] == "query":
                            params[value["name"]] = None
                        if value["in"] == "body":
                            payload = self._parse_data_payload(value, payload_schema)
                        if value["in"] == "formData":
                                payload[value["name"]] = None
                        if value["in"] == "path":
                            path[value["name"]] = None
            except Exception as E:
                logger.debug(E)
                raise Exception(E)
        return params, payload, path

    def _parse_data_payload(self, payload, schema):
        parse_payload = {}
        if 'schema' in payload:
            if 'type' in payload['schema']:
                if payload['schema']['type'] == 'object':
                    if "$ref" in payload['schema']:
                        parse_payload = self._get_reference_schema_data(payload['schema']['$ref'], schema)
                    else:
                        return parse_payload
                elif payload['schema']['type'] == 'array':
                    if "$ref" in payload['schema']['items']:
                        parse_payload = [self._get_reference_schema_data(payload['schema']['items']['$ref'], schema)]
                    else:
                        if "type" in payload['schema']['items'] and \
                                payload['schema']['items']["type"] == "string":
                            return ['string']
                        else:
                            return [{}]
                elif payload['schema']['type'] == 'string':
                    parse_payload[payload["name"]] = 'string'
                else:
                    return parse_payload
            elif "$ref" in payload['schema']:
                parse_payload = self._get_reference_schema_data(payload['schema']['$ref'], schema)
        return parse_payload

    @staticmethod
    def _get_reference_schema_data(data, schema):
        parse_payload = {}
        try:
            if "properties" in schema[str(data).split("/")[-1]]:
                for key, value in schema[str(data).split("/")[-1]]["properties"].items():
                    if key != "title":
                        if "example" in value:
                            parse_payload[key] = value.get("example")
                        else:
                            parse_payload[key] = None
        except Exception as E:
            logger.debug(E)
            raise Exception(E)
        return parse_payload
