
import json
from urllib.parse import urljoin, urlencode

import requests

from src.magistrala.errors import Errors
from .defs import Response, MessagesPage, MessagesPageMetadata


class Messages:
    """
    Messages is used for sending and reading messages.
    It provides methods for sending and reading messages.
    """

    def __init__(self, readers_url: str, http_adapter_url: str):
        """
        Initializes the Messages API client.
        
        Args:
            readers_url: The URL of the readers service.
            http_adapter_url: The URL of the Magistrala Messages adapter.
        """
        self.readers_url = readers_url.rstrip('/')
        self.http_adapter_url = http_adapter_url.rstrip('/')
        self.content_type = "application/json"

    def send(self, domain_id: str, topic: str, msg: str, secret: str) -> Response:
        """
        Sends message to a given Channel via HTTP adapter. The client and Channel must exist and the client connected to the Channel.
        
        Args:
            domain_id: The unique ID of the domain of the channel and the client.
            topic: The topic to send the message to.
            msg: Message to send to the Channel that should be in encoded into
                 bytes format for example:
                 [{"bn":"demo", "bu":"V", "n":"voltage", "u":"V", "v":5}]
            secret: The secret of the client sending the message.
            
        Returns:
            A promise that resolves when the message is sent.
            
        Raises:
            Exception: If the message cannot be sent.
        """
        topic_parts = topic.split(".")
        chan_id = topic_parts.pop(0)  # Remove and get the first element
        subtopic = "/".join(topic_parts)

        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Client {secret}",
        }

        url = urljoin(self.http_adapter_url + '/', f"m/{domain_id}/c/{chan_id}/{subtopic}")
        
        try:
            response = requests.post(
                url,
                headers=headers,
                data=msg,
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))
            
            return Response(
                status=response.status_code,
                message="Message sent successfully"
            )
        except requests.RequestException as error:
            raise error

    def read(
        self,
        domain_id: str,
        channel_id: str,
        pm: MessagesPageMetadata,
        token: str
    ) -> dict:
        """
        Read messages from a given channel.
        
        Args:
            domain_id: The unique ID of the domain.
            channel_id: The ID of the channel to read the message from.
            pm: Query parameters for the request.
            token: Authorization token.
            
        Returns:
            A page of messages.
            
        Raises:
            Exception: If the messages cannot be fetched.
        """
        string_params = {
            key: str(value) for key, value in pm.__dict__.items()
            if value is not None
        }
        
        chan_name_parts = channel_id.split(".", 2)
        chan_id = chan_name_parts[0]
        subtopic_part = ""
        
        if len(chan_name_parts) == 2:
            subtopic_part = chan_name_parts[1].replace(".", "/")

        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.readers_url + '/',
            f"{domain_id}/channels/{chan_id}/messages{subtopic_part}?{urlencode(string_params)}"
        )
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))

            return response.json()
        except requests.RequestException as error:
            raise error