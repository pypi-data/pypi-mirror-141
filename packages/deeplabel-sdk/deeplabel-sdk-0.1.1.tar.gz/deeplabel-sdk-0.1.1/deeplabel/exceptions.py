import functools
from logging import getLogger
logger = getLogger(__name__)
# Root Exception Class for all Deeplabel related Exceptions
class DeeplabelException(Exception):...


class InvalidCredentials(DeeplabelException):...


# Error representing invalid Id for any or detectionId,VideoId,GraphId,NodeId,EdgeId,etc
class InvalidIdError(DeeplabelException):...


# If an api returns response_code > 200
class InvalidAPIResponse(DeeplabelException):...

# VideoUrl doesn't exist anymore
class DownloadFailed(DeeplabelException):...


# Raise when you need to raise value error but handle gracefully since it's client facing
class DeeplabelValueError(DeeplabelException):...


def handle_deeplabel_exceptions(default_factory):
    """Run the func and catch DeeplabelExceptions, and return a default output
    Decorate functions that run in multiprocessing, to process videos/galleries/etc
    in parallel, so that they can be gracefully handled to return some default value
    """
    def caller(func):
        @functools.wraps(func)
        def inner(*args,**kwargs):
            try:
                return func(*args, **kwargs)
            except DeeplabelException as e:
                logger.error(e)
                logger.debug(e, exc_info=True)
                return default_factory()
        return inner
    return caller