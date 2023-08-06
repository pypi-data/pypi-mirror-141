"""Module: Base Generator"""
import copy
import json
import logging
import re
import os
import shutil
import sys
import datetime
import zipfile
from service.template_service import request_template, helpers_templates, testdata_templates, locustfile_templates, \
    flow_scenario_templates, header_manager_templates
from service.template_service import request_helper_templates
from service.generator_service.data_generator import DataGenerator
from service.generator_service.payload_generator import PayloadGenerator
from service.generator_service.auth_generator import SecurityManager
from service.generator_service.header_generator import HeaderManager
from service.comparator_service.base_comparator import BaseComparator
from service.utils.logger import get_logger

logger = get_logger()

folder_dict = {
    "data": {"name": "data", "path": "data"},
    "scripts": {"name": "scripts", "path": "scripts"},
    "locust_scripts": {"name": "locust_scripts", "path": "scripts/locust_scripts"},
    "nfr_requests": {"name": "nfr_requests", "path": "scripts/nfr_requests"},
    "api_requests": {"name": "api_requests", "path": "scripts/nfr_requests/api_requests"},
    "config": {"name": "config", "path": "scripts/nfr_requests/config"},
    "flow_scenarios": {"name": "flow_scenarios", "path": "scripts/nfr_requests/flow_scenarios"},
    "parsers": {"name": "parsers", "path": "scripts/nfr_requests/parsers"},
    "request_helpers": {"name": "request_helpers", "path": "scripts/nfr_requests/parsers/request_helpers"},
    "response_helpers": {"name": "response_helpers", "path": "scripts/nfr_requests/parsers/response_helpers"}
}
folder_dict_deepcopy = copy.deepcopy(folder_dict)
special_char_remover_regex = '[^A-Za-z0-9]+'


