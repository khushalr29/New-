import logging
from ..errors import flatten_errors
from rest_framework import status
from django.http import JsonResponse
from .messages import ResponseMessages
from jsonschema import ValidationError
from rest_framework.response import Response


logger = logging.getLogger(__name__)

class HttpResponseCode:
    OK = status.HTTP_200_OK
    CREATED = status.HTTP_201_CREATED
    BAD_REQUEST = status.HTTP_400_BAD_REQUEST
    NOT_FOUND = status.HTTP_404_NOT_FOUND
    MULTI_STATUS = status.HTTP_207_MULTI_STATUS
    SERVER_ERROR = status.HTTP_500_INTERNAL_SERVER_ERROR
    UNAUTHORIZED = status.HTTP_401_UNAUTHORIZED
    FORBIDDEN = status.HTTP_403_FORBIDDEN
    TOO_MANY_REQUESTS = status.HTTP_429_TOO_MANY_REQUESTS
    CONFLICT = status.HTTP_409_CONFLICT

class ResponseHandler:
    @staticmethod
    def log_response(success: bool, message: str):
        logger.debug(f"HTTP_RESPONSE:: success: {success}, message: {message}")

    @staticmethod
    def success(response_data=None, message=ResponseMessages.SUCCESS):
        ResponseHandler.log_response(success=True, message=message)
        return Response({
            "success": True,
            "data": response_data,
            "message": message
        }, status=HttpResponseCode.OK)

    @staticmethod
    def warn(response_data=None, message=ResponseMessages.WARNING):
        ResponseHandler.log_response(success=False, message=message)
        return Response({
            "success": False,
            "data": response_data,
            "message": message
        }, status=HttpResponseCode.OK)

    @staticmethod
    def bad_request(response_data=None, message=ResponseMessages.BAD_REQUEST):
        ResponseHandler.log_response(success=False, message=message)
        return Response({
            "success": False,
            "data": response_data,
            "message": message
        }, status=HttpResponseCode.BAD_REQUEST)

    @staticmethod
    def unauthorized(response_data=None, message=ResponseMessages.UNAUTHORIZED):
        ResponseHandler.log_response(success=False, message=message)
        return Response({
            "success": False,
            "data": response_data,
            "message": message
        }, status=HttpResponseCode.UNAUTHORIZED)

    @staticmethod
    def forbidden(response_data=None, message=ResponseMessages.FORBIDDEN):
        ResponseHandler.log_response(success=False, message=message)
        return Response({
            "success": False,
            "data": response_data,
            "message": message
        }, status=HttpResponseCode.FORBIDDEN)

    @staticmethod
    def not_found(response_data=None, message=ResponseMessages.NOT_FOUND):
        ResponseHandler.log_response(success=False, message=message)
        return Response({
            "success": False,
            "data": response_data,
            "message": message
        }, status=HttpResponseCode.NOT_FOUND)

    @staticmethod
    def too_many_requests(message=ResponseMessages.TOO_MANY_REQUESTS):
        ResponseHandler.log_response(success=False, message=message)

        return JsonResponse({
            "success": False,
            "message": message
        }, status=HttpResponseCode.TOO_MANY_REQUESTS)

    @staticmethod
    def server_error(response_data=None, message=ResponseMessages.SERVER_ERROR, err=None):
        if err:
            logger.error("Server error", exc_info=err)
        ResponseHandler.log_response(success=False, message=message)
        return Response({
            "success": False,
            "data": response_data,
            "message": message
        }, status=HttpResponseCode.SERVER_ERROR)

    @staticmethod
    def create_success(name: str, response_data: dict = None):
        message = ResponseMessages.create_success_message(name)
        ResponseHandler.log_response(success=True, message=message)
        response_body = {
            "success": True,
            "message": message
        }
        if response_data is not None:
            response_body["data"] = response_data

        return Response(response_body, status=HttpResponseCode.CREATED)

    @staticmethod
    def create_failed(errors=None, message=None):
        if isinstance(errors, dict):
            flat_errors = flatten_errors(errors)
            combined_message = " ".join(flat_errors)
        elif isinstance(errors, list):
            combined_message = " ".join(str(e) for e in errors)
        elif isinstance(errors, str):
            combined_message = errors
        else:
            combined_message = "An unknown error occurred."
        if message:
            combined_message = f"{message}. {combined_message}"

        ResponseHandler.log_response(success=False, message=combined_message)
        return Response({
            "success": False,
            "errors": combined_message
        }, status=HttpResponseCode.BAD_REQUEST)
    @staticmethod
    def update_success(name: str, response_data: dict = None):
        message = ResponseMessages.update_success_message(name)
        ResponseHandler.log_response(success=True, message=message)
        response_body = {
            "success": True,
            "message": message
        }
        if response_data is not None:
            response_body["data"] = response_data
        return Response(response_body, status=HttpResponseCode.OK)

    @staticmethod
    def update_failed(errors=None):
        flat_errors = flatten_errors(errors)
        combined_message = " ".join(flat_errors)
        ResponseHandler.log_response(success=False, message="Validation failed")
        return Response({
            "success": False,
            "errors": combined_message
        }, status=HttpResponseCode.BAD_REQUEST)

    @staticmethod
    def not_found_error():
        message = ResponseMessages.NOT_FOUND
        ResponseHandler.log_response(success=False, message=message)
        return Response({
            "success": False,
            "message": message
        }, status=HttpResponseCode.NOT_FOUND)

    @staticmethod
    def delete_success(name: str):
        message = f"{name} deleted successfully"
        ResponseHandler.log_response(success=True, message=message)
        return Response({
            "success": True,
            "message": message
        }, status=HttpResponseCode.OK)

    @staticmethod
    def partial_delete(data: any):
        message = ResponseMessages.partial_delete_message(data)
        ResponseHandler.log_response(success=False, message=message)
        return Response({
            "success": False,
            "message": message,
            "data": data
        }, status=HttpResponseCode.MULTI_STATUS)

    @staticmethod
    def none_deleted(data: any):
        message = ResponseMessages.none_deleted_message(data)
        ResponseHandler.log_response(success=False, message=message)
        return Response({
            "success": False,
            "message": message,
            "data": data
        }, status=HttpResponseCode.BAD_REQUEST)

    @staticmethod
    def validation_error(exc):
        if isinstance(exc, ValidationError):
            if isinstance(exc.detail, str):
                return Response({"success": False, "errors": exc.detail}, status=status.HTTP_400_BAD_REQUEST)
            elif isinstance(exc.detail, list) and exc.detail:
                return Response({"success": False, "errors": str(exc.detail[0])}, status=status.HTTP_400_BAD_REQUEST)
            elif isinstance(exc.detail, dict):
                val = exc.detail.get("non_field_errors")
                if val:
                    return Response({"success": False, "errors": str(val[0])}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"success": False, "errors": "Validation failed"}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def unexpected_error(error: Exception):
        message = ResponseMessages.UNEXPECTED_ERROR
        logger.error("Unexpected error occurred", exc_info=error)
        ResponseHandler.log_response(success=False, message=message)
        return Response({
            "success": False,
            "message": message,
            "error": str(error)
        }, status=HttpResponseCode.SERVER_ERROR)

    @staticmethod
    def no_matching_data():
        message = ResponseMessages.NO_MATCHING_DATA
        ResponseHandler.log_response(success=False, message=message)
        return Response({
            "success": False,
            "message": message
        }, status=HttpResponseCode.BAD_REQUEST)

    @staticmethod
    def doctor_not_found():
        message = ResponseMessages.DOCTOR_NOT_FOUND
        ResponseHandler.log_response(success=False, message=message)
        return Response({
            "success": False,
            "message": message
        }, status=HttpResponseCode.NOT_FOUND)

    @staticmethod
    def list_success(data: any):
        message = ResponseMessages.DATA_FETCH_SUCCESS
        ResponseHandler.log_response(success=True, message=message)
        return Response({
            "success": True,
            "data": data,
            "message": message
        }, status=HttpResponseCode.OK)

    @staticmethod
    def list_failed(error: any):
        message = ResponseMessages.DATA_FETCH_FAILED.format(error=error)
        ResponseHandler.log_response(success=False, message=message)
        return Response({
            "success": False,
            "message": message
        }, status=HttpResponseCode.BAD_REQUEST)
    
    @staticmethod
    def json_unauthorized(message=None):
        return JsonResponse({
            'success': False,
            'error': message or 'Unauthorized'},
            status=HttpResponseCode.UNAUTHORIZED,
            json_dumps_params={'indent': 4})

    @staticmethod
    def json_forbidden(message=None):
        return JsonResponse({
            'success': False,
            'error': message or 'Forbidden'
            },status=HttpResponseCode.FORBIDDEN,)
    
    @staticmethod
    def dependency_error(message):
        return Response({'success': False, 'message': message}, status=HttpResponseCode.CONFLICT)
    
    @staticmethod
    def json_rate_limited(message=ResponseMessages.TOO_MANY_REQUESTS, data=None):
        response_data = {
            'success': False,
            'message': message
        }
        if data:
            response_data.update(data)
        
        return JsonResponse(response_data, status=HttpResponseCode.TOO_MANY_REQUESTS)
    
    @staticmethod
    def already_exists(name: str):
        message = ResponseMessages.already_exists(name)
        ResponseHandler.log_response(success=True, message=message)
        return Response({
            "success": True,
            "message": message
        }, status=HttpResponseCode.CONFLICT)