from flask import Flask, render_template, request, redirect, url_for, session
import os
import random
import uuid
from datetime import datetime
from flask_session import Session
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# Configure secret key for session management
app.secret_key = 'your_secret_key_here'  # Replace with a secure secret key

# Configure server-side session
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Google Sheets Configuration
SERVICE_ACCOUNT_FILE = 'service_account.json'  # Path to your service account key
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1vu-CJqYwCMzOKUum-U1aF_lGAVPIpU9AhdlmnA-7U3A'  # Replace with your Google Sheet ID

def get_sheet_service():
    """Authenticate and return the Sheets API service."""
    credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build("sheets", "v4", credentials=credentials)
    return service

def append_to_sheet(sheet_name, values):
    """Append a row of data to the specified sheet."""
    service = get_sheet_service()
    range_name = f"{sheet_name}!A1"

    # Define headers for each sheet
    headers = {
        "incomplete": ["test_id", "timestamp", "name", "age", "image_name", "selected_model", "status"],
        "complete": ["test_id", "name", "age", "completion_time", "total_time", "status"],
        "open-qs": ["test_id", "timestamp", "reason", "feedback"]
    }

    # Check if the sheet is empty (no headers)
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name
    ).execute()

    if "values" not in result or not result["values"]:  # No headers exist
        # Add headers as the first row
        header_body = {"values": [headers[sheet_name]]}
        service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name,
            valueInputOption="RAW",
            body=header_body
        ).execute()

    # Append the actual data
    body = {"values": [values]}
    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name,
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body=body
    ).execute()

# Configuration
LOW_RES_DIR = "static/images/selected_256"
MODELS = {
    "ResShift": "static/images/selected_256_ResShift",
    "BSRGAN": "static/images/selected_256_BSRGAN",
    "SwinIR": "static/images/selected_256_SwinIR",
    "Real-ESRGAN": "static/images/selected_256_RealESRGAN",
}

# Get list of image names (assuming same names across all folders)
image_names = os.listdir(LOW_RES_DIR)
random.shuffle(image_names)  # Randomize the order of image sets
image_names = image_names[:5]  # Select 5 images

# Prepare image sets
image_sets = []
for img_name in image_names:
    positions = ['topleft', 'topright', 'bottomleft', 'bottomright']
    random.shuffle(positions)
    super_res_images = []
    model_items = list(MODELS.items())
    random.shuffle(model_items)  # Randomize the model order
    for pos, (model_name, model_path) in zip(positions, model_items):
        img_path = os.path.join(model_path, img_name).replace('static/', '', 1)
        super_res_images.append({
            'model': model_name,
            'path': img_path,
            'position': pos
        })
    low_res_path = os.path.join(LOW_RES_DIR, img_name).replace('static/', '', 1)
    image_sets.append({
        'low_res': low_res_path,
        'super_res_images': super_res_images,
        'img_name': img_name
    })

# Route for the start page
@app.route('/start', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        # Collect user information
        name = request.form.get('name')
        age = request.form.get('age')

        if not name or not age:
            error = "Please provide name and age."
            return render_template('start.html', error=error)

        # Store in session
        session['name'] = name
        session['age'] = age
        session['start_time'] = datetime.now()  # Store start timestamp
        session['test_id'] = str(uuid.uuid4())  # Generate unique test ID

        # Redirect to the single-image selection test
        return redirect(url_for('test'))

    return render_template('start.html')

# Route for the single image selection test
@app.route('/test', methods=['GET', 'POST'])
def test():
    if 'name' not in session or 'age' not in session:
        return redirect(url_for('start'))

    if request.method == 'POST':
        selected_model = request.form.get('selected_model')
        img_name = request.form.get('img_name')
        name = session.get('name')
        age = session.get('age')
        test_id = session.get('test_id')

        if not selected_model:
            error = "Please select a super-resolution image."
            index = int(request.form.get('index', 0))
            current_set = image_sets[index]
            progress = int((index / len(image_sets)) * 100)
            return render_template(
                'index.html',
                image_set=current_set,
                index=index,
                total_images=len(image_sets),
                progress=progress,
                error=error
            )

        # Save the result to the "incomplete" sheet
        append_to_sheet('incomplete', [
            test_id, datetime.now().isoformat(), name, age, img_name, selected_model, "In Progress"
        ])

        # Move to the next image set or finish
        index = int(request.form.get('index', 0)) + 1

        if index >= len(image_sets):
            # Calculate total time taken
            start_time = session.get('start_time')
            total_time = (datetime.now() - start_time).total_seconds()

            # Save to the "complete" sheet
            append_to_sheet('complete', [
                test_id, name, age, datetime.now().isoformat(), total_time, "Completed"
            ])

            return redirect(url_for('thank_you'))

        current_set = image_sets[index]
        progress = int((index / len(image_sets)) * 100)
        return render_template(
            'index.html',
            image_set=current_set,
            index=index,
            total_images=len(image_sets),
            progress=progress
        )

    index = int(request.args.get('index', 0))
    if index >= len(image_sets):
        return redirect(url_for('thank_you'))
    current_set = image_sets[index]
    progress = int((index / len(image_sets)) * 100)
    return render_template(
        'index.html',
        image_set=current_set,
        index=index,
        total_images=len(image_sets),
        progress=progress
    )

@app.route('/thank_you', methods=['GET', 'POST'])
def thank_you():
    if request.method == 'POST':
        reason = request.form.get('reason')
        feedback = request.form.get('feedback')
        test_id = session.get('test_id')

        # Append feedback to the "open-qs" sheet
        append_to_sheet('open-qs', [
            test_id, datetime.now().isoformat(), reason if reason else "No reason provided",
            feedback if feedback else "No feedback provided"
        ])

        # Redirect to a final "Thank You" screen
        return redirect(url_for('start'))

    return render_template('thank_you.html')

# Redirect root to start page
@app.route('/')
def home():
    return redirect(url_for('start'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
