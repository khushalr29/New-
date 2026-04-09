from rest_framework.views import APIView
from django.db.models import Q
from shared.models.contract_management.contract_template import ContractTemplate
from ..serializers.contracttTemplateserializer import ContractTemplateSerializer
from shared.utils.common.pagination import paginate_queryset
from shared.utils.response.handlers import ResponseHandler
from django.shortcuts import get_object_or_404

class ContractTemplateListView(APIView):
    def get(self, request):
        templates = ContractTemplate.active_objects.filter(company=request.user.company).order_by('-created_at')
        
        search_query = request.query_params.get('search')
        if search_query:
            templates = templates.filter(
                Q(template_name__icontains=search_query) |
                Q(subject__icontains=search_query)
            )
        
        return paginate_queryset(templates, request, serializer_class=ContractTemplateSerializer, view=self)

    def post(self, request):
        serializer = ContractTemplateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success("Contract template", serializer.data)
        return ResponseHandler.create_failed(serializer.errors)

class ContractTemplateDetailView(APIView):
    def get_object(self, id, company):
        try:
            return ContractTemplate.active_objects.get(pk=id, company=company)
        except ContractTemplate.DoesNotExist:
            return None

    def get(self, request, id):
        instance = self.get_object(id, request.user.company)
        if not instance:
            return ResponseHandler.not_found_error()
        serializer = ContractTemplateSerializer(instance, context={'request': request})
        return ResponseHandler.success(serializer.data)

    def put(self, request, id):
        instance = self.get_object(id, request.user.company)
        if not instance:
            return ResponseHandler.not_found_error()
        serializer = ContractTemplateSerializer(instance, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return ResponseHandler.update_success("Contract template", serializer.data)
        return ResponseHandler.create_failed(serializer.errors)

    def delete(self, request, id):
        instance = self.get_object(id, request.user.company)
        if not instance:
            return ResponseHandler.not_found_error()
        instance.delete()
        return ResponseHandler.delete_success("Contract template")

