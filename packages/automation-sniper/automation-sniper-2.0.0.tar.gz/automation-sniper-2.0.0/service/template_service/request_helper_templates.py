"""Module: request templates"""

from jinja2 import Template


REQUEST_HELPER_CLASS_TEMPLATE = Template(
    '''import os
import json
from {{ context.team_name }}.{{ context.folder_path.scripts.name }}.{{ context.folder_path.nfr_requests.name }}.{{ context.folder_path.config.name }}.CommonConfig import BASE_URL
from {{ context.team_name }}.{{ context.folder_path.scripts.name }}.{{ context.folder_path.nfr_requests.name }}.{{ context.folder_path.config.name }}.Utils import Helper, deprecated


class {{context.class_name}}:
    """
    This is a request helper class which provide json serialized payload or query params.
    Note: Please edit the payload data before run
    """
    def __init__(self, locust_object):
        """
        Constructor for {{context.class_name}}
        :param locust_object: accept object of locust.
        """
        self.locust_object = locust_object   
             
'''
)

REQUEST_HELPER_METHOD_TEMPLATE = Template(
    '''
    {% if context.deprecated -%}
    @deprecated("This method is deprecated as per latest swagger specs at {{ context.time_data }}.")
    {% endif -%}
    def {{context.function_name}}(self):
        """
        This the request helper method for {{context.function_name}}.  
        :return: 
        """
        request_payload = {{ context.payload }}
        return json.dumps(request_payload)
             
'''
)

REQUEST_HELPER_METHOD_TAG_TEMPLATE = Template(
    '''
    #TODO:METHOD_IMPLEMENTATION_TAG [DONT DELETE]
             
'''
)
