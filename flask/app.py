from flask import Flask, render_template, request, redirect, url_for, session
import os
import random
import csv
from datetime import datetime
from flask_session import Session

app = Flask(__name__)

# Configure secret key for session management
app.secret_key = 'your_secret_key_here'  # Replace with a secure secret key

# Configure server-side session (optional, for scalability)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

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
        'super_res_images': super_res_images
    })

# Route for the start page
@app.route('/start', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        # Collect user information
        name = request.form.get('name')
        age = request.form.get('age')

        if not name or not age:
            error = "Please provide both name and age."
            return render_template('start.html', error=error)

        # Store in session
        session['name'] = name
        session['age'] = age

        return redirect(url_for('test'))

    return render_template('start.html')

# Route for the test page
@app.route('/test', methods=['GET', 'POST'])
def test():
    if 'name' not in session or 'age' not in session:
        return redirect(url_for('start'))

    if request.method == 'POST':
        selected_model = request.form.get('selected_model')
        img_name = request.form.get('img_name')
        name = session.get('name')
        age = session.get('age')

        if not selected_model:
            error = "Please select a super-resolution image."
            return render_template('index.html', image_set=current_set, index=index, total_images=len(image_sets), error=error)

        # Save the result
        with open('results.csv', 'a', newline='') as csvfile:
            fieldnames = ['timestamp', 'name', 'age', 'image_name', 'selected_model']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if os.stat('results.csv').st_size == 0:
                writer.writeheader()
            writer.writerow({
                'timestamp': datetime.now().isoformat(),
                'name': name,
                'age': age,
                'image_name': img_name,
                'selected_model': selected_model
            })

        # Move to the next image set or finish
        index = int(request.form.get('index', 0)) + 1

        if index >= len(image_sets):
            return render_template('thank_you.html')
        else:
            current_set = image_sets[index]
            return render_template('index.html', image_set=current_set, index=index, total_images=len(image_sets))

    index = int(request.args.get('index', 0))
    if index >= len(image_sets):
        return render_template('thank_you.html')
    current_set = image_sets[index]
    return render_template('index.html', image_set=current_set, index=index, total_images=len(image_sets))

# Redirect root to start page
@app.route('/')
def home():
    return redirect(url_for('start'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
