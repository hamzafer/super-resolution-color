# Aligning Subjective and Objective Assessments in Super-Resolution Models
<img width="428" alt="image" src="https://github.com/user-attachments/assets/a1c4e9dc-d7a3-4552-851f-b1be5ee0c6dd" />

A comprehensive study evaluating super-resolution models through both objective metrics and human perception. We compare ResShift, BSRGAN, Real-ESRGAN, and SwinIR using psychophysical experiments with 54+ participants, revealing significant gaps between traditional metrics and human visual preferences.

🌐 **[View Project Website](https://hamzafer.github.io/super-resolution-color/)**

## 📋 Abstract

This research investigates the alignment between subjective human perception and objective computational metrics in super-resolution models. Through systematic evaluation of state-of-the-art SR models and controlled psychophysical experiments, we bridge the gap between computational metrics and human visual quality assessment. Our findings reveal significant discrepancies between traditional metrics like PSNR/SSIM and human preference, with ResShift demonstrating superior performance across both objective metrics and subjective evaluations.

## 🎯 Key Findings

- **ResShift's Superiority**: Consistently outperformed other models in both objective metrics (PSNR: 25.01, LPIPS: 0.231) and subjective evaluations (624/1620 selections)
- **Metric Misalignment**: Traditional metrics like PSNR and SSIM show weak correlation with human preference  
- **Statistical Validation**: Chi-Square test (χ² = 61.40, p < 0.001) confirms significant preference differences
- **Perceptual Factors**: Users prioritize visual naturalness over pixel-perfect accuracy

## 🔬 Methodology

### Experiment 1: Quick Evaluation Interface
- **Participants**: 54 observers
- **Images**: 30 total images
- **Setup**: Choose best HR image from 4 randomized options (1020×676px) around LR center image (255×169px)
- **Duration**: ~15 minutes per participant

### Experiment 2: Pairwise Comparison
- **Participants**: 15 observers  
- **Comparisons**: 900 pairwise comparisons (10 images, 60 pairs per person)
- **Setup**: BenQ calibrated monitor, sRGB, D65, 80 cd/m²
- **Duration**: ~15 minutes per participant

### Models Evaluated
- **ResShift**: Diffusion-based super-resolution
- **BSRGAN**: Blind super-resolution GAN
- **Real-ESRGAN**: Enhanced SRGAN for real-world images  
- **SwinIR**: Transformer-based super-resolution

## 📊 Results Summary

| Model | PSNR↑ | SSIM↑ | LPIPS↓ | CLIPIQA↑ | Exp1 Selections | Exp2 Selections |
|-------|--------|--------|---------|-----------|-----------------|-----------------|
| ResShift | **25.01** | **0.677** | **0.231** | **0.592** | **624** | **309** |
| SwinIR | 23.99 | 0.667 | 0.238 | 0.564 | 377 | 220 |
| RealESRGAN | 24.04 | 0.665 | 0.254 | 0.523 | 351 | 228 |
| BSRGAN | 24.42 | 0.659 | 0.259 | 0.581 | 268 | 143 |

## 🚀 Getting Started

### View Results
Visit our interactive project website: **[hamzafer.github.io/super-resolution-color](https://hamzafer.github.io/super-resolution-color/)**

### Run Locally
```bash
# Clone the repository
git clone https://github.com/hamzafer/super-resolution-color.git
cd super-resolution-color

# Serve the website locally
python3 -m http.server 8000
# Visit http://localhost:8000
```

### Flask Application
```bash
# Navigate to flask directory
cd flask/

# Install dependencies
pip install flask

# Run the application
python app.py
```

## 📈 Statistical Analysis

- **Bradley-Terry Model**: Used for ranking model abilities
- **Chi-Square Test**: Confirmed statistical significance (p < 0.001)
- **Confidence Intervals**: 95% confidence intervals for pairwise comparisons
- **Correlation Analysis**: Between objective metrics and subjective preferences

## 📝 Citation

```bibtex
@inproceedings{zafar2025super_resolution,
  title={Aligning Subjective and Objective Assessments in Super-Resolution Models},
  author={Zafar, Muhammad Hamza and Hardeberg, Jon Y.},
  booktitle={Scandinavian Conference on Image Analysis (SCIA)},
  year={2025}
}
```

## 👥 Authors

- **[Muhammad Hamza Zafar](https://www.linkedin.com/in/ihamzafer/)** - NTNU, Norwegian University of Science and Technology
- **[Jon Y. Hardeberg](https://orcid.org/0000-0003-1150-2498)** - NTNU, Norwegian University of Science and Technology

## 🏛️ Conference

Presented at **[SCIA 2025](https://scia2025.org/)** - Scandinavian Conference on Image Analysis

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Links

- 🌐 **Project Website**: [hamzafer.github.io/super-resolution-color](https://hamzafer.github.io/super-resolution-color/)
- 📄 **Paper**: [Coming Soon]
- 💾 **Dataset**: [Coming Soon]
- 🏛️ **Conference**: [SCIA 2025](https://scia2025.org/)

---

**Keywords**: Super-Resolution, Computer Vision, Human Perception, Psychophysical Experiments, Image Quality Assessment, SCIA 2025
