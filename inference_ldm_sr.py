import os
import time
from diffusers import LDMSuperResolutionPipeline
import torch
from PIL import Image

# Define input datasets and corresponding output directories
datasets = {
    "imagenet256": "/home/hamzaz/hamza/super-resolution-color/dataset/imagenet256/lq",
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

    print(f"\nProcessing dataset: {dataset_name}")
    
    # Get total number of images in the dataset
    all_images = [f for f in os.listdir(input_dir) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    total_images = len(all_images)
    processed_count = 0
    skipped_count = 0
    remaining_images = total_images  # Remaining images to be processed

    # Process each image in the dataset
    dataset_start_time = time.time()
    for idx, filename in enumerate(all_images, start=1):
        img_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)

        # Check if the image has already been processed
        if os.path.exists(output_path):
            skipped_count += 1
            remaining_images -= 1
            print(f"Skipping {filename} as it already exists in the output directory. [{skipped_count}/{total_images} skipped]")
            continue

        # Attempt processing of the image
        try:
            # Free up CUDA memory before processing each image
            torch.cuda.empty_cache()

            processed_count += 1
            low_res_img = Image.open(img_path).convert("RGB")  # Open and convert image to RGB

            # Start timing for this image
            img_start_time = time.time()

            # Perform super-resolution
            print(f"Processing {filename} (Index {idx}/{total_images})")
            upscaled_image = pipeline(low_res_img, num_inference_steps=100, eta=1).images[0]

            # Save the upscaled image with the same filename
            upscaled_image.save(output_path)

            # Log the processing time for this image and show progress
            img_time_taken = time.time() - img_start_time
            print(f"Processed {filename} [{processed_count}/{total_images} processed] in {img_time_taken:.2f} seconds. Saved to {output_path}.")

            # Update remaining images count
            remaining_images = total_images - (processed_count + skipped_count)

        except torch.cuda.OutOfMemoryError as e:
            print(f"Out of Memory Error while processing {filename} (Index {idx}/{total_images}).")
            print("Error details:", e)
            print("Skipping this image and continuing with the next.")
            torch.cuda.empty_cache()  # Clear CUDA cache to try freeing memory for next image

        except Exception as e:
            print(f"Unexpected error while processing {filename} (Index {idx}/{total_images}).")
            print("Error details:", e)
            print("Skipping this image and continuing with the next.")
            torch.cuda.empty_cache()  # Clear CUDA cache in case of other errors

    # Log the processing time and counts for the current dataset
    dataset_time_taken = time.time() - dataset_start_time
    print(f"\nSummary for {dataset_name}:")
    print(f"Total images: {total_images}")
    print(f"Skipped images: {skipped_count}")
    print(f"Processed images: {processed_count}")
    print(f"Remaining images: {remaining_images}")
    print(f"Total processing time for {dataset_name}: {dataset_time_taken:.2f} seconds.")

# Log the total processing time for all datasets
total_time_taken = time.time() - total_start_time
print(f"\nTotal processing time for all datasets: {total_time_taken:.2f} seconds.")
