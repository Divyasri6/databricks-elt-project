#!/bin/bash

# Complete setup script for Steps 4, 5, and 6
# Usage: ./setup_steps_4_5_6.sh

set -e

JENKINS_URL="${JENKINS_URL:-http://34.46.99.31:8080}"
JENKINS_USER="${JENKINS_USER:-admin}"
JENKINS_TOKEN="${JENKINS_TOKEN:-2RhzPWolIaq_QV0Ka6I9NBEKsAK0hCVgxs1M-XjlQfAbuY8wH4Blm1-bhz-Bhqw3}"
DATABRICKS_TOKEN="${DATABRICKS_TOKEN:-dapi44c942c03edf2bf6518e2f649b51becfs}"
GIT_URL="${GIT_URL:-https://github.com/Divyasri6/databricks-elt-project.git}"
JOB_NAME="${JOB_NAME:-databricks-elt-pipeline}"

echo "=========================================="
echo "Jenkins Setup: Steps 4, 5, and 6"
echo "=========================================="
echo ""

cd "$(dirname "$0")/.."

# Step 4: Add Databricks credentials to Jenkins
echo "Step 4: Adding Databricks credentials to Jenkins..."
python3 Databricks_etl1/setup_jenkins_complete.py \
  --jenkins-url "$JENKINS_URL" \
  --username "$JENKINS_USER" \
  --jenkins-token "$JENKINS_TOKEN" \
  --databricks-token "$DATABRICKS_TOKEN" \
  --skip-job

if [ $? -ne 0 ]; then
    echo "Warning: Step 4 may have failed, but continuing..."
fi

echo ""
echo "Step 5: Committing and pushing code to Git..."
echo ""

# Check git status
if ! git status &> /dev/null; then
    echo "Error: Not a git repository"
    exit 1
fi

# Check if there are changes
if [ -z "$(git status --porcelain)" ]; then
    echo "No changes to commit"
else
    echo "Staging changes..."
    git add .
    
    echo "Committing changes..."
    git commit -m "Add Jenkins pipeline setup and automation scripts" || {
        echo "Warning: Commit may have failed (maybe no changes?)"
    }
    
    echo "Pushing to remote..."
    git push origin main || {
        echo "Error: Failed to push to remote"
        echo "Please push manually: git push origin main"
        exit 1
    }
    
    echo "✓ Code pushed successfully"
fi

echo ""
echo "Step 6: Creating Jenkins pipeline job..."
echo ""

# Step 6: Create Jenkins pipeline job
python3 Databricks_etl1/setup_jenkins_complete.py \
  --jenkins-url "$JENKINS_URL" \
  --username "$JENKINS_USER" \
  --jenkins-token "$JENKINS_TOKEN" \
  --git-url "$GIT_URL" \
  --job-name "$JOB_NAME" \
  --skip-credentials

if [ $? -ne 0 ]; then
    echo "Error: Failed to create Jenkins job"
    exit 1
fi

echo ""
echo "=========================================="
echo "✓ All steps completed successfully!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Go to Jenkins: $JENKINS_URL"
echo "2. Open the job: $JENKINS_URL/job/$JOB_NAME"
echo "3. Click 'Build with Parameters'"
echo "4. Select TARGET (dev or prod)"
echo "5. Click 'Build'"

