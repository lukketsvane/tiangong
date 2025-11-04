# GitHub Actions Setup Guide

This guide explains how to set up automatic synchronization between your GitHub repository and Notion database using GitHub Actions.

## 📋 Prerequisites

Before setting up GitHub Actions, make sure you have:

1. ✅ A working Notion integration token
2. ✅ A Notion database ID
3. ✅ Admin access to this GitHub repository

## 🔧 Step-by-Step Setup

### Step 1: Locate Your Credentials

You'll need two pieces of information:

#### Notion Integration Token
- Format: `secret_...` or `ntn_...`
- Example: `ntn_N762533464840bhrKQ0gDmSVkczVpOyKrfkk5m8VRH2b1S`
- Where to find it:
  1. Go to https://www.notion.so/my-integrations
  2. Click on your integration (e.g., "tiangong")
  3. Copy the "Internal Integration Token"

#### Notion Database ID
- Format: 32 character alphanumeric string
- Example: `bffb39a4584c462ca4d4bb9e1c892ccb`
- Where to find it:
  1. Open your Notion database in a browser
  2. Look at the URL: `https://www.notion.so/workspace/DATABASE_ID?v=...`
  3. Copy the DATABASE_ID part (between the last `/` and the `?`)
  
  Example URL:
  ```
  https://www.notion.so/tingogtang/bffb39a4584c462ca4d4bb9e1c892ccb?v=85ae6e584e4d45da8d3a6faf5532d790
                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                    This is your Database ID
  ```

### Step 2: Add Secrets to GitHub Repository

1. **Navigate to Repository Settings**
   - Go to https://github.com/lukketsvane/tiangong
   - Click the **Settings** tab (top menu)

2. **Access Secrets Menu**
   - In the left sidebar, click **Secrets and variables**
   - Click **Actions**

3. **Add NOTION_TOKEN Secret**
   - Click **New repository secret**
   - Name: `NOTION_TOKEN`
   - Secret: Paste your Notion integration token
   - Click **Add secret**

4. **Add NOTION_DATABASE_ID Secret**
   - Click **New repository secret** again
   - Name: `NOTION_DATABASE_ID`
   - Secret: Paste your Notion database ID
   - Click **Add secret**

### Step 3: Verify Secrets

After adding both secrets, you should see:
- ✅ NOTION_TOKEN (Updated: [timestamp])
- ✅ NOTION_DATABASE_ID (Updated: [timestamp])

> **Security Note**: Once added, you won't be able to view secret values. You can only update or delete them.

## 🚀 How the Workflow Works

The GitHub Actions workflow (`.github/workflows/sync-notion.yml`) automatically runs:

### Automatic Triggers

1. **On CSV Changes**
   - When you push changes to `planned_research_main.csv` on the main branch
   - Ensures Notion stays in sync with your latest data

2. **Daily Schedule**
   - Runs every day at 2:00 AM UTC
   - Keeps Notion updated even if CSV hasn't changed

3. **Manual Trigger**
   - You can manually run the workflow anytime
   - See "Running the Workflow Manually" below

## ▶️ Running the Workflow Manually

1. Go to the **Actions** tab in your repository
2. Click **Sync to Notion** in the workflows list
3. Click the **Run workflow** dropdown button
4. Select the branch (usually `main`)
5. Click **Run workflow**

The workflow will:
1. ✅ Install Python dependencies
2. ✅ Run validation tests
3. ✅ Sync all data to Notion
4. ✅ Report results

## 📊 Viewing Workflow Results

After a workflow runs:

1. Go to the **Actions** tab
2. Click on the latest run
3. Click on the **sync** job
4. View the output logs

Successful output will show:
```
Starting sync to Notion...
Found 67 experiments in CSV
Fetching existing pages from Notion...
+ Created: Full Life-Cycle Rice Cultivation
+ Created: Hematopoietic Stem Cell Differentiation
...
Sync complete!
Created: 67 pages
Updated: 0 pages
```

## 🔍 Troubleshooting

### Workflow Fails with "NOTION_TOKEN not found"
- Check that you added the secret with the exact name `NOTION_TOKEN`
- Secret names are case-sensitive

### Workflow Fails with "Error 401: Unauthorized"
- Your integration token may be invalid or expired
- Regenerate the token in Notion and update the GitHub secret

### Workflow Fails with "Database not found"
- Verify the database ID is correct
- Ensure the database hasn't been deleted
- Make sure the integration has access to the database

### Workflow Fails with Property Errors
- Run `python validate_notion.py` locally to check database structure
- Ensure all required properties exist with correct types
- The "Station" property must be a Select type with "Tiangong" and "ISS" options

### How to Update Secrets

1. Go to Settings → Secrets and variables → Actions
2. Click the secret name
3. Click **Update**
4. Enter new value
5. Click **Update secret**

## 📝 Workflow File Reference

The workflow file is located at: `.github/workflows/sync-notion.yml`

Key configuration:
```yaml
on:
  push:
    branches: [main]
    paths: ['planned_research_main.csv']
  workflow_dispatch:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM UTC
```

## 🔒 Security Best Practices

- ✅ Never commit your `.env` file (it's in `.gitignore`)
- ✅ Never share your integration token publicly
- ✅ Use GitHub Secrets for sensitive data
- ✅ Regularly rotate your integration tokens
- ✅ Grant minimum necessary permissions to integrations

## ✨ Benefits of Automated Sync

- **Always Up-to-Date**: Notion reflects latest GitHub data
- **Zero Manual Work**: No need to remember to sync
- **Reliable**: Scheduled runs ensure consistency
- **Transparent**: Full logs of every sync operation
- **Fast**: Updates happen within minutes of changes

## 🎯 Next Steps

After setup is complete:

1. **Test the Integration**
   ```bash
   # Manually trigger a sync from the Actions tab
   ```

2. **Make a Test Change**
   ```bash
   # Edit planned_research_main.csv
   # Push to main branch
   # Watch the workflow automatically run
   ```

3. **View Your Data in Notion**
   - Open https://www.notion.so/tingogtang/bffb39a4584c462ca4d4bb9e1c892ccb
   - See all your experiments synced!

4. **Customize Notion Views**
   - Create filtered views
   - Add custom properties
   - Set up automations

---

**Questions?** Check [README.md](README.md) or [USAGE.md](USAGE.md) for more information.
