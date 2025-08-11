# Copyright (c) Abstract Machines
# SPDX-License-Identifier: Apache-2.0

from dataclasses import dataclass


@dataclass
class Error(Exception):
    """
    Error response structure.
    """
    status: int
    error: str


class Errors:
    """
    Error handling utilities for the Magistrala SDK.
    """
    
    @staticmethod
    def handle_error(error: str, status_code: int) -> Error:
        """
        Creates an Error object with the provided error message and status code.
        
        Args:
            error: The error message.
            status_code: The HTTP status code.
            
        Returns:
            An Error object containing the status and error message.
        """
        return Error(
            status=status_code,
            error=error
        )