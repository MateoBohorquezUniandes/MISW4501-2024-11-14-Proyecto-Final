from seedwork.presentation.exceptions import APIError
from flask import Response

def api_custom_exception_handler(error: APIError) -> Response:
    """
    Funtion for handling API from request processing.

    Args:
        error (BaseAPIError): Custom API error to handle

    Returns:
        Response: HTTP response with corresponding API status code
    """
    return Response(status=error.code)