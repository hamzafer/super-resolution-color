╰─❯ python inference_resshift.py -i /home/hamzaz/hamza/super-resolution-color/dataset/DIV/selected/low -o /home/hamzaz/hamza/super-resolution-color/results/
new/resshift --task realsr --scale 4 --version v3  

# wanst able to adjust the input and output directories always goes to fixed but i copied mine to the fixed directory
╰─❯ python main_test_bsrgan.py \
    --task real_sr \
    --scale 4 \
    --model_path model_zoo/BSRGAN.pth \
    --folder_lq /home/hamzaz/hamza/super-resolution-color/dataset/DIV/selected/low \
    --output /home/hamzaz/hamza/super-resolution-color/results/new/selected_BSRGAN

    
╰─❯ python inference_realesrgan.py \
    -n RealESRGAN_x4plus \
    -i /home/hamzaz/hamza/super-resolution-color/dataset/DIV/selected/low \
    -o /home/hamzaz/hamza/super-resolution-color/results/new/real-esr \
    --outscale 4

python main_test_swinir.py \
    --task real_sr \
    --scale 4 \
    --model_path model_zoo/swinir/003_realSR_BSRGAN_DFO_s64w8_SwinIR-M_x4_GAN.pth \
    --folder_lq /home/hamzaz/hamza/super-resolution-color/dataset/DIV/selected/low \
    --folder_gt /home/hamzaz/hamza/super-resolution-color/dataset/DIV/selected/high \
    --tile 128
