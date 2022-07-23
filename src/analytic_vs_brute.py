import numpy as np
import matplotlib.pyplot as plt

from binary_case_brute import binary_case_brute_force
from binary_case_integration import evaluate_gamma
from binary_case_integration import evaluate_tau

###################################

mu_X = 0.0
sigma_X = 1.0
sigma_eta = 0.25
beta = 0.4
num_data_points = int(1e6)

###################################

gamma_a = evaluate_gamma(sigma_X, sigma_eta, mu_X, beta)[0]
tau_a = evaluate_tau(sigma_X, sigma_eta, mu_X, beta)[0]

gamma_b, tau_b = binary_case_brute_force(mu_X, sigma_X, sigma_eta, beta, mute = True, num_data_points = num_data_points)

print("\n\t# Gamma A: {:.6f}.".format(gamma_a))
print("\t# Gamma B: {:.6f}.".format(gamma_b))
print("\n\t# Tau A: {:.6f}.".format(tau_a))
print("\t# Tau B: {:.6f}.".format(tau_b))

plt.plot(gamma_as, "k-", label = "Analytic")
plt.plot(gamma_bs, "b-", label = "Brute")
plt.legend()
plt.show()