class BaseGenerator:
    """Class: Base Generator"""

    def __init__(self, team_name, upload_path):
        """

        :param team_name:
        """
        self.swagger_meta_data = {}
        logger = get_logger(os.environ)
        self.team_name = team_name
        self.generator_helper = GeneratorHelper(self.team_name)
        # fixme-This path should be storage path
        self.results_path = os.path.join(upload_path, self.team_name)
        self.swagger_meta_data_path = os.path.join(self.results_path, "MetaConfig.json")
        try:
            shutil.rmtree(self.results_path, ignore_errors=True)
        except Exception as E:
            logger.error("Failed to delete old folder : {}".format(E))
        try:
            os.makedirs(self.results_path)
        except Exception as E:
            logger.debug("Failure : {}".format(E))
            raise Exception("Failed to create folder due to permission issue : {}".format(E))
        self.generate_config_file(self.results_path)
        self.generator_helper.generate_audit_log_file(self.results_path, "Got request for team {}".format(self.team_name))
        self.generate_init_file(self.results_path)
        for file_name, file_path_dict in folder_dict.items():
            folder_dict[file_name]["path"] = os.path.join(str(self.results_path), str(file_path_dict.get("path")))
            os.mkdir(folder_dict[file_name]["path"])
            self.generator_helper.generate_audit_log_file(self.results_path, "Folder is created {}".format(folder_dict[file_name]["path"]))
            self.generate_init_file(folder_dict[file_name]["path"])

        self.data_gen_object = DataGenerator(folder_dict["data"]["path"])
        self.payload_generator = PayloadGenerator()
        self.header_generator = HeaderManager()
        self.auth_generator = SecurityManager()

    def generate_request_script(self, swagger_data):
        self.generator_helper.generate_audit_log_file(self.results_path, "Swagger data is {}".format(swagger_data))
        self.generate_config_cases()
        self.generate_common_config_cases(swagger_data)
        self.generate_test_data_provider()
        auth_header = self.auth_generator.generate_security_cases(swagger_data.get("security", {}))
        self.generate_header_manager(auth_header)
        self.swagger_meta_data["path_definitions"] = {}
        self.swagger_meta_data["schema"] = {}
        self.swagger_meta_data["version"] = 0
        for controller, method_list in swagger_data.get("paths").items():
            request_group = re.sub(special_char_remover_regex, '_', str(controller))
            request_helper_path_object, request_helper_claas_context, request_helper_file_name = \
                self.generator_helper.request_helper_class_generator(controller, request_group)
            request_file_path_object, request_claas_context, request_file_name = \
                self.generator_helper.request_class_generator(controller, request_group, request_helper_claas_context)
            flow_scenario_path_object = \
                self.generator_helper.flow_scenario_class_generator(controller, request_group, request_claas_context)
            for _request_data in method_list:
                try:
                    path_name = _request_data["path"]
                    path_method_name = _request_data["method"]
                    deprecated = _request_data["deprecated"]
                except Exception as E:
                    logger.debug("Failure : {}".format(E))
                    raise ValueError(E)
                method_name = self.generator_helper.method_name_fetch(request_group,
                                                                      path_name,
                                                                      path_method_name)
                self.generator_helper.flow_scenario_method_generator(method_name, flow_scenario_path_object, deprecated)
                try:
                    params, payload, path = self.payload_generator._parser_params_or_payload_swagger(
                        _request_data["params"],
                        swagger_data.get("payload_schema"))
                    headers = self.header_generator.parser_header_cookies_swagger(_request_data["params"],
                                                                                  _request_data["consumers"])
                except Exception as E:
                    logger.debug("Failure : {}".format(E))
                    raise Exception(E)
                self.generator_helper.request_payload_generator(method_name,
                                                                path_method_name,
                                                                path_name,
                                                                payload,
                                                                params,
                                                                path,
                                                                headers,
                                                                deprecated,
                                                                request_helper_path_object,
                                                                request_file_path_object)
                try:
                    self.generator_helper.meta_config_schema_generator(self.swagger_meta_data, controller, {
                        "method": _request_data["method"],
                        "path": _request_data["path"],
                        "deprecated": _request_data.get("deprecated", False),
                        "request_payload": {
                            "params": params,
                            "payload": payload,
                            "path": path,
                            "headers": headers
                        }
                    })
                    path_def = self.generator_helper.meta_config_path_definitions_generator(path_name, method_name, request_file_name, request_helper_file_name, deprecated)
                    self.generator_helper.update_meta_config_path_definitions(self.swagger_meta_data, _request_data["method"], path_def)
                except Exception as E:
                    logger.debug("Failure : {}".format(E))
                    raise Exception(E)
            self.generator_helper.tag_generator(request_file_path_object, request_helper_path_object)
            self.generator_helper.generate_config_file(self.swagger_meta_data_path, self.swagger_meta_data)

    def generate_locust_script(self, swagger_data):
        path = folder_dict["locust_scripts"]["path"] + "/" + "{}_locust_file.py".format(self.team_name)
        try:
            file_path = self.generator_helper.file_read_write(path, append=True)
        except Exception as E:
            logger.debug("Failure : {}".format(E))
            raise FileNotFoundError(E)
        try:
            file_path.write(locustfile_templates.MAIN_LOCUST_HEADER.render())
        except Exception as E:
            logger.debug(E)
            raise Exception("Unable to write data into file")
        if "paths" not in swagger_data or swagger_data.get("paths") is None:
            raise ValueError("Path data is empty")
        task_set_list = []
        for key, value in swagger_data.get("paths").items():
            file_name = re.sub(special_char_remover_regex, '_', str(key)) + "_flow"
            flow_class_name = ''.join(
                x for x in re.sub(special_char_remover_regex, ' ', str(key)).title() if not x.isspace()) + "Flow"
            claas_context = self.generator_helper.context_serializers(flow_file_name=file_name,
                                                                      flow_class_name=flow_class_name,
                                                                      )
            try:
                file_path.write(
                    locustfile_templates.MAIN_LOCUST_HEADER_FUNCTION_IMPORT.render(context=claas_context)
                )
            except Exception as E:
                logger.debug(E)
                raise Exception("Unable to write data into file")
        for key, value in swagger_data.get("paths").items():
            file_name = re.sub(special_char_remover_regex, '_', str(key))
            flow_class_name = ''.join(
                x for x in re.sub(special_char_remover_regex, ' ', str(key)).title() if not x.isspace()) + "Flow"
            method_name_list = []
            for _request_data in value:
                suffix_function_name = str(
                    file_name + re.sub(special_char_remover_regex, '_', str(_request_data["path"], ))).lower()
                method_name = _request_data["method"] + "_" + suffix_function_name + "_flow"
                method_name_list.append(method_name)
            method_context = self.generator_helper.context_serializers(
                flow_file_name=re.sub(special_char_remover_regex, '_', str(key)),
                flow_class_name=flow_class_name,
                method_list=method_name_list
            )
            try:
                file_path.write(
                    locustfile_templates.TASK_FLOW_METHOD.render(context=method_context)
                )
            except Exception as E:
                logger.debug(E)
                raise Exception("Unable to write data into file")
            task_set_list.append(file_name)
        taskset_context = self.generator_helper.context_serializers(task_flow_list=task_set_list)
        try:
            file_path.write(
                locustfile_templates.BASE_TASKSET_CLASS.render(context=taskset_context)
            )
        except Exception as E:
            logger.debug(E)
            raise Exception("Unable to write data into file")
        try:
            file_path.close()
            self.generator_helper.generate_audit_log_file(self.results_path, "locust file has created in the path {}".format(self.results_path))
        except Exception as E:
            logger.error(E)

    def get_storage_path(self):
        return self.results_path

    def generate_config_cases(self):
        path_object = self.generator_helper.file_read_write(folder_dict["config"]["path"] + "/Utils.py", write=True)
        try:
            context = self.generator_helper.context_serializers()
            path_object.write(
                helpers_templates.HELPER_CLASS.render(context=context)
            )
        except Exception as E:
            logging.debug(E)
            raise Exception(E)
        finally:
            path_object.close()

    def generate_test_data_provider(self):
        path_object = self.generator_helper.file_read_write(folder_dict["config"]["path"] + "/TestDataProvider.py",
                                                            write=True)
        try:
            context = self.generator_helper.context_serializers()
            path_object.write(
                testdata_templates.DATA_PROVIDER_BASE_FILE.render(context=context)
            )
        except Exception as E:
            logging.debug(E)
            raise Exception(E)
        finally:
            path_object.close()

    def generate_header_manager(self, auth_header):
        path_object = self.generator_helper.file_read_write(folder_dict["config"]["path"] + "/HeaderManager.py",
                                                            write=True)
        try:
            context = self.generator_helper.context_serializers(auth_header=auth_header)
            path_object.write(
                header_manager_templates.HEADER_TEMPLATE.render(context=context)
            )
        except Exception as E:
            logging.debug(E)
            raise Exception(E)
        finally:
            path_object.close()

    def generate_init_file(self, path):
        path_object = self.generator_helper.file_read_write(path + "/__init__.py", write=True)
        try:
            path_object.write("__author__ = 'Automation Sniper Team'\n")
        except Exception as E:
            logging.debug(E)
            raise Exception(E)
        finally:
            path_object.close()

    def generate_config_file(self, path):
        path_object = self.generator_helper.file_read_write(path + "/CONFIG.md", write=True)
        try:
            path_object.write("python_version=3.6.10\n")
        except Exception as E:
            logging.debug(E)
            raise Exception(E)
        finally:
            path_object.close()

    def generate_common_config_cases(self, swagger_data):
        self.host = swagger_data.get("host")
        path_object = self.generator_helper.file_read_write(folder_dict["config"]["path"] + "/CommonConfig.py",
                                                            append=True)
        try:
            path_object.write("BASE_URL = 'http://{}'\n".format(self.host))
            path_object.write("BASE_REQUEST_DATA_DIR = '{}'\n".format("../data"))
        except Exception as E:
            logging.debug(E)
            raise Exception(E)
        finally:
            path_object.close()


