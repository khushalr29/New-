from rest_framework.views import APIView
from django.db.models import Q
from shared.models.contract_management.contract_type import ContractType
from ..serializers.contractTypeserializer import ContractTypeSerializer
from shared.utils.common.pagination import paginate_queryset
from shared.utils.response.handlers import ResponseHandler

class ContractTypeListView(APIView):
    def get(self, request):
        types = ContractType.active_objects.filter(company=request.user.company).order_by('name')
        search_query = request.query_params.get('search')
        if search_query:
            types = types.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            ).distinct()
        return paginate_queryset(types, request, ContractTypeSerializer)

    def post(self, request):
        serializer = ContractTypeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success("Contract type", serializer.data)
        return ResponseHandler.create_failed(serializer.errors)

class ContractTypeDetailView(APIView):
    def get_object(self, id, company):
        try:
            return ContractType.active_objects.get(pk=id, company=company)
        except ContractType.DoesNotExist:
            return None

    def get(self, request, id):
        instance = self.get_object(id, request.user.company)
        if not instance:
            return ResponseHandler.not_found_error()
        serializer = ContractTypeSerializer(instance, context={'request': request})
        return ResponseHandler.success(serializer.data)

    def put(self, request, id):
        instance = self.get_object(id, request.user.company)
        if not instance:
            return ResponseHandler.not_found_error()
        serializer = ContractTypeSerializer(instance, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return ResponseHandler.update_success("Contract type", serializer.data)
        return ResponseHandler.create_failed(serializer.errors)

    def delete(self, request, id):
        instance = self.get_object(id, request.user.company)
        if not instance:
            return ResponseHandler.not_found_error()
        instance.delete()
        return ResponseHandler.delete_success("Contract type")