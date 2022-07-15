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

INITIAL_CENTRE = 0.0
INITIAL_SIGMA = 1.0
INITIAL_VAR = INITIAL_SIGMA**2

CHANNEL_CENTRE = 0.0

#### Acquire Parameters ####

# Most of the required parameters are set up as constants (as above). However, we do need the 'noise parameter'.
# The 'noise' parameter corresponds to the std dev of the Gaussian noise function.

if (len(sys.argv) < 3):
    raise Exception("Two command line parameters are needed: noise and BER, both of which are float values.\nUsage: python band_with_noise.py [noise] [BER].")

channel_sigma = float(sys.argv[1])
channel_var = channel_sigma**2

# Bit error rate (BER)
acceptable_ber = float(sys.argv[2])

#### Generate Data ####

# Generate raw data from Gaussian distribution centred on zero with variance 1. Shift as appropriate (defaults to no shift).
# Gaussian given by np.random.gaussian is a probability density function and is hence scaled by 1 / \sqrt{2\pi\sigma^2}.
# Hence, we 'unscale' to reach a Gaussian distribution of unity peak instead of unity integral.
data = np.sqrt(2 * np.pi * INITIAL_VAR) * INITIAL_SIGMA * np.random.randn((NUM_DATA_POINTS)) + INITIAL_CENTRE

# Next, assign values to data dependent on whether it is left or right of the centre of the Gaussian (1 bit per symbol).
bits = list(map(lambda d : int(d >= INITIAL_CENTRE), data))

#### Add Gaussian noise to data ####
noise = np.sqrt(2 * np.pi * channel_var) * channel_sigma * np.random.randn((NUM_DATA_POINTS)) + CHANNEL_CENTRE

data = np.add(data, noise)

#### Count Bit Error Rate ####

def bit_error_count(data, bits):
    count = 0
    for d, b in list(zip(data, bits)):
        count += (b != (d >= INITIAL_CENTRE))
    return count

bec = bit_error_count(data, bits)

print("BER = {:.5f}%.".format(100.0 * (bec / NUM_DATA_POINTS)))

# np.savetxt("data/data.txt", list(zip(data, bits)), fmt = "%.{}f".format(FLOAT_SIG_FIGS))

# fig, ax = plt.subplots(2)

# ax[0].hist(data, density = True, bins = 60)
# ax[0].set_xlim(-10, 10)
# ax[0].set_title("Data, sigma = {}.".format(INITIAL_SIGMA))

# ax[1].hist(noise, density = True, bins = 60)
# ax[1].set_xlim(-10, 10)
# ax[1].set_title("Noise, sigma = {}.".format(channel_sigma))

# plt.tight_layout()

# plt.show()