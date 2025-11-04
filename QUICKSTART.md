# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies (1 minute)

```bash
pip install -r requirements.txt
```

### Step 2: Set Up Notion (2 minutes)

1. **Create Integration**: Go to https://www.notion.so/my-integrations
   - Click "+ New integration"
   - Name it "Tiangong Sync"
   - Copy the token (starts with `secret_`)

2. **Create Database**: In Notion, create a new table with these properties:
   - Name (Title)
   - Station (Select) - Add options: "Tiangong", "ISS"
   - Discipline (Text)
   - Country/Institution (Text)
   - Timeline Status (Text)
   - Objectives (Text)
   - Expected Outcomes (Text)
   - Principal Investigator (Text)
   - Mission Module (Text)

3. **Connect Integration**: 
   - In your database, click "..." → "Add connections"
   - Select your integration

4. **Get Database ID**: 
   - Copy from URL: `notion.so/YOUR_DATABASE_ID?v=...`

### Step 3: Configure (1 minute)

```bash
# Copy template
cp .env.example .env

# Edit .env and add:
# NOTION_TOKEN=secret_your_token_here
# NOTION_DATABASE_ID=your_database_id_here
```

### Step 4: Test (30 seconds)

```bash
python test_sync.py
```

You should see:
```
✓ All tests passed! Ready to sync to Notion.
```

### Step 5: Sync! (30 seconds)

```bash
python sync_to_notion.py
```

Expected output:
```
Starting sync to Notion...
Found 67 experiments in CSV
+ Created: Full Life-Cycle Rice Cultivation
+ Created: Hematopoietic Stem Cell Differentiation
...
Sync complete!
Created: 67 pages
```

## ✅ Done!

Check your Notion database - all 67 space experiments are now synced! 🎉

---

## Optional: Set Up GitHub Actions

Add these secrets to your GitHub repository (Settings → Secrets):
- `NOTION_TOKEN`: Your integration token
- `NOTION_DATABASE_ID`: Your database ID

The workflow will automatically sync when you update the CSV file!

---

**Need help?** See [README.md](README.md) for detailed instructions or [USAGE.md](USAGE.md) for examples.
