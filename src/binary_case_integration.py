# A prototpye for the numerical integration of the binary sliced Gaussian
# For more information, please see the full report attached to the project.
# This should, in general, be interfaced to by an external program.
#
# Gamma: Integral corresponding to bits that, subject to noise, have been measured to reside at the other side of the guard band.
# Tau: 1 - throughput integral. Integral of pdf inside guard band, such that throughput is 1 - tau.

from typing import Tuple
import numpy as np
from scipy.integrate import dblquad

# The function f(x, y, \mu_X, \sigma_X, \sigma_\eta) as discussed in the attached report.
def _f(Y, X, sigma_X, sigma_eta, mu_X):
    
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


# Numerically evaluate the gamma integral.
# This is done in two sections are the integral limits of y differ either side of the guard band.
def evaluate_gamma(sigma_X, sigma_eta, mu_X, beta) -> Tuple[float, float]:
    return \
        np.add( # np add used as dblquad returns (integral, integral_error)
            dblquad( # Evaluate 'left hand side'
                _f,                                     # Function to integrate
                -np.inf,                                # Lower bound of X
                mu_X,                                   # Upper bound of X
                mu_X + beta,                            # Lower bound of Y
                np.inf,                                 # Upper bound of Y
                args = (sigma_X, sigma_eta, mu_X)       # Extra arguments
            ),
            dblquad( # Evaluate 'right hand side'
                _f,                                     # Function to integrate
                mu_X,                                   # Lower bound of X
                np.inf,                                 # Upper bound of X
                -np.inf,                                # Lower bound of Y
                mu_X - beta,                            # Upper bound of Y
                args = (sigma_X, sigma_eta, mu_X)       # Extra arguments
            )
        )

# Numerically evaluate the tau integral.
# Unlike gamma, this can be achieved in one double integral. See the proof in the attached report.
def evaluate_tau(sigma_X, sigma_eta, mu_X, beta) -> Tuple[float, float]:
    return dblquad(
        _f,                                     # Function to integrate
        -np.inf,                                # Lower bound of X
        np.inf,                                 # Upper bound of X
        mu_X - beta,                            # Lower bound of Y
        mu_X + beta,                            # Upper bound of Y
        args = (sigma_X, sigma_eta, mu_X)       # Extra arguments
    )


if __name__ == "__main__":
    
    mu_X = 0.0
    sigma_X = 1.0
    sigma_eta = 0.25
    beta = 0.3
    
    print("\n\t# sigma_X = {:.3f}.\n\t# sigma_eta = {:.3f}.\n\t# beta = {:.3f}.".format(sigma_X, sigma_eta, beta))
    print("\n\t# Evaluating ...")
    
    gamma, gamma_err = evaluate_gamma(sigma_X, sigma_eta, mu_X, beta)
    
    tau, tau_err = evaluate_tau(sigma_X, sigma_eta, mu_X, beta)
    
    throughput = 1.0 - tau
    
    print("\n\tGamma (QBER) = {:.4f}% with numerical integration error = {:.2e}%.".format(gamma * 100.0, gamma_err * 100.0))
    print("\tTau (1 - t'put) = {:.4f}% with numerical integration error = {:.2e}%.".format(tau * 100.0, tau_err * 100.0))