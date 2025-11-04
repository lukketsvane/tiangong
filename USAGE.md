# Usage Examples

This file contains usage examples for the Notion sync functionality.

## Basic Usage

### 1. First Time Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env and add your credentials
# NOTION_TOKEN=secret_...
# NOTION_DATABASE_ID=...

# Run the sync
python sync_to_notion.py
```

### 2. Expected Output

```
Starting sync to Notion...
CSV file: planned_research_main.csv
Database ID: abc123def456...
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
============================================================
```

### 3. Updating Data

After modifying the CSV file:

```bash
# Run sync again
python sync_to_notion.py
```

Output when updating:
```
Starting sync to Notion...
CSV file: planned_research_main.csv
Database ID: abc123def456...
Found 67 experiments in CSV
Fetching existing pages from Notion...
Found 67 existing pages in Notion
✓ Updated: Full Life-Cycle Rice Cultivation
✓ Updated: Hematopoietic Stem Cell Differentiation
...
============================================================
Sync complete!
Created: 0 pages
Updated: 67 pages
============================================================
```

## Testing Before Sync

```bash
# Run tests to verify everything is configured correctly
python test_sync.py
```

Expected output:
```
============================================================
Tiangong Database - Notion Sync Test Suite
============================================================
Testing CSV parsing...
✓ Successfully read 67 rows from CSV
✓ First experiment: Full Life-Cycle Rice Cultivation
✓ Last experiment: De-Orbit Vehicle Development

Testing Notion property creation...
✓ Created properties for: Full Life-Cycle Rice Cultivation
  - Station: Tiangong
  - Discipline: Space Agriculture
  - Timeline Status: Completed 2023
✓ Property structure is correct

Testing CSV completeness...
✓ All required columns present: 9

============================================================
Test Results:
============================================================
✓ PASS: CSV Parsing
✓ PASS: Property Creation
✓ PASS: CSV Completeness

✓ All tests passed! Ready to sync to Notion.
```

## GitHub Actions Usage

### Setting up Secrets

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add `NOTION_TOKEN` with your integration token
5. Add `NOTION_DATABASE_ID` with your database ID

### Manual Trigger

1. Go to the **Actions** tab in your repository
2. Click on "Sync to Notion" workflow
3. Click **Run workflow** button
4. Select the branch and click **Run workflow**

### Automatic Triggers

The workflow runs automatically:
- When you push changes to `planned_research_main.csv` on the main branch
- Every day at 2 AM UTC
- When manually triggered (see above)

## Troubleshooting

### Error: NOTION_TOKEN not found

Make sure you have created a `.env` file with your credentials:

```bash
cp .env.example .env
# Edit .env and add your token
```

### Error: Notion API error (400)

This usually means the database properties don't match. Verify:
1. Database has all required properties
2. "Station" select property has "Tiangong" and "ISS" options
3. Your integration has access to the database

### Error: Page creation failed

Check that:
1. Your integration is connected to the database
2. The database ID is correct
3. All required properties exist in the database

## Advanced Usage

### Running with Custom CSV File

Modify `sync_to_notion.py` and change the `CSV_FILE` variable:

```python
CSV_FILE = "path/to/your/custom.csv"
```

### Filtering Data

To sync only specific experiments, modify the sync function:

```python
for row in csv_data:
    # Only sync Tiangong experiments
    if row.get("Station") == "Tiangong":
        # ... sync logic
```

## Performance Notes

- The script processes all rows in a single run
- On first run with 67 experiments, expect ~30-60 seconds
- Subsequent updates are faster as it only modifies changed data
- Rate limits: Notion API allows ~3 requests/second
