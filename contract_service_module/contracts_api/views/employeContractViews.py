from rest_framework.views import APIView
from django.db.models import Q
from shared.models.contract_management.employee_contract import EmployeeContract
from ..serializers.employeContractserializer import EmployeeContractSerializer
from shared.utils.common.pagination import paginate_queryset
from shared.utils.response.handlers import ResponseHandler

class EmployeeContractListView(APIView):
    def get(self, request):
        contracts = EmployeeContract.active_objects.filter(company=request.user.company).order_by('-start_date')
        
        employee = request.query_params.get('employee')
        if employee:
            contracts = contracts.filter(employee_id=employee)
        
        contract_type = request.query_params.get('type')
        if contract_type:
            contracts = contracts.filter(contract_type_id=contract_type)

        return paginate_queryset(contracts, request, EmployeeContractSerializer)

    def post(self, request):
        serializer = EmployeeContractSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            start_date = serializer.validated_data.get('start_date')
            end_date = serializer.validated_data.get('end_date')
            if start_date and end_date and start_date >= end_date:
                return ResponseHandler.create_failed(message="End date must be after start date.")
                
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success("Employee contract", serializer.data)
        return ResponseHandler.create_failed(serializer.errors)

class EmployeeContractDetailView(APIView):
    def get_object(self, id, company):
        try:
            return EmployeeContract.active_objects.get(pk=id, company=company)
        except EmployeeContract.DoesNotExist:
            return None

    def get(self, request, id):
        instance = self.get_object(id, request.user.company)
        if not instance:
            return ResponseHandler.not_found_error()
        serializer = EmployeeContractSerializer(instance, context={'request': request})
        return ResponseHandler.success(serializer.data)

    def put(self, request, id):
        instance = self.get_object(id, request.user.company)
        if not instance:
            return ResponseHandler.not_found_error()
        serializer = EmployeeContractSerializer(instance, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return ResponseHandler.update_success("Employee contract", serializer.data)
        return ResponseHandler.create_failed(serializer.errors)

    def delete(self, request, id):
        instance = self.get_object(id, request.user.company)
        if not instance:
            return ResponseHandler.not_found_error()
        instance.delete()
        return ResponseHandler.delete_success("Employee contract")