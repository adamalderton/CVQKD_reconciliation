# Generate simulated data that would be received by a receiver in a CVQKD system.
# First, generate Gaussian data to represent a gaussian modulated variable. It does not matter what this variable is. It could be the X quadrature, for example.
# Second, add Gaussian noise to this data to represent transmission through a Gaussian channel.
# Truncate this (and the source data) to two significant figures for something called 7 bit accuracy? Need to figure out what that is.
# Export this for the post processing step.

import numpy as np
import sys

#### Constants ####

NUM_DATA_POINTS = 1e6

INITIAL_CENTRE = 0.0
INITIAL_SIGMA = 1.0

CHANNEL_CENTRE = 0.0

#### Acquire Parameters ####

# Most of the required parameters are set up as constants (as above). However, we do need the 'noise parameter'.
# The 'noise' parameter corresponds to the std dev of the Gaussian noise function.

if (len(sys.argv) < 3):
    raise Exception("Two command line parameters are needed: noise and BER, both of which are float values.\nUsage: python band_with_noise.py [noise] [BER].")

channel_sigma = float(sys.argv[1])
ber = float(sys.argv[2])

channel_var = channel_sigma**2

print(channel_sigma)
print(ber)

#### Generate Data ####

# First, set up a Gaussian distribution to generate source data. Gaussian is normalised.
# Gaussian given by np.random.gaussian is a probability density function and is hence scaled by 1 / \sqrt{2\pi\sigma^2}.
# Hence, we 'unscale' to reach a Gaussian distribution of unity peak instead of unity integral.
scaling_factor = np.sqrt(2 * np.pi * channel_var)

# Generate unnormalised data


# Apply appropriate scaling


