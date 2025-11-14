#!/bin/bash

# Script to install required Jenkins plugins via REST API
# Usage: ./install_jenkins_plugins.sh <jenkins-url> <username> <api-token>

set -e

JENKINS_URL="${1:-http://34.46.99.31:8080}"
JENKINS_USER="${2}"
JENKINS_TOKEN="${3}"

# Required plugins to install
PLUGINS=(
    "workflow-aggregator"          # Pipeline plugin
    "git"                          # Git plugin
    "credentials-binding"          # Credentials Binding plugin
    "ws-cleanup"                   # Workspace Cleanup Plugin
)

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Jenkins Plugin Installer${NC}"
echo "================================"
echo "Jenkins URL: $JENKINS_URL"
echo ""

# Check if credentials are provided
if [ -z "$JENKINS_USER" ] || [ -z "$JENKINS_TOKEN" ]; then
    echo -e "${YELLOW}Warning: Jenkins credentials not provided${NC}"
    echo "Usage: $0 <jenkins-url> <username> <api-token>"
    echo ""
    echo "To get your API token:"
    echo "1. Go to $JENKINS_URL"
    echo "2. Click on your username (top right)"
    echo "3. Click 'Configure'"
    echo "4. Under 'API Token', click 'Add new token'"
    echo "5. Copy the token and use it with this script"
    echo ""
    read -p "Enter Jenkins username: " JENKINS_USER
    read -sp "Enter Jenkins API token: " JENKINS_TOKEN
    echo ""
fi

# Function to install a plugin
install_plugin() {
    local plugin_name=$1
    echo -e "${YELLOW}Installing plugin: $plugin_name${NC}"
    
    # Check if plugin is already installed
    response=$(curl -s -w "\n%{http_code}" -u "$JENKINS_USER:$JENKINS_TOKEN" \
        "$JENKINS_URL/pluginManager/api/json?depth=1" \
        -H "Content-Type: application/json")
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" -eq 200 ]; then
        if echo "$body" | grep -q "\"shortName\":\"$plugin_name\""; then
            echo -e "${GREEN}Plugin $plugin_name is already installed${NC}"
            return 0
        fi
    fi
    
    # Install plugin
    response=$(curl -s -w "\n%{http_code}" -X POST \
        -u "$JENKINS_USER:$JENKINS_TOKEN" \
        "$JENKINS_URL/pluginManager/installNecessaryPlugins" \
        -H "Content-Type: application/xml" \
        -d "<install plugin=\"$plugin_name@latest\" />")
    
    http_code=$(echo "$response" | tail -n1)
    
    if [ "$http_code" -eq 200 ] || [ "$http_code" -eq 201 ]; then
        echo -e "${GREEN}✓ Plugin $plugin_name installation initiated${NC}"
        return 0
    else
        echo -e "${RED}✗ Failed to install plugin $plugin_name (HTTP $http_code)${NC}"
        return 1
    fi
}

# Test connection
echo "Testing connection to Jenkins..."
response=$(curl -s -w "\n%{http_code}" -u "$JENKINS_USER:$JENKINS_TOKEN" \
    "$JENKINS_URL/api/json")
http_code=$(echo "$response" | tail -n1)

if [ "$http_code" -ne 200 ]; then
    echo -e "${RED}Failed to connect to Jenkins (HTTP $http_code)${NC}"
    echo "Please check:"
    echo "1. Jenkins URL is correct: $JENKINS_URL"
    echo "2. Username and API token are correct"
    echo "3. Jenkins is running and accessible"
    exit 1
fi

echo -e "${GREEN}✓ Connected to Jenkins successfully${NC}"
echo ""

# Install each plugin
failed_plugins=()
for plugin in "${PLUGINS[@]}"; do
    if ! install_plugin "$plugin"; then
        failed_plugins+=("$plugin")
    fi
    echo ""
done

# Summary
echo "================================"
if [ ${#failed_plugins[@]} -eq 0 ]; then
    echo -e "${GREEN}All plugins installed successfully!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Go to $JENKINS_URL"
    echo "2. Click 'Manage Jenkins' → 'Manage Plugins'"
    echo "3. Check if plugins are installed (may need to restart Jenkins)"
    echo "4. If prompted, restart Jenkins"
else
    echo -e "${RED}Some plugins failed to install:${NC}"
    for plugin in "${failed_plugins[@]}"; do
        echo "  - $plugin"
    done
    echo ""
    echo "You may need to install them manually via Jenkins web UI"
fi

