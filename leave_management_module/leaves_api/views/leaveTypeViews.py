from rest_framework.views import APIView
from rest_framework import status
from shared.models.leave_management.leave_type import LeaveType
from ..serializers.leaveTypeSerializer import LeaveTypeSerializer
from shared.utils.response.handlers import ResponseHandler
from django.shortcuts import get_object_or_404
from django.db.models import Q
from shared.utils.common.pagination import paginate_queryset


class LeaveTypeListView(APIView):

    def get(self, request):
        leave_types = LeaveType.active_objects.filter(
            company=request.user.company
        ).order_by('-created_at')

        filters = ['name', 'paid_leave', 'max_days_per_year']
        for param in filters:
            if param in request.query_params:
                value = request.query_params.get(param)
                if param == 'name':
                    leave_types = leave_types.filter(name__iexact=value)
                else:
                    leave_types = leave_types.filter(**{param: value})

        return paginate_queryset(leave_types, request, LeaveTypeSerializer)

    def post(self, request):
        serializer = LeaveTypeSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success("Leave_type", serializer.data)

        return ResponseHandler.create_failed(serializer.errors)


class LeaveTypeDetailsView(APIView):

    def get(self, request, id):
        leave_type = get_object_or_404(
            LeaveType.active_objects,
            id=id,
            company=request.user.company
        )
        serializer = LeaveTypeSerializer(
            leave_type,
            context={'request': request}
        )
        return ResponseHandler.success(serializer.data)

    def put(self, request, id):
        leave_type = get_object_or_404(
            LeaveType.active_objects,
            id=id,
            company=request.user.company
        )

        serializer = LeaveTypeSerializer(
            leave_type,
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return ResponseHandler.update_success("Leave_type", serializer.data)

        return ResponseHandler.create_failed(serializer.errors)

    def patch(self, request, id):
        leave_type = get_object_or_404(
            LeaveType.active_objects,
            id=id,
            company=request.user.company
        )

        serializer = LeaveTypeSerializer(
            leave_type,
            data=request.data,
            partial=True,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return ResponseHandler.update_success("Leave_type", serializer.data)

        return ResponseHandler.create_failed(serializer.errors)

    def delete(self, request, id):
        leave_type = get_object_or_404(
            LeaveType.active_objects,
            id=id,
            company=request.user.company
        )

        leave_type.delete()
        return ResponseHandler.delete_success("Leave_type")