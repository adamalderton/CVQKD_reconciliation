# TODO: Comment documentation!
# Define what gamma is
# Tau: 1 - throughput integral. Integral of pdf inside guard band, such that throughput is 1 - tau.

from typing import Tuple
import numpy as np
from scipy.integrate import dblquad

def _gamma_integral(Y, X, sigma_X, sigma_nu, mu_X):
    
    var_X = sigma_X*sigma_X
    var_nu = sigma_nu*sigma_nu
    
    XmmuX = X - mu_X
    YmX = Y - X
    
    return \
        (1.0 / (2*np.pi * sigma_X * sigma_nu) ) * \
        np.exp(- 0.5 * (
                ( (XmmuX*XmmuX) / (var_X) ) + \
                ( (YmX*YmX) / (var_nu) )
            )
        )


# Numerically evaluate the gamme integral as per the OneNote page. 
def evaluate_gamma(sigma_X, sigma_nu, mu_X, beta) -> Tuple[float, float]:
    return dblquad(
        _gamma_integral,                        # Function to integrate
        -np.inf,                                # Lower bound of X
        mu_X - beta,                            # Upper bound of X
        mu_X + beta,                            # Lower bound of Y
        np.inf,                                 # Upper bound of Y
        args = (sigma_X, sigma_nu, mu_X)        # Extra arguments
    )

# Essentially the same at the gamme integral, except for the fact that different integral limits are given.
# See the OneNote page for more information.
def evaluate_tau(sigma_X, sigma_nu, mu_X, beta) -> Tuple[float, float]:
    return dblquad(
        _gamma_integral,
        -np.inf,
        mu_X - beta,
        mu_X - beta,
        mu_X + beta,
        args = (sigma_X, sigma_nu, mu_X)
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
    
    phi, phi_err = evaluate_tau(np.sqrt(X_var), np.sqrt(noise_var), mu_X, band_width / 2.0)
    
    throughput = 1.0 - phi
    
    print("\n\tQBER = {:.4f}% with numerical integration error = {:.2e}%.".format(gamma * 100.0, gamma_err * 100.0))
    print("\tTPut = {:.4f}% with numerical integration error = {:.2e}%.".format(throughput * 100.0, phi_err * 100.0))