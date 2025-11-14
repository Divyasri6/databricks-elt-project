#!/bin/bash

# Quick script to install Jenkins plugins
# Usage: 
#   export JENKINS_TOKEN="your-token-here"
#   ./run_plugin_install.sh
# Or: JENKINS_TOKEN="your-token" ./run_plugin_install.sh

JENKINS_URL="${JENKINS_URL:-http://34.46.99.31:8080}"
JENKINS_USER="${JENKINS_USER:-admin}"

if [ -z "$JENKINS_TOKEN" ]; then
    echo "Error: JENKINS_TOKEN environment variable is not set"
    echo "Usage: JENKINS_TOKEN='your-token' ./run_plugin_install.sh"
    echo ""
    echo "For this installation, use:"
    echo "JENKINS_TOKEN='2RhzPWolIaq_QV0Ka6I9NBEKsAK0hCVgxs1M-XjlQfAbuY8wH4Blm1-bhz-Bhqw3' ./run_plugin_install.sh"
    exit 1
fi

echo "Installing Jenkins plugins..."
echo "Jenkins URL: $JENKINS_URL"
echo "Username: $JENKINS_USER"
echo ""

cd "$(dirname "$0")"
python3 install_jenkins_plugins.py \
  --jenkins-url "$JENKINS_URL" \
  --username "$JENKINS_USER" \
  --token "$JENKINS_TOKEN"
