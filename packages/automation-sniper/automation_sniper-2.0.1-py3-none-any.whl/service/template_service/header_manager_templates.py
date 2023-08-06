"""Module: request templates"""

from jinja2 import Template


HEADER_TEMPLATE = Template('''import os
import json


"""
Please add custom header in CUSTOM_HEADER dict
"""
CUSTOM_HEADER = {
#"x-test": "true"
}

AUTH_HEADER = {{ context.auth_header }} 


class HeaderManager:
    """
    This is a Header manager class which handle global and custom header support.
    """
    def __init__(self):
        """
        Constructor for HeaderManager to initialize empty header
        """
        self.header = {}
    
    def initialize_header(self):
        """
        This method is responsible to call all header initializer.
        :return: updated header dict
        """
        self.custom_header_initializer()
        self.auth_header_initializer()
        return self.header
        
    def custom_header_initializer(self):
        """
        This method is responsible to handle custom header given by user.
        :return: updated header dict
        """
        return self.header.update(CUSTOM_HEADER) 

    def auth_header_initializer(self):
        """
        This method is responsible to handle auth header
        :return: updated header dict
        """
        auth_header = {}
        #fixme: Please select one auth and comment remaining
        {% if "apiKey" in context.auth_header -%}
        auth_header = {AUTH_HEADER['apiKey']: self._get_auth_header()}
        {% endif -%}
        {% if "basic" in context.auth_header -%}
        auth_header = {'Authorization': "Basic {}".format(self._get_auth_header())}
        {% endif -%}
        {% if "oauth2" in context.auth_header -%}
        auth_header = {'Authorization': "Bearer {}".format(self._get_auth_header())}
        {% endif -%}
        return self.header.update(auth_header)

    @staticmethod
    def _get_auth_header():
        """
        This method handle token generation for auth header handler.
        Note: Please write auth generation logic here.
        :return: token as string
        """
        #fixme: Please add your logic to get token
        token = "API Token"
        return token
''')
