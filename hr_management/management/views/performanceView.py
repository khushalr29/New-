from django.db.models import Q
from rest_framework.views import APIView
from shared.models.hr_management import IndicatorCategory,Indicator,GoalType,EmployeeGoal,ReviewCycle,EmployeeReview
from shared.models.core.useractivity import UserActivityLog
from ..serializers.performanceSerializer import (
IndicatorCategorySerializer,IndicatorCategoryListSerializer,
IndicatorSerializer,IndicatorListSerializer,
GoalTypeSerializer,GoalTypeListSerializer,
EmployeeGoalSerializer,EmployeeGoalListSerializer,
ReviewCycleSerializer,ReviewCycleListSerializer,
EmployeeReviewSerializer,EmployeeReviewListSerializer)
from shared.utils.response.handlers import ResponseHandler
from shared.utils.response.messages import ResponseMessages
from shared.utils.common.pagination import paginate_queryset
from shared.utils.common.centarlisedPermission import check_permissions
from shared.utils.errors.protectedErrors import check_references_and_get_deletable_instances
from django.shortcuts import get_object_or_404
from django.utils import timezone

class IndicatorCategoryView(APIView):
    def get(self, request, id=None):
        if id:
            check_permissions(request, ['view_indicator_category'])
            instance = get_object_or_404(IndicatorCategory, id=id, company=request.user.company)
            serializer = IndicatorCategoryListSerializer(instance)
            return ResponseHandler.success(serializer.data)

        check_permissions(request, ['list_indicator_category'])
        paginate = request.query_params.get("paginate", "true")
        data = IndicatorCategory.objects.filter(company=request.user.company).order_by("-id")
        
        if search := request.query_params.get("search"):
            data = data.filter(category_name__icontains=search)

        if status :=request.query_params.get("status"):
            data = data.filter(status=status)

        if paginate == "false":
            serializer = IndicatorCategoryListSerializer(data, many=True)
            return ResponseHandler.list_success(serializer.data)
        return paginate_queryset(data, request, IndicatorCategoryListSerializer, view=self)

    def post(self, request):
        check_permissions(request, ['add_indicator_category'])
        serializer = IndicatorCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success('indicator_category')
        return ResponseHandler.create_failed(serializer.errors)

    def put(self, request, id=None):
        check_permissions(request, ['change_indicator_category'])
        instance = get_object_or_404(IndicatorCategory, id=id, company=request.user.company)
        serializer = IndicatorCategorySerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return ResponseHandler.update_success('indicator_category')
        return ResponseHandler.update_failed(serializer.errors)

    def delete(self, request):
        check_permissions(request, ['delete_indicator_category'])
        ids = request.data.get("ids", [])
        if not isinstance(ids, list) or not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)

        queryset = IndicatorCategory.objects.filter(id__in=ids, company=request.user.company)
        deletable_instances, reference_details = check_references_and_get_deletable_instances(IndicatorCategory, ids)

        if reference_details:
            return ResponseHandler.dependency_error(message=ResponseMessages.protected_error("indicator_category"))

        queryset.update(deleted_at=timezone.now())
        return ResponseHandler.delete_success("indicator_category")

class IndicatorView(APIView):
    def get(self, request, id=None):
        if id:
            check_permissions(request, ['view_indicator'])
            instance = get_object_or_404(Indicator, id=id, company=request.user.company)
            serializer = IndicatorListSerializer(instance)
            return ResponseHandler.success(serializer.data)

        check_permissions(request, ['list_indicator'])
        paginate = request.query_params.get("paginate", "true")
        data = Indicator.objects.filter(company=request.user.company).order_by("-id")
        
        if search := request.query_params.get("search"):
            data = data.filter(Q(indicator_name__icontains=search)|
            Q(category__category_name__icontains = search)|
            Q(measurement_unit__icontains = search)|
            Q(description__icontains=search)
        )

        if category := request.query_params.get("category"):
            data = data.filter(category__category_name = category)

        if status := request.query_params.get("status"):
            data = data.filter(status=status)

        if paginate == "false":
            serializer = IndicatorListSerializer(data, many=True)
            return ResponseHandler.list_success(serializer.data)
        return paginate_queryset(data, request, IndicatorListSerializer, view=self)

    def post(self, request):
        check_permissions(request, ['add_indicator'])
        serializer = IndicatorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success('indicator')
        return ResponseHandler.create_failed(serializer.errors)

    def put(self, request, id=None):
        check_permissions(request, ['change_indicator'])
        instance = get_object_or_404(Indicator, id=id, company=request.user.company)
        serializer = IndicatorSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return ResponseHandler.update_success('indicator')
        return ResponseHandler.update_failed(serializer.errors)

    def delete(self, request):
        check_permissions(request, ['delete_indicator'])
        ids = request.data.get("ids", [])
        if not isinstance(ids, list) or not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)

        queryset = Indicator.objects.filter(id__in=ids, company=request.user.company)
        deletable_instances, reference_details = check_references_and_get_deletable_instances(Indicator, ids)

        if reference_details:
            return ResponseHandler.dependency_error(message=ResponseMessages.protected_error("indicator"))

        queryset.update(deleted_at=timezone.now())
        return ResponseHandler.delete_success("indicator")

