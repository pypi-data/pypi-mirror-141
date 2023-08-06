import logging

from beartype import beartype

from .exceptions import (ForbiddenError, InvalidQueryError, PicselliaError,
                         ResourceConflictError, ResourceNotFoundError,
                         UnauthorizedError, UnsufficientRessourcesError)

logger = logging.getLogger('picsellia-service-connexion')


@beartype
def check_status_code(response):
    status = int(response.status_code)
    if status in [200, 201, 202, 203]:
        try:
            response_data = response.json()
            if "success" in response_data:
                logger.debug(response_data["success"])
            if "unknown" in response_data:
                logger.warning("Some data could not be used {}".format(response_data["unknown"]))
        except Exception as e:
            logger.debug('Service has returned a {} but response could not be parsed because {}.'.format(response.status_code, str(e)))
        return
    elif status == 204:
        logger.debug('Resource deleted.')
        return
    elif status in [208, 400, 401, 402, 403, 404, 409, 500]:
        try:
            response_data = response.json()
            if "error" in response_data:
                message = response_data["error"]
            else:
                message = response.url
        except Exception as e:
            message = ""
            logger.warning('Platform has returned a {} and response could not be parsed because {}.'
                           .format(response.status_code, str(e)))

        if status == 208:
            raise PicselliaError("An object has already this name in S3.")
        if status == 400:
            raise InvalidQueryError("Invalid query : {}".format(message))
        if status == 401:
            raise UnauthorizedError("Unauthorized : {}".format(message))
        if status == 402:
            raise UnsufficientRessourcesError("{}".format(message))
        if status == 403:
            raise ForbiddenError("Forbidden : {}".format(message))
        if status == 404:
            raise ResourceNotFoundError("Not found : {}".format(message))
        if status == 409:
            raise ResourceConflictError("This resouce already exists : {}".format(message))
        if status == 500:
            raise PicselliaError("Internal server error. Please contact support. {}".format(message))
    else:
        raise Exception("Unknown error (Status code : {}), please contact support".format(response.status_code))
