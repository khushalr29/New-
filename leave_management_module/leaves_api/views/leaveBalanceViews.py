from rest_framework.views import APIView
from shared.models.leave_management.leave_balances import LeaveBalance
from ..serializers.leaveBalanceSerializer import LeaveBalanceSerializer
from django.shortcuts import get_object_or_404
from django.db.models import Q
from shared.utils.response.handlers import ResponseHandler
from shared.utils.common.pagination import paginate_queryset

class LeaveBalanceListView(APIView):
    def get(self, request):
        balance = LeaveBalance.active_objects.filter(company=request.user.company).order_by('-created_at')
        search = request.query_params.get('search')
        if search:
            balance = balance.filter(
                Q(leave_type__name__icontains=search)|
                Q(employee__full_name__icontains=search)
            ).distinct()
        return paginate_queryset(balance, request, LeaveBalanceSerializer)
    
    def post(self, request):
        serializer = LeaveBalanceSerializer(data=request.data, context = {'request': request})
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success("Leave balance", serializer.data)
        return ResponseHandler.create_failed(serializer.errors)
    
class LeaveBalanceDetailsView(APIView):
    def get(self,request,id):
        balance = get_object_or_404(LeaveBalance.active_objects, id=id, company=request.user.company)
        serializer = LeaveBalanceSerializer(balance, context = {'request': request})
        return ResponseHandler.success(serializer.data)
    
    def put(self,request,id):
        balance = get_object_or_404(LeaveBalance.active_objects, id=id, company = request.user.company)
        serializer = LeaveBalanceSerializer(balance, data = request.data, context = {'request': request})
        if serializer.is_valid():
            serializer.save()
            return ResponseHandler.update_success("Leave balance", serializer.data)
        return ResponseHandler.create_failed(serializer.errors)
    
    def patch(self,request,id):
        balance = get_object_or_404(LeaveBalance.active_objects, id=id, company=request.user.company)
        serializer = LeaveBalanceSerializer(balance, data = request.data, partial = True, context = {'request': request})
        if serializer.is_valid():
            serializer.save()
            return ResponseHandler.update_success("Leave_balance", serializer.data)
        return ResponseHandler.create_failed(serializer.errors)
    
    def delete(self,request,id):
        balance = get_object_or_404(LeaveBalance.active_objects, id=id, company = request.user.company)
        balance.delete()
        return ResponseHandler.delete_success("Leave_balance")
    