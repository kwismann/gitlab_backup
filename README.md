# Gitlab backup retention

## How It Works
- **Extracts the date from backup filenames.**
- **Categorizes backups**:
  1. Keeps daily backups for the last 2 weeks.
  2. Keeps one backup per week for the next 6 months.
  3. Keeps one backup per month until 1 year old.
  4. Keeps one backup per year for older backups.
- **Deletes unnecessary backups**, keeping only the required ones.

**Note**: Modify `backup_directory` to point to your actual backup location before running the script.

