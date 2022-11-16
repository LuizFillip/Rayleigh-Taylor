import numpy as np
import matplotlib.pyplot as plt

q_c = 1.6e-19
m_i = 16*1.67e-27
m_e = m_i / 1837.

mag0 = 3.2e-05 

gyro_i = (q_c * mag0 / m_i)

gyro_e = -(q_c * mag0 / m_e)


y = np.arange(100, 580, 10) 

nu = 1e3 * np.exp(-(y - 80.) / 35.)
kappa_i=gyro_i/nu
kappa_e=gyro_e/nu

mu_pi = (1. / mag0) * (kappa_i / (1. + kappa_i**2.))
mu_pe = (1. / mag0) * (kappa_e / (1. + kappa_e**2.))
mu_hi = (1. / mag0) * (kappa_i**2./ (1. + kappa_i**2.))
mu_he = (1. / mag0) * (kappa_e**2./ (1. + kappa_e**2.))



#plt.plot(mu_pi, y)
#plt.plot(mu_pe, y)

plt.plot(mu_pe, y)

#plt.semilogx(mu_pe, y)