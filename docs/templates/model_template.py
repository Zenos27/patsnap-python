"""
Template for creating Pydantic models for new endpoints.

Usage:
1. Copy this template to models/{domain}/{category}.py
2. Replace placeholders with actual values
3. Add proper field descriptions and validation
"""

from __future__ import annotations

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class {EndpointName}Request(BaseModel):
    """Request model for {endpoint_description}.
    
    Example:
        >>> request = {EndpointName}Request(
        ...     query="search term",
        ...     limit=20
        ... )
    """
    
    # Add your request fields here
    query: Optional[str] = Field(None, description="Search query")
    limit: Optional[int] = Field(default=10, ge=1, le=1000, description="Maximum number of results")
    offset: Optional[int] = Field(default=0, ge=0, description="Number of results to skip")
    
    # Add domain-specific fields
    # authority: Optional[List[str]] = Field(None, description="Patent authorities")
    # filters: Optional[Dict[str, Any]] = Field(None, description="Additional filters")


class {EndpointName}Item(BaseModel):
    """Individual item in the {endpoint_description} response."""
    
    # Add response item fields
    id: str = Field(description="Unique identifier")
    title: str = Field(description="Item title")
    # Add more fields as needed


class {EndpointName}Response(BaseModel):
    """Response model for {endpoint_description}.
    
    Example:
        >>> response = {EndpointName}Response(
        ...     results=[...],
        ...     total_count=100
        ... )
    """
    
    results: List[{EndpointName}Item] = Field(description="List of results")
    total_count: int = Field(description="Total number of available results")
    result_count: int = Field(description="Number of results in this response")
    
    # Add pagination info if needed
    # has_more: bool = Field(description="Whether more results are available")
    # next_offset: Optional[int] = Field(None, description="Offset for next page")


__all__ = [
    "{EndpointName}Request",
    "{EndpointName}Item", 
    "{EndpointName}Response",
]
