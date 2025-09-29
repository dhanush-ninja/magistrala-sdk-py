
from urllib.parse import urljoin, urlencode

import requests

from .defs import ClientTelemetry, JournalsPage, JournalsPageMetadata
from src.magistrala.errors import Errors


class Journals:
    """
    Handles interactions with Journal API.
    """

    def __init__(self, journal_url: str):
        """
        Initializes the Journal API client.
        
        Args:
            journal_url: Base URL for the journal API.
        """
        self.journals_url = journal_url.rstrip('/')
        self.content_type = "application/json"
        self.journals_endpoint = "journal"

    def entity_journals(
        self,
        entity_type: str,
        entity_id: str,
        domain_id: str,
        query_params: JournalsPageMetadata,
        token: str
    ) -> dict:
        """
        Retrieve entity journals by entity id matching the provided query parameters.
        
        Args:
            entity_type: Entity type i.e client, channel or group.
            entity_id: The unique ID of the entity.
            domain_id: The unique ID of the domain.
            query_params: Query parameters for the request.
            token: Authorization token.
            
        Returns:
            A page of journals.
            
        Raises:
            Exception: If the journals cannot be fetched.
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
            self.journals_url + '/',
            f"{domain_id}/{self.journals_endpoint}/{entity_type}/{entity_id}?{urlencode(string_params)}"
        )
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))
            
            return response.json()
        except requests.RequestException as error:
            raise error

    def user_journals(
        self,
        user_id: str,
        query_params: JournalsPageMetadata,
        token: str
    ) -> dict:
        """
        Retrieve user journals by user id matching the provided query parameters.
        
        Args:
            user_id: The unique ID of the user.
            query_params: Query parameters for the request.
            token: Authorization token.
            
        Returns:
            A page of journals.
            
        Raises:
            Exception: If the journals cannot be fetched.
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
            self.journals_url + '/',
            f"{self.journals_endpoint}/user/{user_id}?{urlencode(string_params)}"
        )
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))

            return response.json()
        except requests.RequestException as error:
            raise error

    def client_telemetry(
        self, client_id: str, domain_id: str, token: str
    ) -> dict:
        """
        Retrieves client telemetry.
        
        Args:
            client_id: The unique ID of the client.
            domain_id: The unique ID of the domain.
            token: Authorization token.
            
        Returns:
            A client telemetry interface.
            
        Raises:
            Exception: If client telemetry cannot be fetched.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.journals_url + '/',
            f"{domain_id}/{self.journals_endpoint}/client/{client_id}/telemetry"
        )
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))

            return response.json()
        except requests.RequestException as error:
            raise error