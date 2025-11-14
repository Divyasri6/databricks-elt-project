#!/usr/bin/env python3
"""
Verify Databricks Token
Tests if the Databricks PAT is valid and has required permissions
"""

import argparse
import requests
import sys

def test_databricks_token(databricks_host, token):
    """Test if Databricks token is valid"""
    print(f"Testing Databricks token...")
    print(f"Host: {databricks_host}")
    
    # Test token by calling Databricks API
    url = f"{databricks_host}/api/2.0/preview/scim/v2/Me"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Token is valid!")
            print(f"User: {data.get('userName', 'Unknown')}")
            print(f"Display Name: {data.get('displayName', 'Unknown')}")
            return True
        elif response.status_code == 401:
            print("❌ Token is invalid or expired")
            return False
        else:
            print(f"⚠️  Unexpected response: HTTP {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Verify Databricks token")
    parser.add_argument(
        "--token",
        default="dapi6c2c4bb9c81d1d6c6f54cd930b4c5ee2",
        help="Databricks PAT"
    )
    parser.add_argument(
        "--host",
        default="https://1275202838893148.8.gcp.databricks.com",
        help="Databricks workspace host"
    )
    
    args = parser.parse_args()
    
    host = args.host.rstrip('/')
    token = args.token
    
    print("=" * 50)
    print("Databricks Token Verification")
    print("=" * 50)
    print("")
    
    if test_databricks_token(host, token):
        print("")
        print("✅ Token is ready to use in Jenkins!")
        sys.exit(0)
    else:
        print("")
        print("❌ Token verification failed")
        print("Please generate a new token from Databricks:")
        print("1. Go to Databricks → Settings → Developer → Access tokens")
        print("2. Generate new token")
        print("3. Copy the token and update it in the scripts")
        sys.exit(1)

if __name__ == "__main__":
    main()

