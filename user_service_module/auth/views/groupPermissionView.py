from shared.models import User
from django.db.models import Q
from ..renders import UserRenderer
from rest_framework.views import APIView
from shared.models import Role
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Permission
from shared.utils.common import check_permissions
from shared.utils.common import paginate_queryset
from django.db.models.deletion import ProtectedError
from shared.utils.response import ResponseHandler,ResponseMessages
from ..serializers.groupSerializer import GroupSerializer,GroupDetailsSerializer

class GroupCreateView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request):
        check_permissions(request, ['add_role'])

        data = request.data.copy()
        data['company'] = request.user.company.id

        serializer = GroupSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return ResponseHandler.create_success(name="Role")
        return ResponseHandler.create_failed(errors=serializer.errors)

class GroupListView(APIView):
    renderer_classes = [UserRenderer]

    def get(self, request):
        check_permissions(request, ['list_role'])
        groups = Role.objects.filter(company=request.user.company).order_by('name')
        search = request.query_params.get('search')
        if search:
            groups = groups.filter(
                Q(name__icontains=search)
            )
        return paginate_queryset(groups, request, GroupDetailsSerializer, view=self)

class GroupDetailView(APIView):
    renderer_classes = [UserRenderer]

    def get(self, request, id):
        check_permissions(request, ['view_role'])

        try:
            group = Role.objects.get(id=id, company=request.user.company)
        except Role.DoesNotExist:
            return ResponseHandler.not_found(message=ResponseMessages.NO_MATCHING_DATA)

        serializer = GroupDetailsSerializer(group)
        return ResponseHandler.success(response_data=serializer.data, message=ResponseMessages.USER_PERMISSIONS_FETCH_SUCCESS)

class GroupDeleteView(APIView):
    renderer_classes = [UserRenderer]

    def delete(self, request, format=None):
        check_permissions(request, ['delete_role'])

        ids = request.data.get('ids', [])
        if not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)

        groups_to_delete = Role.objects.filter(id__in=ids, company=request.user.company)
        if not groups_to_delete.exists():
            return ResponseHandler.not_found(message=ResponseMessages.NO_MATCHING_DATA)
        try:
            groups_to_delete.delete()
            return ResponseHandler.delete_success('Roles')
        
        except ProtectedError as e:
            return ResponseHandler.dependency_error(
                message=ResponseMessages.protected_error("Roles")
            )
        
class ManagePermissionsForGroupView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, id):
        check_permissions(request, ['add_permission'])
        
        try:
            group = Role.objects.get(id=id, company=request.user.company)
            
            new_group_name = request.data.get('name')

            if new_group_name:
                group.name = new_group_name

            permission_ids_to_assign = request.data.get('assign_permissions', [])
            permission_ids_to_remove = request.data.get('remove_permissions', [])

            if not permission_ids_to_assign and not permission_ids_to_remove and not new_group_name:
                return ResponseHandler.bad_request(message=ResponseMessages.NO_PERMISSIONS_OR_NAME_PROVIDED)

            if permission_ids_to_assign:
                for permission_id in permission_ids_to_assign:
                    try:
                        permission = Permission.objects.get(id=permission_id)
                        group.permissions.add(permission)
                    except Permission.DoesNotExist:
                        return ResponseHandler.not_found(message=ResponseMessages.PERMISSION_NOT_FOUND.format(id=permission_id))

            if permission_ids_to_remove:
                for permission_id in permission_ids_to_remove:
                    try:
                        permission = Permission.objects.get(id=permission_id)
                        group.permissions.remove(permission)
                    except Permission.DoesNotExist:
                        return ResponseHandler.not_found(message=ResponseMessages.PERMISSION_NOT_FOUND.format(id=permission_id))

            group.save()
            return ResponseHandler.update_success("Role")

        except Role.DoesNotExist:
            return ResponseHandler.not_found(message=ResponseMessages.GROUP_NOT_FOUND)

class ManageUserGroupView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, id):
        # We check change_user or similar, but add_role/change_role context is also used.
        check_permissions(request, ['change_user'])

        group_data = request.data.get('groups', [])
        if not group_data:
            return ResponseHandler.bad_request(message=ResponseMessages.GROUPS_REQUIRED)

        try:
            user = User.objects.get(id=id, company=request.user.company)
        except User.DoesNotExist:
            return ResponseHandler.not_found(message=ResponseMessages.USER_NOT_FOUND)

        groups_actions = []

        for group in group_data:
            group_id = group.get('group_ids')
            action = group.get('action')

            if group_id is None or action is None:
                return ResponseHandler.bad_request(message=ResponseMessages.GROUP_ID_AND_ACTION_REQUIRED)

            try:
                group_instance = Role.objects.get(id=group_id, company=request.user.company)
            except Role.DoesNotExist:
                return ResponseHandler.not_found(message=ResponseMessages.GROUP_NOT_FOUND.format(id=group_id))

            if action in ['assign', 'remove']:
                groups_actions.append((action, group_instance))
            else:
                return ResponseHandler.bad_request(message=ResponseMessages.INVALID_ACTION)

        for action, group_instance in groups_actions:
            if action == 'assign':
                user.roles.add(group_instance)
            elif action == 'remove':
                user.roles.remove(group_instance)

        user.save()
        return ResponseHandler.update_success("User roles")
    
class ChangeGroupStatusView(APIView):
    renderer_classes = [UserRenderer]

    def patch(self, request, id):
        check_permissions(request, ['change_role'])

        group = get_object_or_404(Role, id=id, company=request.user.company)
        action = request.data.get('action')

        if action not in ['enable', 'disable']:
            return ResponseHandler.bad_request(message=ResponseMessages.INVALID_ACTION)

        if action == 'enable':
            group.is_enabled = True
        elif action == 'disable':
            group.is_enabled = False

        group.save()
        return ResponseHandler.success(message=f"Role '{group.name}' has been {action}d.")

class EnabledGroupListView(APIView):
    renderer_classes = [UserRenderer]

    def get(self, request):
        check_permissions(request, ['list_role'])

        enabled_groups = Role.objects.filter(
            company=request.user.company, is_enabled=True
        ).order_by('name')

        serializer = GroupDetailsSerializer(enabled_groups, many=True)
        return ResponseHandler.list_success(serializer.data)
