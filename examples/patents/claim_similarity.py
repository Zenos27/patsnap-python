#!/usr/bin/env python3
"""
Patent Claim Similarity Analysis Example

This example demonstrates how to use the Patsnap Python SDK to analyze the similarity
between two patent claim texts using deep learning models.

The claim similarity API can accurately identify similarities in technical features,
structural composition, and expression methods of claims, supporting both Chinese
and English claim texts.

Similarity Score Interpretation:
- Above 0.8: High similarity
- 0.6-0.8: Moderate similarity  
- Below 0.6: Low similarity

Usage:
    python examples/patents/claim_similarity.py
"""

import os
import sys
from pathlib import Path

# Add the parent directory to the path so we can import the SDK
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from patsnap_pythonSDK import PatsnapClient


def main():
    """Main function demonstrating claim similarity analysis."""
    
    # Initialize the client
    # You can set your API key and secret as environment variables:
    # export PATSNAP_API_KEY="your_api_key"
    # export PATSNAP_API_SECRET="your_api_secret"
    
    api_key = os.getenv("PATSNAP_API_KEY")
    api_secret = os.getenv("PATSNAP_API_SECRET")
    
    if not api_key or not api_secret:
        print("Please set PATSNAP_API_KEY and PATSNAP_API_SECRET environment variables")
        return
    
    # Create client instance
    client = PatsnapClient(api_key=api_key, api_secret=api_secret)
    
    # Example claim texts for comparison
    # Source claim - more detailed server system with permission server
    src_claim = """1. A server system including:
    a permission server in communication with a plurality of clients, wherein the permission server utilizes client device information provided by the plurality of clients to determine an identifier corresponding to at least one data stream of a plurality of data streams for each of the plurality of clients;
    a memory; and
    at least one processor configured to multicast data to the plurality of clients, each client storing the identifier provided by the permission server and corresponding to at least one data stream of the plurality of data streams associated with the client,
    wherein the at least one processor is further configured to:
        receive the plurality of the data streams, each of the data streams including data;
        determine the identifier corresponding to at least one of the plurality of received data streams;
        transmit, to the plurality of clients, a mapping between each identifier and a respective multicast stream; and
        multicast data of the plurality of received data streams in accordance with the mapping."""
    
    # Target claim - simplified server system without permission server
    tgt_claim = """1. A server system including:
    a memory; and
    at least one processor configured to multicast data to a plurality of clients, each client storing an identifier corresponding to at least one data stream of a plurality of data streams associated with the client,
    wherein the at least one processor is further configured to:
        receive the plurality of the data streams, each of the data streams including data;
        determine the identifier corresponding to at least one of the plurality of received data streams;
        transmit, to the plurality of clients, a mapping between each identifier and a respective multicast stream; and
        multicast data of the plurality of received data streams in accordance with the mapping."""
    
    try:
        print("Analyzing claim similarity...")
        print("=" * 60)
        
        # Perform claim similarity analysis
        result = client.patents.search.claim_similarity(
            src=src_claim,
            tgt=tgt_claim
        )
        
        # Display results
        print(f"Similarity Score: {result.data.score:.4f}")
        print(f"Status: {'Success' if result.status else 'Failed'}")
        
        if result.error_code != 0:
            print(f"Error Code: {result.error_code}")
            if result.error_msg:
                print(f"Error Message: {result.error_msg}")
        
        # Interpret the similarity score
        print("\nSimilarity Interpretation:")
        if result.data.score > 0.8:
            print("🟢 High similarity detected - Claims are very similar")
            print("   The claims share most technical features and structural elements")
        elif result.data.score > 0.6:
            print("🟡 Moderate similarity detected - Claims have some similarities")
            print("   The claims share some technical features but have notable differences")
        else:
            print("🔴 Low similarity detected - Claims are quite different")
            print("   The claims have few shared technical features or structural elements")
        
        # Display claim comparison
        print("\n" + "=" * 60)
        print("CLAIM COMPARISON")
        print("=" * 60)
        
        print("\nSOURCE CLAIM:")
        print("-" * 40)
        print(src_claim)
        
        print("\nTARGET CLAIM:")
        print("-" * 40)
        print(tgt_claim)
        
        # Analysis insights
        print("\n" + "=" * 60)
        print("ANALYSIS INSIGHTS")
        print("=" * 60)
        
        print("\nKey Differences Identified:")
        print("• Source claim includes a 'permission server' component")
        print("• Source claim has more detailed client-server interaction")
        print("• Target claim is a simplified version focusing on core functionality")
        print("• Both claims share the same core multicast data processing logic")
        
        print(f"\nThe similarity score of {result.data.score:.4f} reflects that while both")
        print("claims describe server systems with multicast capabilities, the source")
        print("claim includes additional permission management functionality that")
        print("differentiates it from the simpler target claim.")
        
    except Exception as e:
        print(f"Error occurred: {e}")
        return


def demonstrate_different_similarity_levels():
    """Demonstrate different levels of claim similarity."""
    
    api_key = os.getenv("PATSNAP_API_KEY")
    api_secret = os.getenv("PATSNAP_API_SECRET")
    
    if not api_key or not api_secret:
        print("Please set PATSNAP_API_KEY and PATSNAP_API_SECRET environment variables")
        return
    
    client = PatsnapClient(api_key=api_key, api_secret=api_secret)
    
    # Test cases with different similarity levels
    test_cases = [
        {
            "name": "High Similarity Test",
            "description": "Nearly identical claims with minor wording differences",
            "src": "1. A method for processing data comprising: receiving input data; processing the input data using a neural network; and outputting processed data.",
            "tgt": "1. A method for data processing comprising: receiving input data; processing said input data using a neural network; and outputting the processed data."
        },
        {
            "name": "Moderate Similarity Test", 
            "description": "Related claims with some shared features but different focus",
            "src": "1. A wireless communication device comprising: an antenna; a processor; and memory storing instructions for signal processing.",
            "tgt": "1. A mobile phone comprising: a display screen; a processor; memory; and wireless communication capabilities."
        },
        {
            "name": "Low Similarity Test",
            "description": "Completely different technical domains",
            "src": "1. A method for baking bread comprising: mixing flour and water; kneading the dough; and baking in an oven.",
            "tgt": "1. A computer system comprising: a central processing unit; random access memory; and a storage device."
        }
    ]
    
    print("\n" + "=" * 80)
    print("DEMONSTRATING DIFFERENT SIMILARITY LEVELS")
    print("=" * 80)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print(f"   {test_case['description']}")
        print("-" * 60)
        
        try:
            result = client.patents.search.claim_similarity(
                src=test_case['src'],
                tgt=test_case['tgt']
            )
            
            score = result.data.score
            print(f"Similarity Score: {score:.4f}")
            
            if score > 0.8:
                level = "HIGH 🟢"
            elif score > 0.6:
                level = "MODERATE 🟡"
            else:
                level = "LOW 🔴"
            
            print(f"Similarity Level: {level}")
            
        except Exception as e:
            print(f"Error in test case {i}: {e}")


if __name__ == "__main__":
    print("Patent Claim Similarity Analysis Example")
    print("=" * 50)
    
    # Run main example
    main()
    
    # Run additional demonstrations
    demonstrate_different_similarity_levels()
    
    print("\n" + "=" * 50)
    print("Example completed!")
