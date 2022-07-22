# Generate simulated data that would be received by a receiver in a CVQKD system.
# First, generate Gaussian data to represent a gaussian modulated variable. It does not matter what this variable is. It could be the X quadrature, for example.
# Second, add Gaussian noise to this data to represent transmission through a Gaussian channel.
# Truncate this (and the source data) to two significant figures for something called 7 bit accuracy? Need to figure out what that is.
# Export this for the post processing step.

import numpy as np
import sys
import matplotlib.pyplot as plt

#### Constants ####

NUM_DATA_POINTS = int(1e6)
FLOAT_SIG_FIGS = 2

# Used to test analytic integrations by generating a large number of samples from the initial Gaussian
# distribution, then adding the appropriate amount of noise and investigating the results. In theory,
# the results should match the analytic versions very closely.
def binary_case_brute_force(mu_X, sigma_X, sigma_eta, beta, mute = True):

    # Guard band boundaries
    b0 = mu_X - beta
    b1 = mu_X + beta

    # Generate raw data from Gaussian distribution centred on mu_X with std. dev. sigma_X.
    if not mute:
        print("\n\t# Generating {:.2e} data points...".format(NUM_DATA_POINTS))
    data = sigma_X * np.random.randn((NUM_DATA_POINTS)) + mu_X

    # Next, assign values to data dependent on whether it is left or right of the centre of the Gaussian (1 bit per symbol).
    # 0 for left, 1 for right.
    if not mute:
        print("\t# Assigning bit values ...")
    bits = list(map(lambda d : int(d >= mu_X), data))

    # Generate Guassian noise, add it to data.
    if not mute:
        print("\t# Generating gaussian noise ...")
    noise = sigma_eta * np.random.randn((NUM_DATA_POINTS))
    if not mute:
        print("\t# Adding Gaussian noise ...")
    data = np.add(data, noise)

    # Evaluate the effective "gamma" integral.
    if not mute:
        print("\t# Counting QBER ...")
    bit_err_count = 0
    for d, b in list(zip(data, bits)):
        bit_err_count += (b != (d >= mu_X))
    
    gamma = bit_err_count / NUM_DATA_POINTS
    
    # Evaluate the effective "tau" integral
    if not mute:
        print("\t# Counting tau bits ...")
    bit_ignore_count = 0
    for d in data:
        bit_ignore_count += (b0 <= d <= b1)
    
    tau = bit_ignore_count / NUM_DATA_POINTS
    
    return gamma, tau

if __name__ == "__main__":
    
    mu_X = 0.0
    sigma_X = 1.0
    sigma_eta = 0.25
    beta = 0.3
    
    gamma, tau = binary_case_brute_force(mu_X, sigma_X, sigma_eta, beta, mute = False)
    
    print("\n\t# Gamma (QBER) = {:.4f}%.".format(gamma * 100.0))
    print("\t# Tau (1 - t'put) = {:.4f}%.".format(tau))