# How Notion Sync Works

This document explains how the Tiangong → Notion synchronization works.

## 🔄 Sync Flow Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     Tiangong GitHub Repository                   │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │   planned_research_main.csv                              │   │
│  │                                                           │   │
│  │  Station,Experiment_Name,Discipline,...                  │   │
│  │  Tiangong,Full Life-Cycle Rice Cultivation,...           │   │
│  │  Tiangong,Zebrafish Aquatic Ecosystem,...                │   │
│  │  ISS,3D Bioprinting - Human Heart Tissue,...             │   │
│  │  ...                                                      │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                    │
│                              │ (1) Read CSV                       │
│                              ▼                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │   sync_to_notion.py                                      │   │
│  │                                                           │   │
│  │  • Reads all experiments from CSV                        │   │
│  │  • Converts to Notion format                             │   │
│  │  • Checks for existing pages                             │   │
│  │  • Creates new or updates existing                       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                    │
└──────────────────────────────┼────────────────────────────────────┘
                               │ (2) Sync via Notion API
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Notion Workspace                         │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │   Tiangong Research Database                             │   │
│  │   https://notion.so/tingogtang/bffb39a...                │   │
│  │                                                           │   │
│  │  ┌───────────────────────────────────────────────────┐  │   │
│  │  │ Name                    │ Station  │ Discipline   │  │   │
│  │  ├───────────────────────────────────────────────────┤  │   │
│  │  │ Full Life-Cycle Rice... │ Tiangong │ Space Agri...│  │   │
│  │  │ Zebrafish Aquatic...    │ Tiangong │ Space Life...│  │   │
│  │  │ 3D Bioprinting - Hea... │ ISS      │ Regenerati...│  │   │
│  │  │ ...                     │ ...      │ ...          │  │   │
│  │  └───────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## 🔍 Detailed Sync Process

### Step 1: CSV Reading
```python
# sync_to_notion.py reads the CSV
csv_data = read_csv_data()
# Result: List of 67+ experiment dictionaries
```

### Step 2: Property Conversion
```python
# Each CSV row is converted to Notion format
properties = create_notion_page_properties(row)
# Example:
{
  "Name": {"title": [{"text": {"content": "Full Life-Cycle Rice Cultivation"}}]},
  "Station": {"select": {"name": "Tiangong"}},
  "Discipline": {"rich_text": [{"text": {"content": "Space Agriculture"}}]},
  ...
}
```

### Step 3: Check Existing Pages
```python
# Get all existing pages from Notion
existing_pages = get_existing_pages(notion, database_id)
# Returns: {"Experiment Name": "page_id", ...}
```

### Step 4: Create or Update
```python
for row in csv_data:
    if experiment_name in existing_pages:
        # Update existing page
        notion.pages.update(page_id, properties)
    else:
        # Create new page
        notion.pages.create(parent=database_id, properties)
```

## 📊 Data Mapping

### CSV → Notion Property Mapping

| CSV Column              | Notion Property        | Type       |
|-------------------------|------------------------|------------|
| Experiment_Name         | Name                   | Title      |
| Station                 | Station                | Select     |
| Discipline              | Discipline             | Text       |
| Country_Institution     | Country/Institution    | Text       |
| Timeline_Status         | Timeline Status        | Text       |
| Objectives              | Objectives             | Text       |
| Expected_Outcomes       | Expected Outcomes      | Text       |
| Principal_Investigator  | Principal Investigator | Text       |
| Mission_Module          | Mission Module         | Text       |

### Example Conversion

**CSV Row:**
```csv
Tiangong,Full Life-Cycle Rice Cultivation,Space Agriculture,China - CAS,Completed 2023,Cultivate rice from seed to grain entirely in orbit,Space-grown rice germplasm with higher yields,CAS,Wentian Life Ecology Cabinet
```

**Notion Page:**
- **Name**: Full Life-Cycle Rice Cultivation
- **Station**: Tiangong (select)
- **Discipline**: Space Agriculture
- **Country/Institution**: China - CAS
- **Timeline Status**: Completed 2023
- **Objectives**: Cultivate rice from seed to grain entirely in orbit
- **Expected Outcomes**: Space-grown rice germplasm with higher yields
- **Principal Investigator**: CAS
- **Mission Module**: Wentian Life Ecology Cabinet

## 🔄 Sync Behavior

### First Sync (Empty Database)
```
CSV: 67 experiments
Notion: 0 pages

Result:
✓ Created: 67 pages
✓ Updated: 0 pages
```

### Second Sync (No Changes)
```
CSV: 67 experiments (unchanged)
Notion: 67 pages

Result:
✓ Created: 0 pages
✓ Updated: 67 pages
(All pages updated with same data)
```

