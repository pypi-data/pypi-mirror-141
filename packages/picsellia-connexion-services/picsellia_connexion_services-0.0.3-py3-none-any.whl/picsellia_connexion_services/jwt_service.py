import json
from urllib.parse import urljoin, urlparse

import requests
from .abstract_service_connexion import AbstractServiceConnexion
from .utils import check_status_code

from .exceptions import NetworkError, UnauthorizedError


class JwtServiceConnexion(AbstractServiceConnexion):

    def __init__(self, host : str, jwt_identifier_data: dict ) -> None:
        """JwtServiceConnexion may be use to handle a JwtAuthentication connexion with a service.
        You need to give a jwt_identifier_data (as a dict) that will be send to the host to ensures validity of your request.
        This data will depend on service contacted. For example for a Deployment / Jwt request on Oracle, this will be :
        {
            "api_token" : <user_api_token>,
            "deployment_id" : <deployment_id>
        }
        """
        self.jwt_identifier_data = jwt_identifier_data
        self.host = urlparse(host)
        self.jwt, self.expires_in = self.generate_jwt()

    def wrapped_request(f):
        def decorated(self, *args, regenerate_jwt=True, **kwargs):
            try:
                resp = f(self, *args, **kwargs)
            except Exception:
                raise NetworkError("Server is not responding, please check your host.")
            
            if resp.status_code == 401:
                res = resp.json()
                if regenerate_jwt and "expired" in res and res["expired"]:
                    self.jwt, self.expires_in = self.generate_jwt()
                    return decorated(self, *args, regenerate_jwt=False, **kwargs)
                else:
                    raise UnauthorizedError("You are not authorized to do this.")
            else:
                check_status_code(resp)
                
            return resp
        return decorated


    def generate_jwt(self):
        url = "".join([self.host, '/login'])
        response = requests.post(url=url, data=json.dumps(self.jwt_identifier_data))
        if response.status_code == 200:
            try:
                response = response.json()
                return response["jwt"], response["expires"]
            except Exception:
                raise UnauthorizedError("Can't connect to Deployment service {}. Please contact support.".format(self))
        else:
            raise UnauthorizedError("Unauthorized action on the deployment services")
    
    def _build_headers(self):
        return { "Authorization": "Bearer {}".format(self.jwt)}

    @wrapped_request
    def get(self, path: str, data: dict = None, params: dict = None, stream=False):
        url = urljoin(self.host, path)
        return requests.get(url=url, data=data, headers=self._build_headers(), params=params, stream=stream)

    @wrapped_request
    def post(self, path: str, data: dict = None, params: dict = None):
        url = urljoin(self.host, path)
        return requests.post(url=url, data=data, headers=self._build_headers(), params=params)

    @wrapped_request
    def put(self, path: str, data: dict = None, params: dict = None):
        url = urljoin(self.host, path)
        return requests.put(url=url, data=data, headers=self._build_headers(), params=params)

    @wrapped_request
    def delete(self, path: str, data: dict = None, params: dict = None):
        url = urljoin(self.host, path)
        return requests.delete(url=url, data=data, headers=self._build_headers(), params=params)
