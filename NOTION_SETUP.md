# Notion Integration Quick Setup

This guide will help you quickly set up the Notion integration for the Tiangong Research Database.

## ✅ Integration Setup

You'll need:
- **Integration Token**: From https://www.notion.so/my-integrations (starts with `secret_` or `ntn_`)
- **Database URL**: Your Notion database URL
- **Database ID**: Extracted from the URL (32 character string)

> **Note**: If you have your credentials ready, they should be placed in a `.env` file. See below for details.

## 🚀 Quick Start (2 minutes)

### Step 1: Ensure Database Properties

Make sure your Notion database has these properties:

1. **Name** (Title)
2. **Station** (Select) - Must have options: "Tiangong" and "ISS"
3. **Discipline** (Text)
4. **Country/Institution** (Text)
5. **Timeline Status** (Text)
6. **Objectives** (Text)
7. **Expected Outcomes** (Text)
8. **Principal Investigator** (Text)
9. **Mission Module** (Text)

### Step 2: Share Database with Integration

1. Open your Notion database
2. Click the "..." menu (top-right)
3. Click "Add connections"
4. Select your integration

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment

Create a `.env` file with your credentials:

```bash
# Option 1: Use the interactive setup script
python setup_notion.py

# Option 2: Manually create .env file
cp .env.example .env
# Then edit .env and add:
# NOTION_TOKEN=your_token_here
# NOTION_DATABASE_ID=your_database_id_here
```

### Step 5: Run the Sync

```bash
python sync_to_notion.py
```

This will sync all 67+ space experiments from the CSV to your Notion database!

## 📋 What Gets Synced

The script will sync all experiments from `planned_research_main.csv` including:

- **Tiangong Experiments**: 28 experiments including:
  - Full Life-Cycle Rice Cultivation
  - Zebrafish Aquatic Ecosystem
  - Artificial Photosynthesis Reactor
  - And more...

- **ISS Experiments**: 40+ experiments including:
  - 3D Bioprinting of human organs
  - ZBLAN Optical Fiber Production
  - Remote Robotic Surgery
  - And more...

## 🔄 Automated Sync with GitHub Actions

### Set Up Repository Secrets

1. Go to your repository: https://github.com/YOUR_USERNAME/YOUR_REPO
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Add these repository secrets:
   - `NOTION_TOKEN`: Your Notion integration token
   - `NOTION_DATABASE_ID`: Your Notion database ID

### Automatic Syncing

Once secrets are configured, the database will automatically sync:
- ✅ When you push changes to `planned_research_main.csv`
- ✅ Daily at 2 AM UTC
- ✅ Manually via the Actions tab

## 📊 View Your Data

After syncing, view your experiments in your Notion database.

## 🎨 Customize Your Notion Database

After the initial sync, you can:
- Create different views (Table, Board, Calendar, Gallery)
- Add filters (e.g., show only Tiangong experiments)
- Sort by any property
- Add additional custom properties
- Create relations to other databases

## 🔧 Troubleshooting

### "Integration not found" error
- Make sure you've shared the database with your integration (Step 2 above)

### "Property type mismatch" error
- Verify the "Station" property is type "Select" (not "Text")
- Ensure "Tiangong" and "ISS" are added as options

### Need to test without syncing?
```bash
python test_sync.py
```

This validates CSV parsing and property structure without connecting to Notion.

## 📚 Additional Resources

- Full README: [README.md](README.md)
- Usage Examples: [USAGE.md](USAGE.md)
- Quick Start: [QUICKSTART.md](QUICKSTART.md)
- Interactive Setup: Run `python setup_notion.py` for guided setup

## 🆘 Need Help?

If you encounter issues:
1. Check that all database properties are correct
2. Verify the integration has access to the database
3. Run `python test_sync.py` to check for configuration issues
4. Review error messages in the sync output

---

**Ready to sync?** Just run: `python sync_to_notion.py` 🚀
