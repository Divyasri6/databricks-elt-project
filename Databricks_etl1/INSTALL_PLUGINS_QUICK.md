# Quick Guide: Install Jenkins Plugins Automatically

I've created automated scripts to install the required Jenkins plugins for you!

## Option 1: Python Script (Recommended)

### Prerequisites
- Python 3 installed
- `requests` library: `pip3 install requests`
- Jenkins API token

### Get Your Jenkins API Token First

1. Go to http://34.46.99.31:8080/
2. Click on your **username** (top right)
3. Click **Configure**
4. Under **API Token**, click **Add new token**
5. Copy the token (you'll need it)

### Run the Script

```bash
cd Databricks_etl1
python3 install_jenkins_plugins.py
```

The script will prompt you for:
- Jenkins username (usually `admin` or your username)
- Jenkins API token (from step above)

Or run with parameters:
```bash
python3 install_jenkins_plugins.py \
  --jenkins-url http://34.46.99.31:8080 \
  --username admin \
  --token YOUR_API_TOKEN
```

## Option 2: Bash Script

```bash
cd Databricks_etl1
./install_jenkins_plugins.sh http://34.46.99.31:8080 admin YOUR_API_TOKEN
```

## What Gets Installed

The scripts will automatically install:
- ✅ **Pipeline** plugin (workflow-aggregator)
- ✅ **Git** plugin
- ✅ **Credentials Binding** plugin
- ✅ **Workspace Cleanup Plugin** (ws-cleanup)

## After Installation

1. Go to Jenkins → **Manage Jenkins** → **Manage Plugins**
2. Check if plugins are installed (may take a few minutes)
3. If prompted, click **Restart Jenkins**
4. Wait for Jenkins to restart
5. Plugins will be available after restart

## Troubleshooting

### "Connection error" or "Failed to connect"
- Check if Jenkins is running: `curl http://34.46.99.31:8080/api/json`
- Verify the URL is correct
- Check if you can access Jenkins in browser

### "Authentication failed"
- Verify your username is correct
- Check if API token is valid (not expired)
- Generate a new API token if needed

### "Plugin installation failed"
- Some plugins may need manual installation
- Go to Jenkins → Manage Plugins → Available
- Search for the plugin and install manually

