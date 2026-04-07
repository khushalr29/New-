from shared.models import Employee
from rest_framework.views import APIView
from rest_framework.response import Response
from shared.utils.response import ResponseHandler, ResponseMessages

class SessionUserTypeView(APIView):
    def get(self, request):
        try:
            # Employee profile is linked via OneToOneField to User
            employee = Employee.objects.get(user=request.user)
            return Response({'employment_type': employee.employment_type})
        
        except Employee.DoesNotExist:
            return ResponseHandler.not_found(
                message=ResponseMessages.STAFF_NOT_FOUND
            )
