from psychopy import visual, event, core, gui, data
import random
import os
import csv

# Directories
LOW_RES_DIR = "/path/to/low_res_images"
MODELS = {
    "ResShift": "/path/to/selected_256_ResShift",
    "BSRGAN": "/path/to/selected_256_BSRGAN",
    "SwinIR": "/path/to/selected_256_SwinIR",
    "Real-ESRGAN": "/path/to/selected_256_RealESRGAN",
}
RESULTS_FILE = "experiment_results.csv"

# Create results file if it doesn't exist
if not os.path.exists(RESULTS_FILE):
    with open(RESULTS_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Trial", "LowRes", "SelectedModel", "TimeTaken"])

# Load images
low_res_images = sorted(os.listdir(LOW_RES_DIR))
model_images = {model: sorted(os.listdir(path)) for model, path in MODELS.items()}

# Randomly pick 5 images for the experiment
EXPERIMENT_IMAGES = random.sample(low_res_images, 5)

# Prepare randomized trials
trials = []
for i, img in enumerate(EXPERIMENT_IMAGES):
    trial = {
        "low_res": os.path.join(LOW_RES_DIR, img),
        "high_res": [
            (model, os.path.join(MODELS[model], img)) for model in MODELS
        ]
    }
    random.shuffle(trial["high_res"])  # Randomize order of high-res images
    trials.append(trial)

# PsychoPy setup
win = visual.Window(size=[1280, 720], units="pix", color=[1, 1, 1], fullscr=False)
mouse = event.Mouse(win=win)

# Experiment
for trial_num, trial in enumerate(trials, start=1):
    clock = core.Clock()
    
    # Load and display images
    low_res = visual.ImageStim(win, image=trial["low_res"], pos=(0, 200), size=(300, 300))
    positions = [(-300, -200), (-100, -200), (100, -200), (300, -200)]
    high_res_stims = [
        visual.ImageStim(win, image=img[1], pos=pos, size=(200, 200))
        for img, pos in zip(trial["high_res"], positions)
    ]
    
    # Instructions
    instructions = visual.TextStim(win, text="Hover over an image to zoom. Click the best image.",
                                    pos=(0, 350), color=[-1, -1, -1])
    instructions.draw()
    low_res.draw()
    for stim in high_res_stims:
        stim.draw()
    win.flip()

    # User interaction
    selected_model = None
    while selected_model is None:
        for stim, pos, (model, _) in zip(high_res_stims, positions, trial["high_res"]):
            if mouse.isPressedIn(stim):
                selected_model = model
                break

        # Zoom effect on hover
        for stim in high_res_stims:
            if stim.contains(mouse):
                stim.size = (300, 300)
            else:
                stim.size = (200, 200)

        # Redraw screen
        low_res.draw()
        for stim in high_res_stims:
            stim.draw()
        instructions.draw()
        win.flip()

    # Record results
    with open(RESULTS_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([trial_num, trial["low_res"], selected_model, clock.getTime()])

    # Inter-trial interval
    core.wait(1)

# End experiment
visual.TextStim(win, text="Thank you for participating!", color=[-1, -1, -1]).draw()
win.flip()
core.wait(2)
win.close()
