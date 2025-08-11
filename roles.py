# Copyright (c) Abstract Machines
# SPDX-License-Identifier: Apache-2.0

import json
from typing import List, Optional
from urllib.parse import urljoin, urlencode

import requests

from .defs import (
    PageMetadata,
    Role,
    RolePage,
    Response,
    BasicPageMeta,
    MembersRolePageQuery,
    MemberRolesPage,
)
from .errors import Errors


class Roles:
    """
    Handles role management operations including creating, updating, and managing roles, actions, and members.
    """

    def __init__(self):
        """
        Initializes the Roles utility class.
        """
        self.content_type = "application/json"

    def list_available_actions(self, url: str, endpoint: str, token: str) -> List[str]:
        """
        Lists all available actions for a given endpoint.
        
        Args:
            url: Base URL for the API.
            endpoint: The API endpoint.
            token: Authorization token.
            
        Returns:
            List of available actions.
            
        Raises:
            Exception: If the actions cannot be retrieved.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        full_url = urljoin(url + '/', f"{endpoint}/roles/available-actions")
        
        try:
            response = requests.get(full_url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            actions_response = response.json()
            return actions_response.get("available_actions", [])
        except requests.RequestException as error:
            raise error

    def create_role(
        self,
        url: str,
        endpoint: str,
        entity_id: str,
        role_name: str,
        token: str,
        optional_actions: Optional[List[str]] = None,
        optional_members: Optional[List[str]] = None
    ) -> Role:
        """
        Creates a new role for an entity.
        
        Args:
            url: Base URL for the API.
            endpoint: The API endpoint.
            entity_id: The unique identifier of the entity.
            role_name: The name of the role to create.
            token: Authorization token.
            optional_actions: Optional list of actions for the role.
            optional_members: Optional list of members for the role.
            
        Returns:
            The created role object.
            
        Raises:
            Exception: If the role cannot be created.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        payload = {
            "role_name": role_name,
            "optional_actions": optional_actions,
            "optional_members": optional_members,
        }

        full_url = urljoin(url + '/', f"{endpoint}/{entity_id}/roles")
        
        try:
            response = requests.post(
                full_url,
                headers=headers,
                data=json.dumps(payload),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Role(**response.json())
        except requests.RequestException as error:
            raise error

    def list_roles(
        self, url: str, endpoint: str, entity_id: str, query_params: PageMetadata, token: str
    ) -> RolePage:
        """
        Lists all roles for an entity with pagination.
        
        Args:
            url: Base URL for the API.
            endpoint: The API endpoint.
            entity_id: The unique identifier of the entity.
            query_params: Pagination and query parameters.
            token: Authorization token.
            
        Returns:
            A page of roles.
            
        Raises:
            Exception: If the roles cannot be retrieved.
        """
        string_params = {
            key: str(value) for key, value in query_params.__dict__.items()
            if value is not None
        }

        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        full_url = urljoin(
            url + '/',
            f"{endpoint}/{entity_id}/roles?{urlencode(string_params)}"
        )
        
        try:
            response = requests.get(full_url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return RolePage(**response.json())
        except requests.RequestException as error:
            raise error

    def view_role(
        self, url: str, endpoint: str, entity_id: str, role_id: str, token: str
    ) -> Role:
        """
        Retrieves details of a specific role.
        
        Args:
            url: Base URL for the API.
            endpoint: The API endpoint.
            entity_id: The unique identifier of the entity.
            role_id: The unique identifier of the role.
            token: Authorization token.
            
        Returns:
            The role object.
            
        Raises:
            Exception: If the role cannot be retrieved.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        full_url = urljoin(url + '/', f"{endpoint}/{entity_id}/roles/{role_id}")
        
        try:
            response = requests.get(full_url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Role(**response.json())
        except requests.RequestException as error:
            raise error

    def update_role(
        self, url: str, endpoint: str, entity_id: str, role_id: str, role: Role, token: str
    ) -> Role:
        """
        Updates an existing role.
        
        Args:
            url: Base URL for the API.
            endpoint: The API endpoint.
            entity_id: The unique identifier of the entity.
            role_id: The unique identifier of the role.
            role: The updated role object.
            token: Authorization token.
            
        Returns:
            The updated role object.
            
        Raises:
            Exception: If the role cannot be updated.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        full_url = urljoin(url + '/', f"{endpoint}/{entity_id}/roles/{role_id}")
        
        try:
            response = requests.put(
                full_url,
                headers=headers,
                data=json.dumps(role.__dict__ if hasattr(role, '__dict__') else role),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Role(**response.json())
        except requests.RequestException as error:
            raise error

    def delete_role(
        self, url: str, endpoint: str, entity_id: str, role_id: str, token: str
    ) -> Response:
        """
        Deletes a role.
        
        Args:
            url: Base URL for the API.
            endpoint: The API endpoint.
            entity_id: The unique identifier of the entity.
            role_id: The unique identifier of the role.
            token: Authorization token.
            
        Returns:
            Response confirming deletion.
            
        Raises:
            Exception: If the role cannot be deleted.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        full_url = urljoin(url + '/', f"{endpoint}/{entity_id}/roles/{role_id}")
        
        try:
            response = requests.delete(full_url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Response(
                status=response.status_code,
                message="Role deleted successfully"
            )
        except requests.RequestException as error:
            raise error

    def add_role_actions(
        self, url: str, endpoint: str, entity_id: str, role_id: str, actions: List[str], token: str
    ) -> List[str]:
        """
        Adds actions to a role.
        
        Args:
            url: Base URL for the API.
            endpoint: The API endpoint.
            entity_id: The unique identifier of the entity.
            role_id: The unique identifier of the role.
            actions: List of actions to add.
            token: Authorization token.
            
        Returns:
            Updated list of actions.
            
        Raises:
            Exception: If the actions cannot be added.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        full_url = urljoin(url + '/', f"{endpoint}/{entity_id}/roles/{role_id}/actions")
        
        try:
            response = requests.post(
                full_url,
                headers=headers,
                data=json.dumps({"actions": actions}),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            add_action_response = response.json()
            return add_action_response.get("actions", [])
        except requests.RequestException as error:
            raise error

    def list_role_actions(
        self, url: str, endpoint: str, entity_id: str, role_id: str, token: str
    ) -> List[str]:
        """
        Lists all actions associated with a role.
        
        Args:
            url: Base URL for the API.
            endpoint: The API endpoint.
            entity_id: The unique identifier of the entity.
            role_id: The unique identifier of the role.
            token: Authorization token.
            
        Returns:
            List of actions.
            
        Raises:
            Exception: If the actions cannot be retrieved.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        full_url = urljoin(url + '/', f"{endpoint}/{entity_id}/roles/{role_id}/actions")
        
        try:
            response = requests.get(full_url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            actions_response = response.json()
            return actions_response.get("actions", [])
        except requests.RequestException as error:
            raise error

    def delete_role_actions(
        self, url: str, endpoint: str, entity_id: str, role_id: str, actions: List[str], token: str
    ) -> Response:
        """
        Deletes specific actions from a role.
        
        Args:
            url: Base URL for the API.
            endpoint: The API endpoint.
            entity_id: The unique identifier of the entity.
            role_id: The unique identifier of the role.
            actions: List of actions to delete.
            token: Authorization token.
            
        Returns:
            Response confirming deletion.
            
        Raises:
            Exception: If the actions cannot be deleted.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        full_url = urljoin(url + '/', f"{endpoint}/{entity_id}/roles/{role_id}/actions/delete")
        
        try:
            response = requests.post(
                full_url,
                headers=headers,
                data=json.dumps({"actions": actions}),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Response(
                status=response.status_code,
                message="Role actions deleted successfully"
            )
        except requests.RequestException as error:
            raise error

    def delete_all_role_actions(
        self, url: str, endpoint: str, entity_id: str, role_id: str, token: str
    ) -> Response:
        """
        Deletes all actions from a role.
        
        Args:
            url: Base URL for the API.
            endpoint: The API endpoint.
            entity_id: The unique identifier of the entity.
            role_id: The unique identifier of the role.
            token: Authorization token.
            
        Returns:
            Response confirming deletion.
            
        Raises:
            Exception: If the actions cannot be deleted.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        full_url = urljoin(url + '/', f"{endpoint}/{entity_id}/roles/{role_id}/actions/delete-all")
        
        try:
            response = requests.post(full_url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Response(
                status=response.status_code,
                message="Role actions deleted successfully"
            )
        except requests.RequestException as error:
            raise error

    def add_role_members(
        self, url: str, endpoint: str, entity_id: str, role_id: str, members: List[str], token: str
    ) -> List[str]:
        """
        Adds members to a role.
        
        Args:
            url: Base URL for the API.
            endpoint: The API endpoint.
            entity_id: The unique identifier of the entity.
            role_id: The unique identifier of the role.
            members: List of member IDs to add.
            token: Authorization token.
            
        Returns:
            Updated list of members.
            
        Raises:
            Exception: If the members cannot be added.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        full_url = urljoin(url + '/', f"{endpoint}/{entity_id}/roles/{role_id}/members")
        
        try:
            response = requests.post(
                full_url,
                headers=headers,
                data=json.dumps({"members": members}),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            add_members_response = response.json()
            return add_members_response.get("members", [])
        except requests.RequestException as error:
            raise error

    def list_role_members(
        self, url: str, endpoint: str, entity_id: str, role_id: str, query_params: BasicPageMeta, token: str
    ):
        """
        Lists all members associated with a role.
        
        Args:
            url: Base URL for the API.
            endpoint: The API endpoint.
            entity_id: The unique identifier of the entity.
            role_id: The unique identifier of the role.
            query_params: Pagination parameters.
            token: Authorization token.
            
        Returns:
            A page of members.
            
        Raises:
            Exception: If the members cannot be retrieved.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        string_params = {
            key: str(value) for key, value in query_params.__dict__.items()
            if value is not None
        }

        full_url = urljoin(
            url + '/',
            f"{endpoint}/{entity_id}/roles/{role_id}/members?{urlencode(string_params)}"
        )
        
        try:
            response = requests.get(full_url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return response.json()
        except requests.RequestException as error:
            raise error

    def delete_role_members(
        self, url: str, endpoint: str, entity_id: str, role_id: str, members: List[str], token: str
    ) -> Response:
        """
        Deletes specific members from a role.
        
        Args:
            url: Base URL for the API.
            endpoint: The API endpoint.
            entity_id: The unique identifier of the entity.
            role_id: The unique identifier of the role.
            members: List of member IDs to delete.
            token: Authorization token.
            
        Returns:
            Response confirming deletion.
            
        Raises:
            Exception: If the members cannot be deleted.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        full_url = urljoin(url + '/', f"{endpoint}/{entity_id}/roles/{role_id}/members/delete")
        
        try:
            response = requests.post(
                full_url,
                headers=headers,
                data=json.dumps({"members": members}),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Response(
                status=response.status_code,
                message="Role members deleted successfully"
            )
        except requests.RequestException as error:
            raise error

    def delete_all_role_members(
        self, url: str, endpoint: str, entity_id: str, role_id: str, token: str
    ) -> Response:
        """
        Deletes all members from a role.
        
        Args:
            url: Base URL for the API.
            endpoint: The API endpoint.
            entity_id: The unique identifier of the entity.
            role_id: The unique identifier of the role.
            token: Authorization token.
            
        Returns:
            Response confirming deletion.
            
        Raises:
            Exception: If the members cannot be deleted.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        full_url = urljoin(url + '/', f"{endpoint}/{entity_id}/roles/{role_id}/members/delete-all")
        
        try:
            response = requests.post(full_url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Response(
                status=response.status_code,
                message="Role members deleted successfully"
            )
        except requests.RequestException as error:
            raise error

    def list_entity_members(
        self, url: str, endpoint: str, entity_id: str, query_params: MembersRolePageQuery, token: str
    ) -> MemberRolesPage:
        """
        Lists all members associated with an entity across all roles.
        
        Args:
            url: Base URL for the API.
            endpoint: The API endpoint.
            entity_id: The unique identifier of the entity.
            query_params: Query and pagination parameters.
            token: Authorization token.
            
        Returns:
            A page of members with their roles.
            
        Raises:
            Exception: If the members cannot be retrieved.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        string_params = {
            key: str(value) for key, value in query_params.__dict__.items()
            if value is not None
        }

        full_url = urljoin(
            url + '/',
            f"{endpoint}/{entity_id}/roles/members?{urlencode(string_params)}"
        )
        
        try:
            response = requests.get(full_url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return MemberRolesPage(**response.json())
        except requests.RequestException as error:
            raise error