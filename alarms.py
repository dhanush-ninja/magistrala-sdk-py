# Copyright (c) Abstract Machines
# SPDX-License-Identifier: Apache-2.0

import json
from urllib.parse import urljoin, urlencode

import requests

from .errors import Errors
from .defs import Alarm, AlarmPageMeta, AlarmsPage, Response


class Alarms:
    """
    A client for managing alarms via the Magistrala Alarms API.
    """

    def __init__(self, alarms_url: str):
        """
        Initializes the Alarms API client.
        
        Args:
            alarms_url: Base URL for the Alarms API.
        """
        self.alarms_url = alarms_url.rstrip('/')
        self.content_type = "application/json"
        self.alarms_endpoint = "alarms"

    def list(
        self, domain_id: str, query_params: AlarmPageMeta, token: str
    ) -> AlarmsPage:
        """
        Lists all alarms within a domain, with optional pagination/filtering.
        
        Args:
            domain_id: The unique ID of the domain.
            query_params: Query parameters for pagination/filtering.
            token: Authorization token.
            
        Returns:
            A page of alarms.
            
        Raises:
            Exception: If the alarm list cannot be retrieved.
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
            self.alarms_url + '/',
            f"{domain_id}/{self.alarms_endpoint}?{urlencode(string_params)}"
        )

        try:
            response = requests.get(url, headers=headers, timeout=30)

            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)

            return AlarmsPage(**response.json())
        except requests.RequestException as error:
            raise error

    def view(self, domain_id: str, alarm_id: str, token: str) -> Alarm:
        """
        Retrieves a single alarm by ID.
        
        Args:
            domain_id: The unique ID of the domain.
            alarm_id: Unique alarm identifier.
            token: Authorization token.
            
        Returns:
            The requested alarm.
            
        Raises:
            Exception: If the alarm cannot be fetched.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.alarms_url + '/',
            f"{domain_id}/{self.alarms_endpoint}/{alarm_id}"
        )

        try:
            response = requests.get(url, headers=headers, timeout=30)

            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)

            return Alarm(**response.json())
        except requests.RequestException as error:
            raise error

    def update(self, domain_id: str, alarm: Alarm, token: str) -> Alarm:
        """
        Updates an existing alarm.
        
        Args:
            domain_id: The unique ID of the domain.
            alarm: Alarm object containing updated fields.
            token: Authorization token.
            
        Returns:
            The updated alarm.
            
        Raises:
            Exception: If the update fails.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.alarms_url + '/',
            f"{domain_id}/{self.alarms_endpoint}/{alarm.id}"
        )

        try:
            response = requests.put(
                url,
                headers=headers,
                data=json.dumps(alarm.__dict__ if hasattr(alarm, '__dict__') else alarm),
                timeout=30
            )

            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)

            return Alarm(**response.json())
        except requests.RequestException as error:
            raise error

    def delete(self, domain_id: str, alarm_id: str, token: str) -> Response:
        """
        Deletes an alarm by ID.
        
        Args:
            domain_id: The unique ID of the domain.
            alarm_id: The unique ID of the alarm.
            token: Authorization token.
            
        Returns:
            A success response object.
            
        Raises:
            Exception: If the delete fails.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.alarms_url + '/',
            f"{domain_id}/{self.alarms_endpoint}/{alarm_id}"
        )

        try:
            response = requests.delete(url, headers=headers, timeout=30)

            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)

            return Response(
                status=response.status_code,
                message="Alarm deleted successfully"
            )
        except requests.RequestException as error:
            raise error