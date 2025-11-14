# Quick Setup: Steps 4, 5, and 6

## ✅ Step 5: COMPLETED (Code Committed)

Your code has been committed locally. **Push to GitHub:**
```bash
cd /Users/divyasrikoppaka/Desktop/office\ code/databricks-elt-project
git push origin main
```

---

## 🚀 Steps 4 and 6: Run These Commands

**From a machine that can access Jenkins (http://34.46.99.31:8080):**

### Complete Setup (Recommended)
```bash
cd Databricks_etl1
JENKINS_TOKEN='2RhzPWolIaq_QV0Ka6I9NBEKsAK0hCVgxs1M-XjlQfAbuY8wH4Blm1-bhz-Bhqw3' \
python3 setup_jenkins_complete.py \
  --jenkins-url http://34.46.99.31:8080 \
  --username admin \
  --jenkins-token "2RhzPWolIaq_QV0Ka6I9NBEKsAK0hCVgxs1M-XjlQfAbuY8wH4Blm1-bhz-Bhqw3" \
  --databricks-token "dapi44c942c03edf2bf6518e2f649b51becfs" \
  --git-url "https://github.com/Divyasri6/databricks-elt-project.git"
```

### Or Use the Shell Script
```bash
cd Databricks_etl1
JENKINS_TOKEN='2RhzPWolIaq_QV0Ka6I9NBEKsAK0hCVgxs1M-XjlQfAbuY8wH4Blm1-bhz-Bhqw3' \
./setup_steps_4_5_6.sh
```

---

## 📋 What This Does

**Step 4:** Adds Databricks credential (`databricks-pat`) to Jenkins
**Step 6:** Creates Jenkins pipeline job (`databricks-elt-pipeline`)

---

## ✅ After Running

1. **Verify in Jenkins:**
   - Go to: http://34.46.99.31:8080/job/databricks-elt-pipeline
   - Credentials: http://34.46.99.31:8080/credentials/store/system/domain/_/

2. **Run the Pipeline:**
   - Click "Build with Parameters"
   - Select TARGET: `dev` or `prod`
   - Click "Build"

---

## 🔍 Troubleshooting

- **Connection timeout**: Run from a machine that can access Jenkins
- **Authentication failed**: Verify Jenkins token is correct
- **Git push failed**: Configure git credentials or push manually

