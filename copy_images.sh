/Users/stan/Downloads/conference-presentations/SCIA/super-resolution-color/latex/Poster/images#!/bin/bash

# Create the destination directory if it doesn't exist
mkdir -p "/Users/stan/Downloads/conference-presentations/SCIA/super-resolution-color/latex/Poster/images"

# Source directory
SOURCE_DIR="/Users/stan/Downloads/conference-presentations/SCIA/super-resolution-color/latex/Images"

# Destination directory
DEST_DIR="/Users/stan/Downloads/conference-presentations/SCIA/super-resolution-color/latex/Poster/images"

# List of files to copy
files=(
    "NTNU_logo.png"
    "exp_1_setup_selection.png"
    "exp2_setup_quick_eval.png"
    "Objective_analysis_barcharts_metrics_all.png"
    "most_picked_bar_chart.png"
    "Number of Selections per Model Pairwisw.png"
    "Borda Count Rankings of Models.png"
    "Preference Matrix Heatmap.png"
    "age_distribution.png"
    "algo_vs_age_preference_chart.png"
    "Most Picked Algorithm per Image.png"
    "word_cloud_feedback.png"
    "word_cloud_reasons.png"
)

echo "Copying images to poster directory..."

# Copy each file
for file in "${files[@]}"; do
    if [ -f "$SOURCE_DIR/$file" ]; then
        cp "$SOURCE_DIR/$file" "$DEST_DIR/"
        echo "✓ Copied: $file"
    else
        echo "✗ Not found: $file"
    fi
done

echo "Done! All images copied to: $DEST_DIR"