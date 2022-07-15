from typing import Tuple
import numpy as np
from scipy.integrate import dblquad

def gamma_integral(Y, X, sigma_X, sigma_nu, mu_X):
    
    var_X = sigma_X**2
    var_nu = sigma_nu**2
    
    XmmuX = X - mu_X
    YmX = Y - X
    
    return \
        (1.0 / (2*np.pi * sigma_X * sigma_nu) ) * \
        np.exp(- 0.5 * (
                ( (XmmuX*XmmuX) / (var_X) ) + \
                ( (YmX*YmX) / (var_nu) )
            )
        )

def evaluate_gamma(sigma_X: float, sigma_nu: float, mu_X: float, beta: float) -> Tuple[float, float]:
    
    return dblquad(
        gamma_integral,                         # Function to integrate
        -np.inf,                                # Lower bound of X
        mu_X - beta,                            # Upper bound of X
        mu_X + beta,                            # Lower bound of Y
        np.inf,                                 # Upper bound of Y
        args = (sigma_X, sigma_nu, mu_X)        # Extra arguments
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
    print("\n\t# Evaluating BER ...")
    
    gamma, gamma_err = evaluate_gamma(np.sqrt(X_var), np.sqrt(noise_var), mu_X, band_width / 2.0)
    
    print("\n\tBER = {:.4f}% with error = {:.2e}%.".format(gamma * 100, gamma_err * 100))