class GoalTypeView(APIView):
    def get(self, request, id=None):
        if id:
            check_permissions(request, ['view_goal_type'])
            instance = get_object_or_404(GoalType, id=id, company=request.user.company)
            serializer = GoalTypeListSerializer(instance)
            return ResponseHandler.success(serializer.data)

        check_permissions(request, ['list_goal_type'])
        paginate = request.query_params.get("paginate", "true")
        data = GoalType.objects.filter(company=request.user.company).order_by("-id")
        
        if search := request.query_params.get("search"):
            data = data.filter(Q(description__icontains=search)|
            Q(goal_name__icontains = search)
            )

        if status :=request.query_params.get("status"):
            data = data.filter(status=status)

        if paginate == "false":
            serializer = GoalTypeListSerializer(data, many=True)
            return ResponseHandler.list_success(serializer.data)
        return paginate_queryset(data, request, GoalTypeListSerializer, view=self)

    def post(self, request):
        check_permissions(request, ['add_goal_type'])
        serializer = GoalTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success('goal_type')
        return ResponseHandler.create_failed(serializer.errors)

    def put(self, request, id=None):
        check_permissions(request, ['change_goal_type'])
        instance = get_object_or_404(GoalType, id=id, company=request.user.company)
        serializer = GoalTypeSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return ResponseHandler.update_success('goal_type')
        return ResponseHandler.update_failed(serializer.errors)

    def delete(self, request):
        check_permissions(request, ['delete_goal_type'])
        ids = request.data.get("ids", [])
        if not isinstance(ids, list) or not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)

        queryset = GoalType.objects.filter(id__in=ids, company=request.user.company)
        deletable_instances, reference_details = check_references_and_get_deletable_instances(GoalType, ids)

        if reference_details:
            return ResponseHandler.dependency_error(message=ResponseMessages.protected_error("goal_type"))

        queryset.update(deleted_at=timezone.now())
        return ResponseHandler.delete_success("goal_type")

class EmployeeGoalView(APIView):
    def get(self, request, id=None):
        if id:
            check_permissions(request, ['view_employeegoal'])
            instance = get_object_or_404(EmployeeGoal, id=id, company=request.user.company)
            serializer = EmployeeGoalListSerializer(instance)
            return ResponseHandler.success(serializer.data)

        check_permissions(request, ['list_employeegoal'])
        paginate = request.query_params.get("paginate", "true")
        data = EmployeeGoal.objects.filter(company=request.user.company).order_by("-id")
        
        if search := request.query_params.get("search"):
            data = data.filter(Q(description__icontains=search)|
            Q(goal_title__icontains = search)|
            Q(employee__full_name__icontains = search)
        )

        if employee := request.query_params.get("employee"):
            data = data.filter(employee__full_name = employee)

        if goal_type := request.query_params.get("goal_type"):
            data = data.filter(goal_type__goal_name = goal_type)

        if status :=request.query_params.get("status"):
            data = data.filter(status=status)

        if paginate == "false":
            serializer = EmployeeGoalListSerializer(data, many=True)
            return ResponseHandler.list_success(serializer.data)
        return paginate_queryset(data, request, EmployeeGoalListSerializer, view=self)

    def post(self, request):
        check_permissions(request, ['add_employeegoal'])
        serializer = EmployeeGoalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success('employeegoal')
        return ResponseHandler.create_failed(serializer.errors)

    def put(self, request, id=None):
        check_permissions(request, ['change_employeegoal'])
        instance = get_object_or_404(EmployeeGoal, id=id, company=request.user.company)
        serializer = EmployeeGoalSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return ResponseHandler.update_success('employeegoal')
        return ResponseHandler.update_failed(serializer.errors)

    def delete(self, request):
        check_permissions(request, ['delete_employeegoal'])
        ids = request.data.get("ids", [])
        if not isinstance(ids, list) or not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)

        queryset = EmployeeGoal.objects.filter(id__in=ids, company=request.user.company)
        deletable_instances, reference_details = check_references_and_get_deletable_instances(EmployeeGoal, ids)

        if reference_details:
            return ResponseHandler.dependency_error(message=ResponseMessages.protected_error("employeegoal"))

        queryset.update(deleted_at=timezone.now())
        return ResponseHandler.delete_success("employeegoal")

