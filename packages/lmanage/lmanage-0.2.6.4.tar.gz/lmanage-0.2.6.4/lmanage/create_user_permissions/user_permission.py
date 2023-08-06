import logging
import coloredlogs
import looker_sdk
from looker_sdk import models

logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO')


def get_role_metadata(
        parsed_yaml: dict) -> list:
    role_permission = []
    del parsed_yaml['role_admin']
    for group_name, group_info in parsed_yaml.items():
        if 'role' in group_name:
            role_name = group_info['role']
            temp = {}
            if 'permissions' in group_info.keys():
                temp['role_name'] = role_name
                temp['permission'] = group_info['permissions']
                temp['model_set_value'] = group_info['model_set']
                temp['teams'] = group_info['team']
                role_permission.append(temp)
            else:
                temp['role_name'] = role_name
                role_permission.append(temp)

    logger.debug(role_permission)
    return role_permission


def sync_permission_set(
        sdk: looker_sdk,
        all_permission_sets: list,
        permission_set_list: list):

    permissions_dict = {p.name: p.id for p in all_permission_sets}
    permissions_dict.pop('Admin')
    yaml_permissions = [role.get('name') for role in permission_set_list]

    for permission_set_name in permissions_dict.keys():

        if permission_set_name not in yaml_permissions:
            permission_id = sdk.search_permission_sets(
                name=permission_set_name)[0].id
            sdk.delete_permission_set(permission_set_id=permission_id)


def create_permission_set(
        sdk: looker_sdk,
        permission_set_list: list):

    final_response = []
    for permission in permission_set_list:
        permission_set_name = permission.get('role_name')
        permissions = permission.get('permission')
        body = models.WritePermissionSet(
            name=permission_set_name.lower(),
            permissions=permissions
        )
        try:
            perm = sdk.create_permission_set(
                body=body
            )
        except looker_sdk.error.SDKError:
            perm = sdk.search_permission_sets(name=permission_set_name)[0]
            pid = perm.id
            perm = sdk.update_permission_set(permission_set_id=pid, body=body)

        temp = {}
        temp['name'] = perm.name
        temp['pid'] = perm.id
        final_response.append(temp)

    logger.debug(final_response)
    return final_response


def create_model_set(
        sdk: looker_sdk,
        model_set_list: list) -> list:

    final_response = []
    for model in model_set_list:
        model_set_metadata = model.get('model_set_value')
        for model_set in model_set_metadata:
            model_set_name = model_set.get('name')
            attributed_models = model_set.get('models')
            body = models.WriteModelSet(
                name=model_set_name.lower(), models=attributed_models)
            try:
                model = sdk.create_model_set(body=body)
            except looker_sdk.error.SDKError as modelerror:
                logger.info(modelerror.args[0])
                model = sdk.search_model_sets(name=model_set_name)[0]
                model_set_id = model.id
                model = sdk.update_model_set(
                    model_set_id=model_set_id, body=body)
            temp = {}
            temp['model_set_name'] = model.name
            temp['model_set_id'] = model.id
            final_response.append(temp)
    logger.info(final_response)
    return final_response


def sync_model_set(
        sdk: looker_sdk,
        all_model_sets: list,
        model_set_list: list):

    model_sets_dict = {p.name: p.id for p in all_model_sets}
    model_sets_dict.pop('All')
    yaml_model = [role.get('model_set_name') for role in model_set_list]

    for model_set_name in model_sets_dict.keys():

        if model_set_name not in yaml_model:
            model_id = sdk.search_model_sets(
                name=model_set_name)[0].id
            sdk.delete_model_set(model_set_id=model_id)


def create_roles(
        sdk: looker_sdk,
        all_model_sets: list,
        all_permission_sets: list,
        role_metadata_list: list) -> list:

    model_set_dict = {model.name: model.id for model in all_model_sets}
    permission_set_dict = {perm.name: perm.id for perm in all_permission_sets}

    role_output = []
    for role in role_metadata_list:
        role_name = role.get('role_name')
        permission_set_id = permission_set_dict.get(role_name.lower())
        applied_model_set_name = role['model_set_value'][0]['name']
        model_set_id = model_set_dict.get(applied_model_set_name.lower())
        body = models.WriteRole(
            name=role_name,
            permission_set_id=permission_set_id,
            model_set_id=model_set_id
        )
        try:
            role = sdk.create_role(
                body=body
            )
        except looker_sdk.error.SDKError as roleerror:
            logger.debug(roleerror)
            role_id = sdk.search_roles(name=role_name)[0].id
            role = sdk.update_role(role_id=role_id, body=body)
        temp = {}
        temp['role_id'] = role.id
        temp['role_name'] = role_name
        role_output.append(temp)
    logger.info(role_output)
    return role_output


def sync_roles(
        sdk: looker_sdk,
        all_roles: list,
        role_metadata_list: list):

    all_role_dict = {role.name: role.id for role in all_roles}
    all_role_dict.pop('Admin')
    yaml_role = [role.get('role_name') for role in role_metadata_list]

    for role_name in all_role_dict.keys():
        if role_name not in yaml_role:
            role_id = sdk.search_roles(name=role_name)[0].id
            sdk.delete_role(role_id=role_id)


def set_role(
        role_id: str,
        sdk: looker_sdk,
        group_id: list) -> str:
    try:
        sdk.set_role_groups(role_id, group_id)
        return logger.info(f'attributing {group_id} permissions on instance')
    except looker_sdk.error.SDKError:
        return logger.info('something went wrong')


def attach_role_to_group(
    sdk: looker_sdk,
    role_metadata: list,
        created_role_metadata: list,
        all_roles: list):

    all_groups = sdk.all_groups()
    role_dict = {role.name: role.id for role in all_roles}
    group_dict = {group.name: group.id for group in all_groups}

    for role in role_metadata:
        teams = role.get('teams')
        role_id = role_dict.get(role.get('role_name'))
        group_id_list = []
        for team in teams:
            group_id = group_dict.get(team)
            group_id_list.append(group_id)
        set_role(role_id=role_id, group_id=group_id_list, sdk=sdk)
