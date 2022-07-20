import numpy as np
import matplotlib.pyplot as plt

# Import appropriate integration functions
from simple_case_integration import evaluate_gamma
from simple_case_integration import evaluate_tau

##################################################

# Adjustable parameters
BETA_MIN = 0.0
BETA_MAX = 1.5
NUM_BETAS = 50
QBER_FILENAME = "results/one_var_simple.png"
IMG_SIZE = (7, 5)
DPI = 300

X_var = 1.0
noise_var = 0.3 # Only adjust band width for now
betas = np.linspace(BETA_MIN, BETA_MAX, NUM_BETAS)

#################

sigma_X = np.sqrt(X_var)
sigma_eta = np.sqrt(noise_var)
mu_X = 0.0
SNR = X_var / noise_var

#################

QBERs = np.empty(len(betas))
taus = np.empty(len(betas))

for i, beta in enumerate(betas):
    # Evaluate gamma then convert it to a percentage by multiplying by 100
    QBERs[i] = evaluate_gamma(sigma_X, sigma_eta, mu_X, beta)[0] * 100.0
    
    # Do the same with tau (= 1 - throughput)
    taus[i] = evaluate_tau(sigma_X, sigma_eta, mu_X, beta)[0] * 100.0

#################

fig, ax = plt.subplots(1, figsize = IMG_SIZE)

ax.plot(betas, QBERs, "k-", label = "QBER")
ax.plot(betas, taus, "k--", label = "tau = 1 - T'put")

ax.set_xlabel("$\\beta$")
ax.set_ylabel("QBER % / Tau %")
ax.set_title("QBER and Tau vs. $\\beta$ for $\\sigma_X^2 = {:.2f}$ and $\sigma_\\eta^2 = {:.2f}$.".format(X_var, noise_var))

ax.legend()

plt.tight_layout()

plt.savefig(QBER_FILENAME, dpi = DPI)