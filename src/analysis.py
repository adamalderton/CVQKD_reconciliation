import numpy as np
import matplotlib.pyplot as plt

from simple_case_integration import evaluate_gamma
from simple_case_integration import evaluate_tau

######################################################

# TODO: Add rate of 'ignores': Amount of data within guard bands.

# CAVEAT: This only analyses 'half' of the X gaussian, hence gamma is not actually a probability
# as only 0.5 of X probability is considered. However, considering that this system is symmetric,
# the extension of the analysis to the right hand side of the Gaussian which would mean that gamma
# would double as there is a 'gamma' either side of the guard band. Therefore, the BER is actually the
# BER for the entire symmetrical system as the factor of half for total gamma and fraction of 
# distribution analysed cancel: (0.5 dist) / (0.5 gamma) = dist / gamma.

######################################################

# Adjustable parameters
BETA_MIN = 0.0
BETA_MAX = 1.5
NUM_BETAS = 50

X_var = 1.0
noise_var = 0.3 # Only adjust band width for now
betas = np.linspace(BETA_MIN, BETA_MAX, NUM_BETAS)

#################

sigma_X = np.sqrt(X_var)
sigma_nu = np.sqrt(noise_var)
mu_X = 0.0
SNR = X_var / noise_var

#################

QBERs = np.empty(len(betas))
taus = np.empty(len(betas))

for i, beta in enumerate(betas):
    # Evaluate gamma then convert it to a percentage by multiplying by 100
    QBERs[i] = evaluate_gamma(sigma_X, sigma_nu, mu_X, beta)[0] * 100.0
    
    # Do the same with tau (= 1 - throughput)
    taus[i] = evaluate_tau(sigma_X, sigma_nu, mu_X, beta)[0] * 100.0

#################

fig, ax = plt.subplots(1, figsize = (7, 5))

ax.plot(betas, QBERs, "k-", label = "QBER")
ax.plot(betas, taus, "k--", label = "tau = 1 - TPut")

ax.set_xlabel("$\\beta$")
ax.set_ylabel("QBER % / Phi %")
ax.set_title("QBER and Phi vs. $\\beta$ for $\\sigma_X^2 = {:.2f}$ and $\sigma_\\nu^2 = {:.2f}$.".format(X_var, noise_var))

ax.legend()

plt.tight_layout()

plt.savefig("simple_case.png", dpi = 300)