# Copyright (c) Abstract Machines
# SPDX-License-Identifier: Apache-2.0

import json
from typing import Optional
from urllib.parse import urljoin, urlencode

import requests

from .errors import Errors
from .defs import (
    User,
    UsersPage,
    ClientsPage,
    GroupsPage,
    Login,
    PageMetadata,
    Token,
    Response,
    ChannelsPage,
)


class Users:
    """
    Handles interactions with the users API, including creating, updating, and managing users, creating and refreshing tokens.
    """

    def __init__(self, users_url: str, clients_url: Optional[str] = None):
        """
        Initializes the Users API client.
        
        Args:
            users_url: Base URL for the users API.
            clients_url: Optional URL for the clients API.
        """
        self.users_url = users_url.rstrip('/')
        self.clients_url = clients_url.rstrip('/') if clients_url else ""
        self.content_type = "application/json"
        self.users_endpoint = "users"
        self.search_endpoint = "search"

    def create(self, user: User, token: Optional[str] = None) -> User:
        """
        Creates a new user.
        
        Args:
            user: User object containing details like name, username and password.
            token: Authorization token.
            
        Returns:
            The created user object.
            
        Raises:
            Exception: If the user cannot be created.
        """
        headers = {
            "Content-Type": self.content_type,
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"

        url = urljoin(self.users_url + '/', self.users_endpoint)
        
        try:
            response = requests.post(
                url,
                headers=headers,
                data=json.dumps(user.dict() if hasattr(user, 'dict') else user),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return User(**response.json())
        except requests.RequestException as error:
            raise error

    def create_token(self, login: Login) -> Token:
        """
        Issue Access and Refresh Token used for authenticating into the system. 
        A user can use either their email or username to login.
        
        Args:
            login: Login object with username and password. The username can either be 
                  the email or the username of the user to be logged in.
                  
        Returns:
            The created token object.
            
        Raises:
            Exception: If the token cannot be created.
        """
        headers = {
            "Content-Type": self.content_type,
        }

        url = urljoin(self.users_url + '/', f"{self.users_endpoint}/tokens/issue")
        
        try:
            response = requests.post(
                url,
                headers=headers,
                data=json.dumps(login.dict() if hasattr(login, 'dict') else login),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Token(**response.json())
        except requests.RequestException as error:
            raise error

    def refresh_token(self, refresh_token: str) -> Token:
        """
        Provides a new access token and refresh token.
        
        Args:
            refresh_token: refresh_token which is gotten from the token struct and used to get a new access token.
            
        Returns:
            The created token object.
            
        Raises:
            Exception: If the token cannot be created.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {refresh_token}",
        }

        url = urljoin(self.users_url + '/', f"{self.users_endpoint}/tokens/refresh")
        
        try:
            response = requests.post(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Token(**response.json())
        except requests.RequestException as error:
            raise error

    def update(self, user: User, token: str) -> User:
        """
        Updates a user's firstName, lastName and metadata.
        
        Args:
            user: User object.
            token: Authorization token.
            
        Returns:
            The updated user object.
            
        Raises:
            Exception: If the user cannot be updated.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(self.users_url + '/', f"{self.users_endpoint}/{user.id}")
        
        try:
            response = requests.patch(
                url,
                headers=headers,
                data=json.dumps(user.dict() if hasattr(user, 'dict') else user),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return User(**response.json())
        except requests.RequestException as error:
            raise error

    def update_email(self, user: User, token: str) -> User:
        """
        Update a user email for a currently logged in user.
        
        Args:
            user: User object with updated email.
            token: Authorization token.
            
        Returns:
            The user object with the updated email.
            
        Raises:
            Exception: If the user email cannot be updated.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(self.users_url + '/', f"{self.users_endpoint}/{user.id}/email")
        
        try:
            response = requests.patch(
                url,
                headers=headers,
                data=json.dumps({"email": user.email}),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return User(**response.json())
        except requests.RequestException as error:
            raise error

    def update_username(self, user: User, token: str) -> User:
        """
        Updates a user's username.
        
        Args:
            user: User object with updated username.
            token: Authorization token.
            
        Returns:
            The user object with the updated username.
            
        Raises:
            Exception: If the user username cannot be updated.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        username = user.credentials.username if user.credentials else None
        url = urljoin(self.users_url + '/', f"{self.users_endpoint}/{user.id}/username")
        
        try:
            response = requests.patch(
                url,
                headers=headers,
                data=json.dumps({"username": username}),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return User(**response.json())
        except requests.RequestException as error:
            raise error

    def update_profile_picture(self, user: User, token: str) -> User:
        """
        Updates the profile picture of a user.
        
        Args:
            user: User object with the updated profile picture.
            token: Authorization token.
            
        Returns:
            The user object with the updated profile picture.
            
        Raises:
            Exception: If the user profile picture cannot be updated.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(self.users_url + '/', f"{self.users_endpoint}/{user.id}/picture")
        
        try:
            response = requests.patch(
                url,
                headers=headers,
                data=json.dumps({"profile_picture": user.profile_picture}),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return User(**response.json())
        except requests.RequestException as error:
            raise error

    def update_user_tags(self, user: User, token: str) -> User:
        """
        Update a user's tags.
        
        Args:
            user: User object with the updated tags.
            token: Authorization token.
            
        Returns:
            The user object with the updated tags.
            
        Raises:
            Exception: If the user tags cannot be updated.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(self.users_url + '/', f"{self.users_endpoint}/{user.id}/tags")
        
        try:
            response = requests.patch(
                url,
                headers=headers,
                data=json.dumps(user.dict() if hasattr(user, 'dict') else user),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return User(**response.json())
        except requests.RequestException as error:
            raise error

    def update_user_password(self, old_secret: str, new_secret: str, token: str) -> User:
        """
        Update a user's password.
        
        Args:
            old_secret: Old password.
            new_secret: New password.
            token: Authorization token.
            
        Returns:
            The user object.
            
        Raises:
            Exception: If the user password cannot be updated.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(self.users_url + '/', f"{self.users_endpoint}/secret")
        
        try:
            response = requests.patch(
                url,
                headers=headers,
                data=json.dumps({"old_secret": old_secret, "new_secret": new_secret}),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return User(**response.json())
        except requests.RequestException as error:
            raise error

    def update_user_role(self, user: User, token: str) -> User:
        """
        Update a user's role.
        
        Args:
            user: User object with the updated role.
            token: Authorization token.
            
        Returns:
            The user object with the updated role.
            
        Raises:
            Exception: If the user role cannot be updated.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(self.users_url + '/', f"{self.users_endpoint}/{user.id}/role")
        
        try:
            response = requests.patch(
                url,
                headers=headers,
                data=json.dumps(user.dict() if hasattr(user, 'dict') else user),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return User(**response.json())
        except requests.RequestException as error:
            raise error

    def user(self, user_id: str, token: str) -> User:
        """
        Gets a user.
        
        Args:
            user_id: User ID.
            token: Authorization token.
            
        Returns:
            The user object.
            
        Raises:
            Exception: If the user cannot be fetched.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(self.users_url + '/', f"{self.users_endpoint}/{user_id}")
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return User(**response.json())
        except requests.RequestException as error:
            raise error

    def user_profile(self, token: str) -> User:
        """
        Gets a user's Profile.
        
        Args:
            token: Authorization token.
            
        Returns:
            The user's profile.
            
        Raises:
            Exception: If the user's profile cannot be fetched.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(self.users_url + '/', f"{self.users_endpoint}/profile")
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return User(**response.json())
        except requests.RequestException as error:
            raise error

    def users(self, query_params: PageMetadata, token: str) -> UsersPage:
        """
        Retrieves all users matching the provided query parameters.
        
        Args:
            query_params: Metadata for pagination or filters.
            token: Authorization token.
            
        Returns:
            A page of users.
            
        Raises:
            Exception: If the users cannot be fetched.
        """
        string_params = {
            key: str(value) for key, value in query_params.items() if value is not None
        }

        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(self.users_url + '/', f"{self.users_endpoint}?{urlencode(string_params)}")
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return UsersPage(**response.json())
        except requests.RequestException as error:
            raise error

    def disable(self, user_id: str, token: str) -> User:
        """
        Disable a user.
        
        Args:
            user_id: The unique identifier of the user to disable.
            token: Authorization token.
            
        Returns:
            The disabled user object.
            
        Raises:
            Exception: If the user cannot be disabled.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(self.users_url + '/', f"{self.users_endpoint}/{user_id}/disable")
        
        try:
            response = requests.post(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return User(**response.json())
        except requests.RequestException as error:
            raise error

    def enable(self, user_id: str, token: str) -> User:
        """
        Enable a user.
        
        Args:
            user_id: The unique identifier of the user to enable.
            token: Authorization token.
            
        Returns:
            The enabled user object.
            
        Raises:
            Exception: If the user cannot be enabled.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(self.users_url + '/', f"{self.users_endpoint}/{user_id}/enable")
        
        try:
            response = requests.post(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return User(**response.json())
        except requests.RequestException as error:
            raise error

    def list_user_groups(
        self, domain_id: str, user_id: str, query_params: PageMetadata, token: str
    ) -> GroupsPage:
        """
        Get memberships of a user.
        
        Args:
            user_id: The unique identifier of the member.
            domain_id: The unique identifier of the domain.
            query_params: Query parameters for example offset and limit.
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
            self.users_url + '/',
            f"{domain_id}/{self.users_endpoint}/{user_id}/groups?{urlencode(string_params)}"
        )
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return GroupsPage(**response.json())
        except requests.RequestException as error:
            raise error

    def list_user_clients(
        self, user_id: str, domain_id: str, query_params: PageMetadata, token: str
    ) -> ClientsPage:
        """
        Get memberships of a user.
        
        Args:
            user_id: The unique identifier of the member.
            domain_id: The unique identifier of the domain.
            query_params: Query parameters for example offset and limit.
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
            f"{domain_id}/{self.users_endpoint}/{user_id}/clients?{urlencode(string_params)}"
        )
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return ClientsPage(**response.json())
        except requests.RequestException as error:
            raise error

    def list_user_channels(
        self, domain_id: str, user_id: str, query_params: PageMetadata, token: str
    ) -> ChannelsPage:
        """
        Retrieves the various channels a user owns.
        
        Args:
            user_id: The unique identifier of the member.
            domain_id: The unique identifier of the domain.
            query_params: Query parameters for example offset and limit.
            token: Authorization token.
            
        Returns:
            A page of channels.
            
        Raises:
            Exception: If the channels cannot be fetched.
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
            f"{domain_id}/{self.users_endpoint}/{user_id}/channels?{urlencode(string_params)}"
        )
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return ChannelsPage(**response.json())
        except requests.RequestException as error:
            raise error

    def reset_password_request(self, email: str, host_url: str) -> Response:
        """
        Sends a request to reset the password to the given email.
        
        Args:
            email: User email.
            host_url: URL of the host UI.
            
        Returns:
            A promise that resolves when the email is sent.
            
        Raises:
            Exception: If the reset request email cannot be sent.
        """
        headers = {
            "Content-Type": self.content_type,
            "Referer": host_url,
        }

        url = urljoin(self.users_url + '/', "password/reset-request")
        
        try:
            response = requests.post(
                url,
                headers=headers,
                data=json.dumps({"email": email}),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Response(
                status=response.status_code,
                message="Email with reset link sent successfully"
            )
        except requests.RequestException as error:
            raise error

    def reset_password(self, password: str, conf_pass: str, token: str) -> Response:
        """
        Resets a user's password.
        
        Args:
            password: updated user password.
            conf_pass: Confirmation password.
            token: Authorization token.
            
        Returns:
            A promise that resolves when the password is reset.
            
        Raises:
            Exception: If the password cannot be reset.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(self.users_url + '/', "password/reset")
        
        try:
            response = requests.put(
                url,
                headers=headers,
                data=json.dumps({"password": password, "confirm_password": conf_pass}),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Response(
                status=response.status_code,
                message="Password reset successfully"
            )
        except requests.RequestException as error:
            raise error

    def delete_user(self, user_id: str, token: str) -> Response:
        """
        Deletes a user.
        
        Args:
            user_id: The unique identifier of the user to enable.
            token: Authorization token.
            
        Returns:
            A promise that resolves when the user is deleted.
            
        Raises:
            Exception: If the user cannot be deleted.
        """
        headers = {
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(self.users_url + '/', f"{self.users_endpoint}/{user_id}")
        
        try:
            response = requests.delete(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Response(
                status=response.status_code,
                message="User deleted successfully"
            )
        except requests.RequestException as error:
            raise error

    def search_users(self, query_params: PageMetadata, token: str) -> UsersPage:
        """
        Search for users.
        
        Args:
            query_params: Query parameters for the request.
            token: Authorization token.
            
        Returns:
            A page of users.
            
        Raises:
            Exception: If the users cannot be fetched.
        """
        string_params = {
            key: str(value) for key, value in query_params.items() if value is not None
        }

        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.users_url + '/',
            f"{self.users_endpoint}/{self.search_endpoint}?{urlencode(string_params)}"
        )
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return UsersPage(**response.json())
        except requests.RequestException as error:
            raise error