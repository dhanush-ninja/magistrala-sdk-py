# Copyright (c) Abstract Machines
# SPDX-License-Identifier: Apache-2.0

import json
from typing import List, Optional
from urllib.parse import urljoin, urlencode

import requests

from .errors import Errors
from .roles import Roles
from .defs import (
    Client,
    ClientsPage,
    Response,
    PageMetadata,
    Role,
    RolePage,
    BasicPageMeta,
    MemberRolesPage,
    MembersPage,
    QueryParamRoles,
)


class Clients:
    """
    Handles interactions with the clients API, including creating, updating, and managing clients, roles, and permissions.
    """

    def __init__(self, clients_url: str):
        """
        Initializes the Clients API client.
        
        Args:
            clients_url: Base URL for the clients API.
        """
        self.clients_url = clients_url.rstrip('/')
        self.content_type = "application/json"
        self.clients_endpoint = "clients"
        self.client_roles = Roles()

    def create_client(self, client: Client, domain_id: str, token: str) -> Client:
        """
        Creates a new client.
        
        Args:
            client: Client object containing details like name and metadata.
            domain_id: The unique ID of the domain.
            token: Authorization token.
            
        Returns:
            The created client object.
            
        Raises:
            Exception: If the client cannot be created.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(self.clients_url + '/', f"{domain_id}/{self.clients_endpoint}")
        
        try:
            response = requests.post(
                url,
                headers=headers,
                data=json.dumps(client.dict() if hasattr(client, 'dict') else client),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Client(**response.json())
        except requests.RequestException as error:
            raise error

    def create_clients(
        self, clients: List[Client], domain_id: str, token: str
    ) -> ClientsPage:
        """
        Creates multiple new clients.
        
        Args:
            clients: An array of client objects, each containing details like name, metadata, and tags.
            domain_id: The unique ID of the domain.
            token: Authorization token.
            
        Returns:
            A page of clients.
            
        Raises:
            Exception: If the clients cannot be created.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(self.clients_url + '/', f"{domain_id}/{self.clients_endpoint}/bulk")
        
        try:
            clients_data = [
                client.dict() if hasattr(client, 'dict') else client
                for client in clients
            ]
            
            response = requests.post(
                url,
                headers=headers,
                data=json.dumps(clients_data),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return ClientsPage(**response.json())
        except requests.RequestException as error:
            raise error

    def enable(self, client_id: str, domain_id: str, token: str) -> Client:
        """
        Enables a previously disabled client by its ID.
        
        Args:
            client_id: The unique ID of the client.
            domain_id: The unique ID of the domain.
            token: Authorization token.
            
        Returns:
            The updated client object with enabled status.
            
        Raises:
            Exception: If the client cannot be enabled.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.clients_url + '/',
            f"{domain_id}/{self.clients_endpoint}/{client_id}/enable"
        )
        
        try:
            response = requests.post(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Client(**response.json())
        except requests.RequestException as error:
            raise error

    def disable(self, client_id: str, domain_id: str, token: str) -> Client:
        """
        Disables an enabled client by its ID.
        
        Args:
            client_id: The unique ID of the client.
            domain_id: The unique ID of the domain.
            token: Authorization token.
            
        Returns:
            The updated client object with disabled status.
            
        Raises:
            Exception: If the client cannot be disabled.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.clients_url + '/',
            f"{domain_id}/{self.clients_endpoint}/{client_id}/disable"
        )
        
        try:
            response = requests.post(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Client(**response.json())
        except requests.RequestException as error:
            raise error

    def update_client(self, client: Client, domain_id: str, token: str) -> Client:
        """
        Updates the information of an existing client.
        
        Args:
            client: The client object.
            domain_id: The unique identifier of the domain.
            token: Authorization token.
            
        Returns:
            The updated client object.
            
        Raises:
            Exception: If the client cannot be updated.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.clients_url + '/',
            f"{domain_id}/{self.clients_endpoint}/{client.id}"
        )
        
        try:
            response = requests.patch(
                url,
                headers=headers,
                data=json.dumps(client.dict() if hasattr(client, 'dict') else client),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Client(**response.json())
        except requests.RequestException as error:
            raise error

    def update_client_secret(
        self, client: Client, domain_id: str, token: str
    ) -> Client:
        """
        Updates an existing client's secret.
        
        Args:
            domain_id: The unique ID of the domain.
            client: Client object with updated secret.
            token: Authorization token.
            
        Returns:
            The updated client object.
            
        Raises:
            Exception: If the client secret cannot be updated.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        secret = client.credentials.secret if client.credentials else None
        url = urljoin(
            self.clients_url + '/',
            f"{domain_id}/{self.clients_endpoint}/{client.id}/secret"
        )
        
        try:
            response = requests.patch(
                url,
                headers=headers,
                data=json.dumps({"secret": secret}),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Client(**response.json())
        except requests.RequestException as error:
            raise error

    def update_client_tags(
        self, client: Client, domain_id: str, token: str
    ) -> Client:
        """
        Updates an existing client's tags.
        
        Args:
            client: Client object with updated tags.
            domain_id: The unique ID of the domain.
            token: Authorization token.
            
        Returns:
            The updated client object.
            
        Raises:
            Exception: If the client tags cannot be updated.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.clients_url + '/',
            f"{domain_id}/{self.clients_endpoint}/{client.id}/tags"
        )
        
        try:
            response = requests.patch(
                url,
                headers=headers,
                data=json.dumps(client.dict() if hasattr(client, 'dict') else client),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Client(**response.json())
        except requests.RequestException as error:
            raise error

    def client(
        self,
        client_id: str,
        domain_id: str,
        token: str,
        list_roles: Optional[bool] = None
    ) -> Client:
        """
        Retrieves a client by its id.
        
        Args:
            client_id: The unique ID of the client.
            domain_id: The unique ID of the domain.
            token: Authorization token.
            list_roles: Whether to include roles in the response.
            
        Returns:
            The requested client object.
            
        Raises:
            Exception: If the client cannot be fetched.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.clients_url + '/',
            f"{domain_id}/{self.clients_endpoint}/{client_id}"
        )
        
        if list_roles is not None:
            url += f"?{QueryParamRoles}={str(list_roles).lower()}"
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Client(**response.json())
        except requests.RequestException as error:
            raise error

    def clients(
        self, query_params: PageMetadata, domain_id: str, token: str
    ) -> ClientsPage:
        """
        Retrieves all clients matching the provided query parameters.
        
        Args:
            query_params: Query parameters for the request.
            domain_id: The unique ID of the domain.
            token: Authorization token.
            
        Returns:
            A page of clients.
            
        Raises:
            Exception: If the clients cannot be fetched.
        """
        string_params = {
            key: str(value) for key, value in query_params.items() if value is not None
        }

        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.clients_url + '/',
            f"{domain_id}/{self.clients_endpoint}?{urlencode(string_params)}"
        )
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return ClientsPage(**response.json())
        except requests.RequestException as error:
            raise error

    def set_client_parent_group(
        self, domain_id: str, client_id: str, parent_group_id: str, token: str
    ) -> Response:
        """
        Sets parent to a client.
        
        Args:
            domain_id: The unique ID of the domain.
            client_id: The unique ID of the client to be updated.
            parent_group_id: The unique ID of the group to be set as the parent.
            token: Authorization token.
            
        Returns:
            A promise that resolves when the parent group is successfully set for the specified client.
            
        Raises:
            Exception: If the parent group cannot be set for the client.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.clients_url + '/',
            f"{domain_id}/{self.clients_endpoint}/{client_id}/parent"
        )
        
        try:
            response = requests.post(
                url,
                headers=headers,
                data=json.dumps({"parent_group_id": parent_group_id}),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Response(
                status=response.status_code,
                message="Client group parent added successfully"
            )
        except requests.RequestException as error:
            raise error

    def delete_client_parent_group(
        self, domain_id: str, client_id: str, token: str
    ) -> Response:
        """
        Removes the parent group from a specified client.
        
        Args:
            domain_id: The unique ID of the domain.
            client_id: The unique ID of the client.
            token: Authorization token.
            
        Returns:
            A promise that resolves when the parent group is successfully removed from the specified client.
            
        Raises:
            Exception: If the parent group cannot be removed from the client.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.clients_url + '/',
            f"{domain_id}/{self.clients_endpoint}/{client_id}/parent"
        )
        
        try:
            response = requests.delete(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Response(
                status=response.status_code,
                message="Client group parent deleted successfully"
            )
        except requests.RequestException as error:
            raise error

    def delete_client(self, client_id: str, domain_id: str, token: str) -> Response:
        """
        Deletes a client with specified id.
        
        Args:
            client_id: The unique ID of the client.
            domain_id: The unique ID of the domain.
            token: Authorization token.
            
        Returns:
            A promise that resolves when the client is deleted.
            
        Raises:
            Exception: If the client cannot be deleted.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.clients_url + '/',
            f"{domain_id}/{self.clients_endpoint}/{client_id}"
        )
        
        try:
            response = requests.delete(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Response(
                status=response.status_code,
                message="Client deleted successfully"
            )
        except requests.RequestException as error:
            raise error

    def list_client_actions(self, domain_id: str, token: str) -> List[str]:
        """
        Lists all actions available to a specific client.
        
        Args:
            domain_id: The unique identifier of the domain.
            token: Authorization token.
            
        Returns:
            A promise that resolves with an array of actions.
            
        Raises:
            Exception: If client actions cannot be fetched.
        """
        try:
            actions = self.client_roles.list_available_actions(
                self.clients_url,
                f"{domain_id}/{self.clients_endpoint}",
                token
            )
            return actions
        except Exception as error:
            raise error

    def create_client_role(
        self,
        client_id: str,
        role_name: str,
        domain_id: str,
        token: str,
        optional_actions: Optional[List[str]] = None,
        optional_members: Optional[List[str]] = None
    ) -> Role:
        """
        Creates a new role within a specific client.
        
        Args:
            client_id: The unique identifier of the client.
            domain_id: The unique ID of the domain.
            role_name: The name of the role to create.
            token: Authorization token.
            optional_actions: Optional actions assigned to the role.
            optional_members: Optional members assigned to the role.
            
        Returns:
            A promise that resolves with the role created.
            
        Raises:
            Exception: If the role cannot be created or already exists.
        """
        try:
            role = self.client_roles.create_role(
                self.clients_url,
                f"{domain_id}/{self.clients_endpoint}",
                client_id,
                role_name,
                token,
                optional_actions,
                optional_members
            )
            return role
        except Exception as error:
            raise error

    def list_client_roles(
        self, client_id: str, domain_id: str, query_params: PageMetadata, token: str
    ) -> RolePage:
        """
        Lists all roles within a specific client.
        
        Args:
            client_id: The unique identifier of the client.
            domain_id: The unique ID of the domain.
            query_params: Metadata for pagination or filters.
            token: Authorization token.
            
        Returns:
            A promise that resolves with a page of roles in the domain.
            
        Raises:
            Exception: If the client is invalid or roles cannot be fetched.
        """
        try:
            roles_page = self.client_roles.list_roles(
                self.clients_url,
                f"{domain_id}/{self.clients_endpoint}",
                client_id,
                query_params,
                token
            )
            return roles_page
        except Exception as error:
            raise error

    def view_client_role(
        self, client_id: str, domain_id: str, role_id: str, token: str
    ) -> Role:
        """
        Retrieves details about a specific role in a client.
        
        Args:
            client_id: The unique identifier of the client.
            domain_id: The unique ID of the domain.
            role_id: The unique identifier of the role.
            token: Authorization token.
            
        Returns:
            A promise that resolves with the role details.
            
        Raises:
            Exception: If the role does not exist or cannot be retrieved.
        """
        try:
            role = self.client_roles.view_role(
                self.clients_url,
                f"{domain_id}/{self.clients_endpoint}",
                client_id,
                role_id,
                token
            )
            return role
        except Exception as error:
            raise error

    def update_client_role(
        self, client_id: str, domain_id: str, role_id: str, role: Role, token: str
    ) -> Role:
        """
        Updates the details of a specific role in a client.
        
        Args:
            client_id: The unique identifier of the client.
            domain_id: The unique ID of the domain.
            role_id: The unique identifier of the role.
            role: The role to be updated.
            token: Authorization token.
            
        Returns:
            A promise that resolves with the updated role.
            
        Raises:
            Exception: If the role cannot be updated.
        """
        try:
            updated_role = self.client_roles.update_role(
                self.clients_url,
                f"{domain_id}/{self.clients_endpoint}",
                client_id,
                role_id,
                role,
                token
            )
            return updated_role
        except Exception as error:
            raise error

    def delete_client_role(
        self, client_id: str, domain_id: str, role_id: str, token: str
    ) -> Response:
        """
        Deletes a specific role from a client.
        
        Args:
            client_id: The unique identifier of the client.
            domain_id: The unique ID of the domain.
            role_id: The unique identifier of the role.
            token: Authorization token.
            
        Returns:
            A promise that resolves when the role is deleted.
            
        Raises:
            Exception: If the role cannot be deleted.
        """
        try:
            response = self.client_roles.delete_role(
                self.clients_url,
                f"{domain_id}/{self.clients_endpoint}",
                client_id,
                role_id,
                token
            )
            return response
        except Exception as error:
            raise error

    def add_client_role_actions(
        self, client_id: str, domain_id: str, role_id: str, actions: List[str], token: str
    ) -> List[str]:
        """
        Adds actions to a specific role in a client.
        
        Args:
            client_id: The unique identifier of the client.
            domain_id: The unique ID of the domain.
            role_id: The unique identifier of the role.
            token: Authorization token.
            actions: The actions to add to the role.
            
        Returns:
            A promise that resolves with an array of actions.
            
        Raises:
            Exception: If the actions cannot be added.
        """
        try:
            response = self.client_roles.add_role_actions(
                self.clients_url,
                f"{domain_id}/{self.clients_endpoint}",
                client_id,
                role_id,
                actions,
                token
            )
            return response
        except Exception as error:
            raise error

    def list_client_role_actions(
        self, client_id: str, domain_id: str, role_id: str, token: str
    ) -> List[str]:
        """
        Lists all actions associated with a specific role in a client.
        
        Args:
            client_id: The unique identifier of the client.
            domain_id: The unique ID of the domain.
            role_id: The unique identifier of the role.
            token: Authorization token.
            
        Returns:
            A promise that resolves with an array of actions.
            
        Raises:
            Exception: If actions cannot be retrieved.
        """
        try:
            updated_role = self.client_roles.list_role_actions(
                self.clients_url,
                f"{domain_id}/{self.clients_endpoint}",
                client_id,
                role_id,
                token
            )
            return updated_role
        except Exception as error:
            raise error

    def delete_client_role_actions(
        self, client_id: str, domain_id: str, role_id: str, actions: List[str], token: str
    ) -> Response:
        """
        Deletes specific actions from a role in a client.
        
        Args:
            client_id: The unique identifier of the client.
            domain_id: The unique ID of the domain.
            role_id: The unique identifier of the role.
            actions: The actions to delete from the role.
            token: Authorization token.
            
        Returns:
            A promise that resolves when actions are deleted.
            
        Raises:
            Exception: If the actions cannot be deleted.
        """
        try:
            response = self.client_roles.delete_role_actions(
                self.clients_url,
                f"{domain_id}/{self.clients_endpoint}",
                client_id,
                role_id,
                actions,
                token
            )
            return response
        except Exception as error:
            raise error

    def delete_all_client_role_actions(
        self, client_id: str, domain_id: str, role_id: str, token: str
    ) -> Response:
        """
        Deletes all actions associated with a specific role in a client.
        
        Args:
            client_id: The unique identifier of the client.
            domain_id: The unique ID of the domain.
            role_id: The unique identifier of the role.
            token: Authorization token.
            
        Returns:
            A promise that resolves when all actions are deleted.
            
        Raises:
            Exception: If the actions cannot be deleted.
        """
        try:
            response = self.client_roles.delete_all_role_actions(
                self.clients_url,
                f"{domain_id}/{self.clients_endpoint}",
                client_id,
                role_id,
                token
            )
            return response
        except Exception as error:
            raise error

    def add_client_role_members(
        self, client_id: str, domain_id: str, role_id: str, members: List[str], token: str
    ) -> List[str]:
        """
        Adds members to a specific role in a client.
        
        Args:
            client_id: The unique identifier of the client.
            domain_id: The unique ID of the domain.
            role_id: The unique identifier of the role.
            members: The IDs of the members to add.
            token: Authorization token.
            
        Returns:
            A promise that resolves with an array of member ids.
            
        Raises:
            Exception: If the members cannot be added.
        """
        try:
            response = self.client_roles.add_role_members(
                self.clients_url,
                f"{domain_id}/{self.clients_endpoint}",
                client_id,
                role_id,
                members,
                token
            )
            return response
        except Exception as error:
            raise error

    def list_client_role_members(
        self,
        client_id: str,
        domain_id: str,
        role_id: str,
        query_params: BasicPageMeta,
        token: str
    ) -> MembersPage:
        """
        Lists all members associated with a specific role in a client.
        
        Args:
            client_id: The unique identifier of the client.
            domain_id: The unique ID of the domain.
            role_id: The unique identifier of the role.
            token: Authorization token.
            
        Returns:
            A promise that resolves with an array of member ids.
            
        Raises:
            Exception: If members cannot be retrieved.
        """
        try:
            updated_role = self.client_roles.list_role_members(
                self.clients_url,
                f"{domain_id}/{self.clients_endpoint}",
                client_id,
                role_id,
                query_params,
                token
            )
            return updated_role
        except Exception as error:
            raise error

    def delete_client_role_members(
        self, client_id: str, domain_id: str, role_id: str, members: List[str], token: str
    ) -> Response:
        """
        Deletes specific members from a role in a client.
        
        Args:
            client_id: The unique identifier of the client.
            domain_id: The unique ID of the domain.
            role_id: The unique identifier of the role.
            members: The IDs of the members to delete.
            token: Authorization token.
            
        Returns:
            A promise that resolves when members are deleted.
            
        Raises:
            Exception: If the members cannot be deleted.
        """
        try:
            response = self.client_roles.delete_role_members(
                self.clients_url,
                f"{domain_id}/{self.clients_endpoint}",
                client_id,
                role_id,
                members,
                token
            )
            return response
        except Exception as error:
            raise error

    def delete_all_client_role_members(
        self, client_id: str, domain_id: str, role_id: str, token: str
    ) -> Response:
        """
        Deletes all members associated with a specific role in a client.
        
        Args:
            client_id: The unique identifier of the client.
            domain_id: The unique ID of the domain.
            role_id: The unique identifier of the role.
            token: Authorization token.
            
        Returns:
            A promise that resolves when all members are deleted.
            
        Raises:
            Exception: If the members cannot be deleted.
        """
        try:
            response = self.client_roles.delete_all_role_members(
                self.clients_url,
                f"{domain_id}/{self.clients_endpoint}",
                client_id,
                role_id,
                token
            )
            return response
        except Exception as error:
            raise error

    def list_client_members(
        self,
        client_id: str,
        domain_id: str,
        query_params: BasicPageMeta,
        token: str
    ) -> MemberRolesPage:
        """
        Lists all members associated with a client.
        
        Args:
            client_id: The unique identifier of the client.
            domain_id: The unique ID of the domain.
            token: Authorization token.
            
        Returns:
            A promise that resolves with a page of members.
            
        Raises:
            Exception: If members cannot be retrieved.
        """
        try:
            members = self.client_roles.list_entity_members(
                self.clients_url,
                f"{domain_id}/{self.clients_endpoint}",
                client_id,
                query_params,
                token
            )
            return members
        except Exception as error:
            raise error