#!/usr/bin/env python

### ANCHOR: data_list
concentrations = [
    2.125, 4.250, 6.375, 8.500, 10.63, 12.75, 14.88, 17.00, 19.13, 21.25,
    23.38, 25.50, 27.63, 29.75, 31.88, 34.00, 36.13, 38.25, 40.38, 42.50,
]
absorbances = [
    0.0572, 0.1391, 0.2049, 0.2754, 0.3420, 
    0.4139, 0.4956, 0.5815, 0.6806, 0.7481,
    0.8242, 0.9130, 1.0043, 1.0809, 1.1511,
    1.2483, 1.3373, 1.4027, 1.4927, 1.5853,
]
### ANCHOR_END: data_list

### ANCHOR: data_array
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

concentrations = np.array(concentrations)
absorbances = np.array(absorbances)
### ANCHOR_END: data_array

### ANCHOR: exercise_01_b
# Rename variables for better readability
x = concentrations
y = absorbances

# Calculate the mean values
x_mean = np.mean(x)
y_mean = np.mean(y)

# Calculate the slope and the intercept
beta_1 = np.sum((x - x_mean) * (y - y_mean)) / np.sum((x - x_mean)**2)
beta_0 = y_mean - beta_1 * x_mean

assert np.isclose(beta_0, -0.04907034)
assert np.isclose(beta_1, 0.03800109)
### ANCHOR_END: exercise_01_b

### ANCHOR: exercise_01_d
# Build the set of equations
a_arr = np.array([
    [len(x),        np.sum(x),      np.sum(x**2)],
    [np.sum(x),     np.sum(x**2),   np.sum(x**3)],
    [np.sum(x**2),  np.sum(x**3),   np.sum(x**4)]
])
b_arr = np.array([np.sum(y), np.sum(x * y), np.sum(x**2 * y)])

# Solve the set of equations
beta = np.linalg.solve(a_arr, b_arr)

# Extract the parameters
beta_0, beta_1, beta_2 = beta

assert np.isclose(beta_0, -0.0208204)
assert np.isclose(beta_1, 0.0343756)
assert np.isclose(beta_2, 8.123859e-5)

# Plot the data, the fit and the residuals
fig, [ax1, ax2] = plt.subplots(1, 2, figsize=(16, 6))

ax1.plot(x, y, 'o', label='data')
ax1.plot(x, beta_0 + beta_1 * x + beta_2 * x**2, label='fit')

ax1.set_xlabel('concentration / mM')
ax1.set_ylabel('absorbance')

ax1.legend()

residuals = y - (beta_0 + beta_1 * x + beta_2 * x**2)
ax2.bar(x, residuals)

ax2.set_xlabel('concentration / mM')
ax2.set_ylabel('residuals')

plt.show()
### ANCHOR_END: exercise_01_d

fig.savefig('../../assets/figures/01-regression/quadreg_lambert_beer.svg')

### ANCHOR: exercise_02_a
# Calculate the coefficients of the polynomial fit
degree = 20
beta = np.polyfit(concentrations, absorbances, degree)

# Plot the data, the fit and the residuals
fig, [ax1, ax2] = plt.subplots(1, 2, figsize=(16, 6))

ax1.plot(x, y, 'o', label='data')
ax1.plot(x, np.polyval(beta, x), label='fit')

ax1.set_xlabel('concentration / mM')
ax1.set_ylabel('absorbance')

ax1.legend()

residuals = y - np.polyval(beta, x)
ax2.bar(x, residuals)

ax2.set_xlabel('concentration / mM')
ax2.set_ylabel('residuals')

plt.show()
### ANCHOR_END: exercise_02_a

fig.savefig('../../assets/figures/01-regression/polyreg_lambert_beer.svg')

### ANCHOR: exercise_02_b
# Create a finer grid for the plot
x_grid = np.linspace(0, 50, 1000)

# Plot the data and the fit
fig, ax = plt.subplots(figsize=(8, 6))

ax.plot(x, y, 'o', label='data')
ax.plot(x, np.polyval(beta, x), label='fit discrete')
ax.plot(x_grid, np.polyval(beta, x_grid), label='fit continuous')

ax.set_xlabel('concentration / mM')
ax.set_ylabel('absorbance')

ax.set_ylim(0, 2.0)

ax.legend()
plt.show()
### ANCHOR_END: exercise_02_b

fig.savefig('../../assets/figures/01-regression/polyreg_lambert_beer_overfitting.svg')

### ANCHOR: exercise_03_a
# Normalize the data
x = concentrations / np.max(concentrations)
y = absorbances / np.max(absorbances)

# Recalculate the coefficients of the polynomial fit without regularization
degree = 20
beta = np.polyfit(x, y, degree)

# Define the objective function with l2 regularization
def objective_function(beta, *args):
    x = args[0]
    y = args[1]
    lambda_ = args[2]
    return np.sum((y - np.polyval(beta, x))**2) + lambda_ * np.linalg.norm(beta)**2

# Minimize the objective function
beta_guess = np.zeros(degree + 1)
lambda_ = 1e-3

res = minimize(
    objective_function,
    beta_guess,
    args=(x, y, lambda_),
    method='CG',
    options={'maxiter': 1000, 'gtol': 1e-6},
)

beta_reg = res.x

# Create a finer grid for the plot
x_grid = np.linspace(0, 1, 1000)

# Plot the data and the fit
fig, ax = plt.subplots(figsize=(8, 6))

ax.plot(x, y, 'o', label='data')
ax.plot(x_grid, np.polyval(beta_reg, x_grid), label='regularized')
ax.plot(x_grid, np.polyval(beta, x_grid), label='not regularized')

ax.set_xlabel('norm. concentration')
ax.set_ylabel('norm. absorbance')

ax.set_xlim(0, 1.1)
ax.set_ylim(0, 1.1)

ax.legend()
plt.show()
### ANCHOR_END: exercise_03_a

fig.savefig('../../assets/figures/01-regression/polyreg_lambert_beer_regularization.svg')