class GeneratorHelper:
    def __init__(self, team_name):
        self.team_name = team_name

    def request_helper_class_generator(self, controller_name, request_group, render=True):
        request_helper_file_name = "{}_helper.py".format(request_group.lower())
        request_helper_path = folder_dict["request_helpers"]["path"] + "/" + request_helper_file_name
        request_helper_claas_context = self.context_serializers(class_name=controller_name, class_suffix="Helper")
        if render:
            request_helper_path_object = self.file_read_write(request_helper_path, append=True)
            try:
                request_helper_path_object.write(
                    request_helper_templates.REQUEST_HELPER_CLASS_TEMPLATE.render(context=request_helper_claas_context)
                )
            except Exception as E:
                logging.debug(E)
                raise Exception("Not able to write data {}".format(E))
            return request_helper_path_object, request_helper_claas_context, request_helper_file_name
        else:
            return request_helper_path, request_helper_claas_context, request_helper_file_name

    def request_class_generator(self, controller_name, request_group, request_helper_claas_context, render=True):
        request_file_name = "{}.py".format(request_group.lower())
        request_file_path = folder_dict["api_requests"]["path"] + "/" + request_file_name
        request_claas_context = self.context_serializers(class_name=controller_name,
                                                         file_name=request_group.lower(),
                                                         file_suffix="_helper",
                                                         import_class_name=request_helper_claas_context.get(
                                                             "class_name")
                                                         )
        if render:
            request_file_path_object = self.file_read_write(request_file_path, append=True)
            try:
                request_file_path_object.write(
                    request_template.REQUEST_CLASS_TEMPLATE.render(context=request_claas_context)
                )
            except Exception as E:
                logging.debug(E)
                raise Exception("Not able to write data {}".format(E))
            return request_file_path_object, request_claas_context, request_file_name
        else:
            return request_file_path, request_claas_context, request_file_name

    def flow_scenario_class_generator(self, controller_name, request_group, request_claas_context):
        flow_scenario_file_name = "{}_flow.py".format(request_group.lower())
        flow_scenario_path = folder_dict["flow_scenarios"]["path"] + "/" + flow_scenario_file_name
        flow_scenario_path_object = self.file_read_write(flow_scenario_path, append=True)
        flow_scenario_claas_context = self.context_serializers(class_name=controller_name,
                                                               file_name=request_group.lower(),
                                                               import_class_name=request_claas_context.get(
                                                                   "class_name"),
                                                               class_suffix="Flow"
                                                               )
        try:
            flow_scenario_path_object.write(
                flow_scenario_templates.FLOW_SCENARIO_CLASS_TEMPLATE.render(context=flow_scenario_claas_context)
            )
        except Exception as E:
            logging.debug(E)
            raise Exception("Not able to write data {}".format(E))
        return flow_scenario_path_object

    def method_name_fetch(self, request_group, path_name, path_method_name):
        try:
            suffix_function_name = str(
                request_group + re.sub(special_char_remover_regex, '_', str(path_name, ))).lower()
            method_name = path_method_name + "_" + suffix_function_name
        except Exception as E:
            logging.debug(E)
            raise Exception(E)
        return method_name

    def flow_scenario_method_generator(self, method_name, flow_scenario_path_object, deprecated):
        flow_scenario_method_context = self.context_serializers(function_name=method_name, deprecated=deprecated)
        try:
            flow_scenario_path_object.write(
                flow_scenario_templates.FLOW_SCENARIO_METHOD_TEMPLATE.render(context=flow_scenario_method_context)
            )
        except Exception as E:
            logging.debug(E)
            raise Exception("Not able to write data {}".format(E))

    def request_payload_generator(self, method_name, path_method_name, path_name, payload, params, path, headers,
                                  deprecated, request_helper_path_object=None,
                                  request_file_path_object=None, render=True):
        request_helper_method_context = self.context_serializers(function_name=method_name+"_helper",
                                                                 payload=payload if len(payload) > 0 else params,
                                                                 deprecated=deprecated)
        request_render_object = None
        request_helper_render_object = None
        if bool(params):
            request_method_context = self.context_serializers(function_name=method_name,
                                                              headers=headers,
                                                              method=path_method_name,
                                                              params=params,
                                                              path=path,
                                                              request_path=path_name,
                                                              request_function_name=request_helper_method_context.get(
                                                                  "function_name"),
                                                              deprecated=deprecated
                                                              )
            if render:
                try:
                    request_helper_path_object.write(
                        request_helper_templates.REQUEST_HELPER_METHOD_TEMPLATE.render(
                            context=request_helper_method_context)
                    )
                    request_file_path_object.write(
                        request_template.REQUEST_METHOD_TEMPLATE.render(context=request_method_context)
                    )
                except Exception as E:
                    logger.debug(E)
                    raise Exception("Unable to write data into file")
            else:
                request_helper_render_object = request_helper_templates.REQUEST_HELPER_METHOD_TEMPLATE.render(
                    context=request_helper_method_context)
                request_render_object = request_template.REQUEST_METHOD_TEMPLATE.render(context=request_method_context)
        elif bool(payload):
            request_method_context = self.context_serializers(function_name=method_name,
                                                              headers=headers,
                                                              method=path_method_name,
                                                              payload=payload,
                                                              path=path,
                                                              request_path=path_name,
                                                              request_function_name=request_helper_method_context.get(
                                                                  "function_name"),
                                                              deprecated=deprecated
                                                              )
            if render:
                try:
                    request_helper_path_object.write(
                        request_helper_templates.REQUEST_HELPER_METHOD_TEMPLATE.render(
                            context=request_helper_method_context)
                    )
                    request_file_path_object.write(
                        request_template.REQUEST_METHOD_TEMPLATE.render(context=request_method_context)
                    )
                except Exception as E:
                    logger.debug(E)
                    raise Exception("Unable to write data into file")
            else:
                request_helper_render_object = request_helper_templates.REQUEST_HELPER_METHOD_TEMPLATE.render(
                    context=request_helper_method_context)
                request_render_object = request_template.REQUEST_METHOD_TEMPLATE.render(context=request_method_context)
        else:
            request_method_context = self.context_serializers(function_name=method_name,
                                                              headers=headers,
                                                              method=path_method_name,
                                                              path=path,
                                                              request_path=path_name,
                                                              deprecated=deprecated
                                                              )
            if render:
                try:
                    request_helper_path_object.write(
                        request_helper_templates.REQUEST_HELPER_METHOD_TEMPLATE.render(
                            context=request_helper_method_context)
                    )
                    request_file_path_object.write(
                        request_template.REQUEST_METHOD_TEMPLATE.render(context=request_method_context)
                    )
                except Exception as E:
                    logger.debug(E)
                    raise Exception("Unable to write data into file")
            else:
                request_helper_render_object = request_helper_templates.REQUEST_HELPER_METHOD_TEMPLATE.render(
                    context=request_helper_method_context)
                request_render_object = request_template.REQUEST_METHOD_TEMPLATE.render(context=request_method_context)
        return request_render_object, request_helper_render_object

    def tag_generator(self, request_file_path_object, request_helper_path_object):
        try:
            request_file_path_object.write(
                request_template.REQUEST_METHOD_TAG_TEMPLATE.render(
                    context=self.context_serializers()
                )
            )
            request_helper_path_object.write(
                request_helper_templates.REQUEST_HELPER_METHOD_TAG_TEMPLATE.render(
                    context=self.context_serializers()
                )
            )
        except Exception as E:
            logging.debug(E)
            raise Exception("Not able to write data {}".format(E))

    def context_serializers(self, **kwargs):
        context_payload = dict()
        context_payload["team_name"] = self.team_name
        context_payload["folder_path"] = folder_dict
        context_payload["time_data"] = datetime.datetime.now()
        if "class_name" in kwargs:
            if "class_suffix" in kwargs:
                context_payload["class_name"] = ''.join(x for x in re.sub(special_char_remover_regex, ' ',
                                                                          str(kwargs["class_name"])).title()
                                                        if not x.isspace()) + kwargs["class_suffix"]
            else:
                context_payload["class_name"] = ''.join(x for x in re.sub(special_char_remover_regex, ' ',
                                                                          str(kwargs["class_name"])).title()
                                                        if not x.isspace())
        if "file_name" in kwargs:
            if "file_suffix" in kwargs:
                context_payload["file_name"] = kwargs["file_name"] + kwargs["file_suffix"]
            else:
                context_payload["file_name"] = kwargs["file_name"]
        if "import_class_name" in kwargs:
            context_payload["import_class_name"] = kwargs["import_class_name"]
        if "function_name" in kwargs:
            if "function_name_suffix" in kwargs:
                context_payload["function_name"] = kwargs["function_name"] + kwargs["function_name_suffix"]
            else:
                context_payload["function_name"] = kwargs["function_name"]
        if "payload" in kwargs:
            context_payload["payload"] = kwargs["payload"]
        if "headers" in kwargs:
            context_payload["headers"] = kwargs["headers"]
        if "path" in kwargs:
            context_payload["path"] = kwargs["path"]
        if "params" in kwargs:
            context_payload["params"] = kwargs["params"]
        if "request_path" in kwargs:
            context_payload["request_path"] = kwargs["request_path"]
        if "request_function_name" in kwargs:
            context_payload["request_function_name"] = kwargs["request_function_name"]
        if "method" in kwargs:
            context_payload["method"] = kwargs["method"]
        if "flow_file_name" in kwargs:
            context_payload["flow_file_name"] = kwargs["flow_file_name"]
        if "flow_class_name" in kwargs:
            context_payload["flow_class_name"] = kwargs["flow_class_name"]
        if "method_list" in kwargs:
            context_payload["method_list"] = kwargs["method_list"]
        if "task_flow_list" in kwargs:
            context_payload["task_flow_list"] = kwargs["task_flow_list"]
        if "auth_header" in kwargs:
            context_payload["auth_header"] = kwargs["auth_header"]
        if "deprecated" in kwargs:
            context_payload["deprecated"] = kwargs["deprecated"]
        return context_payload

    def file_read_write(self, file_path, write=False, append=False):
        try:
            if append:
                file_object = open(file_path, "a")
            elif write:
                file_object = open(file_path, "w")
            else:
                file_object = open(file_path, "r")
        except Exception as E:
            logger.debug(E)
            raise FileNotFoundError
        return file_object

    def meta_config_path_definitions_generator(self, request_path, request_method_name, request_file_name,
                                               request_helper_file_name, deprecated):
        if request_path and request_method_name and request_file_name \
                and request_helper_file_name and deprecated is not None:
            return {
                request_path: {
                    "method_details": {
                        "request_method_name": request_method_name,
                        "request_method_path": folder_dict_deepcopy["api_requests"]["path"] + "/" + request_file_name,
                        "request_helper_name": request_method_name,
                        "request_helper_path": folder_dict_deepcopy["request_helpers"]["path"] + "/" + request_helper_file_name,
                    },
                    "deprecation_status": deprecated
                }
            }
        return {}

    def meta_config_schema_generator(self, swagger_data, controller_name, request_path_list=None, dep_path=None):
        if dep_path is not None:
            for _data in swagger_data["schema"][controller_name]:
                if dep_path == _data["path"]:
                    try:
                        swagger_data["schema"][controller_name].remove(_data)
                        if not bool(swagger_data["schema"][controller_name]):
                            swagger_data["schema"].pop(controller_name)
                        break
                    except Exception as E:
                        logger.debug(E)
                        raise TypeError(E)
        if request_path_list is not None and bool(request_path_list):
            if controller_name in swagger_data["schema"]:
                try:
                    swagger_data["schema"][controller_name].extend([request_path_list])
                except Exception as E:
                    logger.debug(E)
                    raise TypeError(E)
            else:
                try:
                    swagger_data["schema"].update({controller_name: [request_path_list]})
                except Exception as E:
                    logger.debug(E)
                    raise TypeError(E)

    def update_meta_config_path_definitions(self, swagger_data, http_method, data_json=None, dep_path=None):
        if dep_path is not None:
            if dep_path in swagger_data["path_definitions"][http_method]:
                try:
                    swagger_data["path_definitions"][http_method].pop(dep_path)
                except Exception as E:
                    logger.debug(E)
                    raise TypeError(E)
        if data_json is not None and bool(data_json):
            if http_method in swagger_data["path_definitions"]:
                try:
                    swagger_data["path_definitions"][http_method].update(data_json)
                except Exception as E:
                    logger.debug(E)
                    raise TypeError(E)
            else:
                swagger_data["path_definitions"][http_method] = data_json

    def generate_config_file(self, path, config_data):
        if config_data is not None:
            path_object = self.file_read_write(path, write=True)
            try:
                path_object.write(json.dumps(config_data, indent=4))
            except Exception as E:
                logger.debug(E)
                raise Exception("Not able to write data {}".format(E))
            finally:
                path_object.close()
        else:
            logger.error("Invalid meta config details")

    def generate_audit_log_file(self, path, content):
        time_stamp = datetime.datetime.now()
        content_data = "{}: {}".format(time_stamp, content)
        path_object = self.file_read_write(path + "/audit_log.log", append=True)
        try:
            path_object.write("{}\n".format(content_data))
        except Exception as E:
            logging.debug(E)
            raise Exception(E)
        finally:
            path_object.close()


