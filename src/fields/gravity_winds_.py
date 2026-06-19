# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 14:23:40 2026

@author: Luiz
"""

import numpy as np
import matplotlib.pyplot as plt

g0 = 9.8
Re = 6371e3
U0 = 100.0

theta = np.linspace(-np.pi/3, np.pi/3, 100)
q = np.linspace(0.8*Re, 2.0*Re, 80)

TH, Q = np.meshgrid(theta, q)

delta = np.sqrt(1 + 3*np.sin(TH)**2)

A = -(g0 * Re**2 * np.cos(TH)**4) / Q**2

g_mu = A * (-2*np.sin(TH)/delta)
g_q  = A * ( np.cos(TH)/delta)

Vn_mu = U0 * (-2*np.sin(TH)/delta)
Vn_q  = U0 * ( np.cos(TH)/delta)

fig, ax = plt.subplots(1, 2, figsize=(12, 5))

# Campo de g
skip = (slice(None, None, 4), slice(None, None, 4))
ax[0].quiver(np.degrees(TH[skip]), Q[skip]/Re, g_mu[skip], g_q[skip])
ax[0].set_title(r'Campo vetorial de $\mathbf{g}$')
ax[0].set_xlabel(r'$\theta$ (graus)')
ax[0].set_ylabel(r'$q/R_e$')

# Campo de Vn
ax[1].quiver(np.degrees(TH[skip]), Q[skip]/Re, Vn_mu[skip], Vn_q[skip])
ax[1].set_title(r'Campo vetorial de $\mathbf{V}_n$')
ax[1].set_xlabel(r'$\theta$ (graus)')
ax[1].set_ylabel(r'$q/R_e$')

plt.tight_layout()
plt.show()