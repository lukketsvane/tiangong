# 🎯 Setup Summary - Notion Integration for Tiangong Database

This document provides a quick reference for setting up the Notion integration.

## ✅ What's Been Done

Your Tiangong repository now includes:

1. **Core Sync Script** (`sync_to_notion.py`)
   - Syncs CSV data to Notion database
   - Creates and updates Notion pages
   - Handles 67+ space experiments

2. **Setup Tools**
   - `setup_notion.py` - Interactive setup wizard
   - `validate_notion.py` - Database configuration validator
   - `test_sync.py` - CSV and property validation (no API calls)

3. **Documentation**
   - `NOTION_SETUP.md` - Quick start with your credentials
   - `GITHUB_ACTIONS_SETUP.md` - Automated sync setup
   - Updated `README.md` - Complete reference
   - `USAGE.md` - Usage examples
   - `QUICKSTART.md` - 5-minute setup guide

4. **GitHub Actions Workflow**
   - `.github/workflows/sync-notion.yml`
   - Automatic sync on CSV changes
   - Daily scheduled sync
   - Manual trigger option

## 📊 Your Integration Details

- **Integration Token**: `ntn_N762533464840bhrKQ0gDmSVkczVpOyKrfkk5m8VRH2b1S`
- **Database ID**: `bffb39a4584c462ca4d4bb9e1c892ccb`
- **Database URL**: https://www.notion.so/tingogtang/bffb39a4584c462ca4d4bb9e1c892ccb

## 🚀 Quick Start (Choose Your Path)

### Path 1: Local Sync (Fastest)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Ensure database has correct properties (see below)

# 3. Share database with your integration in Notion

# 4. Configuration is ready in .env file

# 5. Validate setup
python validate_notion.py

# 6. Run sync
python sync_to_notion.py
```

### Path 2: GitHub Actions (Automated)

```bash
# 1. Go to repository Settings → Secrets and variables → Actions

# 2. Add secrets:
#    - NOTION_TOKEN: ntn_N762533464840bhrKQ0gDmSVkczVpOyKrfkk5m8VRH2b1S
#    - NOTION_DATABASE_ID: bffb39a4584c462ca4d4bb9e1c892ccb

# 3. Go to Actions tab → Sync to Notion → Run workflow

# 4. Watch it sync automatically!
```

### Path 3: Interactive Setup

```bash
# 1. Run the setup wizard
python setup_notion.py

# 2. Follow the prompts

# 3. Sync when ready
python sync_to_notion.py
```

## 📋 Required Database Properties

Your Notion database **must** have these properties:

| Property Name          | Type       | Notes                              |
|------------------------|------------|------------------------------------|
| Name                   | Title      | Experiment name                    |
| Station                | Select     | Options: "Tiangong", "ISS"         |
| Discipline             | Text       |                                    |
| Country/Institution    | Text       |                                    |
| Timeline Status        | Text       |                                    |
| Objectives             | Text       |                                    |
| Expected Outcomes      | Text       |                                    |
| Principal Investigator | Text       |                                    |
| Mission Module         | Text       |                                    |

> **Critical**: The "Station" property must be a **Select** type with exactly two options: "Tiangong" and "ISS"

## 🔗 Database Connection Checklist

Before running the sync, ensure:

- [ ] Database exists at: https://www.notion.so/tingogtang/bffb39a4584c462ca4d4bb9e1c892ccb
- [ ] All 9 properties are created with correct types
- [ ] "Station" property has "Tiangong" and "ISS" options
- [ ] Database is shared with your "tiangong" integration:
  - Click "..." in database → "Add connections" → Select "tiangong"
- [ ] Integration token is valid and not expired

## 📈 What Gets Synced

The sync will create **67+ Notion pages** from your CSV:

### Tiangong Experiments (28)
- Full Life-Cycle Rice Cultivation
- Zebrafish Aquatic Ecosystem (43-day habitat)
- Artificial Photosynthesis Reactor
- Hematopoietic Stem Cell Differentiation
- Niallia tiangongensis Discovery
- And 23 more...

### ISS Experiments (40+)
- 3D Bioprinted Heart Tissue
- 3D Bioprinted Liver Tissue Patch
- Remote Robotic Surgery (spaceMIRA)
- ZBLAN Optical Fiber Production
- Keytruda Crystallization
- And 35+ more...

## 🧪 Testing Before Sync

### Test 1: CSV Validation (No API)
```bash
python test_sync.py
```
Expected: All tests pass ✓

### Test 2: Database Validation (Requires API)
```bash
python validate_notion.py
```
Expected: All properties validated ✓

### Test 3: Dry Run
The current scripts don't have a dry-run mode, but you can:
1. Create a test database
2. Update `NOTION_DATABASE_ID` in `.env` to test database ID
3. Run `python sync_to_notion.py`
4. Verify results
5. Switch back to production database ID

## 🔧 Troubleshooting

### Cannot Access Notion API
- Check internet connection
- Verify token is not expired
- Ensure token starts with `secret_` or `ntn_`

### "Integration Not Found" Error
- Database must be shared with integration
- Go to database → "..." → "Add connections" → Select your integration

### Property Type Mismatch
- Run `python validate_notion.py` to identify issues
- Fix property types in Notion
- Re-run validation

### Sync Creates Duplicates
- The script matches on experiment name
- If experiment names changed, it creates new entries
- To avoid duplicates: keep experiment names consistent

## 📚 Documentation Reference

| Document                  | Purpose                                |
|---------------------------|----------------------------------------|
| NOTION_SETUP.md           | Quick setup with your credentials      |
| GITHUB_ACTIONS_SETUP.md   | Automated sync configuration           |
| README.md                 | Complete documentation                 |
| USAGE.md                  | Usage examples and workflows           |
| QUICKSTART.md             | 5-minute setup guide                   |
| This file (SETUP.md)      | Summary and quick reference            |

## 🎓 Next Steps

1. **Immediate**: Set up database properties and share with integration
2. **Short-term**: Run local sync to populate database
3. **Medium-term**: Configure GitHub Actions for automation
4. **Long-term**: Customize Notion views and add automations

## 🆘 Getting Help

If you encounter issues:

1. **Check Documentation**
   - Review guides in this repository
   - Check error messages carefully

2. **Validate Configuration**
   ```bash
   python validate_notion.py
   ```

3. **Test Locally First**
   ```bash
   python test_sync.py
   python sync_to_notion.py
   ```

4. **Review Logs**
   - Sync script provides detailed output
   - GitHub Actions shows full logs

## 🎉 Success Criteria

You'll know the setup is successful when:

- ✅ `python test_sync.py` passes all tests
- ✅ `python validate_notion.py` confirms database configuration
- ✅ `python sync_to_notion.py` completes without errors
- ✅ Your Notion database shows 67+ experiment pages
- ✅ Each page has all properties populated
- ✅ GitHub Actions runs successfully (if configured)

---

**Ready to sync?** Pick your path above and get started! 🚀

For detailed instructions, see:
- [NOTION_SETUP.md](NOTION_SETUP.md) - Start here
- [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md) - For automation
