from rest_framework.views import APIView
from rest_framework import status
from shared.models.leave_management.leave_application import LeaveApplication
from ..serializers.leaveApplicationSerializer import LeaveApplicationSerializer
from shared.utils.response.handlers import ResponseHandler
from django.shortcuts import get_object_or_404
from django.db.models import Q
from shared.utils.common.pagination import paginate_queryset

class LeaveApplicationListView(APIView):
    def get(self,request):
        application = LeaveApplication.active_objects.filter(company= request.user.company).order_by('-created_at')
        params = ['leave_type', 'start_date', 'end_date', 'status']
        for param in params:
            if param in request.query_params:
                value = request.query_params.get(param)
                if param == 'status':
                    application = application.filter(status__iexact=value)
                else:
                    application = application.filter(**{param: value})
        return paginate_queryset(application, request, LeaveApplicationSerializer)
    
    def post(self, request):
        serializer = LeaveApplicationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Link the application to the current user's employee profile
            serializer.save(company=request.user.company, employee=request.user.employee_profile)
            return ResponseHandler.create_success("Leave_application", serializer.data)
        return ResponseHandler.create_failed(serializer.errors)
    
class LeaveApplicationDetailsView(APIView):
    def get(self,request,id):
        application = get_object_or_404(LeaveApplication.active_objects, id=id, company=request.user.company)
        serializer= LeaveApplicationSerializer(application, context={'request': request})
        return ResponseHandler.success(serializer.data)
    
    def put(self,request,id):
        application = get_object_or_404(LeaveApplication.active_objects, id=id, company = request.user.company)
        serializer = LeaveApplicationSerializer(application, data = request.data , context = {'request':request})
        if serializer.is_valid():
            serializer.save()
            return ResponseHandler.update_success("Leave_application",serializer.data)
        return ResponseHandler.create_failed(serializer.errors)
    
    def patch(self,request,id):
        application = get_object_or_404(LeaveApplication.active_objects, id = id, company = request.user.company)
        serializer = LeaveApplicationSerializer(application, data = request.data, partial = True, context = {'request': request})
        if serializer.is_valid():
            serializer.save()
            return ResponseHandler.update_success("leave_application", serializer.data)
        return ResponseHandler.create_failed(serializer.errors)
    
    def delete(self,request,id):
        application = get_object_or_404(LeaveApplication.active_objects,id=id, company = request.user.company)
        application.delete()
        return ResponseHandler.delete_success("Leave_application")
    
      