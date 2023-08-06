"""Module: locustfile templates"""

from jinja2 import Template

HELPER_CLASS = Template(
    '''import datetime
import random
import string
import warnings
from {{ context.team_name }}.{{ context.folder_path.scripts.name }}.{{ context.folder_path.nfr_requests.name }}.{{ context.folder_path.config.name }}.TestDataProvider import getContentDict


class Helper:
    @staticmethod
    def get_random_choice_from_values(*args):
        """
        
        :param args: 
        :return: 
        """
        return random.choice(args)

    @staticmethod
    def get_random_int(start: int = -100, end: int = 100):
        """
        
        :param start: 
        :param end: 
        :return: 
        """
        return random.randint(start, end)

    @classmethod
    def get_random_positive_int(cls, start: int = 1, end: int = 100):
        """
        
        :param start: 
        :param end: 
        :return: 
        """
        return cls.get_random_int(start, end)

    @classmethod
    def get_random_negative_int(cls, start: int = -100, end: int = -1):
        """
        
        :param start: 
        :param end: 
        :return: 
        """
        return cls.get_random_int(start, end)

    @classmethod
    def get_random_float(cls, start: int = -100, end: int = 100):
        """
        
        :param start: 
        :param end: 
        :return: 
        """
        return random.random() * cls.get_random_int(start, end)

    @staticmethod
    def get_random_bool():
        """
        
        :return: 
        """
        return random.choice([True, False])

    @staticmethod
    def get_null_value():
        """
        
        :return: 
        """
        return None

    @classmethod
    def get_random_string(cls, min_len: int = 0, max_len: int = 100):
        """
        
        :param min_len: 
        :param max_len: 
        :return: 
        """
        string_len = cls.get_random_int(min_len, max_len)
        return "".join(random.choices(string.ascii_uppercase + string.digits, k=string_len))

    @classmethod
    def get_random_datetime(
        cls,
        result_format: str = "%Y-%m-%d %H:%M:%S",
        min_timestamp: int = 0,
        max_timestamp: int = 1600000000
    ):  # from Unix start time to 09/13/2020 @ 12:26pm (UTC)
        """
        
        :param result_format: 
        :param min_timestamp: 
        :param max_timestamp: 
        :return: 
        """
        result = cls.get_random_int(min_timestamp, max_timestamp)
        result = datetime.datetime.fromtimestamp(result)
        return result.strftime(result_format)

    @classmethod
    def get_random_password(cls, min_len: int = 8, max_len: int = 25):
        """
        
        :param min_len: 
        :param max_len: 
        :return: 
        """
        string_len = cls.get_random_int(min_len, max_len)
        return "".join(random.choices(string.ascii_uppercase + string.digits + string.punctuation, k=string_len))

    @classmethod
    def get_random_email(cls, min_len: int = 10, max_len: int = 25):
        """
        
        :param min_len: 
        :param max_len: 
        :return: 
        """
        username_len = cls.get_random_int(min_len, max_len)
        tld_len = cls.get_random_int(2, 5)
        username_len -= tld_len
        domain_len = cls.get_random_int(5, 10)
        username_len -= domain_len
        if any(i <= 0 for i in [tld_len, domain_len, username_len]):
            return cls.get_random_email()
        tld = "".join(random.choices(string.ascii_lowercase, k=tld_len))
        domain = "".join(random.choices(string.ascii_uppercase + string.digits, k=domain_len))
        username = "".join(random.choices(string.ascii_uppercase + string.digits, k=username_len))
        return f"{ username }@{ domain }.{ tld }"

    @classmethod
    def get_random_ipv4(cls):
        """
        
        :return: 
        """
        result = cls.get_random_int(0, 255)
        for x in range(3):
            result += "." + str(cls.get_random_int(0, 255))
        return result

    @classmethod
    def get_random_ipv6(cls):
        """
        
        :return: 
        """
        result = "".join(random.choices("abcdef" + string.digits, k=4))
        for x in range(7):
            result += ":" + "".join(random.choices("abcdef" + string.digits, k=4))
        return result
    
    @classmethod
    def payload_parser(cls, file_name: str, payload_data: dict):
        """
        
        :param file_name: 
        :param payload_data: 
        :return: 
        """
        parse_payload = {}
        if len(getContentDict(file_name)) > 0:
            random_data_selection = random.choice(getContentDict(file_name))
            for key, value in payload_data.items():
                if random_data_selection[key+"/"+str(value)] is not None:
                    parse_payload[key] = random_data_selection[key+"/"+str(value)]
        return parse_payload
    
    @classmethod
    def url_parser(cls, payload_data: dict, url: str):
        """
        
        :param payload_data: 
        :param url: 
        :return: 
        """
        parse_payload = {}
        for key, value in payload_data.items():
            parse_payload[key] = value
        return url.format(**parse_payload)


def deprecated(message=None):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used."""
    def deprecated_decorator(func):
        def deprecated_func(*args, **kwargs):
            if message is not None:
                raise DeprecationWarning("Called deprecated function {}(). {}".format(
                    func.__name__, message))
            else:
                raise DeprecationWarning("Called deprecated function {}().".format(func.__name__))
        return deprecated_func
    return deprecated_decorator

'''
)

DEPRECATED_HELPER = Template('''
    @deprecated('{{ context.method_data }}')
'''
)
