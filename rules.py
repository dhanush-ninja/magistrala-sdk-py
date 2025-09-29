
import json
from typing import List
from urllib.parse import urljoin, urlencode

import requests

from .defs import Rule, RulesPage, RulesPageMetadata, Response, Schedule
from src.magistrala.errors import Errors


class Rules:
    """
    Handles interactions with rules API, including creating, updating and managing rules.
    """

    def __init__(self, rules_url: str):
        """
        Initializes the Rules API client.
        
        Args:
            rules_url: Base URL for the rules API.
        """
        self.rules_url = rules_url.rstrip('/')
        self.content_type = "application/json"
        self.rules_endpoint = "rules"

    def create(self, domain_id: str, rule: Rule, token: str) -> dict:
        """
        Creates a new rule.
        
        Args:
            domain_id: The unique ID of the domain.
            rule: Rule object with a containing details like name, input_channel, input_topic and logic.
            token: Authorization token.
            
        Returns:
            The created rule object.
            
        Raises:
            Exception: If the rule cannot be created.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(self.rules_url + '/', f"{domain_id}/{self.rules_endpoint}")
        
        try:
            response = requests.post(
                url,
                headers=headers,
                data=json.dumps(rule.dict() if hasattr(rule, 'dict') else rule),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))

            return response.json()
        except requests.RequestException as error:
            raise error

    def view(self, domain_id: str, rule_id: str, token: str) -> dict:
        """
        Retrieves a rule by its id.
        
        Args:
            domain_id: The unique ID of the domain.
            rule_id: The unique ID of the rule.
            token: Authorization token.
            
        Returns:
            The requested rule object.
            
        Raises:
            Exception: If the rule cannot be fetched.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.rules_url + '/',
            f"{domain_id}/{self.rules_endpoint}/{rule_id}"
        )
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))
            return response.json()
        except requests.RequestException as error:
            raise error

    def list(
        self, domain_id: str, query_params: RulesPageMetadata, token: str
    ) -> dict:
        """
        Retrieves all rules matching the provided query parameters.
        
        Args:
            domain_id: The unique ID of the domain.
            query_params: Query parameters for the request.
            token: Authorization token.
            
        Returns:
            A page of rules.
            
        Raises:
            Exception: If the rules cannot be fetched.
        """
        string_params = {
            key: str(value) for key, value in query_params.items() if value is not None
        }

        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.rules_url + '/',
            f"{domain_id}/{self.rules_endpoint}?{urlencode(string_params)}"
        )
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))
            
            return response.json()
        except requests.RequestException as error:
            raise error

    def update(self, domain_id: str, rule: Rule, token: str) -> dict:
        """
        Updates an existing rule.
        
        Args:
            domain_id: The unique ID of the domain.
            rule: rule object with updated properties.
            token: Authorization token.
            
        Returns:
            The updated rule object.
            
        Raises:
            Exception: If the rule cannot be updated.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.rules_url + '/',
            f"{domain_id}/{self.rules_endpoint}/{rule.id}"
        )
        
        try:
            response = requests.patch(
                url,
                headers=headers,
                data=json.dumps(rule.dict() if hasattr(rule, 'dict') else rule),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))

            return response.json()
        except requests.RequestException as error:
            raise error

    def update_tags(
        self, domain_id: str, rule_id: str, tags: List[str], token: str
    ) -> dict:
        """
        Updates an existing rule's tags.
        
        Args:
            domain_id: The unique ID of the domain.
            rule_id: The unique ID of the rule.
            tags: The updated tags for the rule.
            token: Authorization token.
            
        Returns:
            The updated rule object.
            
        Raises:
            Exception: If the rule cannot be updated.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.rules_url + '/',
            f"{domain_id}/{self.rules_endpoint}/{rule_id}/tags"
        )
        
        try:
            response = requests.patch(
                url,
                headers=headers,
                data=json.dumps({"tags": tags}),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))

            return response.json()
        except requests.RequestException as error:
            raise error

    def update_schedule(
        self, domain_id: str, rule_id: str, schedule: Schedule, token: str
    ) -> dict:
        """
        Updates the schedule for a specific rule.
        
        Args:
            domain_id: The unique ID of the domain.
            rule_id: The ID of the rule whose schedule is to be updated.
            schedule: The updated schedule object.
            token: Authorization token.
            
        Returns:
            The updated rule object.
            
        Raises:
            Exception: If the schedule cannot be updated.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.rules_url + '/',
            f"{domain_id}/{self.rules_endpoint}/{rule_id}/schedule"
        )
        
        try:
            response = requests.patch(
                url,
                headers=headers,
                data=json.dumps({
                    "schedule": schedule.dict() if hasattr(schedule, 'dict') else schedule
                }),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))

            return response.json()
        except requests.RequestException as error:
            raise error

    def delete(self, domain_id: str, rule_id: str, token: str) -> Response:
        """
        Deletes a rule.
        
        Args:
            domain_id: The unique ID of the domain.
            rule_id: The unique ID of the rule.
            token: Authorization token.
            
        Returns:
            A promise that resolves when the rule is successfully deleted.
            
        Raises:
            Exception: If the rule cannot be deleted.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.rules_url + '/',
            f"{domain_id}/{self.rules_endpoint}/{rule_id}"
        )
        
        try:
            response = requests.delete(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))
            
            return Response(
                status=response.status_code,
                message="Rule deleted successfully"
            )
        except requests.RequestException as error:
            raise error

    def enable(self, domain_id: str, rule_id: str, token: str) -> dict:
        """
        Enables a previously disabled rule.
        
        Args:
            domain_id: The unique ID of the domain.
            rule_id: The unique ID of the rule.
            token: Authorization token.
            
        Returns:
            The enabled rule object.
            
        Raises:
            Exception: If the rule cannot be enabled.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.rules_url + '/',
            f"{domain_id}/{self.rules_endpoint}/{rule_id}/enable"
        )
        
        try:
            response = requests.post(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))

            return response.json()
        except requests.RequestException as error:
            raise error

    def disable(self, domain_id: str, rule_id: str, token: str) -> dict:
        """
        Disables a specific rule.
        
        Args:
            domain_id: The unique ID of the domain.
            rule_id: The unique ID of the rule.
            token: Authorization token.
            
        Returns:
            The disabled rule object.
            
        Raises:
            Exception: If the rule cannot be disabled.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.rules_url + '/',
            f"{domain_id}/{self.rules_endpoint}/{rule_id}/disable"
        )
        
        try:
            response = requests.post(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))

            return response.json()
        except requests.RequestException as error:
            raise error