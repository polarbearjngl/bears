import allure
import requests
from json import JSONDecodeError
from requests import HTTPError
import logging
import logging.handlers
import contextlib
from http.client import HTTPConnection


class BaseApi(object):
    """Base API class."""

    def __init__(self, host, is_logger_enabled):
        """Base api class.

        Args:
            host: host for sending requests.
            is_logger_enabled: Flag for enable logger.
        """
        self.host = host
        self.is_logger_enabled = is_logger_enabled

    def _request(self, method, url, is_decode_to_json=True, params=None, headers=None, data=None, **kwargs):
        with self.request_to_log():
            resp = requests.request(method=method,
                                    url=url,
                                    params=params,
                                    headers=headers,
                                    data=data,
                                    **kwargs)

        try:
            resp.raise_for_status()
            if not is_decode_to_json:
                return resp

            content = resp.json()
            allure.attach(name='Response text', body=resp.text, attachment_type=allure.attachment_type.TEXT)
        except (HTTPError, JSONDecodeError) as error:
            raise AssertionError('There was an error. \n%s. \nResponse text was %s' % (error, resp.text))

        return content

    @staticmethod
    def debug_requests_start():
        """Switch on logging for requests"""
        HTTPConnection.debuglevel = 1

        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True

    @staticmethod
    def debug_requests_exit():
        """Switch off logging for requests"""
        HTTPConnection.debuglevel = 0

        root_logger = logging.getLogger()
        root_logger.setLevel(logging.WARNING)
        root_logger.handlers = []
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.WARNING)
        requests_log.propagate = False

    @contextlib.contextmanager
    def request_to_log(self):
        self.debug_requests_start() if self.is_logger_enabled else None
        yield
        self.debug_requests_exit() if self.is_logger_enabled else None
