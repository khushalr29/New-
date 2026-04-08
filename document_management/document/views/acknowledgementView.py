from django.db.models import Q
from rest_framework.views import APIView
from shared.models import Acknowledgement, UserActivityLog
from ..serializers.acknowledgementSerializer import AcknowledgementSerializer, AcknowledgementListSerializer
from shared.utils.response.handlers import ResponseHandler
from shared.utils.response.messages import ResponseMessages
from shared.utils.common.pagination import paginate_queryset
from shared.utils.common.centarlisedPermission import check_permissions
from shared.logs.decorators import log_activity
from shared.utils.errors.protectedErrors import check_references_and_get_deletable_instances
from django.shortcuts import get_object_or_404
from django.utils import timezone

class AcknowledgementView(APIView):
    def get(self, request, pk=None):
        if pk:
            check_permissions(request, ['view_acknowledgement'])
            instance = get_object_or_404(Acknowledgement, id=pk)
            serializer = AcknowledgementListSerializer(instance)
            return ResponseHandler.success(serializer.data)
        
        check_permissions(request, ['list_acknowledgement'])
        paginate = request.query_params.get("paginate", "true")
        # Acknowledgement model doesn't have company field in model definition I saw earlier?
        # Let's check shared/shared/models/document_managements/acknowledgement.py again.
        # Wait, I checked it in Step 662. It DOES NOT inherit from TenantModel.
        data = Acknowledgement.objects.all().order_by("-id")
        
        search = request.query_params.get("search")
        if search:
            data = data.filter(Q(document__document_title__icontains=search) | Q(user__full_name__icontains=search))
    
        if paginate == "false":
            serializer = AcknowledgementListSerializer(data, many=True)
            return ResponseHandler.list_success(serializer.data)
        return paginate_queryset(data, request, AcknowledgementListSerializer, view=self)

    @log_activity(UserActivityLog.CREATE, 'Acknowledgement')
    def post(self, request):
        check_permissions(request, ['add_acknowledgement'])
        serializer = AcknowledgementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ResponseHandler.create_success('Acknowledgement')
        return ResponseHandler.create_failed(serializer.errors)

    @log_activity(UserActivityLog.UPDATE, 'Acknowledgement')
    def put(self, request, pk=None):
        check_permissions(request, ['change_acknowledgement'])
        instance = get_object_or_404(Acknowledgement, id=pk)
        serializer = AcknowledgementSerializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return ResponseHandler.update_success('Acknowledgement')
        return ResponseHandler.update_failed(serializer.errors)

    @log_activity(UserActivityLog.DELETE, 'Acknowledgement')
    def delete(self, request):
        check_permissions(request, ['delete_acknowledgement'])
        ids = request.data.get("ids", [])
        if not isinstance(ids, list) or not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)
        
        queryset = Acknowledgement.objects.filter(id__in=ids)
        queryset.delete() # Acknowledgement model doesn't have deleted_at either.
        return ResponseHandler.delete_success("Acknowledgement")
