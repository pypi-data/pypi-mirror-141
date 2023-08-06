from typing import Any, List

from .exceptions import UndefinedNextMockedResponse

from .abstract_service_connexion import AbstractServiceConnexion


class MockedServiceConnexion(AbstractServiceConnexion):

    def __init__(self) -> None:
        self.next_responses = {}
        self.next_responses["get"] = {}
        self.next_responses["post"] = {}
        self.next_responses["put"] = {}
        self.next_responses["delete"] = {}
    
    def reset_response(self, method : str, path : str):
       del self.next_responses[method][path]

    def set_next_mocked_response(self, method : str, path : str, response : Any):
        assert not type(response, list), "Can't set_next_mocked_response with a List. Use set_next_mocked_responses if you want multiple response"
        self.next_responses[method][path] = response

    def set_next_mocked_responses(self, method : str, path : str, responses : List[Any]):
        self.next_responses[method][path] = responses

    def wrapped_request(f):
        def decorated(self : 'MockedServiceConnexion', *args, **kwargs):
            method = f.__name__
            path = kwargs["path"]
            if path not in self.next_responses[method] or self.next_responses[method][path] == None:
                raise UndefinedNextMockedResponse("Path {} with method {} was not ready to receive this request".format(path, method))
            
            resp = f(self, *args, **kwargs)
            self.reset_response(method, path)
            return resp
        return decorated

    @wrapped_request
    def get(self, path: str, data: dict = None, params: dict = None, stream=False):
        return self.next_responses["get"][path]

    @wrapped_request
    def post(self, path: str, data: dict = None, params: dict = None):
        return self.next_responses["post"][path]

    @wrapped_request
    def put(self, path: str, data: dict = None, params: dict = None):
        return self.next_responses["put"][path]

    @wrapped_request
    def delete(self, path: str, data: dict = None, params: dict = None):
        return self.next_responses["delete"][path]

    def assert_no_more_request(self):
        assert self.next_responses["get"] == {}, "One of the get request was not called : {}".format(self.next_responses["get"])
        assert self.next_responses["post"] == {}, "One of the post request was not called : {}".format(self.next_responses["post"])
        assert self.next_responses["put"] == {}, "One of the put request was not called : {}".format(self.next_responses["put"])
        assert self.next_responses["delete"] == {}, "One of the delete request was not called : {}".format(self.next_responses["delete"])
