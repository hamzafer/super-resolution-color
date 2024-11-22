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
app.secret_key = 'your_secret_key_here'

# Configure server-side session
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Google Sheets Configuration
SERVICE_ACCOUNT_FILE = 'service_account.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1vu-CJqYwCMzOKUum-U1aF_lGAVPIpU9AhdlmnA-7U3A'

def get_sheet_service():
    """Authenticate and return the Sheets API service."""
    credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build("sheets", "v4", credentials=credentials)
    return service

def append_to_sheet(sheet_name, values):
    """Batch append rows of data to the specified sheet."""
    service = get_sheet_service()
    range_name = f"{sheet_name}!A1"

    # Define headers for each sheet
    headers = {
        "sessions": ["test_id", "name", "age", "start_time"],
        "completed": ["test_id", "timestamp", "name", "age", "image_name", "selected_model", "status"],
        "open-qs": ["test_id", "timestamp", "reason", "feedback"]
    }

    try:
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
        body = {"values": values}  # Batch write all rows at once
        service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name,
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body=body
        ).execute()

    except Exception as e:
        print(f"Error appending to Google Sheet: {e}")

# Configuration
LOW_RES_DIR = "static/images/selected_256"
MODELS = {
    "ResShift": "static/images/selected_256_ResShift",
    "BSRGAN": "static/images/selected_256_BSRGAN",
    "SwinIR": "static/images/selected_256_SwinIR",
    "Real-ESRGAN": "static/images/selected_256_RealESRGAN",
}

# Prepare the dataset
image_names = os.listdir(LOW_RES_DIR)
random.shuffle(image_names)
image_sets = [
    {
        "low_res": os.path.join(LOW_RES_DIR, img_name).replace('static/', '', 1),
        "super_res_images": [
            {
                "model": model,
                "path": os.path.join(MODELS[model], img_name).replace('static/', '', 1),
            }
            for model in random.sample(MODELS.keys(), len(MODELS))
        ],
        "img_name": img_name,
    }
    for img_name in image_names[:5]
]

# Helper: Save session info to the "sessions" sheet
def save_session_to_sheet(test_id, name, age, start_time):
    append_to_sheet("sessions", [[test_id, name, age, start_time.isoformat()]])

# Helper: Save completed results to the "completed" sheet
def save_results_to_sheet(test_id, name, age, results, completion_time, total_time):
    # Prepare all rows for batch write
    rows = [
        [
            test_id,
            result["timestamp"],
            name,
            age,
            result["image_name"],
            result["selected_model"],
            "Completed",
        ]
        for result in results
    ]
    # Add summary row
    rows.append([
        test_id,
        name,
        age,
        completion_time.isoformat(),
        total_time,
        "Completed",
    ])
    append_to_sheet("completed", rows)

@app.route('/start', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')

        if not name or not age:
            error = "Please provide name and age."
            return render_template('start.html', error=error)

        session['name'] = name
        session['age'] = age
        session['start_time'] = datetime.now()
        session['test_id'] = str(uuid.uuid4())
        session['results'] = []

        save_session_to_sheet(session['test_id'], name, age, session['start_time'])

        return redirect(url_for('test'))

    return render_template('start.html')

@app.route('/test', methods=['GET', 'POST'])
def test():
    if 'name' not in session or 'age' not in session:
        return redirect(url_for('start'))

    if request.method == 'POST':
        selected_model = request.form.get('selected_model')
        img_name = request.form.get('img_name')
        index = int(request.form.get('index', 0))

        if not selected_model:
            error = "Please select a super-resolution image."
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

        session['results'].append({
            "timestamp": datetime.now().isoformat(),
            "image_name": img_name,
            "selected_model": selected_model,
        })

        index += 1
        if index >= len(image_sets):
            return redirect(url_for('saving'))

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
    current_set = image_sets[index]
    progress = int((index / len(image_sets)) * 100)
    return render_template(
        'index.html',
        image_set=current_set,
        index=index,
        total_images=len(image_sets),
        progress=progress
    )

@app.route('/saving', methods=['GET'])
def saving():
    test_id = session['test_id']
    name = session['name']
    age = session['age']
    results = session['results']
    completion_time = datetime.now()
    total_time = (completion_time - session['start_time']).total_seconds()

    save_results_to_sheet(test_id, name, age, results, completion_time, total_time)

    return redirect(url_for('thank_you'))

@app.route('/thank_you', methods=['GET', 'POST'])
def thank_you():
    if request.method == 'POST':
        reason = request.form.get('reason')
        feedback = request.form.get('feedback')
        test_id = session['test_id']

        append_to_sheet('open-qs', [
            [test_id, datetime.now().isoformat(), reason if reason else "No reason provided",
            feedback if feedback else "No feedback provided"]
        ])

        return redirect(url_for('start'))

    return render_template('thank_you.html')

@app.route('/')
def home():
    return redirect(url_for('start'))

if __name__ == '__main__':
    app.run(debug=True)
