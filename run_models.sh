#!/bin/bash

# Default paths
DEFAULT_INPUT_DIR="/home/hamzaz/hamza/super-resolution-color/dataset/DIV/selected/low"
DEFAULT_OUTPUT_DIR="/home/hamzaz/hamza/super-resolution-color/results/new"

# Prompt user for model name
read -p "Enter the model name (resshift, bsrgan, realesrgan, swinir): " model_name

# Prompt for custom input/output directories
read -p "Enter input directory [default: $DEFAULT_INPUT_DIR]: " input_dir
input_dir=${input_dir:-$DEFAULT_INPUT_DIR}

read -p "Enter output directory [default: $DEFAULT_OUTPUT_DIR]: " output_dir
output_dir=${output_dir:-$DEFAULT_OUTPUT_DIR}

# Commands for each model
case $model_name in
  resshift)
    command="python inference_resshift.py -i $input_dir -o $output_dir/resshift --task realsr --scale 4 --version v3"
    ;;
  bsrgan)
    command="python main_test_bsrgan.py \\
        --task real_sr \\
        --scale 4 \\
        --model_path model_zoo/BSRGAN.pth \\
        --folder_lq $input_dir \\
        --output $output_dir/bsrgan"
    ;;
  realesrgan)
    command="python inference_realesrgan.py \\
        -n RealESRGAN_x4plus \\
        -i $input_dir \\
        -o $output_dir/real-esr \\
        --outscale 4"
    ;;
  swinir)
    command="python main_test_swinir.py \\
        --task real_sr \\
        --scale 4 \\
        --model_path model_zoo/swinir/003_realSR_BSRGAN_DFO_s64w8_SwinIR-M_x4_GAN.pth \\
        --folder_lq $input_dir \\
        --folder_gt $output_dir/swinir/gt \\
        --tile 128"
    ;;
  *)
    echo "Model '$model_name' is not recognized. Available models: resshift, bsrgan, realesrgan, swinir"
    exit 1
    ;;
esac

# Run the command
echo "Running command: $command"
eval $command
