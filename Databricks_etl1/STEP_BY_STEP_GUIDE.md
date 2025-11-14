# Step-by-Step Guide: Setting Up and Running Jenkins Pipeline

## Prerequisites Checklist
- [ ] Jenkins is running at http://34.46.99.31:8080/
- [ ] You have access to your Databricks workspace
- [ ] Your code is in a Git repository (GitHub, GitLab, etc.)

---

## Step 1: Access Jenkins Web Interface

1. Open your web browser
2. Navigate to: ** *
3. If this is your first time:
   - You'll see an "Unlock Jenkins" page
   - SSH into your Jenkins server and run:
     ```bash
     sudo cat /var/lib/jenkins/secrets/initialAdminPassword
     ```
   - Copy the password and paste it into the Jenkins web page
   - Click "Continue"
4. Complete the setup wizard:
   - Click "Install suggested plugins"
   - Wait for installation to complete
   - Create an admin user (save credentials!)
   - Click "Save and Finish"

---

## Step 2: Get Your Databricks Personal Access Token (PAT)

1. Log in to your Databricks workspace: https://1275202838893148.8.gcp.databricks.com
2. Click on your **username** (top right) → **Settings**
3. Go to **Developer** → **Access tokens**
4. Click **Generate new token**
5. Add a description: "Jenkins Pipeline Token"
6. Set expiration (recommended: 90 days or custom)
7. Click **Generate**
8. **IMPORTANT**: Copy the token immediately (you won't see it again!)
   - Save it securely (password manager, notes app, etc.)
   dapi44c942c03edf2bf6518e2f649b51becfs

---

## Step 3: Install Required Jenkins Plugins

### Option A: Automated Installation (Recommended)

**Get your Jenkins API token first:**
1. Go to http://34.46.99.31:8080/
2. Click on your **username** (top right)
3. Click **Configure**
4. Under **API Token**, click **Add new token**
5. Copy the token

**Run the installation script:**
```bash
cd Databricks_etl1
python3 install_jenkins_plugins.py --jenkins-url http://34.46.99.31:8080
```

The script will prompt for your username and API token, then automatically install all required plugins.

### Option B: Manual Installation

1. In Jenkins, go to **Manage Jenkins** (left sidebar)
2. Click **Manage Plugins**
3. Go to the **Available** tab
4. Search for and install these plugins (check the boxes, then click "Install without restart"):
   - ✅ **Pipeline** (search for "workflow-aggregator")
   - ✅ **Git**
   - ✅ **Credentials Binding**
   - ✅ **Workspace Cleanup Plugin** (search for "ws-cleanup")
5. After installation, click **Restart Jenkins when installation is complete and no jobs are running**

---

## Step 4: Configure Databricks Credentials in Jenkins

1. In Jenkins, go to **Manage Jenkins** → **Credentials**
2. Click **System** → **Global credentials (unrestricted)**
3. Click **Add Credentials** (left sidebar)
4. Fill in the form:
   - **Kind**: Select **Secret text**
   - **Secret**: Paste your Databricks PAT (from Step 2)
   - **ID**: Type exactly: `databricks-pat`
   - **Description**: "Databricks PAT for bundle operations"
5. Click **OK**
6. Verify: You should see `databricks-pat` in the credentials list

---

## Step 5: Push Your Code to Git Repository

1. Make sure your code is committed and pushed to your Git repository
2. Note your repository URL (you'll need it in the next step)
   - Example: `https://github.com/yourusername/databricks-elt-project.git`
   - Or: `git@github.com:yourusername/databricks-elt-project.git`

---

## Step 6: Create the Pipeline Job in Jenkins

1. In Jenkins dashboard, click **New Item** (left sidebar)
2. Enter item name: `databricks-elt-pipeline`
3. Select **Pipeline** (not "Freestyle project")
4. Click **OK**
5. Scroll down to **Pipeline** section
6. Configure:
   - **Definition**: Select **Pipeline script from SCM**
   - **SCM**: Select **Git**
   - **Repository URL**: Enter your Git repository URL
   - **Credentials**: 
     - If repository is **public**: Leave empty
     - If repository is **private**: Click "Add" → Add your Git credentials
   - **Branch**: Enter `*/main` (or `*/master` if that's your default branch)
   - **Script Path**: Enter `Databricks_etl1/jenkinsfile`
7. Click **Save**

---

## Step 7: Run the Pipeline

### Option A: First Run (Build with Parameters)

1. On the pipeline job page, click **Build with Parameters**
2. You'll see a dropdown for **TARGET**
3. Select:
   - **dev** (for development/testing)
   - **prod** (for production - use carefully!)
4. Click **Build**

### Option B: Subsequent Runs

1. On the pipeline job page, click **Build Now** (uses default: dev)
2. Or click **Build with Parameters** to choose dev/prod

---

## Step 8: Monitor Pipeline Execution

1. Click on the build number (e.g., "#1") in the **Build History** section
2. Click **Console Output** to see real-time logs
3. Watch the stages execute:
   - ✅ Checkout Code
   - ✅ Setup Python Environment
   - ✅ Install Databricks CLI
   - ✅ Validate Bundle
   - ✅ Deploy Bundle
   - ✅ Run ELT Pipeline Job

---

## Step 9: Verify Results

1. **In Jenkins**:
   - Green checkmark = Success ✅
   - Red X = Failure ❌ (check console output for errors)

2. **In Databricks**:
   - Go to: https://1275202838893148.8.gcp.databricks.com
   - Navigate to **Workflows** → **Jobs**
   - Look for "ELT Pipeline (Bronze-Silver-Gold)" job
   - Check if it ran successfully

---

## Troubleshooting Common Issues

### Issue: "Credentials not found"
**Solution**: 
- Go to Step 4 again
- Verify credential ID is exactly `databricks-pat` (case-sensitive)
- Make sure it's in "Global credentials (unrestricted)"

### Issue: "Cannot connect to Databricks"
**Solution**:
- Verify your PAT is valid (not expired)
- Check if Databricks workspace URL is accessible
- Regenerate PAT if needed

### Issue: "Git repository not found"
**Solution**:
- Verify repository URL is correct
- For private repos, add Git credentials in Jenkins
- Check if branch name matches (main vs master)

### Issue: "Python not found"
**Solution**:
- The pipeline will try to install Python dependencies
- If it fails, you may need to configure a Jenkins agent with Python 3 installed

### Issue: "Bundle validation fails"
**Solution**:
- Check `databricks.yml` file is correct
- Verify Databricks host URL matches your workspace
- Ensure PAT has required permissions

---

## Quick Reference

- **Jenkins URL**: http://34.46.99.31:8080/
- **Databricks Workspace**: https://1275202838893148.8.gcp.databricks.com
- **Credential ID**: `databricks-pat`
- **Pipeline Script Path**: `Databricks_etl1/jenkinsfile`
- **Default Target**: `dev`

---

## Next Steps After Successful Run

1. Set up automated triggers (e.g., on Git push)
2. Configure notifications (email, Slack, etc.)
3. Add more stages if needed (testing, linting, etc.)
4. Set up production deployment workflow

---

## Need Help?

- Check Jenkins console output for detailed error messages
- Review Databricks job logs in the Databricks workspace
- Verify all credentials and permissions are set correctly

