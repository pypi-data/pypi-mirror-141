import os
from service.template_service import auth_templates
from service.config.key_config import SECURITY_CONFIG_KEY
from service.utils.logger import get_logger

logger = get_logger()


class SecurityManager:
    def __init__(self):
        logger = get_logger(os.environ)

    def generate_security_cases(self, security_data: dict) -> dict:
        """Method: generate security cases"""

        security_cases = {}
        try:
            for security_type, security_config in security_data.items():
                if security_type == SECURITY_CONFIG_KEY["basic"]:
                    security_cases[SECURITY_CONFIG_KEY["basic"]] = 'Basic'
                elif security_type == SECURITY_CONFIG_KEY["apiKey"]:
                    location = security_config.get("in")
                    name = security_config.get("name")
                    if location.lower() == "header" and name:
                        security_cases["apiKey"] = str(name)
                    else:
                        raise Exception("security header is not configured properly.")
                elif security_type == SECURITY_CONFIG_KEY["oauth2"]:
                    security_cases[SECURITY_CONFIG_KEY["oauth2"]] = 'Bearer'
        except Exception as E:
            logger.debug(E)
            raise Exception(E)
        return security_cases