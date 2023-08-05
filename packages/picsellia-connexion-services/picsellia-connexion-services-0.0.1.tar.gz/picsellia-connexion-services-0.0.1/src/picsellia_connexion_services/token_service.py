from urllib.parse import urljoin, urlparse

import requests

from picsellia_connexion_services import exceptions

from .abstract_service_connexion import AbstractServiceConnexion
from .utils import check_status_code


class TokenServiceConnexion(AbstractServiceConnexion):

    def __init__(self, host : str, api_token : str) -> None:
        """TokenServiceConnexion may be use to handle a Token authentication connexion with a service.
        You need to give an api token valid, recognized by the service called
        """
        self.host = urlparse(host)
        self.api_token = api_token
        self.content_type = "application/json"
        self.headers = {"Authorization": "Token " + api_token, "Content-type": self.content_type}

    def wrapped_request(f):
        def decorated(*args, **kwargs):
            try:
                resp = f(*args, **kwargs)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host.")
            check_status_code(resp)
            return resp

        return decorated

    @wrapped_request
    def get(self, path: str, data: dict = None, params: dict = None, stream=False):
        url = urljoin(self.host, path)
        return requests.get(url=url, data=data, headers=self.headers, params=params, stream=stream)

    @wrapped_request
    def post(self, path: str, data: dict = None, params: dict = None):
        url = urljoin(self.host, path)
        return requests.post(url=url, data=data, headers=self.headers, params=params)

    @wrapped_request
    def put(self, path: str, data: dict = None, params: dict = None):
        url = urljoin(self.host, path)
        return requests.put(url=url, data=data, headers=self.headers, params=params)

    @wrapped_request
    def delete(self, path: str, data: dict = None, params: dict = None):
        url = urljoin(self.host, path)
        return requests.delete(url=url, data=data, headers=self.headers, params=params)
