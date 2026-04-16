from django.db.models import Q
from rest_framework.views import APIView
from shared.models.hr_management.asset_manage import AssetType, Assets
from shared.models.core.useractivity import UserActivityLog
from ..serializers.assetManagementSerializer import AssetTypeSerializer, AssetSerializer, AssetListSerializer 
from shared.utils.response.handlers import ResponseHandler
from shared.utils.response.messages import ResponseMessages
from shared.utils.common.pagination import paginate_queryset
from shared.utils.common.centarlisedPermission import check_permissions
from shared.utils.errors.protectedErrors import check_references_and_get_deletable_instances
from django.shortcuts import get_object_or_404
from django.utils import timezone

class AssetTypeView(APIView):
    def get(self, request, id=None):
        if id:
            check_permissions(request, ['view_asset_type'])
            instance = get_object_or_404(AssetType, id=id, company=request.user.company)
            serializer = AssetTypeSerializer(instance)
            return ResponseHandler.success(serializer.data)

        check_permissions(request, ['list_asset_type'])
        paginate = request.query_params.get("paginate", "true")
        data = AssetType.objects.filter(company=request.user.company).order_by("-id")
        search = request.query_params.get("search")
        if search:
            data = data.filter(asset_type_name__icontains=search)
        status = request.query_params.get("status")
        if status:
            data = data.filter(status=status)
        if paginate == "false":
            serializer = AssetTypeSerializer(data, many=True)
            return ResponseHandler.list_success(serializer.data)
        return paginate_queryset(data, request, AssetTypeSerializer, view=self)

    def post(self, request):
        check_permissions(request, ['add_asset_type'])
        serializer = AssetTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success('asset_type')
        return ResponseHandler.create_failed(serializer.errors)

    def put(self, request, id=None):
        check_permissions(request, ['change_asset_type'])
        instance = get_object_or_404(AssetType, id=id, company=request.user.company)
        serializer = AssetTypeSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return ResponseHandler.update_success('asset_type')
        return ResponseHandler.update_failed(serializer.errors)

    def delete(self, request):
        check_permissions(request, ['delete_asset_type'])
        ids = request.data.get("ids", [])
        if not isinstance(ids, list) or not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)

        queryset = AssetType.objects.filter(id__in=ids, company=request.user.company)
        deletable_instances, reference_details = check_references_and_get_deletable_instances(AssetType, ids)

        if reference_details:
            return ResponseHandler.dependency_error(message=ResponseMessages.protected_error("asset_type"))

        queryset.update(deleted_at=timezone.now())
        return ResponseHandler.delete_success("asset_type")

class AssetView(APIView):
    def get(self, request, id=None):
        if id:
            check_permissions(request, ['view_assets'])
            instance = get_object_or_404(Assets, id=id, company=request.user.company)
            serializer = AssetListSerializer(instance)
            return ResponseHandler.success(serializer.data)

        check_permissions(request, ['list_assets'])
        paginate = request.query_params.get("paginate", "true")
        data = Assets.objects.filter(company=request.user.company).order_by("-id")
        search = request.query_params.get("search")
        if search:
            data = data.filter(Q(asset_code__icontains=search)|
            Q(asset_name__icontains = search) |
            Q(location__icontains = search)
            )
        asset_type  = request.query_params.get("asset_type")
        condition = request.query_params.get("condition")
        purchase_date_from = request.query_params.get("purchase_date_from")
        purchase_date_to = request.query_params.get("purchase_date_to")
        
        if asset_type:
            data = data.filter(asset_type__asset_type_name = asset_type)

        if condition:
            data = data.filter(condition=condition)

        if purchase_date_from:
            data = data.filter(purchase_date_from__gte = purchase_date_from)

        if purchase_date_to:
            data = data.filter(purchase_date_to__lte = purchase_date_to)                

        status = request.query_params.get("status")
        if status:
            data = data.filter(status=status)
        if paginate == "false":
            serializer = AssetListSerializer(data, many=True)
            return ResponseHandler.list_success(serializer.data)
        return paginate_queryset(data, request, AssetListSerializer, view=self)

    def post(self, request):
        check_permissions(request, ['add_assets'])
        serializer = AssetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success('assets')
        return ResponseHandler.create_failed(serializer.errors)

    def put(self, request, id=None):
        check_permissions(request, ['change_assets'])
        instance = get_object_or_404(Assets, id=id, company=request.user.company)
        serializer = AssetSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return ResponseHandler.update_success('assets')
        return ResponseHandler.update_failed(serializer.errors)

    def delete(self, request):
        check_permissions(request, ['delete_assets'])
        ids = request.data.get("ids", [])
        if not isinstance(ids, list) or not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)

        queryset = Assets.objects.filter(id__in=ids, company=request.user.company)
        deletable_instances, reference_details = check_references_and_get_deletable_instances(Assets, ids)

        if reference_details:
            return ResponseHandler.dependency_error(message=ResponseMessages.protected_error("assets"))

        queryset.update(deleted_at=timezone.now())
        return ResponseHandler.delete_success("assets")
    

