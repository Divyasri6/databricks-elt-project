#!/usr/bin/env python3
"""
Complete Jenkins Setup Script
Automates Steps 4, 5, and 6:
- Step 4: Add Databricks credentials to Jenkins
- Step 5: (Git push - handled separately)
- Step 6: Create Jenkins pipeline job
"""

import argparse
import requests
import sys
import xml.etree.ElementTree as ET
from urllib.parse import urljoin
import base64

# Colors for output
class Colors:
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'


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


def verify_credential_exists(jenkins_url, username, token, credential_id):
    """Verify if a credential exists"""
    url = urljoin(jenkins_url, f"/credentials/store/system/domain/_/credential/{credential_id}/api/json")
    try:
        response = requests.get(url, auth=(username, token), timeout=10)
        return response.status_code == 200
    except:
        return False


def add_databricks_credential(jenkins_url, username, token, databricks_token, credential_id="databricks-pat"):
    """Add Databricks PAT as a credential in Jenkins"""
    print_info(f"Adding Databricks credential with ID: {credential_id}")
    
    # Check if credential already exists
    if verify_credential_exists(jenkins_url, username, token, credential_id):
        print_success(f"Credential '{credential_id}' already exists")
        return True
    
    # Jenkins credentials API endpoint
    url = urljoin(jenkins_url, "/credentials/store/system/domain/_/createCredentials")
    
    # XML payload for secret text credential (StringCredentialsImpl)
    xml_payload = f"""<?xml version='1.1' encoding='UTF-8'?>
<com.cloudbees.plugins.credentials.impl.StringCredentialsImpl>
  <scope>GLOBAL</scope>
  <id>{credential_id}</id>
  <description>Databricks PAT for bundle operations</description>
  <secret>{databricks_token}</secret>
</com.cloudbees.plugins.credentials.impl.StringCredentialsImpl>"""
    
    headers = {
        "Content-Type": "application/xml",
    }
    
    try:
        response = requests.post(
            url,
            auth=(username, token),
            data=xml_payload,
            headers=headers,
            timeout=30,
            allow_redirects=False
        )
        
        # 200 or 201 means success, but Jenkins might return 302 for redirect
        if response.status_code in [200, 201, 302]:
            print_success(f"Credential '{credential_id}' added successfully")
            return True
        else:
            # Check if credential already exists
            if response.status_code == 400:
                print_warning(f"Credential '{credential_id}' might already exist")
                # Try to verify if it exists
                if verify_credential_exists(jenkins_url, username, token, credential_id):
                    print_success(f"Credential '{credential_id}' already exists")
                    return True
            print_error(f"Failed to add credential (HTTP {response.status_code})")
            print_error(f"Response: {response.text[:200]}")
            return False
    except requests.exceptions.RequestException as e:
        print_error(f"Error adding credential: {str(e)}")
        return False


