# Copyright (c) Abstract Machines
# SPDX-License-Identifier: Apache-2.0

import json
from typing import List, Optional
from urllib.parse import urljoin, urlencode

import requests

from .errors import Errors
from .defs import (
    Domain,
    PageMetadata,
    DomainsPage,
    Response,
    Role,
    BasicPageMeta,
    RolePage,
    MemberRolesPage,
    MembersPage,
    Invitation,
    InvitationsPage,
    InvitationPageMeta,
    QueryParamRoles,
)
from .roles import Roles


class Domains:
    """
    Handles interactions with the domains API, including creating, updating, and managing domains, roles, and permissions.
    """

    def __init__(self, domains_url: str):
        """
        Initializes the Domains API client.
        
        Args:
            domains_url: Base URL for the domains API.
        """
        self.domains_url = domains_url.rstrip('/')
        self.content_type = "application/json"
        self.domains_endpoint = "domains"
        self.invitations_endpoint = "invitations"
        self.domain_roles = Roles()

    def create_domain(self, domain: Domain, token: str) -> Domain:
        """
        Creates a new domain.
        
        Args:
            domain: Domain object containing details like name and route.
            token: Authorization token.
            
        Returns:
            The created domain object.
            
        Raises:
            Exception: If the domain cannot be created.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(self.domains_url + '/', self.domains_endpoint)
        
        try:
            response = requests.post(
                url,
                headers=headers,
                data=json.dumps(domain.dict() if hasattr(domain, 'dict') else domain),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Domain(**response.json())
        except requests.RequestException as error:
            raise error

    def update_domain(self, domain: Domain, token: str) -> Domain:
        """
        Updates an existing domain's details.
        
        Args:
            domain: Domain object with updated properties.
            token: Authorization token.
            
        Returns:
            The updated domain object.
            
        Raises:
            Exception: If the domain cannot be updated.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(self.domains_url + '/', f"{self.domains_endpoint}/{domain.id}")
        
        try:
            response = requests.patch(
                url,
                headers=headers,
                data=json.dumps(domain.dict() if hasattr(domain, 'dict') else domain),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Domain(**response.json())
        except requests.RequestException as error:
            raise error

    def domain(
        self, domain_id: str, token: str, list_roles: Optional[bool] = None
    ) -> Domain:
        """
        Retrieves a domain by its ID.
        
        Args:
            domain_id: The unique ID of the domain.
            token: Authorization token.
            list_roles: Whether to include roles in the response.
            
        Returns:
            The requested domain object.
            
        Raises:
            Exception: If the domain cannot be fetched.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(self.domains_url + '/', f"{self.domains_endpoint}/{domain_id}")
        
        if list_roles is not None:
            url += f"?{QueryParamRoles}={str(list_roles).lower()}"
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Domain(**response.json())
        except requests.RequestException as error:
            raise error

    def domains(self, query_params: PageMetadata, token: str) -> DomainsPage:
        """
        Retrieves all domains matching the provided query parameters.
        
        Args:
            query_params: Metadata for pagination or filters.
            token: Authorization token.
            
        Returns:
            A page of domains.
            
        Raises:
            Exception: If the domains cannot be fetched.
        """
        string_params = {
            key: str(value) for key, value in query_params.items() if value is not None
        }

        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.domains_url + '/', f"{self.domains_endpoint}?{urlencode(string_params)}"
        )
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return DomainsPage(**response.json())
        except requests.RequestException as error:
            raise error

    def list_user_domains(
        self, user_id: str, query_params: PageMetadata, token: str
    ) -> DomainsPage:
        """
        Retrieves all domains associated with a specific user.
        
        Args:
            user_id: The ID of the user.
            query_params: Metadata for pagination or filters.
            token: Authorization token.
            
        Returns:
            A page of domains associated with the user.
            
        Raises:
            Exception: If the domains of a user cannot be fetched.
        """
        string_params = {
            key: str(value) for key, value in query_params.items() if value is not None
        }

        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.domains_url + '/',
            f"users/{user_id}/domains?{urlencode(string_params)}"
        )
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return DomainsPage(**response.json())
        except requests.RequestException as error:
            raise error

    def enable_domain(self, domain_id: str, token: str) -> Response:
        """
        Enables a specific domain, making it active and accessible.
        
        Args:
            domain_id: The unique identifier of the domain to enable.
            token: Authorization token.
            
        Returns:
            A promise that resolves when the domain is enabled.
            
        Raises:
            Exception: If the domain cannot be enabled.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.domains_url + '/', f"{self.domains_endpoint}/{domain_id}/enable"
        )
        
        try:
            response = requests.post(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Response(
                status=response.status_code,
                message="Domain enabled successfully"
            )
        except requests.RequestException as error:
            raise error

    def disable_domain(self, domain_id: str, token: str) -> Response:
        """
        Disables a specific domain, making it inactive and inaccessible.
        
        Args:
            domain_id: The unique identifier of the domain to disable.
            token: Authorization token.
            
        Returns:
            A promise that resolves when the domain is disabled.
            
        Raises:
            Exception: If the domain cannot be disabled.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.domains_url + '/', f"{self.domains_endpoint}/{domain_id}/disable"
        )
        
        try:
            response = requests.post(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Response(
                status=response.status_code,
                message="Domain disabled successfully"
            )
        except requests.RequestException as error:
            raise error

    def freeze_domain(self, domain_id: str, token: str) -> Response:
        """
        Freezes the specified domain.
        
        Args:
            domain_id: The unique identifier of the domain to disable.
            token: Authorization token.
            
        Returns:
            A promise that resolves when the domain is frozen.
            
        Raises:
            Exception: If the domain cannot be frozen.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.domains_url + '/', f"{self.domains_endpoint}/{domain_id}/freeze"
        )
        
        try:
            response = requests.post(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Response(
                status=response.status_code,
                message="Domain frozen successfully"
            )
        except requests.RequestException as error:
            raise error

    def list_domain_actions(self, token: str) -> List[str]:
        """
        Lists all actions available in a specific domain.
        
        Args:
            token: Authorization token.
            
        Returns:
            A promise that resolves with an array of actions.
            
        Raises:
            Exception: If domain actions cannot be fetched.
        """
        try:
            actions = self.domain_roles.list_available_actions(
                self.domains_url,
                self.domains_endpoint,
                token
            )
            return actions
        except Exception as error:
            raise error

    def create_domain_role(
        self,
        domain_id: str,
        role_name: str,
        token: str,
        optional_actions: Optional[List[str]] = None,
        optional_members: Optional[List[str]] = None
    ) -> Role:
        """
        Creates a new role within a specific domain.
        
        Args:
            domain_id: The unique identifier of the domain.
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
            role = self.domain_roles.create_role(
                self.domains_url,
                self.domains_endpoint,
                domain_id,
                role_name,
                token,
                optional_actions,
                optional_members
            )
            return role
        except Exception as error:
            raise error

    def list_domain_roles(
        self, domain_id: str, query_params: PageMetadata, token: str
    ) -> RolePage:
        """
        Lists all roles within a specific domain.
        
        Args:
            domain_id: The unique identifier of the domain.
            query_params: Metadata for pagination or filters.
            token: Authorization token.
            
        Returns:
            A promise that resolves with a page of roles in the domain.
            
        Raises:
            Exception: If the domain_id is invalid or roles cannot be fetched.
        """
        try:
            roles_page = self.domain_roles.list_roles(
                self.domains_url,
                self.domains_endpoint,
                domain_id,
                query_params,
                token
            )
            return roles_page
        except Exception as error:
            raise error

    def view_domain_role(self, domain_id: str, role_id: str, token: str) -> Role:
        """
        Retrieves details about a specific role in a domain.
        
        Args:
            domain_id: The unique identifier of the domain.
            role_id: The unique identifier of the role.
            token: Authorization token.
            
        Returns:
            A promise that resolves with the role details.
            
        Raises:
            Exception: If the role does not exist or cannot be retrieved.
        """
        try:
            role = self.domain_roles.view_role(
                self.domains_url,
                self.domains_endpoint,
                domain_id,
                role_id,
                token
            )
            return role
        except Exception as error:
            raise error

    def update_domain_role(
        self, domain_id: str, role_id: str, role: Role, token: str
    ) -> Role:
        """
        Updates the details of a specific role in a domain.
        
        Args:
            domain_id: The unique identifier of the domain.
            role_id: The unique identifier of the role.
            role: The role to be updated.
            token: Authorization token.
            
        Returns:
            A promise that resolves with the updated role.
            
        Raises:
            Exception: If the role cannot be updated.
        """
        try:
            updated_role = self.domain_roles.update_role(
                self.domains_url,
                self.domains_endpoint,
                domain_id,
                role_id,
                role,
                token
            )
            return updated_role
        except Exception as error:
            raise error

    def delete_domain_role(self, domain_id: str, role_id: str, token: str) -> Response:
        """
        Deletes a specific role from a domain.
        
        Args:
            domain_id: The unique identifier of the domain.
            role_id: The unique identifier of the role.
            token: Authorization token.
            
        Returns:
            A promise that resolves when the role is deleted.
            
        Raises:
            Exception: If the role cannot be deleted.
        """
        try:
            response = self.domain_roles.delete_role(
                self.domains_url,
                self.domains_endpoint,
                domain_id,
                role_id,
                token
            )
            return response
        except Exception as error:
            raise error

    def add_domain_role_actions(
        self, domain_id: str, role_id: str, actions: List[str], token: str
    ) -> List[str]:
        """
        Adds actions to a specific role in a domain.
        
        Args:
            domain_id: The unique identifier of the domain.
            role_id: The unique identifier of the role.
            token: Authorization token.
            actions: The actions to add to the role.
            
        Returns:
            A promise that resolves with an array of actions.
            
        Raises:
            Exception: If the actions cannot be added.
        """
        try:
            response = self.domain_roles.add_role_actions(
                self.domains_url,
                self.domains_endpoint,
                domain_id,
                role_id,
                actions,
                token
            )
            return response
        except Exception as error:
            raise error

    def list_domain_role_actions(
        self, domain_id: str, role_id: str, token: str
    ) -> List[str]:
        """
        Lists all actions associated with a specific role in a domain.
        
        Args:
            domain_id: The unique identifier of the domain.
            role_id: The unique identifier of the role.
            token: Authorization token.
            
        Returns:
            A promise that resolves with an array of actions.
            
        Raises:
            Exception: If actions cannot be retrieved.
        """
        try:
            updated_role = self.domain_roles.list_role_actions(
                self.domains_url,
                self.domains_endpoint,
                domain_id,
                role_id,
                token
            )
            return updated_role
        except Exception as error:
            raise error

    def delete_domain_role_actions(
        self, domain_id: str, role_id: str, actions: List[str], token: str
    ) -> Response:
        """
        Deletes specific actions from a role in a domain.
        
        Args:
            domain_id: The unique identifier of the domain.
            role_id: The unique identifier of the role.
            actions: The actions to delete from the role.
            token: Authorization token.
            
        Returns:
            A promise that resolves when actions are deleted.
            
        Raises:
            Exception: If the actions cannot be deleted.
        """
        try:
            response = self.domain_roles.delete_role_actions(
                self.domains_url,
                self.domains_endpoint,
                domain_id,
                role_id,
                actions,
                token
            )
            return response
        except Exception as error:
            raise error

    def delete_all_domain_role_actions(
        self, domain_id: str, role_id: str, token: str
    ) -> Response:
        """
        Deletes all actions associated with a specific role in a domain.
        
        Args:
            domain_id: The unique identifier of the domain.
            role_id: The unique identifier of the role.
            token: Authorization token.
            
        Returns:
            A promise that resolves when all actions are deleted.
            
        Raises:
            Exception: If the actions cannot be deleted.
        """
        try:
            response = self.domain_roles.delete_all_role_actions(
                self.domains_url,
                self.domains_endpoint,
                domain_id,
                role_id,
                token
            )
            return response
        except Exception as error:
            raise error

    def add_domain_role_members(
        self, domain_id: str, role_id: str, members: List[str], token: str
    ) -> List[str]:
        """
        Adds members to a specific role in a domain.
        
        Args:
            domain_id: The unique identifier of the domain.
            role_id: The unique identifier of the role.
            members: The IDs of the members to add.
            token: Authorization token.
            
        Returns:
            A promise that resolves with an array of member ids.
            
        Raises:
            Exception: If the members cannot be added.
        """
        try:
            response = self.domain_roles.add_role_members(
                self.domains_url,
                self.domains_endpoint,
                domain_id,
                role_id,
                members,
                token
            )
            return response
        except Exception as error:
            raise error

    def list_domain_role_members(
        self, domain_id: str, role_id: str, query_params: BasicPageMeta, token: str
    ) -> MembersPage:
        """
        Lists all members associated with a specific role in a domain.
        
        Args:
            domain_id: The unique identifier of the domain.
            role_id: The unique identifier of the role.
            token: Authorization token.
            
        Returns:
            A promise that resolves with an array of member ids.
            
        Raises:
            Exception: If members cannot be retrieved.
        """
        try:
            updated_role = self.domain_roles.list_role_members(
                self.domains_url,
                self.domains_endpoint,
                domain_id,
                role_id,
                query_params,
                token
            )
            return updated_role
        except Exception as error:
            raise error

    def delete_domain_role_members(
        self, domain_id: str, role_id: str, members: List[str], token: str
    ) -> Response:
        """
        Deletes specific members from a role in a domain.
        
        Args:
            domain_id: The unique identifier of the domain.
            role_id: The unique identifier of the role.
            members: The IDs of the members to delete.
            token: Authorization token.
            
        Returns:
            A promise that resolves when members are deleted.
            
        Raises:
            Exception: If the members cannot be deleted.
        """
        try:
            response = self.domain_roles.delete_role_members(
                self.domains_url,
                self.domains_endpoint,
                domain_id,
                role_id,
                members,
                token
            )
            return response
        except Exception as error:
            raise error

    def delete_all_domain_role_members(
        self, domain_id: str, role_id: str, token: str
    ) -> Response:
        """
        Deletes all members associated with a specific role in a domain.
        
        Args:
            domain_id: The unique identifier of the domain.
            role_id: The unique identifier of the role.
            token: Authorization token.
            
        Returns:
            A promise that resolves when all members are deleted.
            
        Raises:
            Exception: If the members cannot be deleted.
        """
        try:
            response = self.domain_roles.delete_all_role_members(
                self.domains_url,
                self.domains_endpoint,
                domain_id,
                role_id,
                token
            )
            return response
        except Exception as error:
            raise error

    def list_domain_members(
        self, domain_id: str, query_params: BasicPageMeta, token: str
    ) -> MemberRolesPage:
        """
        Lists all members associated with a domain.
        
        Args:
            domain_id: The unique identifier of the domain.
            token: Authorization token.
            
        Returns:
            A promise that resolves with a page of members.
            
        Raises:
            Exception: If members cannot be retrieved.
        """
        try:
            members = self.domain_roles.list_entity_members(
                self.domains_url,
                self.domains_endpoint,
                domain_id,
                query_params,
                token
            )
            return members
        except Exception as error:
            raise error

    def send_invitation(
        self,
        user_id: str,
        domain_id: str,
        role_id: str,
        token: str,
        resend: Optional[bool] = None
    ) -> Response:
        """
        Sends an invitation to a given user.
        
        Args:
            user_id: The unique ID of the user.
            domain_id: The unique ID of the domain.
            role_id: The unique ID of the role.
            token: Authorization token.
            resend: Option to resend an invitation if it has been rejected.
            
        Returns:
            A promise that resolves when the invitation is sent.
            
        Raises:
            Exception: If the invitation cannot be sent.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        payload = {
            "invitee_user_id": user_id,
            "role_id": role_id,
        }
        
        if resend is not None:
            payload["resend"] = resend

        url = urljoin(
            self.domains_url + '/',
            f"{self.domains_endpoint}/{domain_id}/{self.invitations_endpoint}"
        )
        
        try:
            response = requests.post(
                url,
                headers=headers,
                data=json.dumps(payload),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Response(
                status=response.status_code,
                message="Invitation sent successfully"
            )
        except requests.RequestException as error:
            raise error

    def view_invitation(self, user_id: str, domain_id: str, token: str) -> Invitation:
        """
        Retrieves the invitation for the given user to a given domain.
        
        Args:
            user_id: The unique ID of the user.
            domain_id: The unique ID of the domain.
            token: Authorization token.
            
        Returns:
            The invitation object.
            
        Raises:
            Exception: If the invitation cannot be fetched.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.domains_url + '/',
            f"{self.domains_endpoint}/{domain_id}/{self.invitations_endpoint}/{user_id}"
        )
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Invitation(**response.json())
        except requests.RequestException as error:
            raise error

    def list_domain_invitations(
        self, query_params: InvitationPageMeta, domain_id: str, token: str
    ) -> InvitationsPage:
        """
        Retrieves all domain invitations matching the provided query parameters.
        
        Args:
            query_params: Query parameters for the request.
            domain_id: The unique ID of the domain.
            token: Authorization token.
            
        Returns:
            A page of domain invitations.
            
        Raises:
            Exception: If the domain invitations cannot be fetched.
        """
        string_params = {
            key: str(value) for key, value in query_params.items() if value is not None
        }

        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.domains_url + '/',
            f"{self.domains_endpoint}/{domain_id}/{self.invitations_endpoint}?{urlencode(string_params)}"
        )
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return InvitationsPage(**response.json())
        except requests.RequestException as error:
            raise error

    def list_user_invitations(
        self, query_params: PageMetadata, token: str
    ) -> InvitationsPage:
        """
        Retrieves all user invitations matching the provided query parameters.
        
        Args:
            query_params: Query parameters for the request.
            token: Authorization token.
            
        Returns:
            A page of user invitations.
            
        Raises:
            Exception: If the user invitations cannot be fetched.
        """
        string_params = {
            key: str(value) for key, value in query_params.items() if value is not None
        }

        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.domains_url + '/',
            f"{self.invitations_endpoint}?{urlencode(string_params)}"
        )
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return InvitationsPage(**response.json())
        except requests.RequestException as error:
            raise error

    def accept_invitation(self, domain_id: str, token: str) -> Response:
        """
        Accepts an invitation by adding the user to the domain that they were invited to.
        
        Args:
            domain_id: The unique ID of the domain.
            token: Authorization token.
            
        Returns:
            A promise that resolves when the invitation is accepted.
            
        Raises:
            Exception: If the invitations cannot be accepted.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(self.domains_url + '/', f"{self.invitations_endpoint}/accept")
        
        try:
            response = requests.post(
                url,
                headers=headers,
                data=json.dumps({"domain_id": domain_id}),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Response(
                status=response.status_code,
                message="Invitation accepted successfully"
            )
        except requests.RequestException as error:
            raise error

    def reject_invitation(self, domain_id: str, token: str) -> Response:
        """
        Rejects an invitation.
        
        Args:
            domain_id: The unique ID of the domain.
            token: Authorization token.
            
        Returns:
            A promise that resolves when the invitation is rejected.
            
        Raises:
            Exception: If the invitations cannot be rejected.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(self.domains_url + '/', f"{self.invitations_endpoint}/reject")
        
        try:
            response = requests.post(
                url,
                headers=headers,
                data=json.dumps({"domain_id": domain_id}),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Response(
                status=response.status_code,
                message="Invitation rejected successfully"
            )
        except requests.RequestException as error:
            raise error

    def delete_invitation(self, user_id: str, domain_id: str, token: str) -> Response:
        """
        Deletes an invitation.
        
        Args:
            user_id: The unique ID of the user.
            domain_id: The unique ID of the domain.
            token: Authorization token.
            
        Returns:
            A promise that resolves when the invitation is deleted.
            
        Raises:
            Exception: If the invitations cannot be deleted.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.domains_url + '/',
            f"{self.domains_endpoint}/{domain_id}/{self.invitations_endpoint}/{user_id}"
        )
        
        try:
            response = requests.delete(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Response(
                status=response.status_code,
                message="Invitation deleted successfully"
            )
        except requests.RequestException as error:
            raise error