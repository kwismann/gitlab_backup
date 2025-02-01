import os
import subprocess
import random
from glob import glob
from flask import Flask, flash, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename

# UPLOAD_FOLDER = '/home/kw/repo/gitlab-backup'
UPLOAD_FOLDER = '/misc/backup/gitlab'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'tar'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_token(token):
    # Replace with your validation logic (e.g., JWT decoding)
    if token == os.environ['TOKEN']:
        return True
    return False

@app.route('/list', methods=['GET'])
def list_files():
    if request.method == 'GET':
        # check if the post request has the file part
        auth_header = request.headers.get('Authorization')
        if not auth_header:
                return jsonify({"error": "Authorization header is missing"}), 401
        # Check if it starts with "Bearer "
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Invalid Authorization header format"}), 401

        # Extract the token
        token = auth_header.split(" ")[1]

        # Validate the token
        if not validate_token(token):
            return jsonify({"error": "Invalid or expired token"}), 403

        list_of_files =  glob(os.path.join(app.config['UPLOAD_FOLDER'], '*'))
        return {"files": list_of_files}, 200

    return {"status": "listerror"}, 400
    

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        auth_header = request.headers.get('Authorization')
        if not auth_header:
                return jsonify({"error": "Authorization header is missing"}), 401
        # Check if it starts with "Bearer "
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Invalid Authorization header format"}), 401
        
        # Extract the token
        token = auth_header.split(" ")[1]
        
        # Validate the token
        if not validate_token(token):
            return jsonify({"error": "Invalid or expired token"}), 403

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # full_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)+str(random.randrange(1, 999999))
            full_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(full_filename)
            try:
                file.save(full_filename)
            except (PermissionError, OSError):
                return {"status": "save not allowed"}, 400
            ret = subprocess.run(["sudo", "chattr", "+i", full_filename])
            print("ret = ", ret)
            if ret.returncode != 0:
                return {"status":"cannot change attribute"}, 400

            return {"status":"all is good"}, 200

    return {"status": "error"}, 400

if __name__== '__main__':
    cert_file = '/usr/local/pki/fullchain.pem'
    key_file = '/usr/local/pki/privkey.pem'

    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='0.0.0.0', debug=True, port=18629, ssl_context=(cert_file, key_file))
