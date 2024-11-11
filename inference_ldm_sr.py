import os
import time
from diffusers import LDMSuperResolutionPipeline
import torch
from PIL import Image

# Define input datasets and corresponding output directories
datasets = {
    "imagenet256": "/home/hamzaz/hamza/super-resolution-color/dataset/imagenet256",
    "RealSet80": "/home/hamzaz/hamza/super-resolution-color/dataset/RealSet80"
}

base_output_dir = "/home/hamzaz/hamza/super-resolution-color/results"

# Load the super-resolution pipeline
pipeline = LDMSuperResolutionPipeline.from_pretrained("CompVis/ldm-super-resolution-4x-openimages")
pipeline = pipeline.to("cuda")  # Use GPU if available

# Start total processing time logging
total_start_time = time.time()

# Process each dataset
for dataset_name, input_dir in datasets.items():
    # Create output directory specific to this dataset
    output_dir = os.path.join(base_output_dir, f"{dataset_name}_ldm")
    os.makedirs(output_dir, exist_ok=True)

    print(f"Processing dataset: {dataset_name}")

    # Process each image in the dataset
    dataset_start_time = time.time()
    for filename in os.listdir(input_dir):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):  # Check for image file extensions
            img_path = os.path.join(input_dir, filename)
            low_res_img = Image.open(img_path).convert("RGB")  # Open and convert image to RGB

            # Start timing for this image
            img_start_time = time.time()

            # Perform super-resolution
            upscaled_image = pipeline(low_res_img, num_inference_steps=100, eta=1).images[0]

            # Save the upscaled image with the same filename
            output_path = os.path.join(output_dir, filename)
            upscaled_image.save(output_path)

            # Log the processing time for this image
            img_time_taken = time.time() - img_start_time
            print(f"Processed {filename} in {img_time_taken:.2f} seconds. Saved to {output_path}.")

    # Log the processing time for the current dataset
    dataset_time_taken = time.time() - dataset_start_time
    print(f"Total processing time for {dataset_name}: {dataset_time_taken:.2f} seconds.")

# Log the total processing time for all datasets
total_time_taken = time.time() - total_start_time
print(f"Total processing time for all datasets: {total_time_taken:.2f} seconds.")
