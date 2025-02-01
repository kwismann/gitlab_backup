# Gitlab server upload
This an an API for a gitlab server to upload backups to a remote server. All received backup files are after upload marked as Immutable
The environment variable 'TOKEN' must be set and must be in the HTTP headers as a baerer token.

# Git client upload files
This uploads all missing files from a gitlab server to a remote server.
It checks what files are missing on the remote server and uploads them.
The environment variable 'TOKEN' must be set and must be in the HTTP headers as a baerer token.

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