class ReviewCycleView(APIView):
    def get(self, request, id=None):
        if id:
            check_permissions(request, ['view_reviewcycle'])
            instance = get_object_or_404(ReviewCycle, id=id, company=request.user.company)
            serializer = ReviewCycleListSerializer(instance)
            return ResponseHandler.success(serializer.data)

        check_permissions(request, ['list_reviewcycle'])
        paginate = request.query_params.get("paginate", "true")
        data = ReviewCycle.objects.filter(company=request.user.company).order_by("-id")
        
        if search := request.query_params.get("search"):
            data = data.filter(Q(cycle_name__icontains=search)|
            Q(frequency__icontains = search)|
            Q(description__icontains = search))

        if frequency := request.query_params.get("frequency"):
            data = data.filter(frequency__icontains = frequency)

        if status :=request.query_params.get("status"):
            data = data.filter(status=status)

        if paginate == "false":
            serializer = ReviewCycleListSerializer(data, many=True)
            return ResponseHandler.list_success(serializer.data)
        return paginate_queryset(data, request, ReviewCycleListSerializer, view=self)

    def post(self, request):
        check_permissions(request, ['add_reviewcycle'])
        serializer = ReviewCycleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success('reviewcycle')
        return ResponseHandler.create_failed(serializer.errors)

    def put(self, request, id=None):
        check_permissions(request, ['change_reviewcycle'])
        instance = get_object_or_404(ReviewCycle, id=id, company=request.user.company)
        serializer = ReviewCycleSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return ResponseHandler.update_success('reviewcycle')
        return ResponseHandler.update_failed(serializer.errors)

    def delete(self, request):
        check_permissions(request, ['delete_reviewcycle'])
        ids = request.data.get("ids", [])
        if not isinstance(ids, list) or not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)

        queryset = ReviewCycle.objects.filter(id__in=ids, company=request.user.company)
        deletable_instances, reference_details = check_references_and_get_deletable_instances(ReviewCycle, ids)

        if reference_details:
            return ResponseHandler.dependency_error(message=ResponseMessages.protected_error("reviewcycle"))

        queryset.update(deleted_at=timezone.now())
        return ResponseHandler.delete_success("reviewcycle")

class EmployeeReviewView(APIView):
    def get(self, request, id=None):
        if id:
            check_permissions(request, ['view_employee_review'])
            instance = get_object_or_404(EmployeeReview, id=id, company=request.user.company)
            serializer = EmployeeReviewListSerializer(instance)
            return ResponseHandler.success(serializer.data)

        check_permissions(request, ['list_employee_review'])
        paginate = request.query_params.get("paginate", "true")
        data = EmployeeReview.objects.filter(company=request.user.company).order_by("-id")
        
        if search := request.query_params.get("search"):
            data = data.filter(Q(employee__full_name__icontains=search)|
            Q(reviewer__full_name__icontains = search)
            )

        if employee := request.query_params.get("employee"):
            data = data.filter(employee__full_name = employee)

        if reviewer := request.query_params.get("reviewer"):
            data = data.filter(reviewer__full_name = reviewer)

        if review_cycle := request.query_params.get("review_cycle"):
            data = data.filter(review_cycle__cycle_name = review_cycle)        

        if status :=request.query_params.get("status"):
            data = data.filter(status=status)

        if date_from := request.query_params.get("date_from"):
            data = data.filter(review_date__gte=date_from)

        if date_to := request.query_params.get("date_to"):
            data = data.filter(review_date__lte = date_to)

        if paginate == "false":
            serializer = EmployeeReviewListSerializer(data, many=True)
            return ResponseHandler.list_success(serializer.data)
        return paginate_queryset(data, request, EmployeeReviewListSerializer, view=self)

    def post(self, request):
        check_permissions(request, ['add_employee_review'])
        serializer = EmployeeReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success('employee_review')
        return ResponseHandler.create_failed(serializer.errors)

    def put(self, request, id=None):
        check_permissions(request, ['change_employee_review'])
        instance = get_object_or_404(EmployeeReview, id=id, company=request.user.company)
        serializer = EmployeeReviewSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return ResponseHandler.update_success('employee_review')
        return ResponseHandler.update_failed(serializer.errors)

    def delete(self, request):
        check_permissions(request, ['delete_employee_review'])
        ids = request.data.get("ids", [])
        if not isinstance(ids, list) or not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)

        queryset = EmployeeReview.objects.filter(id__in=ids, company=request.user.company)
        deletable_instances, reference_details = check_references_and_get_deletable_instances(EmployeeReview, ids)

        if reference_details:
            return ResponseHandler.dependency_error(message=ResponseMessages.protected_error("employee_review"))

        queryset.update(deleted_at=timezone.now())
        return ResponseHandler.delete_success("employee_review")