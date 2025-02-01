import os
import re
import datetime
from collections import defaultdict

def parse_backup_date(filename):
    match = re.search(r'\d+_(\d{4})_(\d{2})_(\d{2})', filename)
    if match:
        year, month, day = map(int, match.groups())
        return datetime.date(year, month, day)
    return None

def categorize_backups(backups):
    today = datetime.date.today()
    daily, weekly, monthly, yearly = [], [], [], []
    weekly_buckets, monthly_buckets, yearly_buckets = defaultdict(list), defaultdict(list), defaultdict(list)

    backups.sort(key=lambda b: parse_backup_date(b), reverse=True)

    for backup in backups:
        backup_date = parse_backup_date(backup)
        if not backup_date:
            continue
        
        age = (today - backup_date).days
        if age <= 14:
            daily.append((backup_date, backup))
        elif age <= 180:
            week_start = backup_date - datetime.timedelta(days=backup_date.weekday())
            weekly_buckets[week_start].append((backup_date, backup))
        elif age <= 365:
            month_start = backup_date.replace(day=1)
            monthly_buckets[month_start].append((backup_date, backup))
        else:
            year_start = backup_date.replace(month=1, day=1)
            yearly_buckets[year_start].append((backup_date, backup))
    
    for bucket in weekly_buckets.values():
        weekly.append(max(bucket))
    for bucket in monthly_buckets.values():
        monthly.append(max(bucket))
    for bucket in yearly_buckets.values():
        yearly.append(max(bucket))
    
    return set(daily + weekly + monthly + yearly)

def delete_old_backups(backup_dir):
    backups = [f for f in os.listdir(backup_dir) if re.match(r'\d+_\d{4}_\d{2}_\d{2}', f)]
    
    retained_backups = categorize_backups(backups)
    retained_files = {b[1] for b in retained_backups}
    
    for backup in backups:
        backup_path = os.path.join(backup_dir, backup)
        if backup not in retained_files:
            try:
                print(f"Unlocking and deleting: {backup}")
                os.system(f"sudo chattr -i {backup_path}")
                os.remove(backup_path)
            except Exception as e:
                print(f"Error deleting file: {str(e)}")
        else:
            print(f"Keeping: {backup}")

if __name__ == "__main__":
    backup_directory = "/misc/backup/gitlab"  # Change this to your actual backup directory
    delete_old_backups(backup_directory)

