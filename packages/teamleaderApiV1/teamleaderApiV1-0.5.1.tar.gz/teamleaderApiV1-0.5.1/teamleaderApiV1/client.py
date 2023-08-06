import configparser
import os
from typing import Any

import requests
from ratelimit import limits, sleep_and_retry

from .objects import *


class Client:
    def __init__(
        self,
        api_group=None,
        api_secret=None,
        config_file_path=None,
    ):
        if config_file_path:
            api_group, api_secret = self.read_config_file(config_file_path)
        if not (api_group and api_secret):
            raise ValueError("All parameters should be filled")
        self.api_data = {"api_group": api_group, "api_secret": api_secret}
        self.tasks = Tasks(self.get_request, self.post_request)
        self.subscriptions = Subscriptions(self.get_request, self.post_request)
        self.tickets = Tickets(self.get_request, self.post_request)
        self.companies = Companies(self.get_request, self.post_request)
        self.contacts = Contacts(self.get_request, self.post_request)
        self.calls = Calls(self.get_request, self.post_request)
        self.timetracking = TimeTracking(self.get_request, self.post_request)
        self.deals = Deals(self.get_request, self.post_request)

    def read_config_file(self, config_file_path):
        config = configparser.ConfigParser()
        CONFIG_FILE_PATH = os.path.abspath(config_file_path)
        if not os.path.isfile(CONFIG_FILE_PATH):
            raise FileNotFoundError("Config file not found")
        config.read(CONFIG_FILE_PATH)
        api_group = config["teamleader_v1"]["api_group"]
        api_secret = config["teamleader_v1"]["api_secret"]
        return api_group, api_secret

    @sleep_and_retry
    @limits(calls=15, period=5)
    def teamleader_request(
        self, method, url_addition: str, additional_data
    ) -> Response:
        """

        :param method:
        :param url_addition:
        :param additional_data:
        :return:
        """
        if not url_addition:
            raise ValueError("No url_addition typed")
        additional_data = self._tranform_enums(additional_data)
        additional_data.update(self.api_data)
        url = f"https://app.teamleader.eu/api/{url_addition}.php"
        response = method(url, data=additional_data)
        response.raise_for_status()
        return response

    def post_request(
        self, url_addition: Any, additional_data: Optional[dict] = None
    ) -> Response:
        """

        :param url_addition:
        :param additional_data:
        :return:
        """
        if additional_data is None:
            additional_data = {}
        return self.teamleader_request(requests.post, url_addition, additional_data)

    def get_request(
        self, url_addition: str, additional_data: Optional[dict] = None
    ) -> Response:
        """

        :param url_addition:
        :param additional_data:
        :return:
        """
        if additional_data is None:
            additional_data = {}
        additional_data.update({"Content-Type": "application/json"})
        return self.teamleader_request(requests.get, url_addition, additional_data)

    def _tranform_enums(self, additional_data):
        for key, value in additional_data.items():
            if isinstance(value, Enum):
                additional_data[key] = value.value

        return additional_data
