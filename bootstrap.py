import json
import os
from typing import List
from urllib.parse import urljoin, urlencode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

import requests

from src.magistrala.errors import Errors
from .defs import PageMetadata, BootstrapConfig, BootstrapPage, Response


class Bootstrap:
    """
    Handles interactions with bootstrap API including creating, updating and managing bootstrap configurations.
    """

    def __init__(self, bootstrap_url: str):
        """
        Initializes the Bootstrap API client.
        
        Args:
            bootstrap_url: Base URL for the bootstrap API.
        """
        self.bootstrap_url = bootstrap_url.rstrip('/')
        self.content_type = "application/json"
        self.bootstrap_endpoint = "clients/bootstrap"
        self.configs_endpoint = "clients/configs"
        self.whitelist_endpoint = "clients/state"
        self.bootstrap_certs_endpoint = "clients/configs/certs"
        self.bootstrap_conn_endpoint = "clients/configs/connections"
        self.secure_endpoint = "secure"

    def add_bootstrap(
        self, bootstrap_config: BootstrapConfig, domain_id: str, token: str
    ) -> Response:
        """
        Creates a new bootstrap configuration.
        
        Args:
            bootstrap_config: The bootstrap configuration object containing details like external key, channels, externalId, clientId, etc.
            domain_id: The unique ID of the domain.
            token: Authorization token.
            
        Returns:
            A promise that resolves when the bootstrap configuration is created.
            
        Raises:
            Exception: If the bootstrap configuration cannot be created.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(self.bootstrap_url + '/', f"{domain_id}/{self.configs_endpoint}")
        
        try:
            response = requests.post(
                url,
                headers=headers,
                data=json.dumps(bootstrap_config.__dict__ if hasattr(bootstrap_config, '__dict__') else bootstrap_config),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))
            
            return Response(
                status=response.status_code,
                message="Bootstrap configuration created"
            )
        except requests.RequestException as error:
            raise error

    def whitelist(
        self, bootstrap_config: BootstrapConfig, domain_id: str, token: str
    ) -> Response:
        """
        Updates a bootstrap configuration and changes the status of the config to whitelisted.
        
        Args:
            bootstrap_config: The bootstrap configuration object containing details like external key, channels, externalId, clientId, etc.
            domain_id: The unique ID of the domain.
            token: Authorization token.
            
        Returns:
            A promise that resolves when the bootstrap configuration is whitelisted.
            
        Raises:
            Exception: If the bootstrap configuration cannot be whitelisted.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.bootstrap_url + '/',
            f"{domain_id}/{self.whitelist_endpoint}/{bootstrap_config.client_id}"
        )
        
        try:
            response = requests.put(
                url,
                headers=headers,
                data=json.dumps({"state": bootstrap_config.state}),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))
            
            return Response(
                status=response.status_code,
                message="Bootstrap configuration state updated successfully"
            )
        except requests.RequestException as error:
            raise error

    def update_bootstrap(
        self, bootstrap_config: BootstrapConfig, domain_id: str, token: str
    ) -> Response:
        """
        Updates an existing bootstrap configuration's details.
        
        Args:
            bootstrap_config: The bootstrap configuration object containing details like external key, channels, externalId, clientId, etc.
            domain_id: The unique ID of the domain.
            token: Authorization token.
            
        Returns:
            A promise that resolves when the bootstrap configuration is updated.
            
        Raises:
            Exception: If the bootstrap configuration cannot be updated.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.bootstrap_url + '/',
            f"{domain_id}/{self.configs_endpoint}/{bootstrap_config.client_id}"
        )
        
        try:
            response = requests.put(
                url,
                headers=headers,
                data=json.dumps(bootstrap_config.__dict__ if hasattr(bootstrap_config, '__dict__') else bootstrap_config),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))
            
            return Response(
                status=response.status_code,
                message="Bootstrap configuration updated successfully"
            )
        except requests.RequestException as error:
            raise error

    def view_bootstrap(
        self, client_id: str, domain_id: str, token: str
    ) -> dict:
        """
        Retrieves a bootstrap config by its ID.
        
        Args:
            client_id: The unique identifier of the client.
            domain_id: The unique ID of the domain.
            token: Authorization token.
            
        Returns:
            The requested bootstrap configuration object.
            
        Raises:
            Exception: If the bootstrap configuration cannot be fetched.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.bootstrap_url + '/',
            f"{domain_id}/{self.configs_endpoint}/{client_id}"
        )
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))

            return response.json()
        except requests.RequestException as error:
            raise error

    def update_bootstrap_certs(
        self, bootstrap_config: BootstrapConfig, domain_id: str, token: str
    ) -> dict:
        """
        Updates the details of a specific role in a domain.
        
        Args:
            bootstrap_config: The bootstrap configuration object containing details like external key, channels, externalId, clientId, etc.
            domain_id: The unique ID of the domain.
            token: Authorization token.
            
        Returns:
            The updated bootstrap configuration.
            
        Raises:
            Exception: If the certs cannot be updated.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.bootstrap_url + '/',
            f"{domain_id}/{self.bootstrap_certs_endpoint}/{bootstrap_config.client_id}"
        )
        
        try:
            response = requests.patch(
                url,
                headers=headers,
                data=json.dumps(bootstrap_config.__dict__ if hasattr(bootstrap_config, '__dict__') else bootstrap_config),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))

            return response.json()
        except requests.RequestException as error:
            raise error

    def delete_bootstrap(
        self, client_id: str, domain_id: str, token: str
    ) -> Response:
        """
        Deletes bootstrap configuration with specified id.
        
        Args:
            client_id: The unique ID of the client.
            domain_id: The unique ID of the domain.
            token: Authorization token.
            
        Returns:
            A promise that resolves when the bootstrap configuration is deleted.
            
        Raises:
            Exception: If the bootstrap configuration cannot be deleted.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.bootstrap_url + '/',
            f"{domain_id}/{self.configs_endpoint}/{client_id}"
        )
        
        try:
            response = requests.delete(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))
            
            return Response(
                status=response.status_code,
                message="Bootstrap configuration deleted"
            )
        except requests.RequestException as error:
            raise error

    def bootstrap(self, external_id: str, external_key: str) -> dict:
        """
        Retrieves a configuration with given external ID and encrypted external key.
        
        Args:
            external_id: The external ID of the configuration to be retrieved.
            external_key: The encrypted external key of the configuration to be retrieved.
            
        Returns:
            Returns the requested bootstrap configuration.
            
        Raises:
            Exception: If the bootstrap configuration cannot be retrieved.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Client {external_key}",
        }

        url = urljoin(
            self.bootstrap_url + '/',
            f"{self.bootstrap_endpoint}/{external_id}"
        )
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))

            return response.json()
        except requests.RequestException as error:
            raise error

    def bootstraps(
        self, query_params: PageMetadata, domain_id: str, token: str
    ) -> dict:
        """
        Retrieves all bootstrap configuration matching the provided query parameters.
        
        Args:
            query_params: Query parameters for the request.
            domain_id: The unique ID of the domain.
            token: Authorization token.
            
        Returns:
            A page of bootstrap configurations.
            
        Raises:
            Exception: If the bootstrap configurations cannot be fetched.
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
            self.bootstrap_url + '/',
            f"{domain_id}/{self.configs_endpoint}?{urlencode(string_params)}"
        )
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))
            
            return response.json()
        except requests.RequestException as error:
            raise error

    def update_bootstrap_connection(
        self, client_id: str, domain_id: str, channels: List[str], token: str
    ) -> Response:
        """
        Updates the connection of a bootstrap configuration.
        
        Args:
            client_id: The unique identifier of the client.
            domain_id: The unique ID of the domain.
            channels: An array of unique channels ids to be updated.
            token: Authorization token.
            
        Returns:
            A promise that resolves when the bootstrap configuration connection are updated.
            
        Raises:
            Exception: If the bootstrap configuration cannot be updated.
        """
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {token}",
        }

        url = urljoin(
            self.bootstrap_url + '/',
            f"{domain_id}/{self.bootstrap_conn_endpoint}/{client_id}"
        )
        
        try:
            response = requests.put(
                url,
                headers=headers,
                data=json.dumps({"channels": channels}),
                timeout=30
            )
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))
            
            return Response(
                status=response.status_code,
                message="Bootstrap connection successful"
            )
        except requests.RequestException as error:
            raise error

    def secure_bootstrap(
        self, external_id: str, external_key: str, crypto_key: str
    ) -> dict:
        """
        Secures a bootstrap configuration by encrypting it.
        
        Args:
            external_id: The unique external ID of the bootstrap configuration.
            external_key: The unique external key of the bootstrap configuration.
            crypto_key: The unique crypto key to be used to secure the bootstrap configuration.
            
        Returns:
            Returns the secured bootstrap configuration.
            
        Raises:
            Exception: If the bootstrap configuration cannot be secured.
        """
        encrypted_key = self.bootstrap_encrypt(external_key, crypto_key)
        
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Client {encrypted_key}",
        }

        url = urljoin(
            self.bootstrap_url + '/',
            f"{self.bootstrap_endpoint}/{self.secure_endpoint}/{external_id}"
        )
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if not response.ok:
                error_res = response.json()
                raise Errors.handle_error(error_res.get("message"), response.status_code, error_res.get("error"))
            
            # Decrypt the response
            encrypted_response = response.text
            decrypted_data = self.bootstrap_decrypt(encrypted_response, crypto_key)
            return decrypted_data
        except requests.RequestException as error:
            raise error

    @staticmethod
    def bootstrap_encrypt(text: str, crypto_key: str) -> str:
        """
        Encrypts text using AES-256-CFB encryption.
        
        Args:
            text: The text to encrypt.
            crypto_key: The encryption key.
            
        Returns:
            The encrypted data as a hex string.
        """
        # Generate a random IV
        iv = os.urandom(16)
        
        # Create cipher
        cipher = Cipher(
            algorithms.AES(crypto_key.encode()[:32].ljust(32, b'\0')),
            modes.CFB(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        
        # Encrypt the text
        encrypted = encryptor.update(text.encode('utf-8')) + encryptor.finalize()
        
        # Combine IV and encrypted data
        encrypted_data = iv + encrypted
        
        return encrypted_data.hex()

    @staticmethod
    def bootstrap_decrypt(encrypted_data: str, crypto_key: str) -> dict:
        """
        Decrypts encrypted data using AES-256-CFB decryption.
        
        Args:
            encrypted_data: The encrypted data as a hex string.
            crypto_key: The decryption key.
            
        Returns:
            The decrypted bootstrap configuration.
        """
        # Convert hex string to bytes
        encrypted_buffer = bytes.fromhex(encrypted_data)
        
        # Extract IV (first 16 bytes)
        iv = encrypted_buffer[:16]
        encrypted_content = encrypted_buffer[16:]
        
        # Create cipher
        cipher = Cipher(
            algorithms.AES(crypto_key.encode()[:32].ljust(32, b'\0')),
            modes.CFB(iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        
        # Decrypt the content
        decrypted = decryptor.update(encrypted_content) + decryptor.finalize()
        
        # Parse JSON and return BootstrapConfig
        decrypted_text = decrypted.decode('utf-8')
        return json.loads(decrypted_text)