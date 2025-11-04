# Troubleshooting Guide

## GitHub Action Runs Successfully But No Content in Notion

If your GitHub Action shows a green checkmark but you don't see any experiments in your Notion database, follow these steps:

### Step 1: Check the Action Logs

1. Go to your repository's **Actions** tab
2. Click on the most recent "Sync to Notion" workflow run
3. Click on the "sync" job
4. Look for the output section

**What to look for:**
- Lines like `+ Created: [Experiment Name]` indicate successful creation
- Lines like `✗ Error creating [Experiment Name]: [error]` indicate failures
- Check the final summary: `Created: X pages` and `Errors: Y`

### Step 2: Common Issues & Solutions

#### Issue 1: "All operations failed" or "Created: 0 pages"

**Cause:** Database not shared with integration

**Solution:**
1. Open your Notion database: https://www.notion.so/tingogtang/bffb39a4584c462ca4d4bb9e1c892ccb
2. Click the **"..."** menu in the top-right corner
3. Click **"Add connections"**
4. Find and select your **"tiangong"** integration
5. The integration should now appear in the connections list

**Verify:** Re-run the GitHub Action and check if pages are created.

---

#### Issue 2: "Property validation failed" or "property type does not match"

**Cause:** The "Station" property is the wrong type

**Solution:**
1. Open your Notion database
2. Click on the **"Station"** property header
3. Check if it says **"Select"** (correct) or **"Text"** (wrong)
4. If it's "Text":
   - Click the property → **"Edit property"**
   - Change type to **"Select"**
   - Add two options: **"Tiangong"** and **"ISS"**
5. Save changes

**Verify:** Re-run the GitHub Action.

---

#### Issue 3: "401 Unauthorized" or "Integration not found"

**Cause:** Invalid or expired integration token

**Solution:**
1. Go to https://www.notion.so/my-integrations
2. Find your "tiangong" integration
3. If it says "Revoked" or you can't find it:
   - Create a new integration
   - Copy the new token
   - Update GitHub secret `NOTION_TOKEN` with the new value
4. If the integration exists:
   - Make sure the token in GitHub secrets matches
   - Go to Settings → Secrets and variables → Actions
   - Update `NOTION_TOKEN` if needed

**Verify:** Re-run the GitHub Action.

---

#### Issue 4: "Database not found" or "404 error"

**Cause:** Wrong database ID in GitHub secrets

**Solution:**
1. Open your Notion database in a browser
2. Check the URL: `https://www.notion.so/workspace/DATABASE_ID?v=...`
3. Copy the DATABASE_ID (32 character string)
4. Compare with GitHub secret:
   - Go to Settings → Secrets and variables → Actions
   - Check `NOTION_DATABASE_ID`
   - Update if it doesn't match
5. For your database: the ID should be `bffb39a4584c462ca4d4bb9e1c892ccb`

**Verify:** Re-run the GitHub Action.

---

#### Issue 5: Action shows success but errors were hidden

**Cause:** Previous version of sync script didn't fail on errors

**Solution:**
This has been fixed in the latest version. The script now:
- Shows error count in summary
- Exits with error code if all operations fail
- Displays first few error messages

**Action:** Re-run the workflow to see detailed error messages.

---

### Step 3: Manual Verification

Test the sync locally to see detailed error messages:

```bash
# Clone the repository
git clone https://github.com/lukketsvane/tiangong.git
cd tiangong

# Install dependencies
pip install -r requirements.txt

# Create .env file with your credentials
cat > .env << EOF
NOTION_TOKEN=ntn_N762533464840bhrKQ0gDmSVkczVpOyKrfkk5m8VRH2b1S
NOTION_DATABASE_ID=bffb39a4584c462ca4d4bb9e1c892ccb
EOF

# Validate configuration
python validate_notion.py

# Try the sync
python sync_to_notion.py
```

This will show you exactly what's going wrong.

---

### Step 4: Checklist Before Re-running

- [ ] Notion database exists and is accessible
- [ ] Database is shared with the "tiangong" integration
- [ ] "Station" property is type "Select" with "Tiangong" and "ISS" options
- [ ] All 9 required properties exist (Name, Station, Discipline, Country/Institution, Timeline Status, Objectives, Expected Outcomes, Principal Investigator, Mission Module)
- [ ] GitHub secret `NOTION_TOKEN` is correct and not expired
- [ ] GitHub secret `NOTION_DATABASE_ID` matches your database ID
- [ ] Integration token starts with `secret_` or `ntn_`

---

### Step 5: Understanding Action Output

**Successful sync looks like:**
```
Starting sync to Notion...
Found 67 experiments in CSV
Fetching existing pages from Notion...
Found 0 existing pages in Notion
+ Created: Full Life-Cycle Rice Cultivation
+ Created: Hematopoietic Stem Cell Differentiation
+ Created: Niallia tiangongensis Discovery
...
============================================================
Sync complete!
Created: 67 pages
Updated: 0 pages
Errors: 0
============================================================
```

**Failed sync looks like:**
```
Starting sync to Notion...
Found 67 experiments in CSV
Fetching existing pages from Notion...
Found 0 existing pages in Notion
✗ Error creating Full Life-Cycle Rice Cultivation: Integration not found
✗ Error creating Hematopoietic Stem Cell Differentiation: Integration not found
...
============================================================
Sync complete!
Created: 0 pages
Updated: 0 pages
Errors: 67
============================================================

⚠️  WARNING: No pages were created or updated!

Common issues:
1. Database not shared with integration
   → Open database in Notion → Click '...' → 'Add connections' → Select integration
...
```

---

### Still Having Issues?

1. **Check Action Logs:** Look for specific error messages
2. **Run Locally:** Use `python sync_to_notion.py` to see detailed output
3. **Validate Setup:** Run `python validate_notion.py` to check configuration
4. **Review Checklist:** Ensure all requirements in Step 4 are met

### Quick Diagnostic

Run this command locally to diagnose:

```bash
python validate_notion.py
```

This will check:
- ✅ Configuration is present
- ✅ Can connect to Notion API
- ✅ Database has correct properties
- ✅ Integration has access

---

## Other Common Issues

### Pages Created But Fields Are Empty

**Cause:** Property names don't match exactly

**Solution:**
1. Check property names in Notion database
2. They must match exactly (case-sensitive):
   - Name, Station, Discipline, Country/Institution, Timeline Status
   - Objectives, Expected Outcomes, Principal Investigator, Mission Module
3. No extra spaces or different spelling

---

### Sync Creates Duplicates

**Cause:** Experiment names in CSV changed

**Solution:**
- The sync matches by experiment name
- If names change, new pages are created
- To avoid: Keep experiment names consistent
- To fix: Delete duplicates in Notion manually

---

### "Rate limit exceeded" Error

**Cause:** Too many API requests in short time

**Solution:**
- Notion API allows ~3 requests/second
- This shouldn't happen with 67 experiments
- If it does, wait a few minutes and re-run

---

## Need More Help?

- Review: [SETUP.md](SETUP.md)
- Check: [HOW_IT_WORKS.md](HOW_IT_WORKS.md)
- Validate: Run `python validate_notion.py`
