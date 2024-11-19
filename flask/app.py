from flask import Flask, render_template, request, redirect
import os
import random
import csv
from datetime import datetime

app = Flask(__name__)

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
    super_res_images = []
    for model_name, model_path in MODELS.items():
        super_res_images.append({
            'model': model_name,
            'path': f"{model_path}/{img_name}"
        })
    random.shuffle(super_res_images)  # Randomize order of super-res images
    image_sets.append({
        'low_res': f"{LOW_RES_DIR}/{img_name}",
        'super_res_images': super_res_images
    })

# Route to display images
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_model = request.form['selected_model']
        img_name = request.form['img_name']

        # Save the result
        with open('results.csv', 'a', newline='') as csvfile:
            fieldnames = ['timestamp', 'image_name', 'selected_model']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if os.stat('results.csv').st_size == 0:
                writer.writeheader()
            writer.writerow({
                'timestamp': datetime.now().isoformat(),
                'image_name': img_name,
                'selected_model': selected_model
            })

        # Move to the next image set or finish
        if 'index' not in request.form:
            index = 1
        else:
            index = int(request.form['index']) + 1

        if index >= len(image_sets):
            return render_template('thank_you.html')
        else:
            return redirect(f'/?index={index}')

    index = int(request.args.get('index', 0))
    if index >= len(image_sets):
        return render_template('thank_you.html')
    current_set = image_sets[index]
    return render_template('index.html', image_set=current_set, index=index)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
