
import json
from typing import List, Optional
from urllib.parse import urljoin, urlencode
from dataclasses import asdict
import requests

from src.magistrala.errors import Errors
from .defs import (
    Channel,
    PageMetadata,
    Response,
    ChannelsPage,
    Role,
    RolePage,
    BasicPageMeta,
    MemberRolesPage,
    MembersPage,
    QueryParamRoles,
)
from .roles import Roles


class Channels:
    """
    Handles interactions with channels API, including creating, updating and managing channels.
    """

    def __init__(self, channels_url: str):
        """
        Initializes the Channel API client.
        
        Args:
            channels_url: Base URL for the channels API.
        """
        self.channels_url = channels_url.rstrip('/')
        self.content_type = "application/json"
        self.channels_endpoint = "channels"
        self.channel_roles = Roles()

    def create_channel(self, channel: Channel, token: str) -> dict:
        """
        Creates a new channel.
        
        Args:
            channel: Channel object with a containing details like name, metadata and tags.
            domain_id: The unique ID of the domain.
            token: Authorization token.
            
        Returns:
            The created channel object.
            
        Raises:
            Exception: If the channel cannot be created.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(self.channels_url + '/', f"{channel.domain_id}/{self.channels_endpoint}")
        
        try:
            response = requests.post(
                url,
                headers=headers,
                data=json.dumps(asdict(channel)),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))
            
            return response.json()
        except requests.RequestException as error:
            raise error

    def channel(self, channel_id: str, domain_id: str, token: str, list_roles: Optional[bool] = None) -> dict:
        """
        Retrieves a channel by its id.
        
        Args:
            channel_id: The unique ID of the channel.
            domain_id: The unique ID of the domain.
            token: Authorization token.
            list_roles: Whether to include roles in the response.
            
        Returns:
            The requested channel object.
            
        Raises:
            Exception: If the channel cannot be fetched.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(self.channels_url + '/', f"{domain_id}/{self.channels_endpoint}/{channel_id}")
        
        if list_roles is not None:
            url += f"?{QueryParamRoles}={str(list_roles).lower()}"
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))
            
            return response.json()
        except requests.RequestException as error:
            raise error

    def create_channels(
        self, channels: List[Channel], domain_id: str, token: str
    ) -> dict:
        """
        Creates multiple new channels.
        
        Args:
            channels: An array of channel objects, each containing details like name, metadata, and tags.
            domain_id: The unique ID of the domain.
            token: Authorization token.
            
        Returns:
            A page of channels.
            
        Raises:
            Exception: If the channels cannot be created.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(self.channels_url + '/', f"{domain_id}/{self.channels_endpoint}/bulk")
        
        try:
            channels_data = [
                channel.dict() if hasattr(channel, 'dict') else channel
                for channel in channels
            ]
            
            response = requests.post(
                url,
                headers=headers,
                data=json.dumps(channels_data),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))

            return response.json()
        except requests.RequestException as error:
            raise error

    def channels(self,  domain_id: str, limit: int, offset: int, token: str) -> dict:
        """
        Retrieves all channels matching the provided query parameters.
        
        Args:
            query_params: Query parameters for the request.
            domain_id: The unique ID of the domain.
            token: Authorization token.
            
        Returns:
            A page of channels.
            
        Raises:
            Exception: If the channels cannot be fetched.
        """

        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.channels_url + '/',
            f"{domain_id}/{self.channels_endpoint}?limit={limit}&offset={offset}"
        )
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))
            
            return response.json()
        except requests.RequestException as error:
            raise error

    def update_channel(
        self, channel: Channel, token: str
    ) -> dict:
        """
        Updates an existing channel's metadata and name.
        
        Args:
            channel: Channel object with updated properties.
            domain_id: The unique ID of the domain.
            token: Authorization token.
            
        Returns:
            The updated channel object.
            
        Raises:
            Exception: If the channel cannot be updated.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.channels_url + '/',
            f"{channel.domain_id}/{self.channels_endpoint}/{channel.id}"
        )
        
        try:
            response = requests.patch(
                url,
                headers=headers,
                data=json.dumps(asdict(channel)),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))
            
            return response.json()
        except requests.RequestException as error:
            raise error

    def update_channel_tags(
        self, channel: Channel, domain_id: str, token: str
    ) -> dict:
        """
        Updates an existing channel's tags.
        
        Args:
            channel: Channel object with updated properties.
            domain_id: The unique ID of the domain.
            token: Authorization token.
            
        Returns:
            The updated channel object.
            
        Raises:
            Exception: If the channel tags cannot be updated.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.channels_url + '/',
            f"{domain_id}/{self.channels_endpoint}/{channel.id}/tags"
        )
        
        try:
            response = requests.patch(
                url,
                headers=headers,
                data=json.dumps(channel.dict() if hasattr(channel, 'dict') else channel),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))
            
            return response.json()
        except requests.RequestException as error:
            raise error

    def disable_channel(self, channel_id: str, domain_id: str, token: str) -> dict:
        """
        Disables a specific channel.
        
        Args:
            channel_id: The unique ID of the channel.
            domain_id: The unique ID of the domain.
            token: Authorization token.
            
        Returns:
            The disabled channel object.
            
        Raises:
            Exception: If the channel cannot be disabled.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.channels_url + '/',
            f"{domain_id}/{self.channels_endpoint}/{channel_id}/disable"
        )
        
        try:
            response = requests.post(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))
            
            return response.json()
        except requests.RequestException as error:
            raise error

    def enable_channel(self, channel_id: str, domain_id: str, token: str) -> dict:
        """
        Enables a previously disabled channel.
        
        Args:
            channel_id: The unique ID of the channel.
            domain_id: The unique ID of the domain.
            token: Authorization token.
            
        Returns:
            The enabled channel object.
            
        Raises:
            Exception: If the channel cannot be enabled.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.channels_url + '/',
            f"{domain_id}/{self.channels_endpoint}/{channel_id}/enable"
        )
        
        try:
            response = requests.post(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))
            
            return response.json()
        except requests.RequestException as error:
            raise error

    def delete_channel(self, channel_id: str, domain_id: str, token: str) -> Response:
        """
        Deletes channel with specified id.
        
        Args:
            channel_id: The unique ID of the channel.
            domain_id: The unique ID of the domain.
            token: Authorization token.
            
        Returns:
            A promise that resolves when the channel is deleted.
            
        Raises:
            Exception: If the channel cannot be deleted.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.channels_url + '/',
            f"{domain_id}/{self.channels_endpoint}/{channel_id}"
        )
        
        try:
            response = requests.delete(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))
            
            return Response(
                status=response.status_code,
                message="Channel deleted successfully"
            )
        except requests.RequestException as error:
            raise error

    def connect_client(
        self,
        client_ids: List[str],
        channel_id: str,
        domain_id: str,
        token: str,
        connection_types: List[str] = ["publish", "subscribe"]
    ) -> Response:
        """
        Connects multiple clients to a channel.
        
        Args:
            client_ids: An array of unique clients IDs to be connected.
            channel_id: The unique ID of the channel to which the clients will connect.
            connection_types: Connection types can be 'publish', 'subscribe' or both.
            domain_id: The unique ID of the domain.
            token: Authorization token.
            
        Returns:
            A promise that resolves when the clients are connected to the channel.
            
        Raises:
            Exception: If the clients cannot be connected to the channel.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.channels_url + '/',
            f"{domain_id}/{self.channels_endpoint}/{channel_id}/connect"
        )
        
        payload = {
            "client_ids": client_ids,
            "channel_id": channel_id,
            "types": connection_types,
        }
        
        try:
            response = requests.post(
                url,
                headers=headers,
                data=json.dumps(payload),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))
            
            return Response(
                status=response.status_code,
                message="Clients connected successfully"
            )
        except requests.RequestException as error:
            raise error

    def connect(
        self,
        client_ids: List[str],
        channel_ids: List[str],
        connection_types: List[str],
        domain_id: str,
        token: str
    ) -> Response:
        """
        Connects multiple clients to multiple channels.
        
        Args:
            client_ids: An array of unique clients IDs to be connected.
            channel_ids: An array of unique channels IDs to which the clients will connect.
            connection_types: Connection types can be publish, subscribe or both publish and subscribe.
            domain_id: The unique ID of the channel.
            token: Authorization token.
            
        Returns:
            A promise that resolves when the clients are connected to the channels.
            
        Raises:
            Exception: If the clients cannot be connected to the channel.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.channels_url + '/',
            f"{domain_id}/{self.channels_endpoint}/connect"
        )
        
        payload = {
            "client_ids": client_ids,
            "channel_ids": channel_ids,
            "types": connection_types,
        }
        
        try:
            response = requests.post(
                url,
                headers=headers,
                data=json.dumps(payload),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))
            
            return Response(
                status=response.status_code,
                message="Clients connected successfully"
            )
        except requests.RequestException as error:
            raise error

    def disconnect(
        self,
        client_ids: List[str],
        channel_ids: List[str],
        connection_types: List[str],
        domain_id: str,
        token: str
    ) -> Response:
        """
        Disconnects clients from channels.
        
        Args:
            client_ids: An array of unique clients IDs to be disconnected.
            channel_ids: An array of unique channels IDs to which the clients will disconnect.
            connection_types: Connection types can be publish, subscribe or both publish and subscribe.
            domain_id: The unique ID of the domain.
            token: Authorization token.
            
        Returns:
            A promise that resolves when the clients are disconnected from the channels.
            
        Raises:
            Exception: If the clients cannot be disconnected from the channels.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.channels_url + '/',
            f"{domain_id}/{self.channels_endpoint}/disconnect"
        )
        
        payload = {
            "client_ids": client_ids,
            "channel_ids": channel_ids,
            "types": connection_types,
        }
        
        try:
            response = requests.post(
                url,
                headers=headers,
                data=json.dumps(payload),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))
            
            return Response(
                status=response.status_code,
                message="Clients disconnected successfully"
            )
        except requests.RequestException as error:
            raise error

    def disconnect_client(
        self,
        client_ids: List[str],
        channel_id: str,
        connection_types: List[str],
        domain_id: str,
        token: str
    ) -> Response:
        """
        Disconnects clients from channel.
        
        Args:
            client_ids: An array of unique clients IDs to be disconnected.
            channel_id: The unique ID of the channel from which the clients will be disconnected.
            connection_types: connection types can be publish, subscribe or both publish and subscribe.
            domain_id: The unique ID of the domain.
            token: Authorization token.
            
        Returns:
            A promise that resolves when the clients are disconnected from the channel.
            
        Raises:
            Exception: If the clients cannot be disconnected from the channel.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.channels_url + '/',
            f"{domain_id}/{self.channels_endpoint}/{channel_id}/disconnect"
        )
        
        payload = {
            "client_ids": client_ids,
            "channel_id": channel_id,
            "types": connection_types,
        }
        
        try:
            response = requests.post(
                url,
                headers=headers,
                data=json.dumps(payload),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))
            
            return Response(
                status=response.status_code,
                message="Clients disconnected successfully"
            )
        except requests.RequestException as error:
            raise error

    def set_channel_parent_group(
        self, domain_id: str, channel_id: str, parent_group_id: str, token: str
    ) -> Response:
        """
        Sets parent to a channel.
        
        Args:
            domain_id: The unique ID of the domain.
            channel_id: The unique ID of the channel to be updated.
            parent_group_id: The unique ID of the group to be set as the parent.
            token: Authorization token.
            
        Returns:
            A promise that resolves when the parent group is successfully set for the specified channel.
            
        Raises:
            Exception: If the parent group cannot be set for the channel.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.channels_url + '/',
            f"{domain_id}/{self.channels_endpoint}/{channel_id}/parent"
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
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))
            
            return Response(
                status=response.status_code,
                message="Channel group parent added successfully"
            )
        except requests.RequestException as error:
            raise error

    def delete_channel_parent_group(
        self, domain_id: str, channel_id: str, token: str
    ) -> Response:
        """
        Removes the parent group from a specified channel.
        
        Args:
            domain_id: The unique ID of the domain.
            channel_id: The unique ID of the channel.
            token: Authorization token.
            
        Returns:
            A promise that resolves when the parent group is successfully removed from the specified channel.
            
        Raises:
            Exception: If the parent group cannot be removed from the channel.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.channels_url + '/',
            f"{domain_id}/{self.channels_endpoint}/{channel_id}/parent"
        )
        
        try:
            response = requests.delete(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))
            
            return Response(
                status=response.status_code,
                message="Channel group parent deleted successfully"
            )
        except requests.RequestException as error:
            raise error

    def list_channel_actions(self, domain_id: str, token: str) -> dict:
        """
        Lists all actions available to a specific channel.
        
        Args:
            domain_id: The unique identifier of the domain.
            token: Authorization token.
            
        Returns:
            A promise that resolves with an array of actions.
            
        Raises:
            Exception: If channel actions cannot be fetched.
        """
        try:
            actions = self.channel_roles.list_available_actions(
                self.channels_url,
                f"{domain_id}/{self.channels_endpoint}",
                token
            )
            return actions
        except Exception as error:
            raise error

    def create_channel_role(
        self,
        channel_id: str,
        role_name: str,
        domain_id: str,
        token: str,
        optional_actions: Optional[List[str]] = None,
        optional_members: Optional[List[str]] = None
    ) -> Role:
        """
        Creates a new role within a specific channel.
        
        Args:
            channel_id: The unique identifier of the channel.
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
            role = self.channel_roles.create_role(
                self.channels_url,
                f"{domain_id}/{self.channels_endpoint}",
                channel_id,
                role_name,
                token,
                optional_actions,
                optional_members
            )
            return role
        except Exception as error:
            raise error

    def list_channel_roles(
        self, channel_id: str, domain_id: str, query_params: PageMetadata, token: str
    ) -> dict:
        """
        Lists all roles within a specific channel.
        
        Args:
            channel_id: The unique identifier of the channel.
            domain_id: The unique ID of the domain.
            query_params: Metadata for pagination or filters.
            token: Authorization token.
            
        Returns:
            A promise that resolves with a page of roles in the domain.
            
        Raises:
            Exception: If the channel is invalid or roles cannot be fetched.
        """
        try:
            roles_page = self.channel_roles.list_roles(
                self.channels_url,
                f"{domain_id}/{self.channels_endpoint}",
                channel_id,
                query_params,
                token
            )
            return roles_page
        except Exception as error:
            raise error

    def view_channel_role(
        self, channel_id: str, domain_id: str, role_id: str, token: str
    ) -> dict:
        """
        Retrieves details about a specific role in a channel.
        
        Args:
            channel_id: The unique identifier of the channel.
            domain_id: The unique ID of the domain.
            role_id: The unique identifier of the role.
            token: Authorization token.
            
        Returns:
            A promise that resolves with the role details.
            
        Raises:
            Exception: If the role does not exist or cannot be retrieved.
        """
        try:
            role = self.channel_roles.view_role(
                self.channels_url,
                f"{domain_id}/{self.channels_endpoint}",
                channel_id,
                role_id,
                token
            )
            return role
        except Exception as error:
            raise error

    def update_channel_role(
        self, channel_id: str, domain_id: str, role_id: str, role: Role, token: str
    ) -> dict:
        """
        Updates the details of a specific role in a channel.
        
        Args:
            channel_id: The unique identifier of the channel.
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
            updated_role = self.channel_roles.update_role(
                self.channels_url,
                f"{domain_id}/{self.channels_endpoint}",
                channel_id,
                role_id,
                role,
                token
            )
            return updated_role
        except Exception as error:
            raise error

    def delete_channel_role(
        self, channel_id: str, domain_id: str, role_id: str, token: str
    ) -> Response:
        """
        Deletes a specific role from a channel.
        
        Args:
            channel_id: The unique identifier of the channel.
            domain_id: The unique ID of the domain.
            role_id: The unique identifier of the role.
            token: Authorization token.
            
        Returns:
            A promise that resolves when the role is deleted.
            
        Raises:
            Exception: If the role cannot be deleted.
        """
        try:
            response = self.channel_roles.delete_role(
                self.channels_url,
                f"{domain_id}/{self.channels_endpoint}",
                channel_id,
                role_id,
                token
            )
            return response
        except Exception as error:
            raise error

    def add_channel_role_actions(
        self, channel_id: str, domain_id: str, role_id: str, actions: List[str], token: str
    ) -> List[str]:
        """
        Adds actions to a specific role in a channel.
        
        Args:
            channel_id: The unique identifier of the channel.
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
            response = self.channel_roles.add_role_actions(
                self.channels_url,
                f"{domain_id}/{self.channels_endpoint}",
                channel_id,
                role_id,
                actions,
                token
            )
            return response
        except Exception as error:
            raise error

    def list_channel_role_actions(
        self, channel_id: str, domain_id: str, role_id: str, token: str
    ) -> dict:
        """
        Lists all actions associated with a specific role in a channel.
        
        Args:
            channel_id: The unique identifier of the channel.
            domain_id: The unique ID of the domain.
            role_id: The unique identifier of the role.
            token: Authorization token.
            
        Returns:
            A promise that resolves with an array of actions.
            
        Raises:
            Exception: If actions cannot be retrieved.
        """
        try:
            updated_role = self.channel_roles.list_role_actions(
                self.channels_url,
                f"{domain_id}/{self.channels_endpoint}",
                channel_id,
                role_id,
                token
            )
            return updated_role
        except Exception as error:
            raise error

    def delete_channel_role_actions(
        self, channel_id: str, domain_id: str, role_id: str, actions: List[str], token: str
    ) -> Response:
        """
        Deletes specific actions from a role in a channel.
        
        Args:
            channel_id: The unique identifier of the channel.
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
            response = self.channel_roles.delete_role_actions(
                self.channels_url,
                f"{domain_id}/{self.channels_endpoint}",
                channel_id,
                role_id,
                actions,
                token
            )
            return response
        except Exception as error:
            raise error

    def delete_all_channel_role_actions(
        self, channel_id: str, domain_id: str, role_id: str, token: str
    ) -> Response:
        """
        Deletes all actions associated with a specific role in a channel.
        
        Args:
            channel_id: The unique identifier of the channel.
            domain_id: The unique ID of the domain.
            role_id: The unique identifier of the role.
            token: Authorization token.
            
        Returns:
            A promise that resolves when all actions are deleted.
            
        Raises:
            Exception: If the actions cannot be deleted.
        """
        try:
            response = self.channel_roles.delete_all_role_actions(
                self.channels_url,
                f"{domain_id}/{self.channels_endpoint}",
                channel_id,
                role_id,
                token
            )
            return response
        except Exception as error:
            raise error

    def add_channel_role_members(
        self, channel_id: str, domain_id: str, role_id: str, members: List[str], token: str
    ) -> dict:
        """
        Adds members to a specific role in a channel.
        
        Args:
            channel_id: The unique identifier of the channel.
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
            response = self.channel_roles.add_role_members(
                self.channels_url,
                f"{domain_id}/{self.channels_endpoint}",
                channel_id,
                role_id,
                members,
                token
            )
            return response
        except Exception as error:
            raise error

    def list_channel_role_members(
        self,
        channel_id: str,
        domain_id: str,
        role_id: str,
        query_params: BasicPageMeta,
        token: str
    ) -> dict:
        """
        Lists all members associated with a specific role in a channel.
        
        Args:
            channel_id: The unique identifier of the channel.
            domain_id: The unique ID of the domain.
            role_id: The unique identifier of the role.
            token: Authorization token.
            
        Returns:
            A promise that resolves with an array of member ids.
            
        Raises:
            Exception: If members cannot be retrieved.
        """
        try:
            members = self.channel_roles.list_role_members(
                self.channels_url,
                f"{domain_id}/{self.channels_endpoint}",
                channel_id,
                role_id,
                query_params,
                token
            )
            return members
        except Exception as error:
            raise error

    def delete_channel_role_members(
        self, channel_id: str, domain_id: str, role_id: str, members: List[str], token: str
    ) -> Response:
        """
        Deletes specific members from a role in a channel.
        
        Args:
            channel_id: The unique identifier of the channel.
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
            response = self.channel_roles.delete_role_members(
                self.channels_url,
                f"{domain_id}/{self.channels_endpoint}",
                channel_id,
                role_id,
                members,
                token
            )
            return response
        except Exception as error:
            raise error

    def delete_all_channel_role_members(
        self, channel_id: str, domain_id: str, role_id: str, token: str
    ) -> Response:
        """
        Deletes all members associated with a specific role in a channel.
        
        Args:
            channel_id: The unique identifier of the channel.
            domain_id: The unique ID of the domain.
            role_id: The unique identifier of the role.
            token: Authorization token.
            
        Returns:
            A promise that resolves when all members are deleted.
            
        Raises:
            Exception: If the members cannot be deleted.
        """
        try:
            response = self.channel_roles.delete_all_role_members(
                self.channels_url,
                f"{domain_id}/{self.channels_endpoint}",
                channel_id,
                role_id,
                token
            )
            return response
        except Exception as error:
            raise error

    def list_channel_members(
        self,
        channel_id: str,
        domain_id: str,
        query_params: BasicPageMeta,
        token: str
    ) -> dict:
        """
        Lists all members associated with a channel.
        
        Args:
            channel_id: The unique identifier of the channel.
            domain_id: The unique ID of the domain.
            token: Authorization token.
            
        Returns:
            A promise that resolves with a page of members.
            
        Raises:
            Exception: If members cannot be retrieved.
        """
        try:
            members = self.channel_roles.list_entity_members(
                self.channels_url,
                f"{domain_id}/{self.channels_endpoint}",
                channel_id,
                query_params,
                token
            )
            return members
        except Exception as error:
            raise error