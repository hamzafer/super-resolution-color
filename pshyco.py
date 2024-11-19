import streamlit as st
import os
import random
import pandas as pd
from PIL import Image

# Configure directories
LOW_RES_DIR = "dataset/selected_256"
MODELS = {
    "ResShift": "results/selected_256_ResShift",
    "BSRGAN": "results/selected_256_BSRGAN",
    "SwinIR": "results/selected_256_SwinIR",
    "Real-ESRGAN": "results/selected_256_RealESRGAN",
}

RESULTS_CSV = "experiment_results.csv"

# Load images
def load_images():
    low_res_images = sorted(os.listdir(LOW_RES_DIR))
    model_images = {model: sorted(os.listdir(path)) for model, path in MODELS.items()}
    return low_res_images, model_images

low_res_images, model_images = load_images()

# Randomly pick 5 images for the experiment
EXPERIMENT_IMAGES = random.sample(low_res_images, 5)

# Function to shuffle the model images
def shuffle_model_images(model_paths):
    image_paths = []
    for img in EXPERIMENT_IMAGES:
        image_paths.append({
            "low_res": os.path.join(LOW_RES_DIR, img),
            **{model: os.path.join(path, img) for model, path in model_paths.items()}
        })
    random.shuffle(image_paths)
    return image_paths

# Initialize results
if not os.path.exists(RESULTS_CSV):
    pd.DataFrame(columns=["LowRes", "SelectedModel", "Image"]).to_csv(RESULTS_CSV, index=False)

st.title("Super-Resolution Psychophysical Experiment")

# Display experiment
for idx, image_set in enumerate(shuffle_model_images(MODELS)):
    st.header(f"Experiment {idx + 1}")

    # Display low-resolution image in the center
    low_res_image = Image.open(image_set["low_res"])
    st.image(low_res_image, caption="Low Resolution Image", use_column_width=True)

    # Display high-resolution images
    cols = st.columns(len(MODELS))
    options = list(MODELS.keys())
    random.shuffle(options)

    for i, model in enumerate(options):
        with cols[i]:
            high_res_image = Image.open(image_set[model])
            st.image(
                high_res_image,
                caption=f"{model} (Hover to zoom)",
                use_column_width=True
            )
            if st.button(f"Select {model}", key=f"{idx}_{model}"):
                # Save the result
                result = pd.read_csv(RESULTS_CSV)
                result = result.append({
                    "LowRes": image_set["low_res"],
                    "SelectedModel": model,
                    "Image": image_set[model]
                }, ignore_index=True)
                result.to_csv(RESULTS_CSV, index=False)
                st.success(f"Selection for Experiment {idx + 1} saved!")

st.write("Results will be saved in `experiment_results.csv`.")

# Show results for debugging or analysis
if st.button("Show Results"):
    results = pd.read_csv(RESULTS_CSV)
    st.write(results)
