"""
Template for creating HTTP resource handlers for new endpoints.

Usage:
1. Copy this template to resources/{domain}/{category}.py
2. Replace placeholders with actual values
3. Implement the HTTP calls to actual endpoints
"""

from __future__ import annotations

from typing import Optional, List, Dict, Any

from ...http import HttpClient
from ...models.{domain}.{category} import (
    {EndpointName}Request,
    {EndpointName}Response,
)


class {Domain}{Category}Resource:
    """Resource handler for {domain} {category} operations."""
    
    def __init__(self, http_client: HttpClient) -> None:
        self._http = http_client
    
    def {method_name}(
        self,
        *,
        # Add method parameters here
        query: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        **kwargs
    ) -> {EndpointName}Response:
        """
        {Method description}.
        
        Args:
            query: Search query
            limit: Maximum number of results (default: 10, max: 1000)
            offset: Number of results to skip (default: 0)
            **kwargs: Additional parameters
            
        Returns:
            {EndpointName}Response: The response data
            
        Raises:
            ApiError: If the API request fails
            ValidationError: If the request parameters are invalid
            
        Example:
            >>> resource = {Domain}{Category}Resource(http_client)
            >>> response = resource.{method_name}(
            ...     query="search term",
            ...     limit=20
            ... )
        """
        # Create and validate request
        request = {EndpointName}Request(
            query=query,
            limit=limit,
            offset=offset,
            **kwargs
        )
        
        # Convert request to dict and filter out None values
        params = {k: v for k, v in request.model_dump().items() if v is not None}
        
        # Make HTTP request
        # Replace with actual endpoint URL
        response = self._http.post("/v2/{domain}/{category}/{endpoint}", params=params)
        
        # Parse and return response
        return {EndpointName}Response(**response["data"])


__all__ = ["{Domain}{Category}Resource"]
