from django.db.models import Q
from rest_framework.views import APIView
from shared.models.hr_management import TrainingProgram, TrainingType, TrainingSession, AssignTraining
from shared.models.core.useractivity import UserActivityLog
from ..serializers.trainingSerializer import(
TrainingTypeSerializer, TrainingTypeListSerializer,
TrainingProgramSerializer, TrainingProgramListSerializer,
TrainingSessionSerializer, TrainingSessionListSerializer,
AssignTrainingSerializer, AssignTrainingListSerializer)
from shared.utils.response.handlers import ResponseHandler
from shared.utils.response.messages import ResponseMessages
from shared.utils.common.pagination import paginate_queryset
from shared.utils.common.centarlisedPermission import check_permissions
from shared.utils.errors.protectedErrors import check_references_and_get_deletable_instances
from django.shortcuts import get_object_or_404
from django.utils import timezone

class TrainingTypeView(APIView):
    def get(self, request, id=None):
        if id:
            check_permissions(request, ['view_training_type'])
            instance = get_object_or_404(TrainingType, id=id, company=request.user.company)
            serializer = TrainingTypeListSerializer(instance)
            return ResponseHandler.success(serializer.data)

        check_permissions(request, ['list_training_type'])
        paginate = request.query_params.get("paginate", "true")
        data = TrainingType.objects.filter(company=request.user.company).order_by("-id")
        
        if search := request.query_params.get("search"):
            data = data.filter(Q(description__icontains=search)|
            Q(name__icontains = search)|
            Q(branch__branch_name__icontains = search)
        )

        if branch := request.query_params.get("branch"):
            data = data.filter(branch__branch_name = branch)

        if department := request.query_params.get("department"):
            data = data.filter(Q(branch__departments__department=department) | Q(departments__department=department)).distinct()

        if status :=request.query_params.get("status"):
            data = data.filter(status=status)

        if paginate == "false":
            serializer = TrainingTypeListSerializer(data, many=True)
            return ResponseHandler.list_success(serializer.data)
        return paginate_queryset(data, request, TrainingTypeListSerializer, view=self)

    def post(self, request):
        check_permissions(request, ['add_training_type'])
        serializer = TrainingTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success('training type')
        return ResponseHandler.create_failed(serializer.errors)

    def put(self, request, id=None):
        check_permissions(request, ['change_training_type'])
        instance = get_object_or_404(TrainingType, id=id, company=request.user.company)
        serializer = TrainingTypeSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return ResponseHandler.update_success('training type')
        return ResponseHandler.update_failed(serializer.errors)

    def delete(self, request):
        check_permissions(request, ['delete_training_type'])
        ids = request.data.get("ids", [])
        if not isinstance(ids, list) or not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)

        queryset = TrainingType.objects.filter(id__in=ids, company=request.user.company)
        deletable_instances, reference_details = check_references_and_get_deletable_instances(TrainingType, ids)

        if reference_details:
            return ResponseHandler.dependency_error(message=ResponseMessages.protected_error("training type"))

        queryset.update(deleted_at=timezone.now())
        return ResponseHandler.delete_success("training type")

class TrainingProgramView(APIView):
    def get(self, request, id=None):
        if id:
            check_permissions(request, ['view_training_program'])
            instance = get_object_or_404(TrainingProgram, id=id, company=request.user.company)
            serializer = TrainingProgramListSerializer(instance)
            return ResponseHandler.success(serializer.data)

        check_permissions(request, ['list_training_program'])
        paginate = request.query_params.get("paginate", "true")
        data = TrainingProgram.objects.filter(company=request.user.company).order_by("-id")
        
        if search := request.query_params.get("search"):
            data = data.filter(Q(description__icontains=search)|
            Q(training_type__name__icontains = search)
        )

        if training_type := request.query_params.get("training_type"):
            data = data.filter(training_type__name = training_type)

        if status :=request.query_params.get("status"):
            data = data.filter(status=status)

        if paginate == "false":
            serializer = TrainingProgramListSerializer(data, many=True)
            return ResponseHandler.list_success(serializer.data)
        return paginate_queryset(data, request, TrainingProgramListSerializer, view=self)

    def post(self, request):
        check_permissions(request, ['add_training_program'])
        serializer = TrainingProgramSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success('training program')
        return ResponseHandler.create_failed(serializer.errors)

    def put(self, request, id=None):
        check_permissions(request, ['change_training_program'])
        instance = get_object_or_404(TrainingProgram, id=id, company=request.user.company)
        serializer = TrainingProgramSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return ResponseHandler.update_success('training program')
        return ResponseHandler.update_failed(serializer.errors)

    def delete(self, request):
        check_permissions(request, ['delete_training_program'])
        ids = request.data.get("ids", [])
        if not isinstance(ids, list) or not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)

        queryset = TrainingProgram.objects.filter(id__in=ids, company=request.user.company)
        deletable_instances, reference_details = check_references_and_get_deletable_instances(TrainingProgram, ids)

        if reference_details:
            return ResponseHandler.dependency_error(message=ResponseMessages.protected_error("training program"))

        queryset.update(deleted_at=timezone.now())
        return ResponseHandler.delete_success("training program")

