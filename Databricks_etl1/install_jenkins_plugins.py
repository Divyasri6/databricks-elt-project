#!/usr/bin/env python3
"""
Script to install required Jenkins plugins via REST API
Usage: python3 install_jenkins_plugins.py [--jenkins-url URL] [--username USER] [--token TOKEN]
"""

import argparse
import requests
import sys
import time
from urllib.parse import urljoin

# Required plugins to install
REQUIRED_PLUGINS = [
    "workflow-aggregator",  # Pipeline plugin
    "git",                   # Git plugin
    "credentials-binding",   # Credentials Binding plugin
    "ws-cleanup",            # Workspace Cleanup Plugin
]

# Colors for output
class Colors:
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color


def print_success(message):
    print(f"{Colors.GREEN}✓ {message}{Colors.NC}")


def print_error(message):
    print(f"{Colors.RED}✗ {message}{Colors.NC}")


def print_warning(message):
    print(f"{Colors.YELLOW}⚠ {message}{Colors.NC}")


def print_info(message):
    print(f"{Colors.BLUE}ℹ {message}{Colors.NC}")


def test_connection(jenkins_url, username, token):
    """Test connection to Jenkins"""
    url = urljoin(jenkins_url, "/api/json")
    try:
        response = requests.get(url, auth=(username, token), timeout=10)
        if response.status_code == 200:
            return True, "Connected successfully"
        else:
            return False, f"Failed to connect (HTTP {response.status_code})"
    except requests.exceptions.RequestException as e:
        return False, f"Connection error: {str(e)}"


def get_installed_plugins(jenkins_url, username, token):
    """Get list of installed plugins"""
    url = urljoin(jenkins_url, "/pluginManager/api/json?depth=1")
    try:
        response = requests.get(url, auth=(username, token), timeout=10)
        if response.status_code == 200:
            data = response.json()
            return [plugin["shortName"] for plugin in data.get("plugins", [])]
        return []
    except requests.exceptions.RequestException:
        return []


def install_plugin(jenkins_url, username, token, plugin_name):
    """Install a Jenkins plugin"""
    url = urljoin(jenkins_url, "/pluginManager/installNecessaryPlugins")
    data = f'<install plugin="{plugin_name}@latest" />'
    headers = {"Content-Type": "application/xml"}
    
    try:
        response = requests.post(
            url,
            auth=(username, token),
            data=data,
            headers=headers,
            timeout=30
        )
        return response.status_code in [200, 201]
    except requests.exceptions.RequestException:
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Install required Jenkins plugins",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 install_jenkins_plugins.py --jenkins-url http://34.42.84.254:8080 --username admin --token YOUR_TOKEN
  python3 install_jenkins_plugins.py  # Will prompt for credentials interactively
        """
    )
    
    parser.add_argument(
        "--jenkins-url",
        default="http://34.42.84.254:8080",
        help="Jenkins URL (default: http://34.42.84.254:8080)"
    )
    parser.add_argument(
        "--username",
        help="Jenkins username"
    )
    parser.add_argument(
        "--token",
        help="Jenkins API token"
    )
    
    args = parser.parse_args()
    
    # Get credentials if not provided
    username = args.username
    token = args.token
    
    if not username:
        username = input("Enter Jenkins username: ")
    
    if not token:
        import getpass
        token = getpass.getpass("Enter Jenkins API token: ")
    
    jenkins_url = args.jenkins_url.rstrip('/')
    
    print(f"{Colors.GREEN}Jenkins Plugin Installer{Colors.NC}")
    print("=" * 50)
    print(f"Jenkins URL: {jenkins_url}")
    print("")
    
    # Test connection
    print_info("Testing connection to Jenkins...")
    success, message = test_connection(jenkins_url, username, token)
    if not success:
        print_error(message)
        print("\nPlease check:")
        print("1. Jenkins URL is correct")
        print("2. Username and API token are correct")
        print("3. Jenkins is running and accessible")
        print("\nTo get your API token:")
        print("1. Go to Jenkins → Click your username (top right)")
        print("2. Click 'Configure'")
        print("3. Under 'API Token', click 'Add new token'")
        print("4. Copy the token and use it with this script")
        sys.exit(1)
    
    print_success(message)
    print("")
    
    # Get installed plugins
    print_info("Checking installed plugins...")
    installed_plugins = get_installed_plugins(jenkins_url, username, token)
    print(f"Found {len(installed_plugins)} installed plugins")
    print("")
    
    # Install plugins
    failed_plugins = []
    for plugin in REQUIRED_PLUGINS:
        if plugin in installed_plugins:
            print_success(f"Plugin '{plugin}' is already installed")
        else:
            print_warning(f"Installing plugin: {plugin}")
            if install_plugin(jenkins_url, username, token, plugin):
                print_success(f"Plugin '{plugin}' installation initiated")
                # Wait a bit between installations
                time.sleep(2)
            else:
                print_error(f"Failed to install plugin '{plugin}'")
                failed_plugins.append(plugin)
        print("")
    
    # Summary
    print("=" * 50)
    if not failed_plugins:
        print_success("All plugins installation completed!")
        print("")
        print("Next steps:")
        print("1. Go to Jenkins → Manage Jenkins → Manage Plugins")
        print("2. Check if plugins are installed (may take a few minutes)")
        print("3. If prompted, restart Jenkins")
        print("4. After restart, plugins will be available")
    else:
        print_error("Some plugins failed to install:")
        for plugin in failed_plugins:
            print(f"  - {plugin}")
        print("")
        print("You may need to install them manually via Jenkins web UI")
        sys.exit(1)


if __name__ == "__main__":
    main()