def create_pipeline_job(jenkins_url, username, token, job_name, git_url, branch="*/main", script_path="Databricks_etl1/jenkinsfile"):
    """Create a Jenkins pipeline job"""
    print_info(f"Creating pipeline job: {job_name}")
    
    # Check if job already exists
    url = urljoin(jenkins_url, f"/job/{job_name}/api/json")
    try:
        response = requests.get(url, auth=(username, token), timeout=10)
        if response.status_code == 200:
            print_warning(f"Job '{job_name}' already exists")
            print_info("You may need to update it manually or delete it first")
            return False
    except:
        pass
    
    # Create job
    url = urljoin(jenkins_url, f"/createItem?name={job_name}")
    
    # Pipeline job XML configuration
    xml_config = f"""<?xml version='1.1' encoding='UTF-8'?>
<flow-definition plugin="workflow-job@2.45">
  <actions/>
  <description></description>
  <keepDependencies>false</keepDependencies>
  <properties>
    <hudson.model.ParametersDefinitionProperty>
      <parameterDefinitions>
        <hudson.model.ChoiceParameterDefinition>
          <name>TARGET</name>
          <description>Databricks bundle target environment</description>
          <choices class="java.util.Arrays$ArrayList">
            <a class="string-array">
              <string>dev</string>
              <string>prod</string>
            </a>
          </choices>
        </hudson.model.ChoiceParameterDefinition>
      </parameterDefinitions>
    </hudson.model.ParametersDefinitionProperty>
  </properties>
  <definition class="org.jenkinsci.plugins.workflow.cps.CpsScmFlowDefinition" plugin="workflow-cps@2.94">
    <scm class="hudson.plugins.git.GitSCM" plugin="git@4.11.3">
      <configVersion>2</configVersion>
      <userRemoteConfigs>
        <hudson.plugins.git.UserRemoteConfig>
          <url>{git_url}</url>
        </hudson.plugins.git.UserRemoteConfig>
      </userRemoteConfigs>
      <branches>
        <hudson.plugins.git.BranchSpec>
          <name>{branch}</name>
        </hudson.plugins.git.BranchSpec>
      </branches>
      <doGenerateSubmoduleConfigurations>false</doGenerateSubmoduleConfigurations>
      <submoduleCfg class="list"/>
      <extensions/>
    </scm>
    <scriptPath>{script_path}</scriptPath>
    <lightweight>true</lightweight>
  </definition>
  <triggers/>
  <disabled>false</disabled>
</flow-definition>"""
    
    headers = {
        "Content-Type": "application/xml",
    }
    
    try:
        response = requests.post(
            url,
            auth=(username, token),
            data=xml_config,
            headers=headers,
            timeout=30,
            allow_redirects=False
        )
        
        if response.status_code in [200, 201, 302]:
            print_success(f"Pipeline job '{job_name}' created successfully")
            return True
        else:
            print_error(f"Failed to create job (HTTP {response.status_code})")
            print_error(f"Response: {response.text[:500]}")
            return False
    except requests.exceptions.RequestException as e:
        print_error(f"Error creating job: {str(e)}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Complete Jenkins setup: Add credentials and create pipeline job",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--jenkins-url",
        default="http://34.46.99.31:8080",
        help="Jenkins URL (default: http://34.46.99.31:8080)"
    )
    parser.add_argument(
        "--username",
        default="admin",
        help="Jenkins username (default: admin)"
    )
    parser.add_argument(
        "--jenkins-token",
        required=True,
        help="Jenkins API token"
    )
    parser.add_argument(
        "--databricks-token",
        default="dapi44c942c03edf2bf6518e2f649b51becfs",
        help="Databricks PAT (default: from guide)"
    )
    parser.add_argument(
        "--git-url",
        default="https://github.com/Divyasri6/databricks-elt-project.git",
        help="Git repository URL"
    )
    parser.add_argument(
        "--job-name",
        default="databricks-elt-pipeline",
        help="Jenkins job name (default: databricks-elt-pipeline)"
    )
    parser.add_argument(
        "--branch",
        default="*/main",
        help="Git branch (default: */main)"
    )
    parser.add_argument(
        "--script-path",
        default="Databricks_etl1/jenkinsfile",
        help="Jenkinsfile path (default: Databricks_etl1/jenkinsfile)"
    )
    parser.add_argument(
        "--skip-credentials",
        action="store_true",
        help="Skip adding credentials (Step 4)"
    )
    parser.add_argument(
        "--skip-job",
        action="store_true",
        help="Skip creating job (Step 6)"
    )
    
    args = parser.parse_args()
    
    jenkins_url = args.jenkins_url.rstrip('/')
    
    print(f"{Colors.GREEN}Jenkins Complete Setup{Colors.NC}")
    print("=" * 50)
    print(f"Jenkins URL: {jenkins_url}")
    print(f"Username: {args.username}")
    print(f"Job Name: {args.job_name}")
    print(f"Git URL: {args.git_url}")
    print("")
    
    # Test connection
    print_info("Testing connection to Jenkins...")
    success, message = test_connection(jenkins_url, args.username, args.jenkins_token)
    if not success:
        print_error(message)
        sys.exit(1)
    print_success(message)
    print("")
    
    # Step 4: Add Databricks credentials
    if not args.skip_credentials:
        print(f"{Colors.BLUE}Step 4: Adding Databricks credentials...{Colors.NC}")
        if add_databricks_credential(
            jenkins_url,
            args.username,
            args.jenkins_token,
            args.databricks_token
        ):
            print_success("Step 4 completed")
        else:
            print_warning("Step 4 may have failed, but continuing...")
        print("")
    else:
        print_info("Skipping Step 4 (credentials)")
        print("")
    
    # Step 5: Git push (user needs to do this separately)
    print(f"{Colors.BLUE}Step 5: Git repository{Colors.NC}")
    print_info("Please ensure your code is committed and pushed to:")
    print(f"  {args.git_url}")
    print_info("Run these commands if needed:")
    print("  git add .")
    print("  git commit -m 'Add Jenkins pipeline setup'")
    print("  git push origin main")
    print("")
    
    # Step 6: Create pipeline job
    if not args.skip_job:
        print(f"{Colors.BLUE}Step 6: Creating pipeline job...{Colors.NC}")
        if create_pipeline_job(
            jenkins_url,
            args.username,
            args.jenkins_token,
            args.job_name,
            args.git_url,
            args.branch,
            args.script_path
        ):
            print_success("Step 6 completed")
        else:
            print_error("Step 6 failed")
            sys.exit(1)
        print("")
    else:
        print_info("Skipping Step 6 (job creation)")
        print("")
    
    # Summary
    print("=" * 50)
    print_success("Setup completed!")
    print("")
    print("Next steps:")
    print(f"1. Push your code to Git: {args.git_url}")
    print(f"2. Go to Jenkins: {jenkins_url}")
    print(f"3. Open the job: {jenkins_url}/job/{args.job_name}")
    print("4. Click 'Build with Parameters'")
    print("5. Select TARGET (dev or prod)")
    print("6. Click 'Build'")


if __name__ == "__main__":
    main()

