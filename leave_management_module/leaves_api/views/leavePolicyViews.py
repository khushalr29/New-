from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from shared.models.leave_management.leave_policies import LeavePolicy
from ..serializers.leavePolicySerializer import LeavePolicySerializer
from shared.utils.common.pagination import paginate_queryset
from shared.utils.response.handlers import ResponseHandler
from django.db.models import Q
from rest_framework import status

class LeavePolicyListView(APIView):
    def get(self, request):
        policy = LeavePolicy.active_objects.filter(company=request.user.company).order_by('-created_at')
        search = request.query_params.get('search')
        if search:
            policy = policy.filter(
                Q(policy_name__icontains=search)|
                Q(description__icontains=search)
            ).distinct()
        return paginate_queryset(policy, request, LeavePolicySerializer)
    
    def post(self,request):
        serializer = LeavePolicySerializer(data=request.data, context = {'request': request})
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success("Leave Policy", serializer.data)
        return ResponseHandler.create_failed(serializer.errors)
    
class LeavePolicyDetailsView(APIView):
    def get(self,request,id):
        policy = get_object_or_404(LeavePolicy.active_objects, id=id, company= request.user.company)
        serializer = LeavePolicySerializer(policy, context = {'request': request})
        return ResponseHandler.success(serializer.data)
    
    def put(self,request,id):
        policy = get_object_or_404(LeavePolicy.active_objects, id=id, company=request.user.company)
        serializer = LeavePolicySerializer(policy, data = request.data, context = {'request': request})
        if serializer.is_valid():
            serializer.save()
            return ResponseHandler.update_success("Leave Policy", serializer.data)
        return ResponseHandler.create_failed(serializer.errors)
    
    def patch(self, request, id):
        policy = get_object_or_404(LeavePolicy.active_objects, id=id, company=request.user.company)
        serializer = LeavePolicySerializer(policy, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return ResponseHandler.update_success("Leave Policy", serializer.data)
        return ResponseHandler.create_failed(serializer.errors)

    def delete(self,request,id):
        policy = get_object_or_404(LeavePolicy.active_objects, id=id, company=request.user.company)
        policy.delete()
        return ResponseHandler.delete_success("Leave Policy")