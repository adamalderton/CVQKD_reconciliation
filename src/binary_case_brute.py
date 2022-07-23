# Generate simulated data that would be received by a receiver in a CVQKD system.
# First, generate Gaussian data to represent a gaussian modulated variable. It does not matter what this variable is. It could be the X quadrature, for example.
# Second, add Gaussian noise to this data to represent transmission through a Gaussian channel.
# Truncate this (and the source data) to two significant figures for something called 7 bit accuracy? Need to figure out what that is.
# Export this for the post processing step.

from typing import Tuple
import numpy as np
import sys
import matplotlib.pyplot as plt

#### Constants ####

FLOAT_SIG_FIGS = 2

def bit_error_check(data, bit, b0, b1) -> int:
    if (bit == 0):
        return int((data >= b1))
    else:
        return int((data <= b0))

def bit_ignore_check(data, b0, b1) -> int:
    return int(b0 <= data <= b1)

# Used to test analytic integrations by generating a large number of samples from the initial Gaussian
# distribution, then adding the appropriate amount of noise and investigating the results. In theory,
# the results should match the analytic versions very closely.
def binary_case_brute_force(mu_X, sigma_X, sigma_eta, beta, mute = True, num_data_points = int(1e6)) -> Tuple[float, float]:

    # Guard band boundaries
    b0 = mu_X - beta
    b1 = mu_X + beta

    # Generate raw data from Gaussian distribution centred on mu_X with std. dev. sigma_X.
    if not mute:
        print("\n\t# Generating {:.2e} data points...".format(num_data_points))
    data = sigma_X * np.random.randn((num_data_points)) + mu_X

    # Next, assign values to data dependent on whether it is left or right of the centre of the Gaussian (1 bit per symbol).
    # 0 for left, 1 for right.
    if not mute:
        print("\t# Assigning bit values ...")
    bits = list(map(lambda d : int(d >= mu_X), data))
    
    # Generate Guassian noise, add it to data.
    if not mute:
        print("\t# Generating gaussian noise ...")
    noise = sigma_eta * np.random.randn((num_data_points))
    if not mute:
        print("\t# Adding Gaussian noise ...")
    data = np.add(data, noise)

    # Evaluate the effective "gamma" integral.
    if not mute:
        print("\t# Counting QBER ...")    
    bit_err_count = sum([bit_error_check(*db, b0, b1) for db in zip(data, bits)])
    gamma = bit_err_count / num_data_points
    
    # Evaluate the effective "tau" integral
    if not mute:
        print("\t# Counting tau bits ...")
    bit_ignore_count = sum([bit_ignore_check(d, b0, b1) for d in data])
    tau = bit_ignore_count / num_data_points
    
    return gamma, tau

if __name__ == "__main__":
    
    mu_X = 0.0
    sigma_X = 1.0
    sigma_eta = 0.25
    beta = 0.3
    
    gamma, tau = binary_case_brute_force(mu_X, sigma_X, sigma_eta, beta, mute = False)
    
    print("\n\t# Gamma (QBER) = {:.4f}%.".format(gamma * 100.0))
    print("\t# Tau (1 - t'put) = {:.4f}%.".format(tau))