# Copyright (c) Abstract Machines
# SPDX-License-Identifier: Apache-2.0

import json
from typing import List, Optional
from urllib.parse import urljoin, urlencode

import requests

from .defs import PAT, PatPageMeta, PATsPage, Response, Scope, ScopesPage, ScopesPageMeta
from .errors import Errors


class PATs:
    """
    Handles interactions with the pats, including creating, updating, and managing pats.
    """

    def __init__(self, auth_url: str):
        """
        Initializes the pats client.
        
        Args:
            auth_url: Base URL for the pats API.
        """
        self.auth_url = auth_url.rstrip('/')
        self.content_type = "application/json"
        self.pats_endpoint = "pats"

    def create_pat(
        self, name: str, duration: str, token: str, description: Optional[str] = None
    ) -> PAT:
        """
        Creates a new Personal Access Token (PAT).
        
        Args:
            name: The name of the PAT.
            duration: The validity duration of the PAT (e.g., "24h").
            token: Authorization token.
            description: The description of the PAT.
            
        Returns:
            The created PAT object.
            
        Raises:
            Exception: If the PAT cannot be created.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        payload = {
            "name": name,
            "description": description,
            "duration": duration
        }

        url = urljoin(self.auth_url + '/', self.pats_endpoint)
        
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
            
            return PAT(**response.json())
        except requests.RequestException as error:
            raise error

    def list_pats(self, query_params: PatPageMeta, token: str) -> PATsPage:
        """
        Retrieves all Personal Access Tokens (PATs) matching the provided query parameters.
        
        Args:
            query_params: Metadata for pagination or filters.
            token: Authorization token.
            
        Returns:
            A page of PATs.
            
        Raises:
            Exception: If the PATs cannot be fetched.
        """
        string_params = {
            key: str(value) for key, value in query_params.__dict__.items()
            if value is not None
        }

        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.auth_url + '/',
            f"{self.pats_endpoint}?{urlencode(string_params)}"
        )
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return PATsPage(**response.json())
        except requests.RequestException as error:
            raise error

    def view_pat(self, pat_id: str, token: str) -> PAT:
        """
        Retrieves a Personal Access Token (PAT) by its ID.
        
        Args:
            pat_id: The unique ID of the PAT.
            token: Authorization token.
            
        Returns:
            The requested PAT object.
            
        Raises:
            Exception: If the PAT cannot be fetched.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(self.auth_url + '/', f"{self.pats_endpoint}/{pat_id}")
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return PAT(**response.json())
        except requests.RequestException as error:
            raise error

    def delete_all_pats(self, token: str) -> Response:
        """
        Deletes all Personal Access Tokens (PATs).
        
        Args:
            token: Authorization token.
            
        Returns:
            A promise that resolves when the PATs are deleted.
            
        Raises:
            Exception: If the PATs cannot be deleted.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(self.auth_url + '/', self.pats_endpoint)
        
        try:
            response = requests.delete(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Response(
                status=response.status_code,
                message="PATs deleted successfully"
            )
        except requests.RequestException as error:
            raise error

    def update_name(self, name: str, pat_id: str, token: str) -> PAT:
        """
        Updates the name of a Personal Access Token (PAT).
        
        Args:
            name: The new name for the PAT.
            pat_id: The unique ID of the PAT.
            token: Authorization token.
            
        Returns:
            The updated PAT object.
            
        Raises:
            Exception: If the PAT name cannot be updated.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(self.auth_url + '/', f"{self.pats_endpoint}/{pat_id}/name")
        
        try:
            response = requests.patch(
                url,
                headers=headers,
                data=json.dumps({"name": name}),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return PAT(**response.json())
        except requests.RequestException as error:
            raise error

    def update_description(self, description: str, pat_id: str, token: str) -> PAT:
        """
        Updates the description of a Personal Access Token (PAT).
        
        Args:
            description: The new description for the PAT.
            pat_id: The unique ID of the PAT.
            token: Authorization token.
            
        Returns:
            The updated PAT object.
            
        Raises:
            Exception: If the PAT description cannot be updated.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(self.auth_url + '/', f"{self.pats_endpoint}/{pat_id}/description")
        
        try:
            response = requests.patch(
                url,
                headers=headers,
                data=json.dumps({"description": description}),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return PAT(**response.json())
        except requests.RequestException as error:
            raise error

    def delete_pat(self, pat_id: str, token: str) -> Response:
        """
        Deletes a PAT with specified id.
        
        Args:
            pat_id: The unique ID of the PAT.
            token: Authorization token.
            
        Returns:
            A promise that resolves when the PAT is successfully deleted.
            
        Raises:
            Exception: If the PAT cannot be deleted.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(self.auth_url + '/', f"{self.pats_endpoint}/{pat_id}")
        
        try:
            response = requests.delete(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Response(
                status=response.status_code,
                message="PAT deleted successfully"
            )
        except requests.RequestException as error:
            raise error

    def reset_secret(self, duration: str, pat_id: str, token: str) -> PAT:
        """
        Resets the secret for a Personal Access Token (PAT).
        
        Args:
            duration: The duration for which the new secret will be valid.
            pat_id: The unique ID of the PAT.
            token: Authorization token.
            
        Returns:
            The updated PAT object with the new secret.
            
        Raises:
            Exception: If the secret reset fails.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(self.auth_url + '/', f"{self.pats_endpoint}/{pat_id}/secret/reset")
        
        try:
            response = requests.patch(
                url,
                headers=headers,
                data=json.dumps({"duration": duration}),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return PAT(**response.json())
        except requests.RequestException as error:
            raise error

    def revoke_pat(self, pat_id: str, token: str) -> Response:
        """
        Revokes a Personal Access Token (PAT).
        
        Args:
            pat_id: The unique ID of the PAT.
            token: Authorization token.
            
        Returns:
            A promise that resolves when the PAT is revoked.
            
        Raises:
            Exception: If the PAT revocation fails.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(self.auth_url + '/', f"{self.pats_endpoint}/{pat_id}/secret/revoke")
        
        try:
            response = requests.patch(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Response(
                status=response.status_code,
                message="PAT revoked successfully"
            )
        except requests.RequestException as error:
            raise error

    def add_scope(self, scopes: List[Scope], pat_id: str, token: str) -> Response:
        """
        Adds scopes to a PAT.
        
        Args:
            scopes: An array of scope.
            pat_id: The unique ID of the PAT.
            token: Authorization token.
            
        Returns:
            The requested PAT object.
            
        Raises:
            Exception: If the PAT cannot be fetched.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        # Convert scopes to dict format for serialization
        scopes_data = [
            scope.__dict__ if hasattr(scope, '__dict__') else scope
            for scope in scopes
        ]

        url = urljoin(self.auth_url + '/', f"{self.pats_endpoint}/{pat_id}/scope/add")
        
        try:
            response = requests.patch(
                url,
                headers=headers,
                data=json.dumps({"scopes": scopes_data}),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Response(
                status=response.status_code,
                message="Scope added successfully"
            )
        except requests.RequestException as error:
            raise error

    def list_scopes(
        self, pat_id: str, query_params: ScopesPageMeta, token: str
    ) -> ScopesPage:
        """
        Retrieves all scopes associated with a given PAT.
        
        Args:
            pat_id: The unique ID of the PAT.
            query_params: Metadata for pagination or filters.
            token: Authorization token.
            
        Returns:
            A page of scopes.
            
        Raises:
            Exception: If the scopes cannot be fetched.
        """
        string_params = {
            key: str(value) for key, value in query_params.__dict__.items()
            if value is not None
        }

        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.auth_url + '/',
            f"{self.pats_endpoint}/{pat_id}/scope?{urlencode(string_params)}"
        )
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return ScopesPage(**response.json())
        except requests.RequestException as error:
            raise error

    def delete_scopes(self, pat_id: str, scope_ids: List[str], token: str) -> Response:
        """
        Removes a scope from a PAT.
        
        Args:
            pat_id: The unique ID of the PAT.
            scope_ids: Array of scope IDs to remove.
            token: Authorization token.
            
        Returns:
            A promise that resolves when the scopes are removed.
            
        Raises:
            Exception: If the scopes cannot be removed.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(self.auth_url + '/', f"{self.pats_endpoint}/{pat_id}/scope/remove")
        
        try:
            response = requests.patch(
                url,
                headers=headers,
                data=json.dumps({"scopes_id": scope_ids}),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Response(
                status=response.status_code,
                message="Scopes removed successfully"
            )
        except requests.RequestException as error:
            raise error

    def delete_all_scopes(self, pat_id: str, token: str) -> Response:
        """
        Deletes all scopes associated with a PAT.
        
        Args:
            pat_id: The unique ID of the PAT.
            token: Authorization token.
            
        Returns:
            A promise that resolves when the scopes are deleted.
            
        Raises:
            Exception: If the scoped cannot be deleted.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(self.auth_url + '/', f"{self.pats_endpoint}/{pat_id}/scope")
        
        try:
            response = requests.delete(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Response(
                status=response.status_code,
                message="All scopes deleted successfully"
            )
        except requests.RequestException as error:
            raise error