### Partial Update
```
CSV: 68 experiments (1 new)
Notion: 67 pages

Result:
✓ Created: 1 page
✓ Updated: 67 pages
```

## 🎯 Sync Strategies

### Strategy 1: Match by Name
- The script matches experiments by their **Name** (Experiment_Name)
- If name exists in Notion → **Update**
- If name doesn't exist → **Create**

### Strategy 2: Idempotent Updates
- Running the script multiple times is safe
- Existing pages are updated with current data
- No duplicates are created (if names match)

### Strategy 3: Smart Pagination
- Notion API returns pages in batches
- Script handles pagination automatically
- All existing pages are fetched before syncing

## 🔐 Authentication Flow

```
1. Load .env file
   ├─ NOTION_TOKEN
   └─ NOTION_DATABASE_ID

2. Initialize Notion Client
   └─ Client(auth=NOTION_TOKEN)

3. For each API call:
   ├─ Authorization: Bearer {NOTION_TOKEN}
   └─ Request to: https://api.notion.com/v1/...

4. Responses include:
   ├─ Success: 200 OK
   ├─ Unauthorized: 401 (bad token)
   ├─ Not Found: 404 (bad database ID)
   └─ Validation Error: 400 (bad properties)
```

## 🚀 Automation Flow (GitHub Actions)

```
Trigger Event:
├─ Push to main (CSV changed)
├─ Daily at 2 AM UTC
└─ Manual trigger

     ↓

GitHub Actions Workflow:
├─ 1. Checkout repository
├─ 2. Setup Python 3.12
├─ 3. Install dependencies
├─ 4. Run tests (test_sync.py)
└─ 5. Run sync (sync_to_notion.py)

     ↓

Sync Result:
├─ Success → ✅ Green checkmark
└─ Failure → ❌ Red X (view logs)

     ↓

Notion Database:
└─ Updated with latest data
```

## 🛠️ Error Handling

The script handles various error scenarios:

### Network Errors
```python
try:
    notion.pages.create(...)
except Exception as e:
    print(f"✗ Error creating {experiment_name}: {e}")
    # Continues with next experiment
```

### Invalid Properties
```
Error: Property 'Station' expected type 'select', got 'text'
Solution: Fix property type in Notion database
```

### Missing Integration Access
```
Error: Integration not found or does not have access
Solution: Share database with integration
```

### Rate Limiting
- Notion API: ~3 requests/second
- Script has no built-in rate limiting
- For large datasets, Notion handles this automatically

## 📈 Performance

### Sync Time Estimates

| Experiments | First Sync | Update Sync |
|-------------|------------|-------------|
| 10          | ~5 sec     | ~5 sec      |
| 50          | ~20 sec    | ~20 sec     |
| 67          | ~30 sec    | ~30 sec     |
| 100         | ~45 sec    | ~45 sec     |

Factors affecting speed:
- Network latency
- Notion API response time
- Number of properties per page
- Size of text content

## 🔄 Update Detection

Currently, the script uses a **full update** strategy:

```
For each CSV row:
  If page exists in Notion:
    ✓ Update all properties (even if unchanged)
  Else:
    ✓ Create new page
```

**Future Enhancement**: Could implement change detection to skip unchanged pages.

## 🎓 Technical Details

### API Endpoints Used

1. **Query Database**
   ```
   POST https://api.notion.com/v1/databases/{database_id}/query
   ```
   - Gets all existing pages
   - Used for: Checking what exists

2. **Create Page**
   ```
   POST https://api.notion.com/v1/pages
   ```
   - Creates new database entry
   - Used for: New experiments

3. **Update Page**
   ```
   PATCH https://api.notion.com/v1/pages/{page_id}
   ```
   - Updates existing page properties
   - Used for: Updating experiments

### Property Types

Notion supports various property types:
- **title**: Rich text array (for Name)
- **select**: Single selection (for Station)
- **rich_text**: Rich text array (for all other fields)

Each type has a specific JSON structure that the script handles.

## 📊 Monitoring & Logs

### Local Sync Output
```
Starting sync to Notion...
CSV file: planned_research_main.csv
Database ID: bffb39a4...
Found 67 experiments in CSV
Fetching existing pages from Notion...
Found 0 existing pages in Notion
+ Created: Full Life-Cycle Rice Cultivation
+ Created: Hematopoietic Stem Cell Differentiation
...
============================================================
Sync complete!
Created: 67 pages
Updated: 0 pages
============================================================
```

### GitHub Actions Logs
- Full output visible in Actions tab
- Logs retained for 90 days
- Can be downloaded for analysis

---

**Understanding the sync?** Now you're ready to run it! See [SETUP.md](SETUP.md) for next steps.
