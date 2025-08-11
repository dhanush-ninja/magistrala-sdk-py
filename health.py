# Copyright (c) Abstract Machines
# SPDX-License-Identifier: Apache-2.0

from typing import Optional
from urllib.parse import urljoin

import requests

from .defs import HealthInfo
from .errors import Errors


class Health:
    """
    Health check client for various Magistrala services.
    """

    def __init__(
        self,
        users_url: Optional[str] = None,
        clients_url: Optional[str] = None,
        channels_url: Optional[str] = None,
        bootstrap_url: Optional[str] = None,
        certs_url: Optional[str] = None,
        readers_url: Optional[str] = None,
        http_adapter_url: Optional[str] = None,
        journal_url: Optional[str] = None,
        invitations_url: Optional[str] = None,
        domains_url: Optional[str] = None,
        groups_url: Optional[str] = None,
        auth_url: Optional[str] = None,
    ):
        """
        Initializes the Health check client.
        
        Args:
            users_url: URL for the users service.
            clients_url: URL for the clients service.
            channels_url: URL for the channels service.
            bootstrap_url: URL for the bootstrap service.
            certs_url: URL for the certs service.
            readers_url: URL for the readers service.
            http_adapter_url: URL for the HTTP adapter service.
            journal_url: URL for the journal service.
            invitations_url: URL for the invitations service.
            domains_url: URL for the domains service.
            groups_url: URL for the groups service.
            auth_url: URL for the auth service.
        """
        self.users_url = users_url.rstrip('/') if users_url else None
        self.clients_url = clients_url.rstrip('/') if clients_url else None
        self.channels_url = channels_url.rstrip('/') if channels_url else None
        self.bootstrap_url = bootstrap_url.rstrip('/') if bootstrap_url else None
        self.certs_url = certs_url.rstrip('/') if certs_url else None
        self.readers_url = readers_url.rstrip('/') if readers_url else None
        self.http_adapter_url = http_adapter_url.rstrip('/') if http_adapter_url else None
        self.journal_url = journal_url.rstrip('/') if journal_url else None
        self.invitations_url = invitations_url.rstrip('/') if invitations_url else None
        self.domains_url = domains_url.rstrip('/') if domains_url else None
        self.groups_url = groups_url.rstrip('/') if groups_url else None
        self.auth_url = auth_url.rstrip('/') if auth_url else None
        self.health_endpoint = "health"

    def health(self, service: str) -> HealthInfo:
        """
        Checks the health status of a specified service.
        
        Args:
            service: The name of the service to check health for.
                    Valid services: "clients", "users", "channels", "bootstrap",
                    "certs", "reader", "http-adapter", "journal", "invitations",
                    "domains", "groups", "pats"
                    
        Returns:
            Health information for the specified service.
            
        Raises:
            Exception: If the health check fails or service URL is not configured.
        """
        url = None
        
        service_urls = {
            "clients": self.clients_url,
            "users": self.users_url,
            "channels": self.channels_url,
            "bootstrap": self.bootstrap_url,
            "certs": self.certs_url,
            "reader": self.readers_url,
            "http-adapter": self.http_adapter_url,
            "journal": self.journal_url,
            "invitations": self.invitations_url,
            "domains": self.domains_url,
            "groups": self.groups_url,
            "pats": self.auth_url,
        }
        
        url = service_urls.get(service)
        
        if url is None:
            raise ValueError(f"Service '{service}' is not configured or not supported")
        
        full_url = urljoin(url + '/', self.health_endpoint)
        
        try:
            response = requests.get(full_url, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return HealthInfo(**response.json())
        except requests.RequestException as error:
            raise error