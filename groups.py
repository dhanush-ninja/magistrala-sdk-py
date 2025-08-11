# Copyright (c) Abstract Machines
# SPDX-License-Identifier: Apache-2.0

import json
from typing import List, Optional
from urllib.parse import urljoin, urlencode

import requests

from .errors import Errors
from .defs import (
    Group,
    GroupsPage,
    PageMetadata,
    Response,
    Role,
    RolePage,
    BasicPageMeta,
    HierarchyPageMeta,
    HierarchyPage,
    MemberRolesPage,
    MembersPage,
    QueryParamRoles,
)
from .roles import Roles


class Groups:
    """
    Handles interactions with the groups API, including creating, updating, and managing groups, roles, and permissions.
    """

    def __init__(self, groups_url: str):
        """
        Initializes the Groups API client.
        
        Args:
            groups_url: Base URL for the groups API.
        """
        self.groups_url = groups_url.rstrip('/')
        self.content_type = "application/json"
        self.groups_endpoint = "groups"
        self.group_roles = Roles()

    def create_group(self, group: Group, domain_id: str, token: str) -> Group:
        """
        Creates a new group once the user is authenticated and a valid token is provided. 
        The group's parent or child status in the hierarchy can also be established.
        
        Args:
            group: The group object to be created.
            domain_id: The unique identifier of the domain.
            token: Authorization token.
            
        Returns:
            The created group object.
            
        Raises:
            Exception: If the group cannot be created.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(self.groups_url + '/', f"{domain_id}/{self.groups_endpoint}")
        
        try:
            response = requests.post(
                url,
                headers=headers,
                data=json.dumps(group.dict() if hasattr(group, 'dict') else group),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Group(**response.json())
        except requests.RequestException as error:
            raise error

    def group(
        self,
        group_id: str,
        domain_id: str,
        token: str,
        list_roles: Optional[bool] = None
    ) -> Group:
        """
        Retrieves information about a group by its ID.
        
        Args:
            group_id: The unique identifier of the group.
            domain_id: The unique identifier of the domain.
            token: Authorization token.
            list_roles: Whether to include roles in the response.
            
        Returns:
            The group object with its details.
            
        Raises:
            Exception: If the group information cannot be retrieved.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.groups_url + '/',
            f"{domain_id}/{self.groups_endpoint}/{group_id}"
        )
        
        if list_roles is not None:
            url += f"?{QueryParamRoles}={str(list_roles).lower()}"
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Group(**response.json())
        except requests.RequestException as error:
            raise error

    def groups(
        self, query_params: PageMetadata, domain_id: str, token: str
    ) -> GroupsPage:
        """
        Retrieves a list of groups with pagination support.
        
        Args:
            query_params: The query parameters for pagination (e.g., offset and limit).
            domain_id: The unique identifier of the domain.
            token: Authorization token.
            
        Returns:
            A paginated list of groups.
            
        Raises:
            Exception: If the groups cannot be retrieved.
        """
        string_params = {
            key: str(value) for key, value in query_params.items() if value is not None
        }

        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.groups_url + '/',
            f"{domain_id}/{self.groups_endpoint}?{urlencode(string_params)}"
        )
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return GroupsPage(**response.json())
        except requests.RequestException as error:
            raise error

    def update_group(self, group: Group, domain_id: str, token: str) -> Group:
        """
        Updates the information of an existing group.
        
        Args:
            group: The group object with updated details.
            domain_id: The unique identifier of the domain.
            token: Authorization token.
            
        Returns:
            The updated group object.
            
        Raises:
            Exception: If the group cannot be updated.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.groups_url + '/',
            f"{domain_id}/{self.groups_endpoint}/{group.id}"
        )
        
        try:
            response = requests.put(
                url,
                headers=headers,
                data=json.dumps(group.dict() if hasattr(group, 'dict') else group),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Group(**response.json())
        except requests.RequestException as error:
            raise error

    def enable_group(self, group_id: str, domain_id: str, token: str) -> Group:
        """
        Enables a disabled group by its ID.
        
        Args:
            group_id: The unique identifier of the group.
            domain_id: The unique identifier of the domain.
            token: Authorization token.
            
        Returns:
            The updated group object with enabled status.
            
        Raises:
            Exception: If the group cannot be enabled.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.groups_url + '/',
            f"{domain_id}/{self.groups_endpoint}/{group_id}/enable"
        )
        
        try:
            response = requests.post(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Group(**response.json())
        except requests.RequestException as error:
            raise error

    def disable_group(self, group_id: str, domain_id: str, token: str) -> Group:
        """
        Disables an enabled group by its ID.
        
        Args:
            group_id: The unique identifier of the group.
            domain_id: The unique identifier of the domain.
            token: Authorization token.
            
        Returns:
            The updated group object with disabled status.
            
        Raises:
            Exception: If the group cannot be disabled.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.groups_url + '/',
            f"{domain_id}/{self.groups_endpoint}/{group_id}/disable"
        )
        
        try:
            response = requests.post(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Group(**response.json())
        except requests.RequestException as error:
            raise error

    def delete_group(self, group_id: str, domain_id: str, token: str) -> Response:
        """
        Deletes a group by its ID.
        
        Args:
            group_id: The unique identifier of the group.
            domain_id: The unique identifier of the domain.
            token: Authorization token.
            
        Returns:
            A response object confirming the deletion.
            
        Raises:
            Exception: If the group cannot be deleted.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.groups_url + '/',
            f"{domain_id}/{self.groups_endpoint}/{group_id}"
        )
        
        try:
            response = requests.delete(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Response(
                status=response.status_code,
                message="Group deleted successfully"
            )
        except requests.RequestException as error:
            raise error

    def retrieve_group_hierarchy(
        self,
        group_id: str,
        domain_id: str,
        query_params: HierarchyPageMeta,
        token: str
    ) -> HierarchyPage:
        """
        Retrieves the hierarchical structure of a group, including its parents and children.
        
        Args:
            group_id: The unique identifier of the group.
            domain_id: The unique identifier of the domain.
            query_params: Pagination and query metadata.
            token: Authorization token.
            
        Returns:
            A promise that resolves to the group's hierarchical structure.
            
        Raises:
            Exception: If the hierarchy cannot be retrieved.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        string_params = {
            key: str(value) for key, value in query_params.items() if value is not None
        }

        url = urljoin(
            self.groups_url + '/',
            f"{domain_id}/{self.groups_endpoint}/{group_id}/hierarchy?{urlencode(string_params)}"
        )
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return HierarchyPage(**response.json())
        except requests.RequestException as error:
            raise error

    def add_parent_group(
        self, group_id: str, domain_id: str, parent_id: str, token: str
    ) -> Response:
        """
        Adds a parent group to the specified group within a domain.
        
        Args:
            group_id: The unique identifier of the group.
            domain_id: The unique identifier of the domain.
            parent_id: The unique identifier of the parent group.
            token: Authorization token.
            
        Returns:
            A promise that resolves to the addition response.
            
        Raises:
            Exception: If the parent group cannot be added.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.groups_url + '/',
            f"{domain_id}/{self.groups_endpoint}/{group_id}/parent"
        )
        
        try:
            response = requests.post(
                url,
                headers=headers,
                data=json.dumps({"parent_id": parent_id}),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Response(
                status=response.status_code,
                message="Parent added successfully"
            )
        except requests.RequestException as error:
            raise error

    def remove_parent_group(
        self, group_id: str, domain_id: str, token: str
    ) -> Response:
        """
        Removes the parent group from the specified group within a domain.
        
        Args:
            group_id: The unique identifier of the group.
            domain_id: The unique identifier of the domain.
            token: Authorization token.
            
        Returns:
            A promise that resolves to the removal response.
            
        Raises:
            Exception: If the parent group cannot be removed.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.groups_url + '/',
            f"{domain_id}/{self.groups_endpoint}/{group_id}/parent"
        )
        
        try:
            response = requests.delete(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Response(
                status=response.status_code,
                message="Parent removed successfully"
            )
        except requests.RequestException as error:
            raise error

    def add_children_groups(
        self, group_id: str, domain_id: str, children_ids: List[str], token: str
    ) -> Response:
        """
        Adds child groups to the specified group within a domain.
        
        Args:
            group_id: The unique identifier of the group.
            domain_id: The unique identifier of the domain.
            children_ids: List of unique identifiers of the child groups.
            token: Authorization token.
            
        Returns:
            A promise that resolves to the addition response.
            
        Raises:
            Exception: If the child groups cannot be added.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.groups_url + '/',
            f"{domain_id}/{self.groups_endpoint}/{group_id}/children"
        )
        
        try:
            response = requests.post(
                url,
                headers=headers,
                data=json.dumps({"children_ids": children_ids}),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Response(
                status=response.status_code,
                message="Children added successfully"
            )
        except requests.RequestException as error:
            raise error

    def remove_children_groups(
        self, group_id: str, domain_id: str, children_ids: List[str], token: str
    ) -> Response:
        """
        Removes specific child groups from the specified group within a domain.
        
        Args:
            group_id: The unique identifier of the group.
            domain_id: The unique identifier of the domain.
            children_ids: List of unique identifiers of the child groups to remove.
            token: Authorization token.
            
        Returns:
            A promise that resolves to the removal response.
            
        Raises:
            Exception: If the child groups cannot be removed.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.groups_url + '/',
            f"{domain_id}/{self.groups_endpoint}/{group_id}/children"
        )
        
        try:
            response = requests.delete(
                url,
                headers=headers,
                data=json.dumps({"children_ids": children_ids}),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Response(
                status=response.status_code,
                message="Children removed successfully"
            )
        except requests.RequestException as error:
            raise error

    def remove_all_children_groups(
        self, group_id: str, domain_id: str, token: str
    ) -> Response:
        """
        Removes all child groups from the specified group within a domain.
        
        Args:
            group_id: The unique identifier of the group.
            domain_id: The unique identifier of the domain.
            token: Authorization token.
            
        Returns:
            A promise that resolves to the removal response.
            
        Raises:
            Exception: If the child groups cannot be removed.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.groups_url + '/',
            f"{domain_id}/{self.groups_endpoint}/{group_id}/children/all"
        )
        
        try:
            response = requests.delete(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Response(
                status=response.status_code,
                message="All children removed successfully"
            )
        except requests.RequestException as error:
            raise error

    def list_children_groups(
        self, group_id: str, domain_id: str, query_params: PageMetadata, token: str
    ) -> GroupsPage:
        """
        Retrieves a paginated list of a group's child groups.
        
        Args:
            group_id: The unique identifier of the group.
            query_params: The query parameters for pagination (e.g., offset and limit).
            domain_id: The unique identifier of the domain.
            token: Authorization token.
            
        Returns:
            A paginated list of the group's child groups.
            
        Raises:
            Exception: If the child groups cannot be retrieved.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        string_params = {
            key: str(value) for key, value in query_params.items() if value is not None
        }

        url = urljoin(
            self.groups_url + '/',
            f"{domain_id}/{self.groups_endpoint}/{group_id}/children?{urlencode(string_params)}"
        )
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return GroupsPage(**response.json())
        except requests.RequestException as error:
            raise error

    def list_group_actions(self, domain_id: str, token: str) -> List[str]:
        """
        Lists all available actions for groups within a specified domain.
        
        Args:
            domain_id: The unique identifier of the domain.
            token: Authorization token.
            
        Returns:
            A promise that resolves to an array of available actions.
            
        Raises:
            Exception: If the actions cannot be retrieved.
        """
        try:
            actions = self.group_roles.list_available_actions(
                self.groups_url,
                f"{domain_id}/{self.groups_endpoint}",
                token
            )
            return actions
        except Exception as error:
            raise error

    def create_group_role(
        self,
        group_id: str,
        domain_id: str,
        role_name: str,
        token: str,
        optional_actions: Optional[List[str]] = None,
        optional_members: Optional[List[str]] = None
    ) -> Role:
        """
        Creates a new role within a specific group and domain, with optional actions and members.
        
        Args:
            group_id: The unique identifier of the group.
            domain_id: The unique identifier of the domain.
            role_name: The name of the role to be created.
            token: Authorization token.
            optional_actions: Optional list of actions for the role.
            optional_members: Optional list of members for the role.
            
        Returns:
            A promise that resolves to the created role object.
            
        Raises:
            Exception: If the role cannot be created.
        """
        try:
            role = self.group_roles.create_role(
                self.groups_url,
                f"{domain_id}/{self.groups_endpoint}",
                group_id,
                role_name,
                token,
                optional_actions,
                optional_members
            )
            return role
        except Exception as error:
            raise error

    def list_group_roles(
        self, group_id: str, domain_id: str, query_params: PageMetadata, token: str
    ) -> RolePage:
        """
        Retrieves a paginated list of roles for a specific group within a domain.
        
        Args:
            group_id: The unique identifier of the group.
            domain_id: The unique identifier of the domain.
            query_params: Pagination and query metadata.
            token: Authorization token.
            
        Returns:
            A promise that resolves to a paginated list of roles.
            
        Raises:
            Exception: If the roles cannot be retrieved.
        """
        try:
            roles_page = self.group_roles.list_roles(
                self.groups_url,
                f"{domain_id}/{self.groups_endpoint}",
                group_id,
                query_params,
                token
            )
            return roles_page
        except Exception as error:
            raise error

    def view_group_role(
        self, group_id: str, domain_id: str, role_id: str, token: str
    ) -> Role:
        """
        Retrieves the details of a specific role within a group and domain.
        
        Args:
            group_id: The unique identifier of the group.
            domain_id: The unique identifier of the domain.
            role_id: The unique identifier of the role.
            token: Authorization token.
            
        Returns:
            A promise that resolves to the role details.
            
        Raises:
            Exception: If the role details cannot be retrieved.
        """
        try:
            role = self.group_roles.view_role(
                self.groups_url,
                f"{domain_id}/{self.groups_endpoint}",
                group_id,
                role_id,
                token
            )
            return role
        except Exception as error:
            raise error

    def update_group_role(
        self, group_id: str, domain_id: str, role_id: str, role: Role, token: str
    ) -> Role:
        """
        Updates an existing role within a group and domain.
        
        Args:
            group_id: The unique identifier of the group.
            domain_id: The unique identifier of the domain.
            role_id: The unique identifier of the role.
            role: The updated role object.
            token: Authorization token.
            
        Returns:
            A promise that resolves to the updated role object.
            
        Raises:
            Exception: If the role cannot be updated.
        """
        try:
            updated_role = self.group_roles.update_role(
                self.groups_url,
                f"{domain_id}/{self.groups_endpoint}",
                group_id,
                role_id,
                role,
                token
            )
            return updated_role
        except Exception as error:
            raise error

    def delete_group_role(
        self, group_id: str, domain_id: str, role_id: str, token: str
    ) -> Response:
        """
        Deletes a role within a specific group and domain.
        
        Args:
            group_id: The unique identifier of the group.
            domain_id: The unique identifier of the domain.
            role_id: The unique identifier of the role.
            token: Authorization token.
            
        Returns:
            A promise that resolves to the deletion response.
            
        Raises:
            Exception: If the role cannot be deleted.
        """
        try:
            response = self.group_roles.delete_role(
                self.groups_url,
                f"{domain_id}/{self.groups_endpoint}",
                group_id,
                role_id,
                token
            )
            return response
        except Exception as error:
            raise error

    def add_group_role_actions(
        self, group_id: str, domain_id: str, role_id: str, actions: List[str], token: str
    ) -> List[str]:
        """
        Adds actions to a specific role within a group and domain.
        
        Args:
            group_id: The unique identifier of the group.
            domain_id: The unique identifier of the domain.
            role_id: The unique identifier of the role.
            actions: List of actions to add.
            token: Authorization token.
            
        Returns:
            A promise that resolves to the update response.
            
        Raises:
            Exception: If the actions cannot be added.
        """
        try:
            response = self.group_roles.add_role_actions(
                self.groups_url,
                f"{domain_id}/{self.groups_endpoint}",
                group_id,
                role_id,
                actions,
                token
            )
            return response
        except Exception as error:
            raise error

    def list_group_role_actions(
        self, group_id: str, domain_id: str, role_id: str, token: str
    ) -> List[str]:
        """
        Lists all actions associated with a specific role within a group and domain.
        
        Args:
            group_id: The unique identifier of the group.
            domain_id: The unique identifier of the domain.
            role_id: The unique identifier of the role.
            token: Authorization token.
            
        Returns:
            A promise that resolves to a list of actions.
            
        Raises:
            Exception: If the actions cannot be retrieved.
        """
        try:
            updated_role = self.group_roles.list_role_actions(
                self.groups_url,
                f"{domain_id}/{self.groups_endpoint}",
                group_id,
                role_id,
                token
            )
            return updated_role
        except Exception as error:
            raise error

    def delete_group_role_actions(
        self, group_id: str, domain_id: str, role_id: str, actions: List[str], token: str
    ) -> Response:
        """
        Removes specific actions from a role within a group and domain.
        
        Args:
            group_id: The unique identifier of the group.
            domain_id: The unique identifier of the domain.
            role_id: The unique identifier of the role.
            actions: List of actions to remove.
            token: Authorization token.
            
        Returns:
            A promise that resolves to the deletion response.
            
        Raises:
            Exception: If the actions cannot be removed.
        """
        try:
            response = self.group_roles.delete_role_actions(
                self.groups_url,
                f"{domain_id}/{self.groups_endpoint}",
                group_id,
                role_id,
                actions,
                token
            )
            return response
        except Exception as error:
            raise error

    def delete_all_group_role_actions(
        self, group_id: str, domain_id: str, role_id: str, token: str
    ) -> Response:
        """
        Removes all actions from a role within a group and domain.
        
        Args:
            group_id: The unique identifier of the group.
            domain_id: The unique identifier of the domain.
            role_id: The unique identifier of the role.
            token: Authorization token.
            
        Returns:
            A promise that resolves to the deletion response.
            
        Raises:
            Exception: If the actions cannot be removed.
        """
        try:
            response = self.group_roles.delete_all_role_actions(
                self.groups_url,
                f"{domain_id}/{self.groups_endpoint}",
                group_id,
                role_id,
                token
            )
            return response
        except Exception as error:
            raise error

    def add_group_role_members(
        self, group_id: str, domain_id: str, role_id: str, members: List[str], token: str
    ) -> List[str]:
        """
        Adds members to a specific role within a group and domain.
        
        Args:
            group_id: The unique identifier of the group.
            domain_id: The unique identifier of the domain.
            role_id: The unique identifier of the role.
            members: List of members to add.
            token: Authorization token.
            
        Returns:
            A promise that resolves to the updated list of members.
            
        Raises:
            Exception: If the members cannot be added.
        """
        try:
            response = self.group_roles.add_role_members(
                self.groups_url,
                f"{domain_id}/{self.groups_endpoint}",
                group_id,
                role_id,
                members,
                token
            )
            return response
        except Exception as error:
            raise error

    def list_group_role_members(
        self,
        group_id: str,
        domain_id: str,
        role_id: str,
        query_params: BasicPageMeta,
        token: str
    ) -> MembersPage:
        """
        Lists all members associated with a specific role within a group and domain.
        
        Args:
            group_id: The unique identifier of the group.
            domain_id: The unique identifier of the domain.
            role_id: The unique identifier of the role.
            query_params: Pagination and query metadata.
            token: Authorization token.
            
        Returns:
            A promise that resolves to a list of members.
            
        Raises:
            Exception: If the members cannot be retrieved.
        """
        try:
            updated_role = self.group_roles.list_role_members(
                self.groups_url,
                f"{domain_id}/{self.groups_endpoint}",
                group_id,
                role_id,
                query_params,
                token
            )
            return updated_role
        except Exception as error:
            raise error

    def delete_group_role_members(
        self, group_id: str, domain_id: str, role_id: str, members: List[str], token: str
    ) -> Response:
        """
        Removes specific members from a role within a group and domain.
        
        Args:
            group_id: The unique identifier of the group.
            domain_id: The unique identifier of the domain.
            role_id: The unique identifier of the role.
            members: List of members to remove.
            token: Authorization token.
            
        Returns:
            A promise that resolves to the deletion response.
            
        Raises:
            Exception: If the members cannot be removed.
        """
        try:
            response = self.group_roles.delete_role_members(
                self.groups_url,
                f"{domain_id}/{self.groups_endpoint}",
                group_id,
                role_id,
                members,
                token
            )
            return response
        except Exception as error:
            raise error

    def delete_all_group_role_members(
        self, group_id: str, domain_id: str, role_id: str, token: str
    ) -> Response:
        """
        Removes all members from a role within a group and domain.
        
        Args:
            group_id: The unique identifier of the group.
            domain_id: The unique identifier of the domain.
            role_id: The unique identifier of the role.
            token: Authorization token.
            
        Returns:
            A promise that resolves to the deletion response.
            
        Raises:
            Exception: If the members cannot be removed.
        """
        try:
            response = self.group_roles.delete_all_role_members(
                self.groups_url,
                f"{domain_id}/{self.groups_endpoint}",
                group_id,
                role_id,
                token
            )
            return response
        except Exception as error:
            raise error

    def list_group_members(
        self,
        group_id: str,
        domain_id: str,
        query_params: BasicPageMeta,
        token: str
    ) -> MemberRolesPage:
        """
        Lists all members associated with a group.
        
        Args:
            group_id: The unique identifier of the group.
            domain_id: The unique ID of the domain.
            token: Authorization token.
            
        Returns:
            A promise that resolves with a page of members.
            
        Raises:
            Exception: If members cannot be retrieved.
        """
        try:
            members = self.group_roles.list_entity_members(
                self.groups_url,
                f"{domain_id}/{self.groups_endpoint}",
                group_id,
                query_params,
                token
            )
            return members
        except Exception as error:
            raise error