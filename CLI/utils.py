import os
import numpy as np
import matplotlib.pyplot as plt


READ_PATH = "Files"
SAVE_PATH = "Processed"

CAM_WIDTH = 640
CAM_HEIGHT = 360
CAM_FPS = 30


if not os.path.exists(SAVE_PATH):
    os.makedirs(SAVE_PATH)


def blend(fg: np.ndarray, bg: np.ndarray, alpha: float) -> np.ndarray:
    fg = fg / 255
    bg = bg / 255
    image = fg * alpha + (1-alpha) * bg
    return np.clip(image*255, 0, 255).astype("uint8")


def show(image: np.ndarray) -> None:
    plt.figure()
    plt.imshow(image)
    plt.axis("off")
    figmanager = plt.get_current_fig_manager()
    figmanager.window.state("zoomed")
    plt.show()
