from configparser import Interpolation
import numpy as np
import matplotlib.pyplot as plt
from one_var_analysis import QBER_FILENAME

# Import appropriate integration functions
from simple_case_integration import evaluate_gamma
from simple_case_integration import evaluate_tau

##################################################

# Adjustable parameters
BETA_MIN = 0.0
BETA_MAX = 0.5
NUM_BETAS = 20
NOISE_MIN = 0.01 # Don't divide by zero
NOISE_MAX = 0.3
NUM_NOISES = 20
X_VAR = 1.0

QBER_FILENAME = "results/two_var_simple_QBER.png"
TAU_FILENAME = "results/two_var_simple_TAU.png"
IMG_SIZE = (7, 5)
DPI = 300
FONTSIZE = 16
QBER_CONTOUR_LEVELS = (2, 4, 6)
TAU_CONTOUR_LEVELS = (10, 20, 30)

#################

sigma_etas = np.linspace(NOISE_MIN, NOISE_MAX, NUM_NOISES) # Equivalent to sigma_nu in the corresponding notes
betas = np.linspace(BETA_MIN, BETA_MAX, NUM_BETAS)
sigma_X = np.sqrt(X_VAR)
mu_X = 0.0

#################

QBERs = np.empty((NUM_BETAS, NUM_NOISES))
taus = np.empty(QBERs.shape)

for i, beta in enumerate(betas):
    for j, sigma_eta, in enumerate(sigma_etas):
        
        if (j == 0):
            print("# {} / {} combinations processed.".format(i * NUM_BETAS, NUM_BETAS * NUM_NOISES))
        
        # Evaluate gamma then convert it to a percentage by multiplying by 100
        QBERs[i][j] = evaluate_gamma(sigma_X, sigma_eta, mu_X, beta)[0] * 100.0
        
        # Do the same with tau (= 1 - throughput)
        taus[i][j] = evaluate_tau(sigma_X, sigma_eta, mu_X, beta)[0] * 100.0
        
#################

print("# Producing images ...")

############## PRODUCE QBER IMAGE ###############

fig, ax = plt.subplots(1, figsize = IMG_SIZE)

img = ax.imshow(QBERs, cmap = "gist_gray", interpolation = "bicubic", origin = "lower", aspect = "auto", extent = (NOISE_MIN, NOISE_MAX, BETA_MIN, BETA_MAX))
cnt = ax.contour(QBERs, levels = QBER_CONTOUR_LEVELS, colors = ("yellow", "blue", "red"), extent = (NOISE_MIN, NOISE_MAX, BETA_MIN, BETA_MAX))

ax.set_xlabel("$\\sigma_\\eta$", fontsize = FONTSIZE)
ax.set_ylabel("$\\beta$", fontsize = FONTSIZE)

cbar = plt.colorbar(img, ax = ax)
cbar.set_label("QBER %", fontsize = FONTSIZE)
cbar.add_lines(cnt)
cbar.minorticks_on()

plt.tight_layout()

plt.savefig(QBER_FILENAME, dpi = DPI)

############## PRODUCE THROUGHPUT IMAGE ###############

fig, ax = plt.subplots(1, figsize = IMG_SIZE)

img = ax.imshow(taus, cmap = "gist_gray", interpolation = "bicubic", origin = "lower", aspect = "auto", extent = (NOISE_MIN, NOISE_MAX, BETA_MIN, BETA_MAX))
cnt = ax.contour(taus, levels = TAU_CONTOUR_LEVELS, colors = ("yellow", "blue", "red"), extent = (NOISE_MIN, NOISE_MAX, BETA_MIN, BETA_MAX))

ax.set_xlabel("$\\sigma_\\eta$", fontsize = FONTSIZE)
ax.set_ylabel("$\\beta$", fontsize = FONTSIZE)

cbar = plt.colorbar(img, ax = ax)
cbar.set_label("$\\tau$ %", fontsize = FONTSIZE)
cbar.add_lines(cnt)
cbar.minorticks_on()

plt.tight_layout()

plt.savefig(TAU_FILENAME, dpi = DPI)