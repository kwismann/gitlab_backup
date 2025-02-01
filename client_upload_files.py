import os
import requests

# Configuration
UPLOAD_SERVER = "https://mail.klaas.dk:18629"
LOCAL_FOLDER = "/var/opt/gitlab/backups"
BEARER_TOKEN = os.environ['TOKEN']  # Replace with your actual token
HEADERS = {"Authorization": f"Bearer {BEARER_TOKEN}"}


def get_remote_files():
    """Fetches the list of files from the upload server."""
    try:
        response = requests.get(f"{UPLOAD_SERVER}/list", headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        return set(os.path.basename(f) for f in data.get("files", []))
    except requests.RequestException as e:
        print(f"Error fetching remote file list: {e}")
        return None


def upload_file(file_path):
    """Uploads a file to the server."""
    try:
        with open(file_path, "rb") as f:
            files = {"file": f}
            response = requests.post(f"{UPLOAD_SERVER}/upload", headers=HEADERS, files=files)
            response.raise_for_status()
            print(f"Uploaded: {file_path}")
    except requests.RequestException as e:
        print(f"Failed to upload {file_path}: {e}")


def main():
    """Main function to compare and upload missing files."""
    remote_files = get_remote_files()
    if remote_files is not None:
        local_files = {f for f in os.listdir(LOCAL_FOLDER) if os.path.isfile(os.path.join(LOCAL_FOLDER, f))}

        missing_files = local_files - remote_files
        if not missing_files:
            print("All files are already uploaded.")
            return

        for file in missing_files:
            file_path = os.path.join(LOCAL_FOLDER, file)
            upload_file(file_path)


if __name__ == "__main__":
    main()
