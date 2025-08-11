# Copyright (c) Abstract Machines
# SPDX-License-Identifier: Apache-2.0

import json
from urllib.parse import urljoin

import requests

from .errors import Errors
from .defs import Cert, CertsPage, Response


class Certs:
    """
    Handles interactions with certs API, including issuing, viewing, revoking certificates and manage certificates.
    """

    def __init__(self, certs_url: str):
        """
        Initializes the Certs API client.
        
        Args:
            certs_url: Base URL for the certs API.
        """
        self.certs_url = certs_url.rstrip('/')
        self.content_type = "application/json"
        self.certs_endpoint = "certs"

    def issue_cert(
        self, client_id: str, valid: str, domain_id: str, token: str
    ) -> Cert:
        """
        Issues a certificate to a client.
        
        Args:
            client_id: The unique ID of the client to be issued a certificate.
            valid: The time in hours for which the certificate is valid such as '10h'.
            domain_id: The unique ID of the domain.
            token: Authorization token.
            
        Returns:
            A promise that resolves with the certificate issued.
            
        Raises:
            Exception: If the certificate cannot be issued.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(self.certs_url + '/', f"{domain_id}/{self.certs_endpoint}")
        
        payload = {
            "client_id": client_id,
            "ttl": valid
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
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Cert(**response.json())
        except requests.RequestException as error:
            raise error

    def view_cert_by_client(
        self, client_id: str, domain_id: str, token: str
    ) -> CertsPage:
        """
        Retrieves all certs matching the provided client ID.
        
        Args:
            client_id: The unique ID of the client.
            domain_id: The unique ID of the domain.
            token: Authorization token.
            
        Returns:
            A page of certs.
            
        Raises:
            Exception: If the certs cannot be fetched.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(self.certs_url + '/', f"{domain_id}/serials/{client_id}")
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return CertsPage(**response.json())
        except requests.RequestException as error:
            raise error

    def view_cert(self, cert_id: str, domain_id: str, token: str) -> Cert:
        """
        Retrieves a certificate by its id.
        
        Args:
            cert_id: The unique ID of the certificate.
            domain_id: The unique ID of the domain.
            token: Authorization token.
            
        Returns:
            The requested cert object.
            
        Raises:
            Exception: If the cert cannot be fetched.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.certs_url + '/',
            f"{domain_id}/{self.certs_endpoint}/{cert_id}"
        )
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Cert(**response.json())
        except requests.RequestException as error:
            raise error

    def revoke_cert(self, cert_id: str, domain_id: str, token: str) -> Response:
        """
        Revokes and deletes a certificate with specified id.
        
        Args:
            cert_id: The unique ID of the certificate to be revoked.
            domain_id: The unique ID of the domain.
            token: Authorization token.
            
        Returns:
            A promise that resolves when the cert is revoked.
            
        Raises:
            Exception: If the cert cannot be revoked.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.certs_url + '/',
            f"{domain_id}/{self.certs_endpoint}/{cert_id}"
        )
        
        try:
            response = requests.delete(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code)
            
            return Response(
                status=response.status_code,
                message="Cert revoked successfully"
            )
        except requests.RequestException as error:
            raise error