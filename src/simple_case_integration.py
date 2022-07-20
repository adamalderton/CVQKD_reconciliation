# A prototpye for the numerical integration of the binary sliced Gaussian
# For more information, please see the full report attached to the project.
# This should, in general, be interfaced to by an external program.
#
# Gamma: Integral corresponding to bits that, subject to noise, have been measured to reside at the other side of the guard band.
# Tau: 1 - throughput integral. Integral of pdf inside guard band, such that throughput is 1 - tau.

######################################################

# CAVEAT: This only analyses 'half' of the X gaussian, hence gamma is not actually a probability
# as only 0.5 of X probability is considered. However, considering that this system is symmetric,
# the extension of the analysis to the right hand side of the Gaussian which would mean that gamma
# would double as there is a 'gamma' either side of the guard band. Therefore, the BER is actually the
# BER for the entire symmetrical system as the factor of half for total gamma and fraction of 
# distribution analysed cancel: (0.5 dist) / (0.5 gamma) = dist / gamma.

######################################################

from typing import Tuple
import numpy as np
from scipy.integrate import dblquad

def _gamma_integral(Y, X, sigma_X, sigma_eta, mu_X):
    
    var_X = sigma_X*sigma_X
    var_nu = sigma_eta*sigma_eta
    
    XmmuX = X - mu_X
    YmX = Y - X
    
    return \
        (1.0 / (2*np.pi * sigma_X * sigma_eta) ) * \
        np.exp(- 0.5 * (
                ( (XmmuX*XmmuX) / (var_X) ) + \
                ( (YmX*YmX) / (var_nu) )
            )
        )


# Numerically evaluate the gamme integral as per the OneNote page. 
def evaluate_gamma(sigma_X, sigma_eta, mu_X, beta) -> Tuple[float, float]:
    return dblquad(
        _gamma_integral,                        # Function to integrate
        -np.inf,                                # Lower bound of X
        mu_X,                                   # Upper bound of X
        mu_X + beta,                            # Lower bound of Y
        np.inf,                                 # Upper bound of Y
        args = (sigma_X, sigma_eta, mu_X)       # Extra arguments
    )

# Essentially the same at the gamme integral, except for the fact that different integral limits are given.
# See the OneNote page for more information.
def evaluate_tau(sigma_X, sigma_eta, mu_X, beta) -> Tuple[float, float]:
    return dblquad(
        _gamma_integral,
        -np.inf,                                # Lower bound of X
        mu_X,                                   # Upper bound of X
        mu_X - beta,                            # Lower bound of Y
        mu_X + beta,                            # Upper bound of Y
        args = (sigma_X, sigma_eta, mu_X)       # Extra arguments
    )


if __name__ == "__main__":
    
    # Adjustable parameters
    X_var = 1.0
    noise_var = 0.1
    band_width = 0.1
    
    ############
    
    SNR = X_var / noise_var
    mu_X = 0.0
    
    ############
    
    print("\n\t# X_var = {:.3f}.\n\t# noise_var = {:.3f}.\n\t# guard_band_width = {:.3f}.".format(X_var, noise_var, band_width))
    print("\n\t# Evaluating ...")
    
    gamma, gamma_err = evaluate_gamma(np.sqrt(X_var), np.sqrt(noise_var), mu_X, band_width / 2.0)
    
    tau, tau_err = evaluate_tau(np.sqrt(X_var), np.sqrt(noise_var), mu_X, band_width / 2.0)
    
    throughput = 1.0 - tau
    
    print("\n\tQBER = {:.4f}% with numerical integration error = {:.2e}%.".format(gamma * 100.0, gamma_err * 100.0))
    print("\tTPut = {:.4f}% with numerical integration error = {:.2e}%.".format(throughput * 100.0, tau_err * 100.0))