class TrainingSessionView(APIView):
    def get(self, request, id=None):
        if id:
            check_permissions(request, ['view_training_session'])
            instance = get_object_or_404(TrainingSession, id=id, company=request.user.company)
            serializer = TrainingSessionListSerializer(instance)
            return ResponseHandler.success(serializer.data)

        check_permissions(request, ['list_training_session'])
        paginate = request.query_params.get("paginate", "true")
        data = TrainingSession.objects.filter(company=request.user.company).order_by("-id")
        
        if search := request.query_params.get("search"):
            data = data.filter(Q(description__icontains=search)|
            Q(training_program__name__icontains = search) |
            Q(session_name__icontains = search)|
            Q(trainer__full_name__icontains = search)|
            Q(location__icontains = search)
        )

        if trainer := request.query_params.get("trainer"):
            data = data.filter(trainer__full_name = trainer)


        if training_program := request.query_params.get("training_program"):
            data = data.filter(training_program__name = training_program)

        if status :=request.query_params.get("status"):
            data = data.filter(status=status)

        if location := request.query_params.get("location"):
            data = data.filter(location=location)   

        if session_type := request.query_params.get("session_type"):
            data = data.filter(session_type=session_type)   

        if start_date := request.query_params.get("start_date"):
            data = data.filter(start_date=start_date)

        if end_date := request.query_params.get("end_date"):
            data = data.filter(end_date=end_date)
            
        if paginate == "false":
            serializer = TrainingSessionListSerializer(data, many=True)
            return ResponseHandler.list_success(serializer.data)
        return paginate_queryset(data, request, TrainingSessionListSerializer, view=self)

    def post(self, request):
        check_permissions(request, ['add_training_session'])
        serializer = TrainingSessionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success('training session')
        return ResponseHandler.create_failed(serializer.errors)

    def put(self, request, id=None):
        check_permissions(request, ['change_training_session'])
        instance = get_object_or_404(TrainingSession, id=id, company=request.user.company)
        serializer = TrainingSessionSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return ResponseHandler.update_success('training session')
        return ResponseHandler.update_failed(serializer.errors)

    def delete(self, request):
        check_permissions(request, ['delete_training_session'])
        ids = request.data.get("ids", [])
        if not isinstance(ids, list) or not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)

        queryset = TrainingSession.objects.filter(id__in=ids, company=request.user.company)
        deletable_instances, reference_details = check_references_and_get_deletable_instances(TrainingSession, ids)

        if reference_details:
            return ResponseHandler.dependency_error(message=ResponseMessages.protected_error("training session"))

        queryset.update(deleted_at=timezone.now())
        return ResponseHandler.delete_success("training session")

class AssignTrainingView(APIView):
    def get(self, request, id=None):
        if id:
            check_permissions(request, ['view_assign_training'])
            instance = get_object_or_404(AssignTraining, id=id, company=request.user.company)
            serializer = AssignTrainingListSerializer(instance)
            return ResponseHandler.success(serializer.data)

        check_permissions(request, ['list_assign_training'])
        paginate = request.query_params.get("paginate", "true")
        data = AssignTraining.objects.filter(company=request.user.company).order_by("-id")
        
        if search := request.query_params.get("search"):
            data = data.filter(Q(feedback__icontains=search)|
            Q(training_program__name__icontains = search) |
            Q(notes__icontains = search)|
            Q(employee__full_name__icontains = search)
        )

        if employee := request.query_params.get("employee"):
            data = data.filter(employee__full_name = employee)

        if training_program := request.query_params.get("training_program"):
            data = data.filter(training_program__name = training_program)

        if status :=request.query_params.get("status"):
            data = data.filter(status=status)

        if start_date := request.query_params.get("start_date"):
            data = data.filter(start_date=start_date)

        if end_date := request.query_params.get("end_date"):
            data = data.filter(end_date=end_date)
            
        if paginate == "false":
            serializer = AssignTrainingListSerializer(data, many=True)
            return ResponseHandler.list_success(serializer.data)
        return paginate_queryset(data, request, AssignTrainingListSerializer, view=self)

    def post(self, request):
        check_permissions(request, ['add_assign_training'])
        serializer = AssignTrainingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success('assign training')
        return ResponseHandler.create_failed(serializer.errors)

    def put(self, request, id=None):
        check_permissions(request, ['change_assign_training'])
        instance = get_object_or_404(AssignTraining, id=id, company=request.user.company)
        serializer = AssignTrainingSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return ResponseHandler.update_success('assign training')
        return ResponseHandler.update_failed(serializer.errors)

    def delete(self, request):
        check_permissions(request, ['delete_assign_training'])
        ids = request.data.get("ids", [])
        if not isinstance(ids, list) or not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)

        queryset = AssignTraining.objects.filter(id__in=ids, company=request.user.company)
        deletable_instances, reference_details = check_references_and_get_deletable_instances(AssignTraining, ids)

        if reference_details:
            return ResponseHandler.dependency_error(message=ResponseMessages.protected_error("assign training"))

        queryset.update(deleted_at=timezone.now())
        return ResponseHandler.delete_success("assign training")