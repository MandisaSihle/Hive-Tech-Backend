from rest_framework.response import Response

def error_response(message="An error occurred", status_code=400):
    return Response({
        "success": False,
        "message": message
    }, status=status_code)