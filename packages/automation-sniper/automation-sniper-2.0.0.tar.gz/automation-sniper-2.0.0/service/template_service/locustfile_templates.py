"""Module: locustfile templates"""

from jinja2 import Template

MAIN_LOCUST_HEADER = Template(
    """import os
import sys
sys.path.append(os.path.join(os.getcwd(), "../../"))
from locust import TaskSet, HttpUser
"""
)
MAIN_LOCUST_HEADER_FUNCTION_IMPORT = Template(
    """
from {{ context.team_name }}.{{ context.folder_path.scripts.name }}.{{ context.folder_path.nfr_requests.name }}.{{ context.folder_path.flow_scenarios.name }}.{{ context.flow_file_name }} import {{ context.flow_class_name }}
"""
)

TASK_FLOW_METHOD =Template('''

def {{ context.flow_file_name }}_task_flow(self):
    """
    This is the taskflow method for {{ context.flow_file_name }} which will call Flow class method.
    :param self: 
    :return:
    """
    {{ context.flow_file_name }}_flow_object = {{ context.flow_class_name }}(self)
    {% for _method in context.method_list -%}
    {{ context.flow_file_name }}_flow_object.{{ _method }}()
    {% endfor %}
''')

BASE_TASKSET_CLASS = Template('''

class FlowTaskset(TaskSet):
    """
    It is a collection of tasks that will be executed much like the ones declared directly on a HttpUser class.
    Here you can defined all your task flow with weightage.
    The min/max wait times control the amount of time each simulated user waits between executing tasks. 
    Each user will execute a task at random, wait a random amount of time between min_wait and max_wait, and then repeat.
    min_wait: wait in ms. 
    max_wait: wait in ms. 
    tasks: It accept key as task flow method and value as weightage. Based on the weightage It will prioritize the run.
    """
    min_wait = 3000
    max_wait = 10000
    tasks = {
        {% for flow in context.task_flow_list -%}
         {{ flow }}_task_flow: 1,
        {% endfor %}
    }

    def on_start(self):
        """
        A TaskSet class can optionally declare an on_start function,
        which is called when a simulated user starts executing that TaskSet class.
        This can be used to log in or apply credentials once before beginning the load test.
        :return:
        """
        pass

    def on_stop(self):
        """
        A TaskSet class can optionally declare an on_stop function,
        which is called when user task executed.
        This can be used to log out or delete test config once load test is done.
        :return:
        """
        pass


class Checkout(HttpUser):
    """
    HttpUser is the most commonly used User. It adds a client attribute which is used to make HTTP requests.
    host: host in string format. It accept host url on which you are going to put load.
    tasks: It is the collection of all taskset you are going to execute.
    """
    tasks = [FlowTaskset]
    host = ""
    '''
)