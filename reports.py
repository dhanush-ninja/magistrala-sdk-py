
import json
from urllib.parse import urljoin, urlencode

import requests

from .defs import (
    ReportConfig,
    ReportConfigPage,
    ReportPage,
    Response,
    RulesPageMetadata,
    Schedule,
    Template,
)
from src.magistrala.errors import Errors


class Reports:
    """
    Handles interactions with the reports API, including creating, retrieving, updating,
    enabling/disabling, deleting, and downloading reports and report configurations.
    """

    def __init__(self, reports_url: str):
        """
        Initializes the Reports API client.
        
        Args:
            reports_url: Base URL for the reports API.
        """
        self.reports_url = reports_url.rstrip('/')
        self.content_type = "application/json"
        self.reports_endpoint = "reports"
        self.configs_endpoint = "configs"

    def generate_report(
        self, domain_id: str, report_config: ReportConfig, token: str
    ) -> dict:
        """
        Generates a report using a provided report configuration.
        
        Args:
            domain_id: The unique ID of the domain.
            report_config: Configuration for generating the report.
            token: Authorization token.
            
        Returns:
            The generated report data.
            
        Raises:
            Exception: If the report generation fails.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(self.reports_url + '/', f"{domain_id}/{self.reports_endpoint}")
        
        try:
            response = requests.post(
                url,
                headers=headers,
                data=json.dumps(report_config.__dict__ if hasattr(report_config, '__dict__') else report_config),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))
            
            return response.json()
        except requests.RequestException as error:
            raise error

    def add_report_config(
        self, domain_id: str, report_config: ReportConfig, token: str
    ) -> dict:
        """
        Adds a new report configuration.
        
        Args:
            domain_id: The unique ID of the domain.
            report_config: Report configuration to add.
            token: Authorization token.
            
        Returns:
            The added report configuration.
            
        Raises:
            Exception: If the configuration cannot be added.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.reports_url + '/',
            f"{domain_id}/{self.reports_endpoint}/{self.configs_endpoint}"
        )
        
        try:
            response = requests.post(
                url,
                headers=headers,
                data=json.dumps(report_config.__dict__ if hasattr(report_config, '__dict__') else report_config),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))

            return response.json()
        except requests.RequestException as error:
            raise error

    def view_report_config(
        self, domain_id: str, config_id: str, token: str
    ) -> dict:
        """
        Retrieves a report configuration by ID.
        
        Args:
            domain_id: The unique ID of the domain.
            config_id: The unique ID of the config.
            token: Authorization token.
            
        Returns:
            The requested report configuration.
            
        Raises:
            Exception: If the configuration cannot be fetched.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.reports_url + '/',
            f"{domain_id}/{self.reports_endpoint}/{self.configs_endpoint}/{config_id}"
        )
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))

            return response.json()
        except requests.RequestException as error:
            raise error

    def list_report_configs(
        self, domain_id: str, query_params: RulesPageMetadata, token: str
    ) -> dict:
        """
        Lists report configurations with optional query parameters.
        
        Args:
            domain_id: The unique ID of the domain.
            query_params: Query parameters for pagination and filtering.
            token: Authorization token.
            
        Returns:
            Paginated report configurations.
            
        Raises:
            Exception: If configurations cannot be listed.
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
            self.reports_url + '/',
            f"{domain_id}/{self.reports_endpoint}/{self.configs_endpoint}?{urlencode(string_params)}"
        )
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))
            
            return response.json()
        except requests.RequestException as error:
            raise error

    def update_report_config(
        self, domain_id: str, config: ReportConfig, token: str
    ) -> dict:
        """
        Updates an existing report configuration.
        
        Args:
            domain_id: The unique ID of the domain.
            config: Report configuration with updated values.
            token: Authorization token.
            
        Returns:
            The updated report configuration.
            
        Raises:
            Exception: If the configuration cannot be updated.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.reports_url + '/',
            f"{domain_id}/{self.reports_endpoint}/{self.configs_endpoint}/{config.id}"
        )
        
        try:
            response = requests.patch(
                url,
                headers=headers,
                data=json.dumps(config.__dict__ if hasattr(config, '__dict__') else config),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))

            return response.json()
        except requests.RequestException as error:
            raise error

    def update_report_schedule(
        self, domain_id: str, config_id: str, schedule: Schedule, token: str
    ) -> dict:
        """
        Updates an existing report schedule.
        
        Args:
            domain_id: The unique ID of the domain.
            config_id: The unique ID of the config.
            schedule: Report schedule with updated values.
            token: Authorization token.
            
        Returns:
            The updated report config.
            
        Raises:
            Exception: If the schedule cannot be updated.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        schedule_data = schedule.__dict__ if hasattr(schedule, '__dict__') else schedule

        url = urljoin(
            self.reports_url + '/',
            f"{domain_id}/{self.reports_endpoint}/{self.configs_endpoint}/{config_id}/schedule"
        )
        
        try:
            response = requests.patch(
                url,
                headers=headers,
                data=json.dumps({"schedule": schedule_data}),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))

            return response.json()
        except requests.RequestException as error:
            raise error

    def delete_report_config(
        self, domain_id: str, config_id: str, token: str
    ) -> Response:
        """
        Deletes a report configuration.
        
        Args:
            domain_id: The unique ID of the domain.
            config_id: The unique ID of the config.
            token: Authorization token.
            
        Returns:
            Deletion status.
            
        Raises:
            Exception: If the configuration cannot be deleted.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.reports_url + '/',
            f"{domain_id}/{self.reports_endpoint}/{self.configs_endpoint}/{config_id}"
        )
        
        try:
            response = requests.delete(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))
            
            return Response(
                status=response.status_code,
                message="Report config deleted successfully"
            )
        except requests.RequestException as error:
            raise error

    def enable_report_config(
        self, domain_id: str, config_id: str, token: str
    ) -> dict:
        """
        Enables a report configuration.
        
        Args:
            domain_id: The unique ID of the domain.
            config_id: The unique ID of the config.
            token: Authorization token.
            
        Returns:
            The enabled report configuration.
            
        Raises:
            Exception: If the configuration cannot be enabled.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.reports_url + '/',
            f"{domain_id}/{self.reports_endpoint}/{self.configs_endpoint}/{config_id}/enable"
        )
        
        try:
            response = requests.post(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))

            return response.json()
        except requests.RequestException as error:
            raise error

    def disable_report_config(
        self, domain_id: str, config_id: str, token: str
    ) -> dict:
        """
        Disables a report configuration.
        
        Args:
            domain_id: The unique ID of the domain.
            config_id: The unique ID of the config.
            token: Authorization token.
            
        Returns:
            The disabled report configuration.
            
        Raises:
            Exception: If the configuration cannot be disabled.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.reports_url + '/',
            f"{domain_id}/{self.reports_endpoint}/{self.configs_endpoint}/{config_id}/disable"
        )
        
        try:
            response = requests.post(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))
            
            return ReportConfig(**response.json())
        except requests.RequestException as error:
            raise error

    def update_report_template(
        self, domain_id: str, report_id: str, report_template: str, token: str
    ) -> None:
        """
        Updates report template.
        
        Args:
            domain_id: The unique ID of the domain.
            report_id: The unique ID of the report.
            report_template: Template for the report.
            token: Authorization token.
            
        Raises:
            Exception: If the template cannot be updated.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.reports_url + '/',
            f"{domain_id}/{self.reports_endpoint}/{self.configs_endpoint}/{report_id}/template"
        )
        
        try:
            response = requests.put(
                url,
                headers=headers,
                data=json.dumps({"report_template": report_template}),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))
        except requests.RequestException as error:
            raise error

    def view_report_template(
        self, domain_id: str, report_id: str, token: str
    ) -> dict:
        """
        Views report template.
        
        Args:
            domain_id: The unique ID of the domain.
            report_id: The unique ID of the report.
            token: Authorization token.
            
        Returns:
            The template used to generate report configuration.
            
        Raises:
            Exception: If the report template cannot be retrieved.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.reports_url + '/',
            f"{domain_id}/{self.reports_endpoint}/{self.configs_endpoint}/{report_id}/template"
        )
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))

            return response.json()
        except requests.RequestException as error:
            raise error

    def delete_report_template(
        self, domain_id: str, report_id: str, token: str
    ) -> None:
        """
        Deletes report template.
        
        Args:
            domain_id: The unique ID of the domain.
            report_id: The unique ID of the report.
            token: Authorization token.
            
        Raises:
            Exception: If the report template cannot be deleted.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.reports_url + '/',
            f"{domain_id}/{self.reports_endpoint}/{self.configs_endpoint}/{report_id}/template"
        )
        
        try:
            response = requests.delete(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))
        except requests.RequestException as error:
            raise error