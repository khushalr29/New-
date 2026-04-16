from django.db.models import Q
from rest_framework.views import APIView
from shared.models.hr_management import Promotion
from shared.models.core.useractivity import UserActivityLog
from ..serializers.promotionsSerializer import PromotionSerializer, PromotionListSerializer
from shared.utils.response.handlers import ResponseHandler
from shared.utils.response.messages import ResponseMessages
from shared.utils.common.pagination import paginate_queryset
from shared.utils.common.centarlisedPermission import check_permissions
from shared.utils.errors.protectedErrors import check_references_and_get_deletable_instances
from django.shortcuts import get_object_or_404
from django.utils import timezone

class PromotionsView(APIView):
    def get(self, request, id=None):
        if id:
            check_permissions(request, ['view_promotions'])
            instance = get_object_or_404(Promotion, id=id, company=request.user.company)
            serializer = PromotionListSerializer(instance)
            return ResponseHandler.success(serializer.data)

        check_permissions(request, ['list_promotions'])
        paginate = request.query_params.get("paginate", "true")
        data = Promotion.objects.filter(company=request.user.company).order_by("-id")
        search = request.query_params.get("search")
        if search:
            data = data.filter(Q(old_designation__name__icontains=search)|
            Q(new_designation__name__icontains=search)|
            Q(description__icontains=search)|
            Q(employee__full_name__icontains=search)|
            Q(reason_for_promotion__icontains=search))

        if employee := request.query_params.get("employee"):
            data = data.filter(employee__full_name=employee)
        if designation := request.query_params.get("designation"):
            data = data.filter(Q(old_designation__name=designation)|Q(new_designation__name=designation))
        
        if start_date := request.query_params.get("start_date"):
            data = data.filter(promotion_date__gte=start_date)
        if end_date := request.query_params.get("end_date"):
            data = data.filter(promotion_date__lte=end_date)

        status = request.query_params.get("status")
        if status:
            data = data.filter(status=status)

        if paginate == "false":
            serializer = PromotionListSerializer(data, many=True)
            return ResponseHandler.list_success(serializer.data)
        return paginate_queryset(data, request, PromotionListSerializer, view=self)

    def post(self, request):
        check_permissions(request, ['add_promotions'])
        serializer = PromotionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success('promotions')
        return ResponseHandler.create_failed(serializer.errors)

    def put(self, request, id=None):
        check_permissions(request, ['change_promotions'])
        instance = get_object_or_404(Promotion, id=id, company=request.user.company)
        serializer = PromotionSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return ResponseHandler.update_success('promotions')
        return ResponseHandler.update_failed(serializer.errors)

    def delete(self, request):
        check_permissions(request, ['delete_promotions'])
        ids = request.data.get("ids", [])
        if not isinstance(ids, list) or not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)
            
        queryset = Promotion.objects.filter(id__in=ids, company=request.user.company)
        deletable_instances, reference_details = check_references_and_get_deletable_instances(Promotion, ids)

        if reference_details:
            return ResponseHandler.dependency_error(message=ResponseMessages.protected_error("promotions"))

        queryset.update(deleted_at=timezone.now())
        return ResponseHandler.delete_success("promotions")
