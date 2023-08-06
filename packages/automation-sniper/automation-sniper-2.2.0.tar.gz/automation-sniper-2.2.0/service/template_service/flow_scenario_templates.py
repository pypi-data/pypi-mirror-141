"""Module: request templates"""

from jinja2 import Template


FLOW_SCENARIO_CLASS_TEMPLATE = Template(
    '''import os
import json
from {{ context.team_name }}.{{ context.folder_path.scripts.name }}.{{ context.folder_path.nfr_requests.name }}.{{ context.folder_path.config.name }}.CommonConfig import BASE_URL
from {{ context.team_name }}.{{ context.folder_path.scripts.name }}.{{ context.folder_path.nfr_requests.name }}.{{ context.folder_path.config.name }}.Utils import Helper, deprecated
from {{ context.team_name }}.{{ context.folder_path.scripts.name }}.{{ context.folder_path.nfr_requests.name }}.{{ context.folder_path.api_requests.name }}.{{ context.file_name }} import {{ context.import_class_name }}


class {{context.class_name}}:
    """
    This is {{context.class_name}} which call all flow implementation method
    """
    def __init__(self, locust_object):
        """
        Constructor for {{context.class_name}}
        :param locust_object: accept object of locust.
        """
        self.locust_object = locust_object  
        self.request_object = {{ context.import_class_name }}(self.locust_object)
                  
'''
)

FLOW_SCENARIO_METHOD_TEMPLATE = Template(
    '''
    {% if context.deprecated -%}
    @deprecated("This method is deprecated as per latest swagger specs at {{ context.time_data }}.")
    {% endif -%}
    def {{context.function_name}}_flow(self):
        """
        This is the flow method for {{context.function_name}} which will call actual api implementation method
        :return: 
        """
        self.request_object.{{context.function_name}}()
             
'''
)