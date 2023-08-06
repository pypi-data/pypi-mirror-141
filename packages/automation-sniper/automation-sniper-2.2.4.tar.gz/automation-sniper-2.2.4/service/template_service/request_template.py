"""Module: request templates"""

from jinja2 import Template


REQUEST_CLASS_TEMPLATE = Template(
    '''import os
import json
from {{ context.team_name }}.{{ context.folder_path.scripts.name }}.{{ context.folder_path.nfr_requests.name }}.{{ context.folder_path.config.name }}.CommonConfig import BASE_URL
from {{ context.team_name }}.{{ context.folder_path.scripts.name }}.{{ context.folder_path.nfr_requests.name }}.{{ context.folder_path.config.name }}.Utils import Helper, deprecated
from {{ context.team_name }}.{{ context.folder_path.scripts.name }}.{{ context.folder_path.nfr_requests.name }}.{{ context.folder_path.parsers.name }}.{{ context.folder_path.request_helpers.name }}.{{ context.file_name }} import {{ context.import_class_name }}
from {{ context.team_name }}.{{ context.folder_path.scripts.name }}.{{ context.folder_path.nfr_requests.name }}.{{ context.folder_path.config.name }}.HeaderManager import HeaderManager


class {{context.class_name}}:
    """
    {{context.class_name}} class which do actual api call etc
    """
    def __init__(self, locust_object):
        """
        This this constructor for {{context.class_name}}. Which initializes host data, header data and helper data.
        :param locust_object: 
        """
        self.user = locust_object.user
        self.locust_object = locust_object
        self.request_helper = {{ context.import_class_name }}(self.locust_object)
        if bool(self.user.host):
            self.host = self.user.host
        else:
            self.host = BASE_URL
        self.helper_object = Helper()
        self.header = HeaderManager().initialize_header()
           
'''
)

REQUEST_METHOD_TEMPLATE = Template(
    '''
    {% if context.deprecated -%}
    @deprecated("This method is deprecated as per latest swagger specs at {{ context.time_data }}.")
    {% endif -%}
    def {{context.function_name}}(self):
        """
        Actual API request implementation for {{context.function_name}}
        :return: 
        """
        {% if context.headers | length > 0 -%}
        path_headers = {{ context.headers }}
        headers = path_headers.update(self.header)
        {% endif -%}
        {% if 'params' in context -%}
        params = self.request_helper.{{ context.request_function_name }}()
        {% endif -%}
        {% if 'payload' in context -%}
        payload = self.request_helper.{{ context.request_function_name }}()
        {% endif -%}
        {% if context.path | length != 0 -%}
        path_payload = {{ context.path }}
        request_path = self.helper_object.url_parser(path_payload, "{{ context.request_path }}")
        self.url = self.host+request_path
        {% else -%}
        self.url = self.host+"{{ context.request_path }}"
        {% endif -%}
        {% if 'params' in context -%}
        response = self.locust_object.client.{{ context.method }}(self.url, headers=headers, params=params, name="{{context.function_name}}")
        {% elif 'payload' in context -%}
        response = self.locust_object.client.{{ context.method }}(self.url, headers=headers, data=payload, name="{{context.function_name}}")
        {% else -%}
        response = self.locust_object.client.{{ context.method }}(self.url, headers=headers, name="{{context.function_name}}")
        {% endif %}      
'''
)

REQUEST_METHOD_TAG_TEMPLATE = Template(
    '''
    #TODO:METHOD_IMPLEMENTATION_TAG [DONT DELETE]
             
'''
)
