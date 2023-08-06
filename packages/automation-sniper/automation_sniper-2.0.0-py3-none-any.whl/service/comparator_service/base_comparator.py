
import copy
from service.generator_service.payload_generator import PayloadGenerator
from service.generator_service.header_generator import HeaderManager


class BaseComparator:
    def __init__(self):
        self.payload_generator = PayloadGenerator()
        self.header_generator = HeaderManager()

    def base_compare(self, v1_config, v2_config):
        swagger_data_v1 = v1_config
        swagger_data_v2 = self.parse_swagger_data(v2_config)
        new_controller, new_api_in_controller, deprecated = self._fetch_new_and_deprecated_controller(swagger_data_v1,
                                                                                                swagger_data_v2)
        return new_controller, new_api_in_controller, deprecated

    def _fetch_new_and_deprecated_controller(self, v1_path, v2_path):
        v1_schema_path = v1_path["schema"]
        v2_schema_path = v2_path["schema"]
        new_controller = {}
        new_api_in_controller = {}
        deprecate_data = copy.deepcopy(v1_path["schema"])
        for controller, method in v2_schema_path.items():
            api_path_list = []
            if controller not in v1_schema_path:
                new_controller[controller] = v2_schema_path[controller]
            else:
                for _payload in method:
                    if _payload not in v1_schema_path[controller]:
                        api_path_list.append(_payload)
                    else:
                        deprecate_data[controller].remove(_payload)
                if bool(api_path_list):
                    new_api_in_controller[controller] = api_path_list
                if not bool(deprecate_data[controller]):
                    deprecate_data.pop(controller)
        deprecate_data = self.check_if_new_api_belongs_to_deprepacred(new_api_in_controller, deprecate_data)
        return new_controller, new_api_in_controller, deprecate_data

    def check_if_new_api_belongs_to_deprepacred(self, newapi, depapi):
        depapi_copy = copy.deepcopy(depapi)
        for _key, _value in depapi.items():
            if _key in newapi:
                for _data in _value:
                    if _data["path"] in [path["path"] for path in newapi[_key]]:
                        depapi_copy[_key].remove(_data)
                if not bool(depapi_copy[_key]):
                    depapi_copy.pop(_key)
        return depapi_copy

    def parse_swagger_data(self, config_data):
        json_to_update = {}
        schema_json = {}
        json_to_update["schema"] = schema_json
        for key, value in config_data["paths"].items():
            api_list = []
            json_to_update["schema"] = schema_json
            schema_json[key] = api_list
            for _request_data in value:
                params, payload, path = self.payload_generator._parser_params_or_payload_swagger(
                    _request_data["params"],
                    config_data.get("payload_schema")
                )
                headers = self.header_generator.parser_header_cookies_swagger(_request_data["params"], _request_data["consumers"])
                api_list.append(
                    {
                        "method": _request_data["method"],
                        "path": _request_data["path"],
                        "deprecated": _request_data.get("deprecated", False),
                        "request_payload": {
                            "params": params,
                            "payload": payload,
                            "path": path,
                            "headers": headers
                        }
                    }
                )
        return json_to_update


