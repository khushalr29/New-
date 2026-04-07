from django.db.models import Q
from django.db import transaction 
from ..renders import UserRenderer
from rest_framework.views import APIView
from shared.models import User,UserActivityLog
from django.shortcuts import get_object_or_404
from shared.logs.decorators import log_activity
from shared.utils.common import paginate_queryset
from shared.utils.common import check_permissions   
from django.db.models.deletion import ProtectedError
from shared.utils.response import ResponseHandler,ResponseMessages
from shared.serializers.userSerializers import UserCreationSerializer
from ..serializers.userSerializer import UserListSerializer,UserUpdateSerializer,UserDetailSerializer

class UserCreationView(APIView):
    renderer_classes = [UserRenderer]

    @log_activity(UserActivityLog.CREATE, 'User')
    def post(self, request):
        check_permissions(request, ['add_user'])

        data = request.data.copy()
        company = request.user.company
        data['company'] = company.id

        if User.objects.filter(company=company).count() >= company.no_of_users:
            return ResponseHandler.forbidden(message=ResponseMessages.max_user(company.no_of_users))

        if not data.get('account_type'):
            data['account_type'] = 'sub_admin'
            
        serializer = UserCreationSerializer(data=data)
        if serializer.is_valid():
             with transaction.atomic():
                serializer.save()
                return ResponseHandler.success(
                    message=ResponseMessages.USER_CREATION_EMAIL_NOTICE
                )
        return ResponseHandler.create_failed(serializer.errors)

class UserListView(APIView):
    renderer_classes = [UserRenderer]
    
    def get(self, request, format=None):
        check_permissions(request, ['list_user'])

        users = User.objects.filter(
            company=request.user.company,
            is_superuser=False).exclude(id=request.user.id)
        
        filter_params = ['gender', 'roles']
        for param in filter_params:
            value = request.query_params.get(param)
            if value:
                users = users.filter(**{f'{param}__id': value})
        search = request.query_params.get('search')
        if search:
            users = users.filter(
                Q(email__icontains=search) |
                Q(full_name__icontains=search) |
                Q(phone_number__icontains=search)
            )

        users = users.order_by('full_name')
        return paginate_queryset(users, request, UserListSerializer, view=self)

class UserDetailView(APIView):
    renderer_classes = [UserRenderer]

    def get_object(self, id, company):
        try:
            return User.objects.get(id=id, company=company)
        except User.DoesNotExist:
            return None
    
    @log_activity(UserActivityLog.VIEW, 'User')
    def get(self, request, id, format=None):
        check_permissions(request, ['view_user'])

        user = self.get_object(id, request.user.company)
        if user is None:
            return ResponseHandler.not_found_error()

        serializer = UserDetailSerializer(user, context={'request': request})
        return ResponseHandler.success(serializer.data)
    
class UserUpdationView(APIView):
    renderer_classes = [UserRenderer]

    def get_object(self, id, company):
        try:
            return User.objects.get(id=id, company=company)
        except User.DoesNotExist:
            return None
        
    @log_activity(UserActivityLog.UPDATE, 'User')
    def put(self, request, id, *args, **kwargs):
        check_permissions(request, ['change_user'])

        user = self.get_object(id, request.user.company)
        if user is None:
            return ResponseHandler.not_found_error()

        serializer = UserUpdateSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return ResponseHandler.update_success("User")

        return ResponseHandler.update_failed(serializer.errors)

class UserDeleteView(APIView):
    renderer_classes = [UserRenderer]

    @log_activity(UserActivityLog.DELETE, 'User')
    def delete(self, request, format=None):
        check_permissions(request, ['delete_user'])

        ids = request.data.get('ids', [])
        if not ids:
            return ResponseHandler.no_matching_data()

        users_to_delete = User.objects.filter(id__in=ids, company=request.user.company)
        if not users_to_delete.exists():
            return ResponseHandler.no_matching_data()

        try:
            users_to_delete.delete()
            return ResponseHandler.delete_success('User')
        
        except ProtectedError as e:
            return ResponseHandler.dependency_error(
                message=ResponseMessages.protected_error("User")
            )

class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    
    def get(self, request, format=None):
        serializer = UserDetailSerializer(request.user, context={'request': request})
        return ResponseHandler.success(serializer.data)

class ChangeUserStatusView(APIView):
    @log_activity(UserActivityLog.CHANGE_STATUS, 'User')
    def patch(self, request, id):
        user = get_object_or_404(User, id=id, company=request.user.company)
        action = request.data.get('action')

        if action not in ['enable', 'disable']:
            return ResponseHandler.bad_request(message=ResponseMessages.INVALID_ACTION)

        if action == 'enable':
            user.is_enabled = True

        elif action == 'disable':
            user.is_enabled = False

        user.save()
        return ResponseHandler.success()

class EnabledUserListView(APIView):
    
    def get(self, request):
        check_permissions(request, ['view_user'])

        company = request.user.company
        users = User.objects.filter(
            is_enabled=True,
            company=company
        ).order_by('full_name')

        serializer = UserListSerializer(users, many=True)
        return ResponseHandler.list_success(serializer.data)
