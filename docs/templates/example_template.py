"""
Template for creating usage examples for new endpoints.

Usage:
1. Copy this template to examples/{domain}/{method_name}.py
2. Replace placeholders with actual values
3. Add realistic usage scenarios
"""

import patsnap_pythonSDK as patsnap

# Configure the SDK
patsnap.configure(
    client_id="your_client_id",
    client_secret="your_client_secret"
)

def basic_usage():
    """Basic usage example."""
    print("=== Basic {Method Description} ===")
    
    try:
        # Make the API call
        results = patsnap.{domain}.{category}.{method_name}(
            query="example search term",
            limit=10
        )
        
        print(f"Found {results.total_count} total results")
        print(f"Showing {results.result_count} results:")
        
        for i, item in enumerate(results.results, 1):
            print(f"{i}. {item.title} (ID: {item.id})")
            
    except Exception as e:
        print(f"Error: {e}")


def advanced_usage():
    """Advanced usage with filters and pagination."""
    print("\n=== Advanced {Method Description} ===")
    
    try:
        # Advanced search with filters
        results = patsnap.{domain}.{category}.{method_name}(
            query="advanced search term",
            limit=20,
            offset=0,
            # Add domain-specific parameters
            # authority=["US", "CN"],
            # filters={"date_range": "2020-2023"}
        )
        
        print(f"Advanced search found {results.total_count} results")
        
        # Process results
        for item in results.results[:5]:  # Show first 5
            print(f"- {item.title}")
            # Add more processing as needed
            
    except Exception as e:
        print(f"Error in advanced usage: {e}")


def pagination_example():
    """Example of paginating through results."""
    print("\n=== Pagination Example ===")
    
    page_size = 10
    offset = 0
    all_results = []
    
    try:
        while True:
            results = patsnap.{domain}.{category}.{method_name}(
                query="pagination example",
                limit=page_size,
                offset=offset
            )
            
            if not results.results:
                break
                
            all_results.extend(results.results)
            print(f"Fetched page {offset // page_size + 1}, got {len(results.results)} results")
            
            # Check if we have more results
            if len(results.results) < page_size:
                break
                
            offset += page_size
            
        print(f"Total results collected: {len(all_results)}")
        
    except Exception as e:
        print(f"Error in pagination: {e}")


if __name__ == "__main__":
    basic_usage()
    advanced_usage()
    pagination_example()
    
    print("\n=== Example Complete ===")
    print("Remember to replace 'your_client_id' and 'your_client_secret' with actual values!")
