"""
Template for creating namespace classes for new endpoints.

Usage:
1. Copy this template to namespaces/{domain}/{category}.py
2. Replace placeholders with actual values
3. Add methods for each endpoint in this category
"""

from __future__ import annotations

from ...http import HttpClient
from ...resources.{domain}.{category} import {Domain}{Category}Resource


class {Domain}{Category}Namespace:
    """Namespace for {domain} {category} operations."""
    
    def __init__(self, http_client: HttpClient) -> None:
        self._resource = {Domain}{Category}Resource(http_client)
    
    def {method_name}(self, **kwargs):
        """
        {Method description}.
        
        Args:
            **kwargs: Parameters passed to the underlying resource method
            
        Returns:
            {EndpointName}Response: The response data
            
        Example:
            >>> results = patsnap.{domain}.{category}.{method_name}(
            ...     query="search term",
            ...     limit=20
            ... )
        """
        return self._resource.{method_name}(**kwargs)


__all__ = ["{Domain}{Category}Namespace"]
