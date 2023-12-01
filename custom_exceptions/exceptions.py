from rest_framework.exceptions import APIException

class Exception500(APIException):
    status_code = 500
class Exception400(APIException):
    status_code = 400

class Exception409(APIException):
    status_code = 409

class Exception404(APIException):
    status_code = 404

class Exception204(APIException):
    status_code = 204

class Exception200(APIException):
    status_code = 200