class VersionBaseGenerator:
    def __init__(self, team_name, script_path, upload_path):
        self.team_name = team_name
        self.results_path = os.path.join(upload_path, self.team_name)
        try:
            shutil.rmtree(self.results_path, ignore_errors=True)
        except Exception as E:
            logger.debug(E)
            logger.error("Failed to delete old folder : {}".format(E))
        try:
            file_object = zipfile.ZipFile(script_path, "r", zipfile.ZIP_DEFLATED)
        except Exception as E:
            logger.debug(E)
            raise FileNotFoundError("Zip file is not present {}".format(E))
        self.file_name_list = file_object.namelist()
        if self.team_name + "/MetaConfig.json" and self.team_name + "/scripts/" not in file_object.namelist():
            raise FileNotFoundError("config and script folder not present")
        if self.team_name + "/audit_log.log" not in file_object.namelist():
            raise FileNotFoundError("audit log file is not present")
        try:
            with zipfile.ZipFile(script_path, 'r') as zip_ref:
                zip_ref.extractall(upload_path)
        except Exception as E:
            logger.debug(E)
            raise Exception("Zip file extraction failure {}".format(E))
        self.extract_file_path = os.path.join(upload_path, team_name)
        self.comparator_service = BaseComparator()
        try:
            self.swagger_meta_data = json.loads(open(self.extract_file_path + "/MetaConfig.json", "r").read())
        except Exception as E:
            logger.debug(E)
            raise Exception("not able to read the json data {}".format(E))
        self.swagger_meta_data_copy = copy.deepcopy(self.swagger_meta_data)
        self.generator_helper = GeneratorHelper(self.team_name)
        self.generator_helper.generate_audit_log_file(self.results_path, "Got request for team {} for version comparison".format(self.team_name))
        if self.team_name + "/" + folder_dict["api_requests"]["path"] + "/" not in self.file_name_list:
            raise Exception("path doesnt exist :{}".format(folder_dict["api_requests"]["path"]))
        if self.team_name + "/" + folder_dict["request_helpers"]["path"] + "/" not in self.file_name_list:
            raise Exception("path doesnt exist :{}".format(folder_dict["request_helpers"]["path"]))
        try:
            self.meta_config_file_path = os.path.join(self.extract_file_path, "MetaConfig.json")
            self.config_meta_json = json.loads(open(self.meta_config_file_path, "r").read())
        except Exception as E:
            raise FileNotFoundError(E)
        folder_dict["request_helpers"]["path"] = os.path.join(str(self.extract_file_path),
                                                              str(folder_dict["request_helpers"]["path"]))
        folder_dict["api_requests"]["path"] = os.path.join(str(self.extract_file_path),
                                                           str(folder_dict["api_requests"]["path"]))
        self.helper_folder_path = folder_dict_deepcopy["request_helpers"]["path"]
        self.api_request_folder_path = folder_dict_deepcopy["api_requests"]["path"]

    def base_generator(self, new_swagger_data):
        new_controller, new_api_in_controller, deprecated = self.comparator_service.base_compare(self.swagger_meta_data,
                                                                                                 new_swagger_data)
        logger.debug("new_controller : {}\n new_api_controller : {}\n deprecated : {}\n".format(new_controller,
                                                                                                new_api_in_controller,
                                                                                                deprecated))
        self.generator_helper.generate_audit_log_file(self.results_path, "New Controller Details: {}\n"
                                                                         "New Api in Controller Details: {}\n"
                                                                         "Deprecated API/Controller Details : "
                                                                         "{}\n".format(new_controller,
                                                                                       new_api_in_controller,
                                                                                       deprecated))
        if bool(new_controller):
            self.new_controller_generator(new_controller)
        if bool(new_api_in_controller):
            self.generator_for_new_api(new_api_in_controller)
        if bool(deprecated):
            self.generator_for_deprecated_api(deprecated)
        if "version" in self.swagger_meta_data_copy:
            if bool(new_controller) or bool(new_api_in_controller) or bool(deprecated):
                self.swagger_meta_data_copy["version"] = int(self.swagger_meta_data_copy["version"]) + 1
        else:
            logger.debug("Version details not present in meta file.")
            raise Exception("Version details not present in meta file.")
        self.generator_helper.generate_config_file(self.meta_config_file_path, self.swagger_meta_data_copy)

    def new_controller_generator(self, swagger_data):
        for controller_name, controller_method in swagger_data.items():
            request_group = re.sub(special_char_remover_regex, '_', str(controller_name))
            request_file_name = "{}.py".format(request_group.lower())
            if self.team_name + "/" + self.api_request_folder_path + "/" + request_file_name in self.file_name_list:
                raise FileExistsError("Already file has created for new controller")
            request_helper_path_object, request_helper_claas_context, request_helper_file_name = \
                self.generator_helper.request_helper_class_generator(controller_name, request_group)
            request_file_path_object, request_file_name = \
                self.generator_helper.request_class_generator(controller_name, request_group,
                                                              request_helper_claas_context)
            for _request_data in controller_method:
                path_name = _request_data["path"]
                http_method = _request_data["method"]
                deprecated = _request_data["deprecated"]
                payload = _request_data["request_payload"].get("payload")
                params = _request_data["request_payload"].get("params")
                path = _request_data["request_payload"].get("path")
                headers = _request_data["request_payload"].get("headers")
                method_name = self.generator_helper.method_name_fetch(request_group,
                                                                      path_name,
                                                                      http_method)
                self.generator_helper.request_payload_generator(method_name,
                                                                http_method,
                                                                path_name,
                                                                payload,
                                                                params,
                                                                path,
                                                                headers,
                                                                deprecated,
                                                                request_helper_path_object,
                                                                request_file_path_object)
                self.generator_helper.meta_config_schema_generator(self.swagger_meta_data_copy, controller_name, _request_data)
                path_def = self.generator_helper.meta_config_path_definitions_generator(path_name, method_name, request_file_name, request_helper_file_name, deprecated)
                self.generator_helper.update_meta_config_path_definitions(self.swagger_meta_data_copy, http_method, path_def)
            self.generator_helper.tag_generator(request_file_path_object, request_helper_path_object)

    def generator_for_new_api(self, new_api_in_controller):
        for controller_name, controller_method in new_api_in_controller.items():
            request_group = re.sub(special_char_remover_regex, '_', str(controller_name))
            request_helper_path, request_helper_claas_context, request_helper_file_name = \
                self.generator_helper.request_helper_class_generator(controller_name, request_group, render=False)
            if self.team_name + "/" + self.helper_folder_path + "/" + request_helper_file_name not in self.file_name_list:
                raise FileExistsError("Helper file not present or renamed {}".format(request_helper_file_name))
            request_file_path, request_file_name = \
                self.generator_helper.request_class_generator(controller_name, request_group,
                                                              request_helper_claas_context, render=False)
            if self.team_name + "/" + self.api_request_folder_path + "/" + request_file_name not in self.file_name_list:
                raise FileExistsError("Request file not present or renamed {}".format(request_file_name))
            for _request_data in controller_method:
                path_name = _request_data["path"]
                http_method = _request_data["method"]
                deprecated = _request_data["deprecated"]
                payload = _request_data["request_payload"].get("payload")
                params = _request_data["request_payload"].get("params")
                path = _request_data["request_payload"].get("path")
                headers = _request_data["request_payload"].get("headers")
                if _request_data["path"] in self.swagger_meta_data["path_definitions"][_request_data["method"]]:
                    deprecated_request_method = self.swagger_meta_data["path_definitions"][_request_data["method"]][_request_data["path"]]["method_details"]["request_method_name"]
                    deprecated_helper_method = self.swagger_meta_data["path_definitions"][_request_data["method"]][_request_data["path"]]["method_details"]["request_helper_name"]
                    method_name = self.generator_helper.method_name_fetch(request_group,path_name, http_method) + (
                                          "_v" + str(self.config_meta_json["version"] + 1))
                else:
                    deprecated_request_method = None
                    deprecated_helper_method = None
                    method_name = self.generator_helper.method_name_fetch(request_group,path_name, http_method)
                request_render_object, request_helper_render_object = self.generator_helper.request_payload_generator(
                    method_name,
                    http_method,
                    path_name,
                    payload,
                    params,
                    path,
                    headers,
                    deprecated,
                    render=False
                )
                if _request_data["deprecated"]:
                    if not self.config_meta_json["path_definitions"][_request_data["method"]][_request_data["path"]]["deprecation_status"]:
                        file_lines_list, method_implement_tag_index, deprecated_method_index = self.get_index_of_file(
                            request_file_path,
                            deprecated_function_name=deprecated_request_method
                        )
                        self.update_file_data(file_lines_list=file_lines_list,
                                              file_path=request_file_path,
                                              deprecated_method_index=deprecated_method_index,
                                              )
                        file_lines_list, method_implement_tag_index, deprecated_method_index = self.get_index_of_file(
                            request_helper_path,
                            deprecated_function_name=deprecated_helper_method
                        )
                        self.update_file_data(file_lines_list=file_lines_list,
                                              file_path=request_helper_path,
                                              deprecated_method_index=deprecated_method_index,
                                              )
                        self.generator_helper.meta_config_schema_generator(self.swagger_meta_data_copy, controller_name, _request_data, dep_path=path_name)
                        path_def = self.generator_helper.meta_config_path_definitions_generator(path_name, method_name, request_file_name, request_helper_file_name, deprecated)
                        self.generator_helper.update_meta_config_path_definitions(self.swagger_meta_data_copy, http_method, path_def, dep_path=path_name)
                else:
                    if deprecated_request_method and deprecated_helper_method is not None:
                        if not self.config_meta_json["path_definitions"][_request_data["method"]][_request_data["path"]]["deprecation_status"]:
                            file_lines_list, method_implement_tag_index, deprecated_method_index = self.get_index_of_file(
                                request_file_path,
                                deprecated_function_name=deprecated_request_method
                            )
                            self.update_file_data(file_lines_list=file_lines_list,
                                                  file_path=request_file_path,
                                                  method_implement_tag_index=method_implement_tag_index,
                                                  deprecated_method_index=deprecated_method_index,
                                                  new_method_name=method_name,
                                                  method_render_data=request_render_object
                                                  )
                            file_lines_list, method_implement_tag_index, deprecated_method_index = \
                                self.get_index_of_file(request_helper_path,
                                                       deprecated_function_name=deprecated_helper_method
                                                       )
                            self.update_file_data(file_lines_list=file_lines_list,
                                                  file_path=request_helper_path,
                                                  method_implement_tag_index=method_implement_tag_index,
                                                  deprecated_method_index=deprecated_method_index,
                                                  new_method_name=method_name,
                                                  method_render_data=request_helper_render_object
                                                  )
                            self.generator_helper.meta_config_schema_generator(self.swagger_meta_data_copy, controller_name, _request_data, dep_path=path_name)
                            path_def = self.generator_helper.meta_config_path_definitions_generator(path_name, method_name, request_file_name, request_helper_file_name, deprecated)
                            self.generator_helper.update_meta_config_path_definitions(self.swagger_meta_data_copy, http_method, path_def, dep_path=path_name)
                    else:
                        file_lines_list, method_implement_tag_index, deprecated_method_index = self.get_index_of_file(
                            request_file_path)
                        self.update_file_data(file_lines_list=file_lines_list,
                                              file_path=request_file_path,
                                              method_implement_tag_index=method_implement_tag_index,
                                              deprecated_method_index=deprecated_method_index,
                                              new_method_name=method_name,
                                              method_render_data=request_render_object,
                                              new_method=True
                                              )
                        file_lines_list, method_implement_tag_index, deprecated_method_index = self.get_index_of_file(
                            request_helper_path)
                        self.update_file_data(file_lines_list=file_lines_list,
                                              file_path=request_helper_path,
                                              method_implement_tag_index=method_implement_tag_index,
                                              deprecated_method_index=deprecated_method_index,
                                              new_method_name=method_name,
                                              method_render_data=request_helper_render_object,
                                              new_method=True
                                              )
                        self.generator_helper.meta_config_schema_generator(self.swagger_meta_data_copy, controller_name, _request_data)
                        path_def = self.generator_helper.meta_config_path_definitions_generator(path_name, method_name, request_file_name, request_helper_file_name, deprecated)
                        self.generator_helper.update_meta_config_path_definitions(self.swagger_meta_data_copy, http_method, path_def)

    def generator_for_deprecated_api(self, deprecated):
        for controller_name, controller_method in deprecated.items():
            request_group = re.sub(special_char_remover_regex, '_', str(controller_name))
            request_helper_path, request_helper_claas_context, request_helper_file_name = \
                self.generator_helper.request_helper_class_generator(controller_name, request_group, render=False)
            if self.team_name + "/" + self.helper_folder_path + "/" + request_helper_file_name not in self.file_name_list:
                raise FileExistsError("Helper file not present or renamed {}".format(request_helper_file_name))
            request_file_path, request_file_name = \
                self.generator_helper.request_class_generator(controller_name, request_group,
                                                              request_helper_claas_context, render=False)
            if self.team_name + "/" + self.api_request_folder_path + "/" + request_file_name not in self.file_name_list:
                raise FileExistsError("Request file not present or renamed {}".format(request_file_name))
            for _request_data in controller_method:
                path_name = _request_data["path"]
                http_method = _request_data["method"]
                deprecated = _request_data["deprecated"]
                if _request_data["method"] in self.config_meta_json["path_definitions"] \
                        and _request_data["path"] in self.config_meta_json["path_definitions"][_request_data["method"]] \
                            and not self.config_meta_json["path_definitions"][_request_data["method"]][_request_data["path"]]["deprecation_status"]:
                    request_file_method_name = self.config_meta_json["path_definitions"][_request_data["method"]][_request_data["path"]]["method_details"]["request_method_name"]
                    file_lines_list, method_implement_tag_index, deprecated_method_index = self.get_index_of_file(
                        request_file_path,
                        deprecated_function_name=request_file_method_name)

                    self.update_file_data(file_lines_list=file_lines_list,
                                          file_path=request_file_path,
                                          deprecated_method_index=deprecated_method_index,
                                          )
                    request_file_helper_method_name = self.config_meta_json["path_definitions"][_request_data["method"]][_request_data["path"]]["method_details"]["request_helper_name"]
                    file_lines_list, method_implement_tag_index, deprecated_method_index = self.get_index_of_file(
                        request_helper_path,
                        deprecated_function_name=request_file_helper_method_name)
                    self.update_file_data(file_lines_list=file_lines_list,
                                          file_path=request_helper_path,
                                          deprecated_method_index=deprecated_method_index,
                                          )
                    self.generator_helper.meta_config_schema_generator(self.swagger_meta_data_copy, controller_name, dep_path=path_name)
                    self.generator_helper.update_meta_config_path_definitions(self.swagger_meta_data_copy, http_method, dep_path=path_name)

    def update_file_data(self, file_lines_list, file_path, method_implement_tag_index=None,
                         deprecated_method_index=None,
                         new_method_name=None, method_render_data=None, new_method=False):
        if deprecated_method_index is not None:
            if new_method_name is not None:
                context = {
                    "method_data": "This method is deprecated at {}. Please use new method : {}()".format(datetime.datetime.now(), new_method_name)}
            else:
                context = {"method_data": "This method is deprecated as per latest swagger specs at {}.".format(datetime.datetime.now())}
            try:
                file_lines_list.insert(deprecated_method_index - 1,
                                       helpers_templates.DEPRECATED_HELPER.render(context=context))
            except Exception as E:
                logger.debug(E)
                raise Exception(E)
        if method_render_data is not None and method_implement_tag_index is not None:
            if new_method:
                try:
                    file_lines_list.insert(method_implement_tag_index-1, method_render_data)
                except Exception as E:
                    logger.debug(E)
                    raise Exception(E)
            else:
                try:
                    file_lines_list.insert(method_implement_tag_index, method_render_data)
                except Exception as E:
                    logger.debug(E)
                    raise Exception(E)
        file_path_object = self.generator_helper.file_read_write(file_path, write=True)
        file_path_object.writelines(file_lines_list)
        file_path_object.close()

    def get_index_of_file(self, file_path, deprecated_function_name=None):

        file_object = self.generator_helper.file_read_write(file_path)
        try:
            file_lines_list = file_object.readlines()
        except Exception as E:
            logger.debug(E)
            raise Exception("Not able to read file content {}".format(E))
        finally:
            file_object.close()
        method_implement_tag_index = None
        deprecated_method_index = None
        for _data in file_lines_list:
            if (_data.strip()).startswith("#TODO:METHOD_IMPLEMENTATION_TAG"):
                method_implement_tag_index = file_lines_list.index(_data)
            if deprecated_function_name is not None:
                if (_data.strip()).startswith("def {}".format(deprecated_function_name)):
                    if _data.strip().split("(")[0] == "def {}".format(deprecated_function_name):
                        deprecated_method_index = file_lines_list.index(_data)
        if method_implement_tag_index is None:
            raise Exception("Not able to get tag index")
        if deprecated_function_name is not None and deprecated_method_index is None:
            raise Exception("Deprecated function is not available in old framework")
        return file_lines_list, method_implement_tag_index, deprecated_method_index
