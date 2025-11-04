# ✅ Notion Integration Checklist

Use this checklist to set up your Notion integration step by step.

## 📋 Pre-Setup Checklist

- [ ] I have a Notion account
- [ ] I have admin access to the Notion workspace
- [ ] I have admin access to the GitHub repository
- [ ] I have Python 3.7+ installed (for local sync)

## 🔧 Part 1: Notion Setup

### Step 1: Create Integration
- [ ] Go to https://www.notion.so/my-integrations
- [ ] Click "+ New integration"
- [ ] Name it "Tiangong Database Sync" (or similar)
- [ ] Select your workspace
- [ ] Click "Submit"
- [ ] Copy the integration token
- [ ] Save token somewhere safe (starts with `secret_` or `ntn_`)

### Step 2: Create/Configure Database
- [ ] Open or create database in Notion
- [ ] Add property: **Name** (Title)
- [ ] Add property: **Station** (Select)
  - [ ] Add option: "Tiangong"
  - [ ] Add option: "ISS"
- [ ] Add property: **Discipline** (Text)
- [ ] Add property: **Country/Institution** (Text)
- [ ] Add property: **Timeline Status** (Text)
- [ ] Add property: **Objectives** (Text)
- [ ] Add property: **Expected Outcomes** (Text)
- [ ] Add property: **Principal Investigator** (Text)
- [ ] Add property: **Mission Module** (Text)

### Step 3: Share Database
- [ ] Open your Notion database
- [ ] Click "..." menu (top-right)
- [ ] Click "Add connections"
- [ ] Select your integration
- [ ] Verify "Connected" appears next to integration name

### Step 4: Get Database ID
- [ ] Copy your database URL
- [ ] Extract the 32-character ID from URL
  - Format: `https://www.notion.so/workspace/DATABASE_ID?v=...`
- [ ] Save database ID somewhere safe

## 💻 Part 2: Local Setup (Optional but Recommended)

### Step 5: Clone Repository
- [ ] Clone the repository: `git clone https://github.com/lukketsvane/tiangong.git`
- [ ] Navigate to directory: `cd tiangong`

### Step 6: Install Dependencies
- [ ] Run: `pip install -r requirements.txt`
- [ ] Verify installation succeeded

### Step 7: Configure Environment
Choose one option:

**Option A: Use Setup Wizard**
- [ ] Run: `python setup_notion.py`
- [ ] Follow the prompts
- [ ] Enter your integration token
- [ ] Enter your database ID

**Option B: Manual Configuration**
- [ ] Copy `.env.example` to `.env`
- [ ] Edit `.env` file
- [ ] Add your `NOTION_TOKEN`
- [ ] Add your `NOTION_DATABASE_ID`
- [ ] Save file

### Step 8: Validate Configuration
- [ ] Run: `python test_sync.py`
- [ ] Verify all tests pass
- [ ] Run: `python validate_notion.py`
- [ ] Verify database validation succeeds

### Step 9: First Sync
- [ ] Run: `python sync_to_notion.py`
- [ ] Watch the output for errors
- [ ] Verify "Sync complete!" message
- [ ] Note number of created/updated pages

### Step 10: Verify in Notion
- [ ] Open your Notion database
- [ ] Verify 67+ experiment pages exist
- [ ] Spot-check a few pages for correct data
- [ ] Verify all properties are populated

## 🤖 Part 3: GitHub Actions Setup (Recommended)

### Step 11: Add GitHub Secrets
- [ ] Go to repository on GitHub
- [ ] Navigate to Settings → Secrets and variables → Actions
- [ ] Click "New repository secret"
- [ ] Add secret `NOTION_TOKEN` with your token value
- [ ] Click "Add secret"
- [ ] Click "New repository secret" again
- [ ] Add secret `NOTION_DATABASE_ID` with your database ID
- [ ] Click "Add secret"
- [ ] Verify both secrets appear in the list

### Step 12: Test Workflow
- [ ] Go to Actions tab
- [ ] Click "Sync to Notion" workflow
- [ ] Click "Run workflow" dropdown
- [ ] Select branch (main)
- [ ] Click "Run workflow" button
- [ ] Wait for workflow to complete
- [ ] Verify green checkmark (success)
- [ ] Click on the workflow run to view logs

### Step 13: Verify Automated Sync
- [ ] Check Notion database for updates
- [ ] Verify data matches CSV
- [ ] Confirm no errors in workflow logs

## 🎯 Part 4: Usage & Maintenance

### Step 14: Test CSV Update
- [ ] Make a small test change to `planned_research_main.csv`
- [ ] Commit and push to main branch
- [ ] Watch GitHub Actions automatically trigger
- [ ] Verify sync completes successfully
- [ ] Check Notion for the update

### Step 15: Schedule Verification
- [ ] Verify daily sync is configured (2 AM UTC)
- [ ] Check workflow runs in Actions tab after 24 hours
- [ ] Confirm scheduled runs are working

## 🎨 Part 5: Notion Customization (Optional)

### Step 16: Create Views
- [ ] Create "Tiangong Only" view
  - [ ] Filter: Station = Tiangong
- [ ] Create "ISS Only" view
  - [ ] Filter: Station = ISS
- [ ] Create "Completed" view
  - [ ] Filter: Timeline Status contains "Completed"
- [ ] Create "Ongoing" view
  - [ ] Filter: Timeline Status contains "Ongoing"

### Step 17: Add Custom Properties (Optional)
- [ ] Consider adding: Tags (multi-select)
- [ ] Consider adding: Priority (select)
- [ ] Consider adding: Notes (text)
- [ ] Consider adding: Related Links (URL)

### Step 18: Set Up Automations (Optional)
- [ ] Create automation for new experiment notifications
- [ ] Create automation for status changes
- [ ] Set up database rollups or relations

## 📊 Troubleshooting Checklist

If sync fails, check:

- [ ] Integration token is correct and not expired
- [ ] Database ID is correct
- [ ] Database is shared with integration
- [ ] All 9 required properties exist
- [ ] "Station" property is Select type (not Text)
- [ ] "Station" has "Tiangong" and "ISS" options
- [ ] Internet connection is working
- [ ] GitHub secrets are set correctly (for Actions)

## ✅ Success Criteria

You've successfully completed setup when:

- [ ] Local sync works: `python sync_to_notion.py` succeeds
- [ ] Notion database has 67+ experiments
- [ ] All experiment properties are populated correctly
- [ ] GitHub Actions workflow runs successfully
- [ ] Automatic sync triggers on CSV changes
- [ ] Daily scheduled sync works

## 📚 Reference Documents

- [ ] Read [NOTION_SETUP.md](NOTION_SETUP.md) for quick setup
- [ ] Read [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md) for automation details
- [ ] Read [HOW_IT_WORKS.md](HOW_IT_WORKS.md) to understand the sync process
- [ ] Read [SETUP.md](SETUP.md) for comprehensive overview
- [ ] Bookmark [README.md](README.md) for complete reference

## 🎉 Next Steps After Setup

- [ ] Add more experiments to CSV
- [ ] Create custom Notion views
- [ ] Share database with team members
- [ ] Set up Notion notifications
- [ ] Explore Notion API for custom integrations
- [ ] Consider adding more properties
- [ ] Create Notion templates for experiment pages

## 📝 Notes

Use this space to track your setup progress or issues:

```
Date: ___________
Progress: ____________________________________________
Issues encountered: __________________________________
Solutions applied: ___________________________________
Additional notes: ____________________________________
```

---

**Stuck on a step?** Check the detailed guides or review troubleshooting section above.

**All done?** Congratulations! 🎉 Your Notion integration is fully set up and automated!
