# Gitlab backup retention

# How It Works:
Extracts the date from backup filenames.
Categorizes backups:
Keeps daily backups for the last 2 weeks.
Keeps one backup per week for the next 6 months.
Keeps one backup per month until 1 year old.
Keeps one backup per year for older backups.
Deletes unnecessary backups, keeping only the required ones.
Modify backup_directory to point to your actual backup location before running the script. Let me know if you need any refinements! 
