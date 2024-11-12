# Aligning Subjective and Objective Assessments in Super-Resolution Models

This repository contains the code, datasets, and documentation for the project **"Aligning Subjective and Objective Assessments in Super-Resolution Models"**. The goal is to bridge the gap between objective metrics and human perceptual quality through psychophysical experiments.

## Project Overview
This project aims to:
- Review and test state-of-the-art (SOTA) super-resolution (SR) models.
- Conduct a psychophysical experiment to evaluate subjective quality on SR outputs.
- Compare subjective user preferences with traditional objective metrics (PSNR, SSIM, LPIPS).
  
## Workflow
1. **Database Preparation**: Collect and prepare real-world and animation datasets.
2. **Model Inference**: Run SOTA SR models to generate high-resolution images.
3. **Objective Metrics Calculation**: Compute objective metrics on generated images.
4. **Subjective Assessment**: Conduct a user study to rate image quality.
5. **Analysis**: Compare subjective preferences with objective metrics to assess alignment.

## Repository Structure
```
├── data/                # Datasets for real-world and animation images
├── models/              # SOTA SR models used for inference
├── scripts/             # Scripts for data preparation, inference, and metric calculation
├── experiments/         # Psychophysical experiment setup and results
├── results/             # Generated high-res images and metric scores
├── analysis/            # Code and notebooks for comparison and analysis
└── README.md            # Project overview and instructions
```

## Installation
Clone the repository and install the required packages:
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
pip install -r requirements.txt
```

## Usage
1. **Data Preparation**: Place datasets in the `data/` directory.
2. **Run Inference**: Use `scripts/inference.py` to generate high-res images from SR models.
3. **Calculate Metrics**: Run `scripts/calculate_metrics.py` to compute objective metrics.
4. **Conduct Subjective Assessment**: Set up and run the psychophysical experiment as outlined in `experiments/`.
5. **Analyze Results**: Use `analysis/` for comparing subjective and objective results.

## Results
Results of the analysis, including comparisons of objective and subjective assessments, are stored in the `results/` and `analysis/` directories.

## Contributing
Feel free to submit pull requests for improvements, bug fixes, or new features related to SR models and psychophysical assessment techniques.

## License
This project is licensed under the MIT License.
