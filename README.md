# Tiangong Research Database

A comprehensive database of space research experiments conducted on the Tiangong Space Station and the International Space Station (ISS). This repository includes automated synchronization with Notion databases.

## 📊 Database Contents

The `planned_research_main.csv` file contains detailed information about space experiments including:

- **Station**: Tiangong or ISS
- **Experiment Name**: Official name of the experiment
- **Discipline**: Scientific field (e.g., Space Agriculture, Materials Science, Astrophysics)
- **Country/Institution**: Conducting organization
- **Timeline Status**: Current status (Completed, Ongoing, Planned)
- **Objectives**: Research goals
- **Expected Outcomes**: Anticipated results and applications
- **Principal Investigator**: Lead researcher
- **Mission Module**: Location on the space station

## 🔄 Notion Synchronization

This repository includes a Python script to automatically sync the CSV database to Notion, allowing you to manage and visualize the data in Notion's collaborative workspace.

### Prerequisites

- Python 3.7 or higher
- A Notion account
- A Notion integration with access to your database

### Setup Instructions

#### 1. Create a Notion Integration

1. Go to [Notion Integrations](https://www.notion.so/my-integrations)
2. Click "+ New integration"
3. Give it a name (e.g., "Tiangong Database Sync")
4. Select the workspace where your database is located
5. Click "Submit"
6. Copy the "Internal Integration Token" (starts with `secret_`)

#### 2. Create a Notion Database

1. In Notion, create a new database (table view recommended)
2. Add the following properties:
   - **Name** (Title) - Experiment Name
   - **Station** (Select) - **Important**: Add two options: "Tiangong" and "ISS"
   - **Discipline** (Text)
   - **Country/Institution** (Text)
   - **Timeline Status** (Text)
   - **Objectives** (Text)
   - **Expected Outcomes** (Text)
   - **Principal Investigator** (Text)
   - **Mission Module** (Text)

3. Share the database with your integration:
   - Click the "..." menu in the top-right of your database
   - Click "Add connections"
   - Select your integration

4. Copy the database ID from the URL:
   - The URL format is: `https://www.notion.so/your-database-id?v=...`
   - Copy the part between the last `/` and the `?`

#### 3. Configure the Sync Script

1. Clone this repository:
   ```bash
   git clone https://github.com/lukketsvane/tiangong.git
   cd tiangong
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```

4. Edit the `.env` file and add your credentials:
   ```
   NOTION_TOKEN=secret_your_integration_token_here
   NOTION_DATABASE_ID=your_database_id_here
   ```

#### 4. Run the Sync

Execute the sync script:
```bash
python sync_to_notion.py
```

The script will:
- Read all experiments from `planned_research_main.csv`
- Check for existing pages in your Notion database
- Create new pages for experiments that don't exist
- Update existing pages with current data

### Sync Output

The script provides detailed feedback:
- `+ Created: [Experiment Name]` - New page created
- `✓ Updated: [Experiment Name]` - Existing page updated
- `✗ Error: [Details]` - Any errors encountered

Example output:
```
Starting sync to Notion...
CSV file: planned_research_main.csv
Database ID: abc123...
Found 68 experiments in CSV
Fetching existing pages from Notion...
Found 0 existing pages in Notion
+ Created: Full Life-Cycle Rice Cultivation
+ Created: Hematopoietic Stem Cell Differentiation
...
============================================================
Sync complete!
Created: 68 pages
Updated: 0 pages
============================================================
```

## 🔒 Security Notes

- **Never commit your `.env` file** - It contains sensitive credentials
- The `.env` file is excluded in `.gitignore`
- Use `.env.example` as a template for others
- Keep your Notion integration token secure

## 📝 Data Management

### Updating the Database

1. Edit the `planned_research_main.csv` file
2. Run `python sync_to_notion.py` to sync changes to Notion
3. The script will update existing pages and create new ones

### CSV Format

The CSV must maintain the following column headers:
- Station
- Experiment_Name
- Discipline
- Country_Institution
- Timeline_Status
- Objectives
- Expected_Outcomes
- Principal_Investigator
- Mission_Module

## 🤖 Automated Sync with GitHub Actions

The repository includes a GitHub Actions workflow that automatically syncs the database to Notion:

- **Triggers**:
  - When `planned_research_main.csv` is updated (push to main branch)
  - Daily at 2 AM UTC (scheduled)
  - Manually via GitHub Actions UI

### Setting up GitHub Actions

1. Go to your repository **Settings** → **Secrets and variables** → **Actions**
2. Add the following repository secrets:
   - `NOTION_TOKEN`: Your Notion integration token
   - `NOTION_DATABASE_ID`: Your Notion database ID

3. The workflow will automatically run when you push changes to the CSV file

You can also manually trigger the sync:
- Go to **Actions** tab in your repository
- Click on "Sync to Notion" workflow
- Click "Run workflow"

## 🚀 Features

- **Automated Sync**: One command to sync all data (or automatic via GitHub Actions)
- **Smart Updates**: Only creates or updates pages as needed
- **Error Handling**: Detailed error messages for troubleshooting
- **Batch Processing**: Efficiently handles large datasets
- **Idempotent**: Safe to run multiple times
- **CI/CD Integration**: GitHub Actions workflow for automatic syncing

## 📚 Research Highlights

This database includes groundbreaking experiments such as:

**Tiangong Station:**
- Full life-cycle rice cultivation in orbit
- Blood cell precursor generation in space
- Discovery of radiation-resistant bacteria
- 43-day zebrafish aquatic habitat (longest vertebrate habitat in space)

**ISS:**
- 3D bioprinting of human organs (heart tissue, meniscus, liver patches)
- Remote robotic surgery demonstration
- ZBLAN optical fiber production (superior to Earth-based manufacturing)
- Advanced plant growth systems

## 🤝 Contributing

Contributions are welcome! Please feel free to:
- Add new experiments to the CSV
- Report inaccuracies
- Suggest improvements to the sync script
- Enhance documentation

## 📄 License

This data is compiled from publicly available sources about space research programs.

## 🔗 Resources

- [Notion API Documentation](https://developers.notion.com/)
- [Tiangong Space Station](https://en.wikipedia.org/wiki/Tiangong_space_station)
- [International Space Station](https://www.nasa.gov/mission_pages/station/main/index.html)

## 💡 Tips

- Run the sync script regularly to keep Notion up-to-date
- Use Notion's views and filters to analyze the data
- Create custom properties in Notion for additional metadata
- Set up Notion automations based on experiment status

---

**Note**: Make sure to set up your Notion integration and database before running the sync script. See the Setup Instructions above for detailed steps.
